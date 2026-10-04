# Port Terms Assistant

Local RAG assistant for port and shipping documents: ask about free time, demurrage, detention and procedures,
get cited answers, and compute charges with plain code. Gemma (Ollama) + Chroma + Streamlit. Documents stay on your machine.

## Setup
```
ollama pull gemma3:4b
ollama pull nomic-embed-text
pip install -r requirements.txt
python test_demurrage.py
python ingest.py
streamlit run app.py
```
Put documents in `data/docs/<shipping_line_or_terminal>/` (PDF, .md or .txt). The folder name becomes the filter in the sidebar.
A fictional sample is included so you can test end to end. Replace it before your real demo, and use only sample or
anonymized documents in any public repo. Override models with `GEN_MODEL` and `EMBED_MODEL`.

## Known limits
- Tables in PDFs often extract badly. Check retrieved text if numbers look wrong.
- Scanned PDFs have no text layer and need OCR first.
- Answers can be wrong. Citations are checked to appear in the retrieved text, but a human should confirm any charge.

## For the write-up
- Write 15-20 real questions with known answers, and record: correct and cited / correct but poorly cited / wrong / correctly "not found".
- Compare two settings (chunk size, TOP_K, or model size) on the same questions.
- Keep one failure and the fix (for example: wrong provider retrieved, so add the sidebar filter).
