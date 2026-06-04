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
        """Block only clearly unrelated topics, not ambiguous appliance questions."""
        clearly_unrelated = re.search(
            r'\b(weather|stock|recipe|sports|politics|movie|music|song|travel|hotel|flight|taxes|homework|essay)\b',
            text,
            re.IGNORECASE,
        )
        return bool(clearly_unrelated)

    def exact_product_match(self, query: str) -> List[Dict]:
        normalized = self.normalize(query)
        matches = []
        seen_ids = set()
        for product in self.search_products:
            part_number = product.get('partNumber', '') if isinstance(product, dict) else getattr(product, 'part_number', '')
            title = (product.get('title', '') if isinstance(product, dict) else getattr(product, 'title', '')).lower()

            pid = product.get('id') if isinstance(product, dict) else getattr(product, 'id', None)
            if pid in seen_ids:
                continue

            if part_number and part_number.lower() in normalized:
                matches.append(product)
                seen_ids.add(pid)
                continue
            if title and (title in normalized or normalized in title):
                matches.append(product)
                seen_ids.add(pid)
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

    def create_prompt(self, query: str, retrieved_docs: List[Dict], exact_matches: List[Dict], history: List[Dict] = None) -> str:
        intro = (
            'You are a helpful PartSelect assistant specializing in refrigerator and dishwasher replacement parts. '
            'Answer clearly and thoroughly using the product and repair information provided. '
            'Use bullet points or numbered steps when explaining installation or repair. '
            'If exact product matches are found, lead with those details. '
            'If the question is completely unrelated to appliance parts or repairs, politely say you only assist with PartSelect refrigerator and dishwasher parts.'
        )

        exact_items = []
        for prod in exact_matches[:3]:
            compatibility = prod.get('compatibility') or []
            use_cases = prod.get('useCases') or []
            exact_items.append(
                f"- {prod.get('title', 'Unknown product')} (Part# {prod.get('partNumber', 'N/A')}, "
                f"Price: {prod.get('price', 'N/A')}) | "
                f"Fits: {', '.join(compatibility) if compatibility else 'See compatibility list'}. "
                f"Use cases: {', '.join(use_cases) if use_cases else 'General replacement'}."
            )

        exact_context = '\n'.join(exact_items) if exact_items else 'No exact part number match found.'

        formatted_docs = []
        for doc in retrieved_docs:
            text = doc.get('text', '')
            text = ' '.join(text.split())
            if len(text) > 500:
                text = text[:500].rstrip() + '...'
            formatted_docs.append(f"- {doc['id']}: {text}")

        context = '\n'.join(formatted_docs)
        if len(context) > 2500:
            context = context[:2500].rstrip() + '\n...'

        intent = self.infer_intent(query)
        intent_instructions = {
            'installation': 'The user wants installation or replacement guidance. Give step-by-step instructions where possible.',
            'compatibility': 'The user wants to know if a part fits their model. Focus on compatibility details and model numbers.',
            'repair': 'The user needs repair or troubleshooting help. Explain the likely cause and how to fix it using the available context.',
            'general': 'Answer the user\'s question using the most relevant product and repair context available.',
        }

        history_section = ''
        if history:
            recent = history[-4:]
            lines = []
            for turn in recent:
                role = turn.get('role', '')
                text = turn.get('text', '')
                if role and text:
                    lines.append(f"{role.capitalize()}: {text}")
            if lines:
                history_section = 'Conversation so far:\n' + '\n'.join(lines) + '\n\n'

        return (
            f"{intro}\n\n"
            f"{history_section}"
            f"Exact product matches:\n{exact_context}\n\n"
            f"Relevant repair and product context:\n{context}\n\n"
            f"User intent: {intent}. {intent_instructions[intent]}\n\n"
            f"User question: {query}\n\n"
            "Answer:"
        )

    def generate_response(self, query: str, history: List[Dict] = None) -> Dict:
        normalized = self.normalize(query)

        if self.is_out_of_scope(normalized) and not self.is_order_request(normalized):
            return {
                'reply': 'I only assist with PartSelect refrigerator and dishwasher replacement parts. Please ask a related parts or repair question.',
                'products': [],
            }

        if self.is_order_request(normalized):
            return {
                'reply': 'I can help with order status and support for PartSelect parts. Please provide your order number or the last 4 digits used at checkout.',
                'products': [],
            }

        exact_matches = self.exact_product_match(normalized)
        retrieved = self.store.query(normalized, n_results=5)

        prompt = self.create_prompt(query, retrieved, exact_matches, history=history)
        answer = generate_text(prompt, max_tokens=600)

        return {
            'reply': answer,
            'products': [self.product_to_output(prod) for prod in exact_matches[:4]] if exact_matches else [],
        }

    def ingest_corpus(self):
        """Ingest documents from CSV files into the vector store."""
        csv_docs = load_all_documents()
        self.store.add_documents(csv_docs)
