> Aditya:
# Veri-RAG Enterprise

Tagline: Secure Offline Enterprise Knowledge Retrieval with Multi-Agent Verification

---

## Introduction

Veri-RAG Enterprise is an advanced Retrieval-Augmented Generation (RAG) system engineered for offline environments where data privacy, security, and factual accuracy are non-negotiable. Unlike standard RAG chatbots that simply summarize retrieved text, Veri-RAG employs a Multi-Agent Architecture to eliminate hallucinations.

The system features a dedicated Auditor Agent that cross-checks every generated response against source documents before the final output is presented to the user. The entire pipeline runs locally on your machine (CPU or GPU) using Llama 3 (via Ollama) and ChromaDB, ensuring no data ever leaves the secure infrastructure.

---

## Key Capabilities

- 100% Offline Operation  
  Fully functional without internet access once the models are pulled.

- Zero-Hallucination Pipeline  
  A 3-step workflow (**Analyst → Auditor → Editor**) ensures every claim is backed by the source text.

- Compliance & Safety Layer  
  The Auditor Agent specifically scans for prohibited actions or missing safety warnings in the draft.

- Hardware Agnostic  
  Automatically detects GPU (CUDA) for acceleration but falls back gracefully to CPU with extended timeouts.

- Interactive Neural Dashboard  
  A modern, theme-aware Streamlit interface that visualizes the “thought process” of the agents in real time.

---

## Technology Stack

- Core Logic: Python 3.10+
- Frontend: Streamlit (UI/UX)
- Backend: FastAPI (Async Streaming)
- LLM Runtime: Ollama (hosting Llama 3)
- Orchestration: LangChain (Chains, Prompts)
- Vector Database: ChromaDB (Local Persistence)
- Embeddings: HuggingFace (`all-MiniLM-L6-v2`)

---

## 1. Setup Information (Internal)

### System Requirements

- OS: Ubuntu/Linux (preferred) or macOS  
- Python: Version 3.10 is recommended  
- Dependency: Ollama must be installed  

    curl -fsSL https://ollama.com/install.sh | sh
  

- RAM: 8 GB minimum (16 GB recommended for CPU performance)

### Running the Project

1. Place all files in the folder structure shown below.
2. Open a terminal in the project folder.
3. Make the script executable:

      chmod +x run.sh
   

4. Run the startup script:

      ./run.sh
   

5. The script will handle virtual env creation, installing dependencies, pulling Llama 3, and starting both servers.

---

## A. Repository Structure

This is the file tree you should see in your GitHub repo:

Veri-RAG-Enterprise/
│
├── backend/
│   ├── __init__.py        # (Empty file)
│   ├── main.py            # FastAPI entry point
│   └── rag_engine.py      # Core logic & Agents
│
├── frontend/
│   └── dashboard.py       # Streamlit UI
│
├── requirements.txt       # Dependencies
├── run.sh                 # Startup script
├── README.md              # Project documentation
└── .gitignore             # (Recommended to ignore data/ and env/ folders)

---

## 2. Run the System

We have provided a unified startup script that handles virtual environments, dependency installation, Ollama model pulling, and server startup.

chmod +x run.sh
./run.sh

### What This Script Does

- Creates a virtual environment offline_mechanic_env.
- Installs Python dependencies from requirements.txt.
- Checks if ollama is running; starts it if not.
- Pulls the llama3 model (if not already present).
- Launches the Backend API (Port `8000`).
- Launches the Frontend Dashboard (Port `8501`).

---

## 3. Usage Guide

### Access the Dashboard

Open the following URL in your browser:

http://localhost:8501

### Ingest Knowledge

1. Open the Sidebar (left side of the dashboard).
2. Upload a PDF (e.g., Policy Manual, Technical SOP).
3. Click "🚀 Upload & Vectorize".

> Note: On CPU, this may take 1–2 minutes.

### Ask a Question

1. Type your query in the chat bar.
2. Observe the agents as they process your request:

   - 🔍 Retrieval: Finds relevant

> Aditya:
pages.
   - 👨‍💻 Analyst: Drafts the content.
   - 👮 Auditor: Verifies facts (Pass/Flag).
   - 📝 Synthesis: Generates the final report.

### Stop / Reset

If a query gets stuck or you entered the wrong prompt, click "⛔ Stop / Reset" in the sidebar to restart the session immediately.

---

## 🔧 Troubleshooting

### "Connection Error" / Timeout

- If running on CPU, complex queries may time out.  
- The system is configured with a 600s (10-minute) timeout.  
- Try asking simpler questions or reducing query complexity.

### Telemetry Errors in Terminal

- ChromaDB telemetry is disabled in rag_engine.py to keep logs clean.  
- If you still see telemetry-related logs, ensure you are using the latest version of the code.

### Port Conflicts

- Ensure ports 8000 (Backend API) and 8501 (Frontend Dashboard) are free before running the system.
- Stop any other services using these ports or reconfigure them if necessary.

---
