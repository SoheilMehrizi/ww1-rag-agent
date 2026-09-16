"""
Hard-coded configuration for the WWI RAG agent.

No environment variables are read anywhere in this project — every setting
lives here as a plain constant. Edit this file directly to change behavior.
"""

# ---------------------------------------------------------------------------
# Source document
# ---------------------------------------------------------------------------
# The knowledge base is a single PDF. No other loader (web, txt, docx, csv...)
# is wired into the pipeline on purpose.
PDF_PATH = "docs/ww1.pdf"

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# ---------------------------------------------------------------------------
# Embeddings (multilingual, so Persian / Arabic / English queries all work)
# ---------------------------------------------------------------------------
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-base"

# ---------------------------------------------------------------------------
# Vector store (Chroma, persisted to disk)
# ---------------------------------------------------------------------------
CHROMA_PERSIST_DIR = "chroma_db"
CHROMA_COLLECTION_NAME = "ww1_knowledge_base"
TOP_K = 4

# ---------------------------------------------------------------------------
# Arvan Cloud AI gateway (OpenAI-compatible chat completions endpoint)
# ---------------------------------------------------------------------------
ARVAN_ENDPOINT = (
    "https://arvancloudai.ir/gateway/models/Qwen3-30B-A3B/"
    "-PCq8hHs5kP1mI7Jg00djd0mNmvG-ovlBmUPycaEKHNiFHyhGL7Z_-5tvUdFEV6FT7go"
    "XBGqTV6FSdn8hPqv0lxZ1YyBMMl5zMPwm93Ok47Ug8Qo3MRheNIdpcGXCueoGHDzNQya"
    "wSTPdRaNzlexgtuZemH5Tfsh9mvpeMGxpM5T7AfuMcavTnsi-929DgGhyVxtQYeSfECv"
    "0_bMa18Bz0OBl_Gq7FH9dQ1cBam3EkO5H6bPkEv8QLidHT4JHFNj/v1"
)
ARVAN_API_KEY = "apikey b71a3492-1801-52e4-80a9-ef3de382b466"
ARVAN_MODEL_NAME = "Qwen3-30B-Esfand"

# Chat completion request settings
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 800
LLM_TIMEOUT_SECONDS = 60
