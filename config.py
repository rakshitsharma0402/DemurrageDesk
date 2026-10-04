import os

GEN_MODEL = os.getenv("GEN_MODEL", "gemma3:4b")      # check `ollama list` for the exact tag you pulled
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
DB_DIR = "chroma_db"
DOCS_DIR = "data/docs"          # data/docs/<shipping_line_or_terminal>/<file.pdf|md|txt>
CHUNK_CHARS = 900
TOP_K = 5
