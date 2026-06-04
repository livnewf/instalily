# PartSelect Chat Agent

A full-stack chat agent for PartSelect's e-commerce platform, scoped to refrigerator and dishwasher replacement parts. The agent answers product questions, guides installation and repair, surfaces matching parts as product cards, and routes order inquiries — all within a branded Next.js interface backed by a Python RAG pipeline powered by Claude.

---

## Features

### User-Facing
- **Conversational chat** with multi-turn memory — follow-up questions retain context from earlier in the conversation
- **Product cards** surface directly in the chat for exact part number matches, showing title, part number, price, compatibility, and use cases
- **Quick-action prompts** on load for common intents (installation, compatibility, repair, finding a part)
- **Intent detection** routes each query to the most relevant response style — installation steps use numbered lists, repair questions include likely causes, compatibility questions focus on model fit
- **Order support routing** — order/tracking queries receive a focused response directing users to provide their order number
- **Links to PartSelect** — header icons link directly to PartSelect.com and support phone number; hero section links to model-number lookup and order self-service
- **Enter to submit** — standard keyboard UX with Shift+Enter for newline

### Agent Behavior
- Focused on refrigerator and dishwasher parts only; off-topic questions (recipes, weather, sports, etc.) are declined gracefully
- Part number queries (e.g. `PS11752778`) trigger exact catalog lookup before semantic search
- Semantic search retrieves the 5 most relevant documents across parts, repairs, and blog content
- Conversation history (last 4 turns) is included in every prompt for contextual follow-ups

---

## Architecture

```
Browser (Next.js)
    │  POST /api/chat { query, history }
    ▼
Next.js API Route (route.ts)
    │  Proxies to Python backend
    ▼
FastAPI Backend (app.py)
    │
    ├── PartSelectAgent (agent.py)
    │     ├── Intent detection & scope guard
    │     ├── Exact part number match  ──▶  CSV catalog (9,600+ parts)
    │     ├── Vector search            ──▶  ChromaDB + sentence-transformers
    │     └── Prompt assembly + LLM call
    │
    └── LLM: Anthropic Claude Haiku (llm_client.py)
```

### Frontend — Next.js (App Router)
- `app/page.tsx` — branded shell with PartSelect header, hero section, and `<ChatPanel />`
- `components/ChatPanel.tsx` — stateful chat UI; manages message history, sends `{ query, history }` to the API route, renders product cards inline
- `components/ProductCard.tsx` — displays matched parts with title, part number, price, compatibility, and use cases
- `app/api/chat/route.ts` — thin proxy forwarding requests to the Python backend

### Backend — Python / FastAPI
- `backend/app.py` — FastAPI server with `/chat` and `/product-search` endpoints
- `backend/agent.py` — core agent logic: intent detection, exact match, vector retrieval, prompt construction, LLM call
- `backend/vector_store.py` — ChromaDB wrapper with `all-MiniLM-L6-v2` embeddings for semantic search
- `backend/ingest_csv.py` — loads and formats parts, repairs, and blog CSVs into documents for ingestion
- `backend/llm_client.py` — LLM abstraction with Anthropic as primary backend, OpenAI and local transformers as fallbacks
- `backend/schemas.py` — Pydantic models for request/response validation including conversation history

### Data
All data sourced from [zehuiwu/partselect-agent](https://github.com/zehuiwu/partselect-agent) due to PartSelect's web-scraping restrictions.

| File | Contents | Rows |
|---|---|---|
| `backend/data/all_parts.csv` | Part name, ID, price, symptoms, brand, appliance type, availability, URL | ~9,600 |
| `backend/data/all_repairs.csv` | Repair guides by symptom, difficulty, video links | ~21 |
| `backend/data/partselect_blogs.csv` | Blog article titles and URLs | ~215 |

The vector store is built on first run and persisted to `backend/chroma_db/`.

---

## Running the App

### Prerequisites
- Node.js 18+
- Python 3.10+
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

### 1. Install dependencies

```bash
# Python
cd /path/to/instalily
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Node
npm install
```

### 2. Start the Python backend

```bash
ANTHROPIC_API_KEY=sk-ant-... ./run_backend.sh
```

The first run ingests all CSVs and builds the vector store — this takes ~1–2 minutes. Subsequent starts are fast.

### 3. Start the Next.js frontend

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Extensibility

| Area | How to extend |
|---|---|
| **Add more appliance categories** | Add CSVs to `backend/data/`, update `ingest_csv.py` to load them, and expand the intent/scope regex patterns in `agent.py` |
| **Swap the LLM** | `llm_client.py` is a single-function abstraction — swap the Anthropic call for any other provider without touching the agent |
| **Richer product cards** | Add fields (e.g. install video URL, product URL) to `ProductOutput` in `schemas.py` and `ProductCard.tsx` |
| **Persistent user sessions** | The `history` field is already passed end-to-end — storing it server-side (Redis, database) would enable session persistence across page reloads |
| **Live catalog** | Replace the CSV loader in `ingest_csv.py` with a PartSelect API or product feed; the vector store and agent are catalog-agnostic |
| **Streaming responses** | The Anthropic SDK supports streaming — update `llm_client.py` to yield chunks and add a streaming API route for faster perceived response time |

---

## Example Queries the Agent Handles

- *"How do I install part PS11752778?"*
- *"Is this spray arm compatible with my WDT780SAEM1?"*
- *"My Whirlpool fridge ice maker stopped working — what could be wrong?"*
- *"What's the price of the defrost heater for an LG refrigerator?"*
- *"My dishwasher is leaking from the door — what part do I need?"*
- *"I need to track my order"*
