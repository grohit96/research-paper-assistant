from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import RagEngine
from pdf_utils import extract_text_from_pdf, chunk_text

app = FastAPI(title="Research Paper Assistant API")

# Allow frontend (React) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG engine (kept in memory for now)
rag = RagEngine()

# Request model for questions
class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    # Save temporarily
    with open("uploaded.pdf", "wb") as f:
        f.write(pdf_bytes)

    text = extract_text_from_pdf("uploaded.pdf")
    chunks = chunk_text(text)

    if not chunks:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    rag.index_chunks(chunks)
    return {"chunks_indexed": len(chunks)}

@app.post("/ask")
def ask(payload: Question):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = rag.answer(payload.question)
    return result
