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

## 📂 Project Structure
