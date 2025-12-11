from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from backend.rag_engine import UniversalBrain

app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Brain
brain = UniversalBrain()

class QueryRequest(BaseModel):
    query: str

@app.post("/query_stream")
def query_stream(request: QueryRequest):
    def event_stream():
        try:
            for chunk in brain.stream_ask(request.query):
                yield chunk + "\n"
        except Exception as e:
            import json
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")

@app.post("/ingest")
def trigger_ingestion():
    # This cleans the Vector DB
    status = brain.ingest_data()
    return {"status": status}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. CLEANUP: Wipe the 'data/' folder so we don't mix old PDFs with new ones
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data")
    
    # 2. SAVE: Save only the new file
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": "Old data wiped. New file uploaded successfully."}
