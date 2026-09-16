"""
Run this once (and again any time docs/ww1.pdf changes) to (re)build the
Chroma vector store from the PDF.

    python ingest.py
"""

from pdf_loader import load_pdf_documents
from text_splitter import split_documents
from vector_store import build_vector_store


def main() -> None:
    print("Loading docs/ww1.pdf ...")
    documents = load_pdf_documents()
    print(f"Loaded {len(documents)} page(s).")

    print("Splitting into chunks ...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunk(s).")

    print("Embedding and writing to Chroma ...")
    build_vector_store(chunks)
    print("Done. Vector store is ready.")


if __name__ == "__main__":
    main()
