# RAG Q&A Bot for PDF Manual

## Overview

A RAG Q&A bot for a 500-page PDF manual using voyage-3-large embeddings and rerank-2.5 for high accuracy, built with Flask.

## Setup

1. Clone the repository:

```bash
git clone <repo_url>
cd rag_qa_bot
```

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. Set Voyage AI API key in `.env`:

   ```bash
   echo "VOYAGE_API_KEY=your_key_here" > .env
   ```

3. Place your PDF manual in `data/manual.pdf`.

4. Run the server:

   ```bash
   python app.py
   ```

   For production, use Gunicorn:

   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## Usage

Query via HTTP:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "How to troubleshoot error X?"}' http://localhost:8000/query
```

## Notes

- Indexes are saved in `indexes/` for reuse.
- Replace mock LLM call in `app.py` with actual API (e.g., Grok at https://x.ai/api).
- Uses Voyage AI’s voyage-3-large for embeddings and rerank-2.5 for reranking (get API key at https://voyageai.com).
- Tune `config.yaml` for chunk size, overlap, etc.
- Flask’s debug mode is enabled by default; disable in production (`debug=False`).