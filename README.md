# WWI RAG Agent

A small, modular Retrieval-Augmented Generation pipeline that answers
questions about World War I, grounded in a single PDF (`docs/ww1.pdf`), using
Chroma for vector search and the Arvan Cloud AI gateway (Qwen3-30B-Esfand)
for generation.

## Layout

| File | Responsibility |
|---|---|
| `config.py` | All settings, hard-coded (no environment variables). |
| `pdf_loader.py` | Loads `docs/ww1.pdf` — the only document loader in the project. |
| `text_splitter.py` | Splits loaded pages into overlapping chunks. |
| `vector_store.py` | Builds/opens the Chroma collection and runs similarity search. |
| `prompts.py` | System prompt and prompt assembly (grounding, citations, multilingual, anti-hallucination, prompt-injection safety). |
| `llm_client.py` | Calls the Arvan Cloud AI gateway's chat completions endpoint. |
| `ingest.py` | One-time script: PDF → chunks → Chroma. |
| `rag_pipeline.py` | Retrieval + generation, combined into one function. |
| `main.py` | Interactive command-line entry point. |

## Usage

```bash
pip install -r requirements.txt

# Place your file at docs/ww1.pdf, then build the vector store:
python ingest.py

# Ask questions:
python main.py
```

Re-run `python ingest.py` any time `docs/ww1.pdf` changes — it rebuilds the
Chroma collection from scratch.
