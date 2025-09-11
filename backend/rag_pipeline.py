import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
from openai import OpenAI

load_dotenv()  # load .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RagEngine:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def index_chunks(self, chunks: List[str]):
        embeddings = self.model.encode(chunks)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))
        self.chunks = chunks

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec).astype("float32"), k)
        results = []
        for idx, score in zip(I[0], D[0]):
            results.append({"text": self.chunks[idx], "score": float(score)})
        return results

    def generate_answer(self, question: str, contexts: List[Dict]) -> str:
    # Extract only text fields safely
        context_texts = [str(c.get("text", "")) for c in contexts if isinstance(c, dict)]
        context_text = "\n\n".join(context_texts)

        prompt = f"""
        You are a helpful assistant answering questions about a research paper.
        Use only the context below to answer the question concisely.

        Context:
        {context_text}

        Question: {question}
        Answer:
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight and cheap
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()


    def answer(self, question: str) -> Dict:
        ctx = self.retrieve(question)
        concise_answer = self.generate_answer(question, ctx)
        return {
            "question": question,
            "contexts": ctx,
            "answer": concise_answer
        }
