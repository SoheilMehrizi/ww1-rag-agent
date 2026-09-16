"""
Command-line entry point for the WWI RAG agent.

First build the vector store once with:
    python ingest.py

Then ask questions with:
    python main.py
"""

from rag_pipeline import answer_question


def main() -> None:
    print("WWI RAG agent. Type a question (or 'exit' to quit).")
    while True:
        question = input("\n> ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        answer = answer_question(question)
        print(f"\n{answer}")


if __name__ == "__main__":
    main()
