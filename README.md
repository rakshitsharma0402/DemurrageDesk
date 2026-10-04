# 🚢 DemurrageDesk: Port Terms Assistant

DemurrageDesk is a professional-grade, local RAG (Retrieval-Augmented Generation) assistant designed to parse complex port and shipping terminal documents. It allows users to query free-time rules, demurrage rates, and procedures, providing strictly cited answers and deterministic charge calculations.

**Everything runs locally.** Your documents never leave your machine.

## ✨ Key Features
- **Strict Citations**: The assistant provides direct quotes from documents. A verification layer ensures that the AI didn't hallucinate the quote.
- **Deterministic Calculator**: Instead of letting the LLM do math (which is error-prone), the AI extracts the rules into a structured format, and a pure-Python engine calculates the final charges.
- **Provider Filtering**: Organize documents by shipping line or terminal; filter queries using the sidebar to avoid cross-provider confusion.
- **Privacy First**: Built with Ollama, ChromaDB, and Streamlit for a 100% local execution environment.

## 🛠️ Tech Stack
- **LLM**: Gemma (via Ollama)
- **Embeddings**: nomic-embed-text (via Ollama)
- **Vector Database**: ChromaDB
- **UI**: Streamlit
- **PDF Parsing**: PyMuPDF (fitz)

## 🚀 Getting Started

### 1. Prerequisites
Install [Ollama](https://ollama.ai/) and pull the required models:
```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Data Ingestion
Place your documents (PDF, .md, or .txt) in the following structure:
`data/docs/<shipping_line_or_terminal>/your_document.pdf`

Then, index them into the vector database:
```bash
python ingest.py
```

### 4. Running the App
```bash
streamlit run app.py
```

## ⚠️ Known Limitations & Safeguards
- **PDF Tables**: Tables in PDFs can be challenging to extract. Always verify the retrieved text if numbers seem unusual.
- **OCR**: Scanned PDFs without a text layer are not supported and require OCR preprocessing.
- **Human-in-the-loop**: While the system provides citations, a human should always confirm the final extracted rule before acting on a calculated charge.

## 🧪 Testing
You can run the standalone charge calculator tests to ensure math accuracy:
```bash
python test_demurrage.py
```
