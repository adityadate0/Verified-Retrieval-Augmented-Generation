from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from backend.rag_engine import UniversalBrain

app = FastAPI()

# FIX: Add CORS to allow Streamlit to communicate freely
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
        # We wrap this in a try-except to ensure the stream closes cleanly
        try:
            for chunk in brain.stream_ask(request.query):
                yield chunk + "\n"
        except Exception as e:
            # Send an error chunk so frontend knows to stop
            import json
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")

@app.post("/ingest")
def trigger_ingestion():
    status = brain.ingest_data()
    return {"status": status}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists("data"):
        os.makedirs("data")
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Uploaded successfully"}
