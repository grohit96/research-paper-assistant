# 📚 Research Paper Assistant (RAG Web App)

A **web application** that lets you **upload any research paper (PDF)** and then **ask natural language questions** about it.  
Built using **FastAPI + React + FAISS + LLMs**, this project demonstrates how to apply **Retrieval-Augmented Generation (RAG)** to make academic and technical documents interactive.  

---

## ✨ Features
- 📂 Upload a PDF research paper
- 🔍 Automatic text extraction, chunking, and embedding generation
- 🧠 Store embeddings in a **vector database (FAISS)**
- 💬 Ask questions in natural language → get answers grounded in the paper
- 📖 Answers include **references/snippets** from the original text
- 🌐 Clean web app (React + Tailwind) with file upload + chat interface
- 🐳 Easy to run with **Docker Compose**

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, PyMuPDF/pdfplumber, FAISS, OpenAI/HuggingFace embeddings, LangChain (optional)  
- **Frontend:** React (Vite) + TailwindCSS  
- **Infra:** Docker, Docker Compose, GitHub Actions (CI/CD)  

---

🚀 How to Run Research Paper Assistant
Option 1: Run with Docker (Recommended ✅)

This bundles backend + frontend into one container.

# Clone the repo
git clone https://github.com/grohit96/research-paper-assistant.git
cd research-paper-assistant

# Build the image
docker build -t research-assistant .

# Run the container
docker run -p 8000:8000 research-assistant


👉 Open your browser at http://localhost:8000

You’ll see the web app (upload PDFs, ask questions).

Option 2: Run Locally without Docker (Dev Mode)

Run backend & frontend separately.

Backend (FastAPI)

cd backend
python -m venv venv
source venv/bin/activate   # (on Windows: venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000


Backend runs at → http://127.0.0.1:8000

Frontend (React + Vite)

cd frontend
npm install
npm run dev


Frontend runs at → http://127.0.0.1:5173

📂 Project Structure
backend/        # FastAPI backend (PDF ingestion, RAG pipeline, Q&A)
frontend/       # React frontend (file upload + chat UI)
Dockerfile      # Build fullstack image (backend + built frontend)
requirements.txt

