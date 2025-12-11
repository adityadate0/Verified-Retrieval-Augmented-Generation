#!/bin/bash

# 1. Setup Environment
if [ ! -d "veri_rag_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv veri_rag_env
    source veri_rag_env/bin/activate
    pip install --upgrade pip
else
    source veri_rag_env/bin/activate
fi

# 2. Check Dependencies & Start Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    # Wait for Ollama Port to be active
    echo "Waiting for Ollama to spin up..."
    while ! nc -z localhost 11434; do   
      sleep 1
    done
fi

if ! ollama list | grep -q "llama3"; then
    echo "Pulling Llama3 (This may take a while)..."
    ollama pull llama3
fi

mkdir -p data chroma_db

echo "Installing Requirements..."
pip install -r requirements.txt

# 3. Configure Streamlit
mkdir -p ~/.streamlit
echo '[general]
email = ""
' > ~/.streamlit/credentials.toml

# 4. Start Servers
echo "Starting Backend API..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "⏳ Waiting 5 seconds for Backend to initialize..."
sleep 5

echo "Starting Frontend..."
streamlit run frontend/dashboard.py &
FRONTEND_PID=$!

echo "🚀 System Online at http://localhost:8501"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
