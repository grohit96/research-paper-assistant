from pdf_utils import extract_text_from_pdf, chunk_text
from rag_pipeline import RagEngine

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # same test PDF you used earlier

    # 1. Extract + chunk text
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    print(f"Loaded {len(chunks)} chunks")

    # 2. Build RAG engine
    rag = RagEngine()
    rag.index_chunks(chunks)

    # 3. Ask some test questions
    queries = [
        "What is the main problem this paper solves?",
        "What method does the paper propose?",
        "Summarize the experiments"
    ]

    for q in queries:
        result = rag.answer(q)
        print(f"\nQ: {q}")
        print(f"Draft Answer: {result['draft_answer'][:300]}...")
        print("Top contexts:")
        for ctx in result["contexts"][:2]:
            print(f"  - Score {ctx['score']:.3f}: {ctx['text'][:150]}...")
