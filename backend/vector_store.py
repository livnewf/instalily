import os
import logging
from typing import List, Dict

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self, persist_dir: str = 'backend/chroma_db'):
        self.persist_dir = persist_dir
        self.client = chromadb.Client(
            Settings(
                persist_directory=self.persist_dir,
                is_persistent=True,
            )
        )
        self.collection = self.client.get_or_create_collection(
            name='partselect',
            metadata={'description': 'PartSelect embedding collection'},
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.embedding_model.encode(texts, show_progress_bar=False, convert_to_numpy=True).tolist()

    def add_documents(self, documents: List[Dict]):
        ids = [doc['id'] for doc in documents]
        texts = [doc['text'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]
        embeddings = self.embed_texts(texts)

        # Deduplicate by ID preserving first occurrence.
        seen = set()
        unique_ids = []
        unique_texts = []
        unique_metadatas = []
        unique_embeddings = []
        duplicates = 0
        for i, _id in enumerate(ids):
            if _id in seen:
                duplicates += 1
                logging.warning(f"VectorStore.add_documents: duplicate id {_id} at index {i}; skipping.")
                continue
            seen.add(_id)
            unique_ids.append(_id)
            unique_texts.append(texts[i])
            unique_metadatas.append(metadatas[i])
            unique_embeddings.append(embeddings[i] if embeddings is not None else None)

        if duplicates:
            logging.info(f"VectorStore.add_documents: skipped {duplicates} duplicate ids.")

        if not unique_ids:
            logging.info("VectorStore.add_documents: no new documents to add after deduplication.")
            return

        self.collection.add(ids=unique_ids, documents=unique_texts, metadatas=unique_metadatas, embeddings=unique_embeddings)
        # chromadb client may or may not expose persist(); handle gracefully
        try:
            self.client.persist()
        except AttributeError:
            logging.info("Chroma client has no persist() method; skipping explicit persist.")

    def query(self, query_text: str, n_results: int = 4) -> List[Dict]:
        embedding = self.embed_texts([query_text])[0]
        results = self.collection.query(query_embeddings=[embedding], n_results=n_results, include=['documents', 'metadatas', 'distances'])
        docs = []
        for i in range(len(results['ids'][0])):
            docs.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
            })
        return docs

    def needs_ingest(self) -> bool:
        return self.collection.count() == 0
