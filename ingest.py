"""Index tariff/terms documents into Chroma.

Folder layout: data/docs/<provider>/<file>. The folder name becomes the `provider`
metadata (shipping line or terminal), which the app uses as a filter.
Supports .pdf, .md and .txt. Page numbers are stored on every chunk for citations.
"""
import pathlib

import chromadb
import fitz  # pymupdf
import ollama

from config import CHUNK_CHARS, DB_DIR, DOCS_DIR, EMBED_MODEL


def pages(path: pathlib.Path):
    if path.suffix.lower() == ".pdf":
        with fitz.open(path) as pdf:
            for i, page in enumerate(pdf, start=1):
                yield i, page.get_text()
    else:
        yield 1, path.read_text(encoding="utf-8")


def split(text: str, size: int = CHUNK_CHARS):
    """Paragraph-based chunks of ~size chars, carrying the last paragraph over as overlap."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunk, out = [], []
    for p in paras:
        if chunk and sum(len(x) for x in chunk) + len(p) > size:
            out.append("\n\n".join(chunk))
            chunk = chunk[-1:]
        chunk.append(p)
    if chunk:
        out.append("\n\n".join(chunk))
    return out


def main():
    docs, metas = [], []
    for path in sorted(pathlib.Path(DOCS_DIR).rglob("*")):
        if path.suffix.lower() not in {".pdf", ".md", ".txt"}:
            continue
        provider = path.parent.name if path.parent != pathlib.Path(DOCS_DIR) else "general"
        for page_no, text in pages(path):
            for piece in split(text):
                docs.append(piece)
                metas.append({"source": path.name, "page": page_no, "provider": provider})
    if not docs:
        raise SystemExit(f"No documents found under {DOCS_DIR}/")

    client = chromadb.PersistentClient(DB_DIR)
    try:
        client.delete_collection("docs")
    except Exception:
        pass
    col = client.create_collection("docs")
    for i in range(0, len(docs), 32):
        batch = docs[i:i + 32]
        embs = ollama.embed(model=EMBED_MODEL, input=batch)["embeddings"]
        col.add(ids=[str(i + j) for j in range(len(batch))], documents=batch,
                embeddings=embs, metadatas=metas[i:i + 32])
    print(f"Indexed {len(docs)} chunks from {len({m['source'] for m in metas})} files.")


if __name__ == "__main__":
    main()
