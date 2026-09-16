"""
Builds and queries the Chroma vector store for the WWI knowledge base.

Embeddings are multilingual so a Persian, Arabic, or English question can all
retrieve the same underlying (likely English) source passages.
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

import config


def get_embedding_function() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)


def build_vector_store(chunks: list[Document]) -> Chroma:
    """Embed chunks and persist them to disk, replacing any existing collection."""
    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_function(),
        collection_name=config.CHROMA_COLLECTION_NAME,
        persist_directory=config.CHROMA_PERSIST_DIR,
    )


def load_vector_store() -> Chroma:
    """Reopen a previously-built Chroma collection from disk."""
    return Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        persist_directory=config.CHROMA_PERSIST_DIR,
    )


def retrieve_relevant_chunks(vector_store: Chroma, query: str) -> list[Document]:
    """Return the top-K chunks most relevant to the query."""
    return vector_store.similarity_search(query, k=config.TOP_K)
