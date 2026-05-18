# Upwork API Support Bot

A RAG-based chatbot that answers developer questions about the Upwork API using the official documentation.

---

## What It Does

- Reads the Upwork API documentation PDF
- Splits it into chunks and stores them in a local vector database (ChromaDB)
- When you ask a question, it finds the most relevant chunks and sends them to Meta-Llama
- The AI answers **only from the documentation** — no hallucinations

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| LLM | Meta-Llama 3.1 8B (via DeepInfra) |
| Framework | LangChain |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| UI | Streamlit |

---

## Project Structure

```
upwork_rag_bot/
├── ingest.py         # Load PDF → chunk → embed → save to ChromaDB
├── rag.py            # Retrieve chunks + call LLM
├── app.py            # Streamlit UI
├── requirements.txt  # Python dependencies
├── .env.example      # API key template
└── SUMMARY.md        # Technical write-up
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
```bash
copy .env.example .env
```
Open `.env` and add your key:
```
DEEPINFRA_API_KEY=your_api_key_here
```

### 3. Place the PDF in this folder
Make sure `API_Documentation_Partial.pdf` is in the same folder as `ingest.py`.

### 4. Build the vector store (run once)
```bash
python ingest.py
```
This reads the PDF, creates chunks, embeds them, and saves to `chroma_store/`.

### 5. Start the app
```bash
streamlit run app.py
```

---

## How RAG Works

```
User Question
     ↓
Convert question to vector (embedding)
     ↓
Find top 3 similar chunks in ChromaDB
     ↓
Send chunks + question to Meta-Llama
     ↓
AI answers only from those chunks
     ↓
Display answer + sources + latency
```

---

## Important Notes

- Run `ingest.py` only once — the vector store is saved to disk
- Never commit your `.env` file
- The embedding model downloads ~90MB on first run (one time only)
- `chroma_store/` folder is auto-generated — no need to submit it