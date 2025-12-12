# Veri-RAG Enterprise

Secure Offline Enterprise Knowledge Retrieval with Multi-Agent Verification

---

## Introduction

Veri-RAG Enterprise is an advanced Retrieval-Augmented Generation (RAG) system engineered for offline environments where data privacy, security, and factual accuracy are non-negotiable. Unlike standard RAG chatbots that simply summarize retrieved text, Veri-RAG employs a Multi-Agent Architecture to eliminate hallucinations.

The system features a dedicated **Auditor Agent** that cross-checks every generated response against source documents before the final output is presented to the user. The entire pipeline runs locally on your machine (CPU or GPU) using Llama 3 (via Ollama) and ChromaDB, ensuring no data ever leaves the secure infrastructure.

---

## Key Capabilities

- **100% Offline Operation**  
  Fully functional without internet access once the models are pulled.

- **Zero-Hallucination Pipeline**  
  A 3-step workflow (**Analyst → Auditor → Editor**) ensures every claim is backed by the source text.

- **Compliance & Safety Layer**  
  The Auditor Agent specifically scans for prohibited actions or missing safety warnings in the draft.

- **Hardware Agnostic**  
  Automatically detects GPU (CUDA) for acceleration but falls back gracefully to CPU with extended timeouts.

- **Interactive Neural Dashboard**  
  A modern, theme-aware Streamlit interface that visualizes the “thought process” of the agents in real time.

---

## Technology Stack

- **Core Logic:** Python 3.10+
- **Frontend:** Streamlit (UI/UX)
- **Backend:** FastAPI (Async Streaming)
- **LLM Runtime:** Ollama (hosting Llama 3)
- **Orchestration:** LangChain (Chains, Prompts)
- **Vector Database:** ChromaDB (Local Persistence)
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

---

## 1. Setup Information

### System Requirements

- **OS:** Ubuntu/Linux (preferred) or macOS  
- **Python:** Version 3.10 is recommended  
- **Dependency:** Ollama must be installed  

  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- **RAM:** 8 GB minimum (16 GB recommended for CPU performance)

### Running the Project

Clone the Repository

```bash

git clone https://github.com/adityadate0/Verified-Retrieval-Augmented-Generation.git

cd Verified-Retrieval-Augmented-Generation

```
1. Place all files in the folder structure shown below.
2. Open a terminal in the project folder.
3. Make the script executable:

   ```bash
   chmod +x run.sh
   ```

4. Run the startup script:

   ```bash
   ./run.sh
   ```

5. The script will handle virtual env creation, installing dependencies, pulling Llama 3, and starting both servers.

---

## A. Repository Structure

This is the file tree you should see in your GitHub repo:

```text
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
```

---

## 2. Run the System

We have provided a unified startup script that handles virtual environments, dependency installation, Ollama model pulling, and server startup.

```bash
chmod +x run.sh
./run.sh
```

### What This Script Does

- Creates a virtual environment `veri_rag_env`.
- Installs Python dependencies from `requirements.txt`.
- Checks if `ollama` is running; starts it if not.
- Pulls the `llama3` model (if not already present).
- Launches the Backend API (Port `8000`).
- Launches the Frontend Dashboard (Port `8501`).

---

## 3. Usage Guide


### Access the Dashboard
Open [http://localhost:8501](http://localhost:8501) in your browser.

### Try the "Trap Test" (Recommended)
We have provided a sample document to test the system's ability to catch violations.

1. **Upload:** Go to the Sidebar and upload `samples/Server_Access_Document.pdf`.
2. **Vectorize:** Click **"🚀 Upload & Vectorize"**.
3. **Ask a Trap Question:**
   > "I need to perform the monthly fan cleaning routine on Tuesday at 5:00 AM. Please list the steps."
4. **Observe the Result:**
   * The **Analyst** might try to answer.
   * The **Auditor** will detect that 5:00 AM is outside the allowed 02:00-04:00 AM window.
   * The **Final Response** will be a refusal/correction.

### Normal Usage
* Upload your own PDF manuals (SOPs, Policy Documents, etc.).
* Ask questions. The system will strictly enforce the rules found in your text.

### Stop / Reset

If a query gets stuck or you entered the wrong prompt, click **"⛔ Stop / Reset"** in the sidebar to restart the session immediately.

---

## 🔧 Troubleshooting

## ⚡ Performance & GPU Support

By default, the project runs in **Safe Mode (CPU)** to ensure compatibility with all hardware, including older laptops.

**To enable GPU Acceleration**
1. Open `run.sh`.
2. Change line 5 to: `ENABLE_GPU=true`.
3. Restart the system: `./run.sh`.

### "Connection Error" / Timeout

- If running on CPU, complex queries may time out.  
- The system is configured with a **600s (10-minute) timeout**.  
- Try asking simpler questions or reducing query complexity.

### Telemetry Errors in Terminal

- ChromaDB telemetry is disabled in `rag_engine.py` to keep logs clean.  
- If you still see telemetry-related logs, ensure you are using the latest version of the code.

### Port Conflicts

- Ensure ports **8000** (Backend API) and **8501** (Frontend Dashboard) are free before running the system.
- Stop any other services using these ports or reconfigure them if necessary.

---
