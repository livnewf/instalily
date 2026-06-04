import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .vector_store import VectorStore
from .agent import PartSelectAgent
from .schemas import ChatRequest, ChatResponse, ProductOutput, ProductSearchRequest

app = FastAPI(title='PartSelect Chat Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

vector_store = VectorStore(persist_dir=os.getenv('VECTOR_PERSIST_DIR', 'backend/chroma_db'))
agent = PartSelectAgent(vector_store)


@app.on_event('startup')
def startup_event():
    if vector_store.needs_ingest():
        agent.ingest_corpus()


@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = agent.generate_response(request.query)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post('/product-search', response_model=List[ProductOutput])
def product_search(request: ProductSearchRequest):
    try:
        matches = agent.exact_product_match(request.query)
        return [agent.product_to_output(prod) for prod in matches]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
