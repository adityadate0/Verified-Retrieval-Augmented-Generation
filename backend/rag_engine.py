import os
import shutil

# --- CRITICAL FIX: DISABLE TELEMETRY ---
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL"] = "chromadb.telemetry.posthog.Posthog" 

import json
import torch
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
        # 1. SMART HARDWARE ACCELERATION
        try:
            if torch.cuda.is_available():
                capability = torch.cuda.get_device_capability()
                if capability[0] >= 7:
                    device_type = "cuda"
                    print(f"🚀 Brain Initialized on: {device_type.upper()}")
                else:
                    device_type = "cpu"
                    print(f"⚠️ GPU Incompatible. Using CPU.")
            else:
                device_type = "cpu"
                print(f"🚀 Brain Initialized on: CPU")
        except:
            device_type = "cpu"

        # 2. EMBEDDINGS
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': device_type},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # 3. LLM (Using Llama 3)
        self.llm = OllamaLLM(model="llama3", temperature=0, num_ctx=2048)
        
        # 4. VECTOR STORE SETUP
        # We initialize it once here.
        if os.path.exists(DB_PATH):
            self.vector_store = Chroma(
                persist_directory=DB_PATH, 
                embedding_function=self.embeddings
            )
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        else:
            self.vector_store = None

    def ingest_data(self):
        """Safely clears old data and adds new PDFs."""
        
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            return "Data folder created. Please add PDFs."
            
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        if not documents:
            return "No PDFs found in data/ folder."
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # --- CRITICAL FIX: SAFE RESET ---
        # Instead of deleting the folder (which crashes the server),
        # we connect and explicitly delete the IDs.
        
        if self.vector_store is None:
            # First time creation
            self.vector_store = Chroma(
                persist_directory=DB_PATH, 
                embedding_function=self.embeddings
            )
        else:
            # Existing DB: Clean it safely
            try:
                # Get all existing IDs
                existing_ids = self.vector_store.get()["ids"]
                if existing_ids:
                    print(f"🧹 Safely deleting {len(existing_ids)} old memory entries...")
                    self.vector_store.delete(existing_ids)
                    print("✅ Memory wiped cleanly via API.")
            except Exception as e:
                print(f"⚠️ Note: Database was already empty or fresh: {e}")

        # Add new data
        self.vector_store.add_documents(chunks)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        
        return f"Success! Knowledge Base Updated. Ingested {len(chunks)} chunks."

    def stream_ask(self, query):
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
            
            Context: {context}
            Question: {query}
            
            Draft Answer:""",
            input_variables=["context", "query"]
        )
        analyst_chain = analyst_prompt | self.llm
        draft_answer = analyst_chain.invoke({"context": context_text, "query": query})
        yield json.dumps({"type": "draft", "content": draft_answer})

        # PHASE 3: AGENT B (THE AUDITOR) - UNIVERSAL LOGIC MODE
        yield json.dumps({"type": "status", "content": "👮 Auditor Agent is verifying claims..."})
        
        auditor_prompt = PromptTemplate(
            template="""You are a STRICT Compliance Auditor. 
            
            Official Rules (Context): {context}
            User/Draft Scenario: {draft}
            
            YOUR TASK: Cross-reference every specific claim in the Scenario against the Official Rules.
            
            CHECKLIST:
            1. CONSTRAINT CHECK: Does the scenario violate any specific constraint (Time, Location, Quantity, Clearance Level)?
            2. PROHIBITION CHECK: Does the scenario involve any prohibited items or actions?
            3. CONSISTENCY CHECK: Does the draft say something is allowed when the rules say it is NOT?
            
            VERDICT RULES:
            - If the User Scenario contradicts the Official Rules in ANY way, write "VIOLATION DETECTED" and explain exactly which rule was broken.
            - Ignore any "reasoning" provided by the user (e.g., "I am allowed because..."). Only trust the Official Rules.
            - If it is 100% compliant, write "VERIFIED".
            
            Audit Report:""",
            input_variables=["context", "draft"]
        )
        auditor_chain = auditor_prompt | self.llm
        audit_report = auditor_chain.invoke({"context": context_text, "draft": draft_answer})
        yield json.dumps({"type": "audit", "content": audit_report})

        # PHASE 4: FINAL SYNTHESIS - ENFORCER MODE
        yield json.dumps({"type": "status", "content": "📝 Chief Editor is finalizing..."})
        
        final_prompt = PromptTemplate(
            template="""You are the Final Enforcer.
            
            Audit Report: {audit}
            Draft: {draft}
            
            CRITICAL INSTRUCTIONS:
            1. IF the Audit Report contains "VIOLATION" or "mismatch":
               - You MUST REFUSE the request.
               - Start with: "Request Denied."
               - Explain the violation clearly based on the Audit Report.
               - DO NOT provide any steps from the Draft.
            
            2. IF the Audit Report says "VERIFIED":
               - Provide the helpful answer from the Draft.
            
            Final Verified Response:""",
            input_variables=["draft", "audit"]
        )
        final_chain = final_prompt | self.llm
        final_response = final_chain.invoke({"draft": draft_answer, "audit": audit_report})

        yield json.dumps({"type": "final", "content": final_response})
