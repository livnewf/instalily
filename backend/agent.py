import re
from typing import List, Dict

from .ingest_csv import load_all_documents, load_products_for_search
from .vector_store import VectorStore
from .llm_client import generate_text


class PartSelectAgent:
    def __init__(self, store: VectorStore):
        self.store = store
        self.search_products = load_products_for_search()

    @staticmethod
    def normalize(text: str) -> str:
        return text.strip().lower()

    @staticmethod
    def is_order_request(text: str) -> bool:
        return bool(re.search(r'\b(order|track|status|shipping|invoice|purchase|buy)\b', text, re.IGNORECASE))

    @staticmethod
    def infer_intent(text: str) -> str:
        if re.search(r'\b(install|installation|replace|mount|attach|installing|how do i|how can i)\b', text, re.IGNORECASE):
            return 'installation'
        if re.search(r'\b(compatible|fit|fits|works with|will this work|model|matching|interchange|replacement for)\b', text, re.IGNORECASE):
            return 'compatibility'
        if re.search(r'\b(fix|repair|broken|not working|leak|leaking|icemaker|ice maker|freeze|cold|no ice|no water|stopped)\b', text, re.IGNORECASE):
            return 'repair'
        return 'general'

    @staticmethod
    def is_out_of_scope(text: str) -> bool:
        return not bool(
            re.search(
                r'\b(refrigerator|fridge|dishwasher|part|water filter|ice maker|spray arm|latch|heater|pump|gasket)\b',
                text,
                re.IGNORECASE,
            )
        )

    def exact_product_match(self, query: str) -> List[Dict]:
        normalized = self.normalize(query)
        matches = []
        for product in self.search_products:
            part_number = getattr(product, 'part_number', None) or product.get('partNumber') if isinstance(product, dict) else None
            title = getattr(product, 'title', '').lower() if not isinstance(product, dict) else product.get('title', '').lower()
            compatibility = getattr(product, 'compatibility', []) if not isinstance(product, dict) else product.get('compatibility', [])

            if part_number and part_number.lower() in normalized:
                matches.append(product)
                continue
            if any(brand.lower() in normalized for brand in compatibility if isinstance(brand, str)):
                matches.append(product)
                continue
            if title and (title in normalized or normalized in title):
                matches.append(product)
        return matches

    @staticmethod
    def product_to_output(product: Dict) -> Dict:
        if isinstance(product, dict):
            return {
                'id': product.get('id', ''),
                'title': product.get('title', ''),
                'category': product.get('category', ''),
                'partNumber': product.get('partNumber', ''),
                'description': product.get('description', ''),
                'price': product.get('price', ''),
                'compatibility': product.get('compatibility', []),
                'useCases': product.get('useCases', []),
            }

        return {
            'id': product.id,
            'title': product.title,
            'category': product.category,
            'partNumber': product.part_number,
            'description': product.description,
            'price': product.price,
            'compatibility': product.compatibility,
            'useCases': product.use_cases,
        }

    def create_prompt(self, query: str, retrieved_docs: List[Dict], exact_matches: List[Dict]) -> str:
        intro = (
            'You are a helpful PartSelect chatbot assistant for refrigerator and dishwasher parts. '
            'Answer in a concise, natural paragraph using only the most relevant product and repair information available. '
            'If exact product matches are found, combine those product details with repair or blog context to give the best answer. '
            'Do not repeat raw source formatting or display metadata fields. '
            'If the question is unrelated, explain that you only handle PartSelect refrigerator and dishwasher parts.'
        )

        exact_items = []
        for prod in exact_matches[:2]:
            compatibility = prod.get('compatibility') or []
            use_cases = prod.get('useCases') or []
            exact_items.append(
                f"- {prod.get('title', 'Unknown product')} (Part {prod.get('partNumber', 'N/A')}) "
                f"Compatibility: {', '.join(compatibility) if compatibility else 'None'}. "
                f"Use cases: {', '.join(use_cases) if use_cases else 'None'}."
            )

        exact_context = '\n'.join(exact_items) if exact_items else 'No exact product match found.'

        formatted_docs = []
        for doc in retrieved_docs:
            text = doc.get('text', '')
            text = ' '.join(text.split())
            if len(text) > 250:
                text = text[:250].rstrip() + '...'
            formatted_docs.append(f"- {doc['id']}: {text}")

        context = '\n'.join(formatted_docs)
        if len(context) > 900:
            context = context[:900].rstrip() + '\n...'

        intent = self.infer_intent(query)
        intent_instructions = {
            'installation': 'The user wants to know how to install or replace a part. Focus on installation guidance and relevant product details.',
            'compatibility': 'The user wants to know whether a part fits their model. Focus on compatibility and whether the part is appropriate.',
            'repair': 'The user is asking for repair or troubleshooting help. Focus on how to fix the underlying issue using product and repair guide context.',
            'general': 'The user is asking a general question. Use the context to provide the most relevant answer.'
        }

        return (
            f"{intro}\n\n"
            f"Exact product matches:\n{exact_context}\n\n"
            f"Relevant context:\n{context}\n\n"
            f"User intent: {intent}. {intent_instructions[intent]}\n\n"
            f"User question: {query}\n\n"
            "Answer using the above product and repair information in complete, natural sentences."
        )

    def generate_response(self, query: str) -> Dict:
        normalized = self.normalize(query)

        if self.is_out_of_scope(normalized) and not self.is_order_request(normalized):
            return {
                'reply': 'I only assist with PartSelect refrigerator and dishwasher replacement parts. Please ask a related parts or order support question.',
                'products': [],
            }

        if self.is_order_request(normalized):
            return {
                'reply': (
                    'I can help with order status and order support for PartSelect parts. Please provide your order number or the last 4 digits used at checkout.'
                ),
                'products': [],
            }

        exact_matches = self.exact_product_match(normalized)
        retrieved = self.store.query(normalized, n_results=2)

        prompt = self.create_prompt(query, retrieved, exact_matches)
        answer = generate_text(prompt)

        return {
            'reply': answer,
            'products': [self.product_to_output(prod) for prod in exact_matches[:4]] if exact_matches else [],
        }

    def ingest_corpus(self):
        """Ingest documents from CSV files into the vector store."""
        csv_docs = load_all_documents()
        self.store.add_documents(csv_docs)
