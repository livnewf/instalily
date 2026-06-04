# PartSelect Chat Agent

A focused Next.js chat agent prototype for PartSelect that supports refrigerator and dishwasher replacement parts.

## Features

- Modern Next.js chat interface with quick action buttons
- Backend logic tailored to refrigerator and dishwasher parts only
- Product card responses for part recommendations
- Order and tracking support guidance
- Extensible structure for adding a vector search or external catalog later

## Architecture

- Frontend: Next.js app router with client-side chat interaction
- Backend: API route handles incoming queries and responds using a catalog retrieval engine
- Data: In-memory product catalog for refrigerator and dishwasher parts

## Run locally

1. Install dependencies

   ```bash
   npm install
   cd backend
   python -m pip install -r requirements.txt
   ```

2. Run the Python backend

   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

3. Run the frontend

   ```bash
   cd ..
   npm run dev
   ```

4. Open http://localhost:3000

## Extensibility

- Add a dedicated vector database backend in `backend/vector_store.py`
- Expand the catalog in `backend/data/catalog.py`
- Customize prompt logic in `backend/agent.py`
- Configure the frontend proxy in `app/api/chat/route.ts`

## Scraping and ingestion

- Use `backend/scrape.py` to perform a one-time scrape of refrigerator and dishwasher items from PartSelect.
- Results are saved to `backend/data/partselect_scraped_products.json`.
- If the site blocks direct requests, use a proxy or a network environment that allows access.

## Notes

- This project now includes merged chat agent behaviors inspired by the Instalily template, including product cards, quick action prompts, and scoped refrigerator/dishwasher support.
