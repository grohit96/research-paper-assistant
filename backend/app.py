from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_pipeline import RagEngine
from backend.pdf_utils import extract_text_from_pdf, chunk_text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Research Paper Assistant API")

# Allow frontend to call backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔴 In production, restrict to actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG engine instance
rag = RagEngine()

# Request model for /ask
class Question(BaseModel):
    question: str


# ----------------- API ROUTES -----------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    with open("uploaded.pdf", "wb") as f:
        f.write(pdf_bytes)

    text = extract_text_from_pdf("uploaded.pdf")
    chunks = chunk_text(text)

    print(f"📄 Extracted {len(text.split())} words, created {len(chunks)} chunks")  # DEBUG

    if not chunks:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    rag.index_chunks(chunks)

    return {"status": "ok", "chunks_indexed": len(chunks)}


@app.post("/ask")
def ask(payload: Question):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = rag.answer(payload.question)
    return {
        "answer": result.get("answer", "No answer received."),
        "contexts": result.get("contexts", []),
    }


# ----------------- STATIC FRONTEND -----------------

# Serve frontend build only after API routes are defined
app.mount("/", StaticFiles(directory="frontend_dist", html=True), name="static")

# Optional: serve index.html at root
@app.get("/")
async def serve_root():
    return FileResponse("frontend_dist/index.html")
