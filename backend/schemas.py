from pydantic import BaseModel
from typing import List, Optional

class HistoryMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[HistoryMessage]] = None

class ProductSearchRequest(BaseModel):
    query: str

class ProductOutput(BaseModel):
    id: str
    title: str
    category: str
    partNumber: str
    description: str
    price: str
    compatibility: List[str]
    useCases: List[str]

class ChatResponse(BaseModel):
    reply: str
    products: List[ProductOutput]
