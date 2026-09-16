"""Ties retrieval (Chroma) and generation (Arvan gateway) into one call."""

from vector_store import load_vector_store, retrieve_relevant_chunks
from prompts import build_messages
from llm_client import chat_completion


def answer_question(question: str) -> str:
    """Run one full RAG turn: retrieve relevant chunks, then ask the LLM."""
    vector_store = load_vector_store()
    chunks = retrieve_relevant_chunks(vector_store, question)
    messages = build_messages(question, chunks)
    return chat_completion(messages)
