\# Veri-RAG Enterprise: Offline Multi-Agent Knowledge Engine

\*\*Secure. Accurate. Compliant.\*\*

Veri-RAG Enterprise is a specialized Retrieval-Augmented Generation system designed for sensitive, offline environments. Unlike standard chatbots, it utilizes a \*\*Multi-Agent Architecture\*\* to eliminate hallucinations and enforce strict compliance with uploaded documentation.

\## 🚀 Key Features

\* \*\*100% Offline:\*\* Runs locally using Ollama (Llama 3) and ChromaDB. No data leaves your machine.

\* \*\*Zero-Hallucination Protocol:\*\*

1\. \*\*Analyst Agent:\*\* Drafts an answer strictly from context.

2\. \*\*Auditor Agent:\*\* Reviews the draft against source text to flag inaccuracies.

3\. \*\*Editor Agent:\*\* Synthesizes the final verified report.

\* \*\*Compliance Layer:\*\* Automatically detects and flags prohibited actions or missing safety warnings in the draft.

\* \*\*Hardware Agnostic:\*\* Auto-detects GPU (CUDA) for speed, but fully functional on CPU (with adjusted timeouts).

\* \*\*Modern Dashboard:\*\* Theme-aware Streamlit UI with real-time thought process visualization.

\## 🛠️ Technology Stack

\* \*\*Frontend:\*\* Streamlit

\* \*\*Backend:\*\* FastAPI (Async Streaming)

\* \*\*LLM Engine:\*\* Ollama (Llama 3)

\* \*\*Orchestration:\*\* LangChain v0.3

\* \*\*Vector Store:\*\* ChromaDB (Local Persisted)

\* \*\*Embeddings:\*\* HuggingFace (\`all-MiniLM-L6-v2\`)

\---

\## 📂 Repository Structure

\`\`\`text

Veri-RAG-Enterprise/

│

├── backend/

│ ├── main.py # FastAPI entry point

│ └── rag\_engine.py # Core logic & Agents

│

├── frontend/

│ └── dashboard.py # Streamlit UI

│

├── requirements.txt # Dependencies

├── run.sh # Unified startup script

└── README.md # Project documentation

⚙️ Setup Information
--------------------

### Prerequisites

*   **OS:** Ubuntu / Linux / macOS (Preferred).
    
*   **Python:** 3.10+
    
*   **Ollama:** Must be installed. [Download here](https://ollama.com/).
    
*   **RAM:** 8GB Minimum (16GB recommended for CPU performance).
    

### 🚀 Run the System

We have provided a unified startup script that handles virtual environments, dependency installation, Ollama model pulling, and server startup.

1.  bashgit clone \[https://github.com/adityadate0/Verified-Retrieval-Augmented-Generation.git\](https://github.com/adityadate0/Verified-Retrieval-Augmented-Generation.git)cd Verified-Retrieval-Augmented-Generation
    
2.  Bashchmod +x run.sh./run.sh
    

**What this script does:**

*   Creates a virtual environment veri\_rag\_env.
    
*   Installs Python dependencies from requirements.txt.
    
*   Checks if ollama is running; starts it if not.
    
*   Pulls the llama3 model (if not already present).
    
*   Launches the Backend API (Port 8000).
    
*   Launches the Frontend Dashboard (Port 8501).
    

📖 Usage Guide
--------------

1.  **Access the Dashboard:**Open [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501) in your browser.
    
2.  **Ingest Knowledge:**
    
    *   Open the **Sidebar** (Left).
        
    *   Upload a PDF (e.g., Policy Manual, Technical SOP).
        
    *   Click **"🚀 Upload & Vectorize"**.
        
    *   _Note: On CPU, this may take 1-2 minutes._
        
3.  **Ask a Question:**
    
    *   Type your query in the chat bar.
        
    *   **Watch the Agents work:**
        
        *   🔍 Retrieval: Finds relevant pages.
            
        *   👨‍💻 Analyst: Drafts the content.
            
        *   👮 Auditor: Verifies facts (Pass/Flag).
            
        *   📝 Synthesis: Generates the final report.
            
4.  **Stop/Reset:**
    
    *   If a query gets stuck or you entered the wrong prompt, click **"⛔ Stop / Reset"** in the sidebar to restart the session immediately.
        

🔧 Troubleshooting
------------------

*   **"Connection Error" / Timeout:**If running on CPU, complex queries may time out. The system is configured with a 600s (10-minute) timeout. Try asking simpler questions.
    
*   **Telemetry Errors in Terminal:**We have disabled ChromaDB telemetry in rag\_engine.py to keep logs clean. If you see them, ensure you are using the latest version of the code provided in this repo.
    
*   **Port Conflicts:**Ensure ports **8000** and **8501** are free before running.
