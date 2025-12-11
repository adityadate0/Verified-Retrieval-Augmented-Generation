# Veri-RAG Enterprise: Offline Multi-Agent Knowledge Engine

**Secure. Accurate. Compliant.**

Veri-RAG Enterprise is a specialized Retrieval-Augmented Generation system designed for sensitive, offline environments. Unlike standard chatbots, it utilizes a **Multi-Agent Architecture** to eliminate hallucinations and enforce strict compliance with uploaded documentation.

## 🚀 Key Features

* **100% Offline:** Runs locally using Ollama (Llama 3) and ChromaDB. No data leaves your machine.
* **Zero-Hallucination Protocol:**
    1.  **Analyst Agent:** Drafts an answer strictly from context.
    2.  **Auditor Agent:** Reviews the draft against source text to flag inaccuracies.
    3.  **Editor Agent:** Synthesizes the final verified report.
* **Compliance Layer:** Automatically detects and flags prohibited actions or missing safety warnings in the draft.
* **Hardware Agnostic:** Auto-detects GPU (CUDA) for speed, but fully functional on CPU (with adjusted timeouts).
* **Modern Dashboard:** Theme-aware Streamlit UI with real-time thought process visualization.

## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI (Async Streaming)
* **LLM Engine:** Ollama (Llama 3)
* **Orchestration:** LangChain v0.3
* **Vector Store:** ChromaDB (Local Persisted)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

## 📦 Installation & Setup

### Prerequisites
* OS: Ubuntu / Linux / macOS
* Python: 3.10+
* [Ollama](https://ollama.com/) installed.

### 1. Clone the Repository
```bash
git clone https://github.com/adityadate0/Verified-Retrieval-Augmented-Generation.git
cd Verified-Retrieval-Augmented-Generation


