import re

import chromadb
import ollama
from pydantic import BaseModel

from config import DB_DIR, EMBED_MODEL, GEN_MODEL, TOP_K


class Citation(BaseModel):
    source: str
    page: int
    quote: str          # one full sentence copied exactly from the excerpt


class Answer(BaseModel):
    # Field order matters: the model writes its evidence first, then the answer.
    citations: list[Citation]
    answer: str
    found: bool = False  # overwritten by code: True only if a quote is verified in the retrieved text


class Tier(BaseModel):
    from_day: int
    to_day: int | None = None
    rate: float


class Rule(BaseModel):
    free_days: int
    tiers: list[Tier]
    currency: str = ""
    notes: str = ""     # e.g. calendar vs working days, container size, import/export


def _col():
    return chromadb.PersistentClient(DB_DIR).get_collection("docs")


def providers() -> list[str]:
    return sorted({m["provider"] for m in _col().get(include=["metadatas"])["metadatas"]})


def retrieve(question: str, provider: str | None = None, k: int = TOP_K):
    q = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]
    kw = {"where": {"provider": provider}} if provider else {}
    res = _col().query(query_embeddings=[q], n_results=k, **kw)
    return [{"text": d, **m} for d, m in zip(res["documents"][0], res["metadatas"][0])]


def _context(chunks):
    return "\n\n".join(f"[{c['source']} p.{c['page']}]\n{c['text']}" for c in chunks)


def _norm(s: str) -> str:
    """Lowercase and keep only letters/digits, so markdown, bullets and spacing don't break quote matching."""
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def ask(question: str, chunks):
    system = (
        "You answer questions about port, terminal and shipping line terms using ONLY the excerpts provided. "
        "Rules: (1) First list citations: each has the source file, page, and ONE full sentence copied character "
        "for character from the excerpt (do not shorten, merge or reword sentences). "
        "(2) Then write a short answer based only on those quotes. If a quote gives a rule for a range of days "
        "(for example days 8 to 14), say which range the asked day falls in. "
        "(3) If the excerpts do not contain the answer, return an empty citations list and the answer "
        "'Not found in your documents.' Never say the excerpts lack the answer while also citing them. "
        "(4) Respect container size, import vs export, and which line or terminal applies; if unclear, say so. "
        "(5) Do not add up charges; the calculator does that."
    )
    resp = ollama.chat(
        model=GEN_MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": f"Excerpts:\n{_context(chunks)}\n\nQuestion: {question}"}],
        format=Answer.model_json_schema(), options={"temperature": 0},
    )
    ans = Answer.model_validate_json(resp["message"]["content"])
    good, bad = [], []
    for cit in ans.citations:
        q = _norm(cit.quote)
        match = next((c for c in chunks if len(q) >= 10 and q in _norm(c["text"])), None)
        if match:  # trust the retrieved chunk's source/page over whatever the model wrote
            good.append(Citation(source=match["source"], page=match["page"], quote=cit.quote))
        else:
            bad.append(cit)
    ans.found = bool(good)
    if not good:
        ans.answer = ("I couldn't back this answer with a quote from your documents, so I'm not showing it."
                      if bad else "Not found in your documents.")
    return ans, good, bad


def extract_rule(question: str, chunks) -> Rule:
    """Pull free days and rate tiers out of the retrieved text. A human confirms before any maths."""
    system = (
        "Extract the free days and the per-day rate tiers from the excerpts for the case in the question. "
        "Tiers use absolute day numbers (for example free 7 days, then days 8-14 at 40, day 15 onward at 80 gives "
        "free_days=7 and tiers [{8,14,40},{15,null,80}]). Use only numbers present in the excerpts. "
        "If you can't find them, return free_days=0 and no tiers, and explain in notes."
    )
    resp = ollama.chat(
        model=GEN_MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": f"Excerpts:\n{_context(chunks)}\n\nCase: {question}"}],
        format=Rule.model_json_schema(), options={"temperature": 0},
    )
    return Rule.model_validate_json(resp["message"]["content"])