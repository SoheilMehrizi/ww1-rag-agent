# WWI RAG Agent

A multilingual Retrieval-Augmented Generation (RAG) agent that answers
customer-support questions about World War I, grounded strictly in a single
source PDF. **LangChain orchestrates the entire pipeline** — document
loading, chunking, vector retrieval, prompt templating, generation, and
output parsing are all LangChain components composed into one LCEL chain.

```
retriever  ->  format_docs  ->  prompt  ->  llm  ->  output parser
```

The LLM is [Arvan Cloud AI](https://panel.arvancloud.ir/aiaas)'s gateway
(`Qwen3-30B-Esfand`), wrapped as a LangChain `ChatOpenAI` model.

---

## ⚠️ Security notice

The current notebook has an **Arvan API key hard-coded in plaintext** in the
configuration cell, and this repository is public. Treat that key as
compromised:

1. **Rotate/revoke it** in the [Arvan panel](https://panel.arvancloud.ir/) immediately.
2. Before committing again, move the key out of the notebook — e.g. load it
   from a git-ignored `secrets.py`, a `.env` file (via `python-dotenv`), or
   an environment variable — even if the rest of the config stays
   hard-coded for simplicity.
3. Consider scrubbing the old key from git history (`git filter-repo` /
   BFG Repo-Cleaner), since rotating the key alone doesn't remove it from
   past commits.

---

## How it works

1. **Load** — `PyPDFLoader` reads every page of the source PDF. This is the
   only document loader in the project; no web/txt/docx loaders are wired
   in.
2. **Split** — `RecursiveCharacterTextSplitter` breaks pages into
   overlapping chunks (1000 chars, 150 overlap) small enough to fit
   alongside a prompt.
3. **Embed & store** — each chunk is embedded with a multilingual model
   (`intfloat/multilingual-e5-base`) and persisted to a local **Chroma**
   vector store, so a Persian, Arabic, or English question can all retrieve
   the same underlying passages.
4. **Retrieve** — at query time, the top-4 most relevant chunks are pulled
   back via a LangChain retriever.
5. **Prompt** — a `ChatPromptTemplate` assembles a system prompt (grounding
   rules, citation format, multilingual answering, hallucination
   prevention, conflicting-evidence handling, prompt-injection resistance)
   plus the retrieved context and the user's question.
6. **Generate** — the prompt is sent to `Qwen3-30B-Esfand` via the Arvan
   Cloud AI gateway, wrapped as a LangChain `ChatOpenAI` model.
7. **Parse** — `StrOutputParser` extracts the final answer string.

## Getting started

### Prerequisites
- Python 3.10+
- Jupyter Lab / Notebook
- An Arvan Cloud AI API key (see the security notice above before reusing
  the one currently in the notebook)

### Setup
```bash
git clone https://github.com/SoheilMehrizi/ww1-rag-agent.git
cd ww1-rag-agent
jupyter lab
```

Place your source file at the path set in the config cell (currently
`World_War_I.pdf`, in the repo root), then open `ww1_rag_agent.ipynb` and
run the cells top to bottom:

| Section | What it does |
|---|---|
| 0. Install dependencies | `%pip install` for LangChain, Chroma, sentence-transformers, etc. |
| 1. Configuration | All settings as constants — PDF path, chunk size, embedding model, Chroma settings, Arvan endpoint/key/model. |
| 2–6. Pipeline components | Loader, splitter, vector store + retriever, prompt template, LLM wrapper. |
| 7. Ingest | Builds the Chroma vector store from the PDF (run once, or again whenever the PDF changes). |
| 8. RAG pipeline | Assembles the LCEL chain and exposes `answer_question(question)`. |
| 9. Try it | Runs one example question end to end. |
| 10. Interactive loop | Ask questions one after another in the notebook; type `exit` to stop. |

> **Note:** `HuggingFaceEmbeddings` from `langchain_community` logs a
> deprecation warning on import. It still works, but the maintained
> replacement is the `langchain-huggingface` package
> (`pip install -U langchain-huggingface` and
> `from langchain_huggingface import HuggingFaceEmbeddings`).

## Sample results

From an actual run against a 60-page World War I PDF:

**Ingestion**
```
Loading docs/ww1.pdf ...
Loaded 60 page(s).
Splitting into chunks ...
Created 228 chunk(s).
Embedding and writing to Chroma ...
Done. Vector store is ready.
```

**Q: What events led to the outbreak of World War I?**

> The events that led to the outbreak of World War I include the rise of
> the German Empire, which disturbed the long-standing balance of power in
> Europe, as mentioned in [Source 2 - page 1]. Additionally, the failure of
> the League of Nations to manage instability during the interwar period
> contributed to the outbreak of World War II in 1939, but this is not
> directly related to the causes of World War I [Source 1 - page 2]. The
> specific events leading to the outbreak of World War I are not detailed
> in the provided context.

This response is a good example of the grounding rules working as intended:
the model distinguishes what the retrieved passages actually support from
what they don't, rather than filling the gap with outside knowledge.

**Q: Who assassinated Archduke Franz Ferdinand?**

> Gavrilo Princip, a Bosnian Serb, killed Archduke Franz Ferdinand of
> Austria. He was one of the members of the group known as Young Bosnia,
> which included other individuals such as Cvjetko Popović, Nedeljko
> Čabrinović, Trifko Grabež, Vaso Čubrilović, and Muhamed Mehmedbašić. They
> were part of a movement that aimed to free Bosnia from Austrian rule.
> Princip shot and killed Franz Ferdinand and his wife Sophie during the
> assassination on 28 June 1914 [Source 1], [Source 3].

**Q: Who started World War I?**

> The question of who started World War I is complex and has been the
> subject of much historical debate. The CONTEXT provided does not
> explicitly state a single nation as the sole starter of the war, but it
> does mention that the conflict began in 1914, following the assassination
> of Archduke Franz Ferdinand of Austria, which triggered a chain of events
> leading to the war. The CONTEXT also notes that the causes of the war
> included the rise of the German Empire, which disturbed the long-standing
> balance of power in Europe [Source 3]. However, no specific nation is
> identified as the sole aggressor in the CONTEXT provided. Therefore,
> based on the information given, it is not possible to definitively answer
> who started the war.

**Q: (a deliberately underspecified follow-up question)**

> The CONTEXT provided does not contain information about who was
> assassinated before the war.

This is the refusal behavior in action: rather than guessing at an
under-specified or unanswerable question, the assistant explicitly says the
context doesn't support an answer.

*(The last two exchanges above are from an interactive session; the exact
question wording wasn't preserved by the notebook, only the answers — the
questions shown are reconstructed from context.)*

## Project structure
```
ww1-rag-agent/
├── ww1_rag_agent.ipynb   # the full pipeline, one notebook
├── World_War_I.pdf       # source document (path set in the config cell)
└── chroma_db/            # persisted vector store (created on first ingest run)
```

## Troubleshooting

**`AuthenticationError: 401 Unauthorized`** — LangChain's `ChatOpenAI`
forces its own `Authorization: Bearer <api_key>` header on every request
internally. If your gateway needs a different auth scheme (Arvan uses
`apikey <key>`), setting it via `default_headers` at client construction
does **not** work — the auto-injected `Bearer` header wins and you'll get a
401 even though a key is present. Pass it as a per-request header instead:

```python
ChatOpenAI(
    ...,
    model_kwargs={"extra_headers": {"Authorization": ARVAN_API_KEY}},
)
```

`extra_headers` is applied last by the SDK and does override the automatic
header. This is already implemented in section 6 of the notebook.

## Roadmap ideas
- Move secrets out of the notebook (see the security notice above)
- Add a `requirements.txt` / `pyproject.toml` pin for reproducible installs
- Swap `HuggingFaceEmbeddings` for the maintained `langchain-huggingface` package
- Add automated eval questions with expected citations, to catch regressions
- Add a license (MIT, Apache-2.0, etc. — none is currently set)
