# 🚢 DemurrageDesk: Port Terms Assistant

**A privacy-first local RAG assistant for shipping tariffs and terminal documents.**

DemurrageDesk lets users ask questions about free-time rules, demurrage rates, and port procedures in plain English. It provides **verified citations** to the source document and uses a **deterministic Python calculator** instead of letting an LLM perform the math.

> **LLM for interpretation. Python for arithmetic. Evidence before answers.**

🔒 **Everything runs locally. Your documents never leave your machine.**

---

## 🎥 Demo

[▶️ Watch the DemurrageDesk Demo](https://youtu.be/0rzp8J_cE7c)

The demo shows:

- Asking a question about a shipping tariff
- Retrieving relevant document excerpts
- Returning the source file and page number
- Verifying the citation against the source
- Extracting free days and tiered rates
- Calculating the estimated demurrage charge with Python

---

## ✨ Features

- 📚 **Local RAG** — query your own shipping line and terminal documents
- 🔎 **Verified citations** — citations are checked against the retrieved source
- 🧮 **Deterministic calculator** — Python calculates charges; the LLM extracts the rules
- 🚢 **Provider filtering** — separate documents by shipping line or terminal
- 🔐 **Privacy-first** — Gemma, embeddings, ChromaDB, and the application run locally
- 👤 **Human-in-the-loop** — review extracted free days and rate tiers before calculation

---

## 🛡️ How It Works

```text
PDF / Markdown / TXT
        ↓
   PyMuPDF Parsing
        ↓
 Chunk + Page Metadata
        ↓
    Embeddings
        ↓
     ChromaDB
        ↓
    Retrieval
        ↓
      Gemma
        ↓
 Citation Verification
        ↓
 Structured Rate Rules
        ↓
 Python Calculator
        ↓
 Charge + Breakdown
```

### Why separate the LLM from the calculator?

Consider a tariff with:

```text
Days 1–7   → Free
Days 8–14  → $40/day
Day 15+    → $80/day
```

For a container held for 16 days:

```text
7 × $40 + 2 × $80 = $440
```

The LLM extracts the rule.

**Python performs the calculation.**

The application also verifies that the model's quoted evidence exists in the retrieved document before treating the answer as supported.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Gemma 3 via Ollama |
| Embeddings | nomic-embed-text via Ollama |
| Vector Database | ChromaDB |
| PDF Parsing | PyMuPDF |
| Structured Output | Pydantic |
| UI | Streamlit |
| Calculator | Pure Python |

---

## 📁 Project Structure

```text
DemurrageDesk/
├── app.py
├── config.py
├── demurrage.py
├── ingest.py
├── rag.py
├── test_demurrage.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
│
├── data/
│   └── docs/
│       └── <shipping_line_or_terminal>/
│           └── documents.pdf
│
└── chroma_db/
```

### Core files

- **`app.py`** — Streamlit interface
- **`rag.py`** — retrieval, Gemma interaction, citation verification, and rule extraction
- **`ingest.py`** — document parsing, chunking, embeddings, and ChromaDB indexing
- **`demurrage.py`** — deterministic charge calculation
- **`test_demurrage.py`** — calculator tests
- **`config.py`** — application configuration

---

## 🚀 Getting Started

### 1. Install Ollama

Install [Ollama](https://ollama.com/) and pull the required models:

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

Verify them:

```bash
ollama list
```

### 2. Clone the repository

```bash
git clone https://github.com/rakshitsharma0402/DemurrageDesk.git
cd DemurrageDesk
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your documents

Place PDF, Markdown, or text files under:

```text
data/docs/<shipping_line_or_terminal>/
```

For example:

```text
data/docs/
├── carrier_a/
│   └── tariff.pdf
└── terminal_b/
    └── terms.pdf
```

### 5. Build the vector index

```bash
python ingest.py
```

### 6. Run the application

```bash
streamlit run app.py
```

---

## 🧪 Testing

Run the deterministic calculator tests:

```bash
python test_demurrage.py
```

Tests cover:

- Free-time periods
- Tier transitions
- Open-ended tiers
- Tier ordering
- Deterministic charge calculations

---

## ⚠️ Limitations

- Complex PDF tables may not extract correctly.
- Scanned PDFs require OCR preprocessing.
- Local language models can still misunderstand complex tariff language.
- Calendar-day vs. working-day rules should be confirmed against the contract.
- Always verify the source document before using a calculated charge operationally.

**DemurrageDesk is a reading and calculation aid, not a billing authority.**

---

## 🏆 Hacktoberfest Weekend Challenge

Built for the **Hacktoberfest Weekend Challenge: Build for a Friend**.

### Prize Category

**Best Use of Gemma**

Gemma runs locally through Ollama as the generation model powering the document question-answering workflow.
