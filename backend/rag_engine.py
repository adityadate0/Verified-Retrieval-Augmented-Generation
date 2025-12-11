import os

# --- CRITICAL FIX: DISABLE TELEMETRY BEFORE IMPORTS ---
# This stops Chroma from trying to phone home, which kills the error.
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL"] = "chromadb.telemetry.posthog.Posthog" 

import json
import torch
# Now it is safe to import libraries that rely on Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import chromadb

DATA_PATH = "data/"
DB_PATH = "chroma_db/"

class UniversalBrain:
    def __init__(self):
        # 1. HARDWARE ACCELERATION
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Brain Initialized on: {device_type.upper()}")

        # 2. EMBEDDINGS
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': device_type}
        )
        
        # 3. LLM (Ollama)
        self.llm = OllamaLLM(model="llama3", temperature=0)
        
        # 4. VECTOR STORE SETUP
        if os.path.exists(DB_PATH):
            self.vector_store = Chroma(
                persist_directory=DB_PATH, 
                embedding_function=self.embeddings
                # No need for client_settings here anymore, the env var handles it globally
            )
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        else:
            self.vector_store = None

    def ingest_data(self):
        """Reads PDFs and vectorizes them."""
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            return "Data folder created. Please add PDFs."
            
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        if not documents:
            return "No PDFs found in data/ folder."
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Re-initialize Chroma with new data
        self.vector_store = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=DB_PATH
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        return f"Success! Ingested {len(chunks)} knowledge chunks."

    def stream_ask(self, query):
        """
        Generator function that streams the Multi-Agent thought process.
        """
        if not self.vector_store:
            yield json.dumps({"type": "error", "content": "System Offline. Please Ingest Data."})
            return

        # PHASE 1: RETRIEVAL
        yield json.dumps({"type": "status", "content": "🔍 Scanning Vector Database..."})
        docs = self.retriever.invoke(query)
        context_text = "\n\n".join([d.page_content for d in docs])
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        yield json.dumps({"type": "sources", "content": sources})
        
        # PHASE 2: AGENT A (THE ANALYST)
        yield json.dumps({"type": "status", "content": "👨‍💻 Analyst Agent is drafting initial response..."})
        
        analyst_prompt = PromptTemplate(
            template="""You are an Expert Data Analyst. Answer the user's question based ONLY on the context below. 
            Be comprehensive and structured.
            
            Context: {context}
            Question: {query}
            
            Draft Answer:""",
            input_variables=["context", "query"]
        )
        analyst_chain = analyst_prompt | self.llm
        draft_answer = analyst_chain.invoke({"context": context_text, "query": query})
        
        # Stream the Draft to UI
        yield json.dumps({"type": "draft", "content": draft_answer})

        # PHASE 3: AGENT B (THE AUDITOR)
        yield json.dumps({"type": "status", "content": "👮 Auditor Agent is checking for hallucinations & prohibitions..."})
        
        auditor_prompt = PromptTemplate(
            template="""You are a Senior QA Auditor. Review the Draft Answer against the Context.
            
            Context: {context}
            Draft Answer: {draft}
            
            Task:
            1. Detect Hallucinations (facts in Draft not present in Context).
            2. Check for missing critical details or Prohibitions (e.g., "Strictly Prohibited").
            3. If the draft is accurate, simply say "VERIFIED".
            
            Audit Report:""",
            input_variables=["context", "draft"]
        )
        auditor_chain = auditor_prompt | self.llm
        audit_report = auditor_chain.invoke({"context": context_text, "draft": draft_answer})
        
        # Stream the Audit Log to UI
        yield json.dumps({"type": "audit", "content": audit_report})

        # PHASE 4: FINAL SYNTHESIS
        yield json.dumps({"type": "status", "content": "📝 Chief Editor is finalizing the verified report..."})
        
        final_prompt = PromptTemplate(
            template="""You are the Final Editor. Produce the final response.
            
            1. Incorporate the Draft Answer.
            2. Apply corrections from the Audit Report.
            3. Structure the output clearly.
            
            Draft: {draft}
            Audit Report: {audit}
            
            Final Verified Response:""",
            input_variables=["draft", "audit"]
        )
        final_chain = final_prompt | self.llm
        final_response = final_chain.invoke({"draft": draft_answer, "audit": audit_report})

        # Stream the Final Result
        yield json.dumps({"type": "final", "content": final_response})
