# PartSelect Python Backend

This backend provides a Python-based RAG pipeline for the PartSelect chatbot.

## Key components

- `app.py` — FastAPI service exposing `/chat`
- `catalog.py` — curated product and support content
- `vector_store.py` — Chroma-based vector store for semantic retrieval
- `agent.py` — RAG orchestration, exact match handling, and prompt generation
- `llm_client.py` — LLM adapter using `llm` or `transformers`

## Install

```bash
cd backend
python -m pip install -r requirements.txt
```

## Run

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Environment

You can configure:

- `OPENAI_API_KEY` — use OpenAI via `llm`
- `OPENAI_MODEL` — model name such as `gpt-4o-mini`
- `LOCAL_MODEL` — fallback local transformers model
- `VECTOR_PERSIST_DIR` — Chroma persistence path

## Notes

This backend is designed around a dedicated vector store for durable retrieval and constrained PartSelect knowledge.

## Scraping and ingestion

A one-time scraper is available in `backend/scrape.py` that targets refrigerator and dishwasher category pages and also ingests repair/support documentation from PartSelect's refrigerator and dishwasher repair sections.

The scraper writes two files:

- `backend/data/partselect_scraped_products.json`
- `backend/data/partselect_scraped_support.json`

Run:

```bash
cd backend
python scrape.py
```

If the site returns HTTP 403 access denied, the scraper may need a proxy or another network environment to fetch the pages successfully.
