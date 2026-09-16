"""
Loads the WWI knowledge base from a single PDF file.

This is intentionally the only loader in the project. If the knowledge base
ever needs a second source, add a new small module rather than growing this
one into a multi-format loader.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

import config


def load_pdf_documents() -> list[Document]:
    """Load every page of config.PDF_PATH as a LangChain Document."""
    loader = PyPDFLoader(config.PDF_PATH)
    return loader.load()
