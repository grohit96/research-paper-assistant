import re
import fitz  # PyMuPDF
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file."""
    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        texts.append(page.get_text("text"))
    raw = "\n".join(texts)
    # cleanup
    raw = re.sub(r"[ \t]+", " ", raw)      # remove extra spaces
    raw = re.sub(r"\n{2,}", "\n\n", raw)   # remove extra newlines
    return raw.strip()

def chunk_text(
    text: str,
    words_per_chunk: int = 500,
    overlap: int = 50
) -> List[Dict]:
    """Split text into overlapping chunks of ~500 words."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + words_per_chunk, len(words))
        chunk_words = words[start:end]
        chunks.append({
            "text": " ".join(chunk_words),
            "meta": {"start_word": start, "end_word": end}
        })
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks
