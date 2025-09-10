from pdf_utils import extract_text_from_pdf, chunk_text

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # put a PDF in backend/ folder and rename it sample.pdf
    text = extract_text_from_pdf(pdf_path)
    print("Raw text length:", len(text))

    chunks = chunk_text(text)
    print(f"Generated {len(chunks)} chunks")
    for i, c in enumerate(chunks[:3]):  # print first 3 chunks
        print(f"\n--- Chunk {i+1} ---\n{c['text'][:300]}...")
