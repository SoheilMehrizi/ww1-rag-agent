"""Splits loaded documents into overlapping chunks for embedding."""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

import config


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks sized per config.CHUNK_SIZE/CHUNK_OVERLAP."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)
