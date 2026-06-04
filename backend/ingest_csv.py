import csv
import json
import os
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PARTS_CSV = os.path.join(DATA_DIR, 'all_parts.csv')
REPAIRS_CSV = os.path.join(DATA_DIR, 'all_repairs.csv')
BLOGS_CSV = os.path.join(DATA_DIR, 'partselect_blogs.csv')


def infer_category(appliance_text: str) -> str:
    text = (appliance_text or '').strip().lower()
    if 'dishwasher' in text:
        return 'Dishwasher'
    if 'refrigerator' in text or 'freezer' in text:
        return 'Refrigerator'
    return 'Refrigerator'


def parse_product_row(row: Dict[str, str], idx: int) -> Dict:
    part_id = row.get('part_id') or row.get('mpn_id') or f'part_{idx}'
    part_name = row.get('part_name', 'Unknown Part').strip()
    part_price = row.get('part_price', '').strip()
    brand = row.get('brand', '').strip()
    symptoms = row.get('symptoms', '').strip()
    appliance_types = row.get('appliance_types', '').strip()
    replace_parts = row.get('replace_parts', '').strip()
    availability = row.get('availability', '').strip()
    product_url = row.get('product_url', '').strip()

    category = infer_category(appliance_types)
    compatibility = [brand] if brand else []
    use_cases = []
    if symptoms:
        use_cases.append(symptoms)
    if replace_parts:
        use_cases.append(replace_parts)
    if appliance_types:
        use_cases.append(appliance_types)

    text_parts = [
        f"Product: {part_name}",
        f"Brand: {brand}",
        f"Category: {category}",
    ]

    if part_price:
        text_parts.append(f"Price: {part_price}")
    if symptoms:
        text_parts.append(f"Fixes symptoms: {symptoms}")
    if replace_parts:
        text_parts.append(f"Replacement parts: {replace_parts}")
    if availability:
        text_parts.append(f"Availability: {availability}")
    if product_url:
        text_parts.append(f"Product URL: {product_url}")

    document_text = ' '.join([part for part in text_parts if part])

    return {
        'id': f'product_{part_id}',
        'title': part_name,
        'category': category,
        'partNumber': part_id,
        'description': f'{part_name} ({category})',
        'price': part_price or 'N/A',
        'compatibility': compatibility,
        'useCases': use_cases,
        'url': product_url,
        'document': {
            'id': f'product_{part_id}',
            'text': document_text,
            'metadata': {
                'type': 'product',
                'part_id': part_id,
                'brand': brand,
                'price': part_price,
                'url': product_url,
            }
        }
    }


def load_products() -> List[Dict]:
    """Load product data from CSV and convert to document format."""
    documents = []
    
    try:
        with open(PARTS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                parsed = parse_product_row(row, idx)
                documents.append(parsed['document'])
    
    except FileNotFoundError:
        print(f"Warning: {PARTS_CSV} not found")
    except Exception as e:
        print(f"Error loading products: {e}")
    
    print(f"Loaded {len(documents)} products")
    return documents


def load_products_for_search() -> List[Dict]:
    """Load product data from CSV and build a searchable product catalog."""
    products = []
    
    try:
        with open(PARTS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                parsed = parse_product_row(row, idx)
                products.append({
                    'id': parsed['id'],
                    'title': parsed['title'],
                    'category': parsed['category'],
                    'partNumber': parsed['partNumber'],
                    'description': parsed['description'],
                    'price': parsed['price'],
                    'compatibility': parsed['compatibility'],
                    'useCases': parsed['useCases'],
                })
    except FileNotFoundError:
        print(f"Warning: {PARTS_CSV} not found")
    except Exception as e:
        print(f"Error loading search products: {e}")
    
    print(f"Loaded {len(products)} searchable products")
    return products


def load_repairs() -> List[Dict]:
    """Load repair/troubleshooting guide data from CSV."""
    documents = []
    
    try:
        with open(REPAIRS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                product = row.get('Product', 'Unknown')
                symptom = row.get('symptom', 'Unknown')
                description = row.get('description', '')
                parts = row.get('parts', '')
                difficulty = row.get('difficulty', '')
                repair_video = row.get('repair_video_url', '')
                
                text_parts = [
                    f"How to fix {symptom.lower()} {product.lower()}",
                    f"{description}",
                ]
                
                if parts:
                    text_parts.append(f"Common parts needed: {parts}")
                
                if difficulty:
                    text_parts.append(f"Difficulty: {difficulty}")
                
                if repair_video:
                    text_parts.append(f"Video guide available")
                
                text = ' '.join(text_parts)
                
                documents.append({
                    'id': f'repair_{idx}_{symptom.replace(" ", "_")}',
                    'text': text,
                    'metadata': {
                        'type': 'repair',
                        'product': product,
                        'symptom': symptom,
                        'difficulty': difficulty,
                        'video_url': repair_video,
                    }
                })
    
    except FileNotFoundError:
        print(f"Warning: {REPAIRS_CSV} not found")
    except Exception as e:
        print(f"Error loading repairs: {e}")
    
    print(f"Loaded {len(documents)} repair guides")
    return documents


def load_blogs() -> List[Dict]:
    """Load blog article data from CSV."""
    documents = []
    
    try:
        with open(BLOGS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                title = row.get('title', 'Unknown Article')
                url = row.get('url', '')
                
                text = f"{title}. Visit the guide at PartSelect for full instructions."
                
                documents.append({
                    'id': f'blog_{idx}_{title.replace(" ", "_")[:30]}',
                    'text': text,
                    'metadata': {
                        'type': 'blog',
                        'title': title,
                        'url': url,
                    }
                })
    
    except FileNotFoundError:
        print(f"Warning: {BLOGS_CSV} not found")
    except Exception as e:
        print(f"Error loading blogs: {e}")
    
    print(f"Loaded {len(documents)} blog articles")
    return documents


def load_all_documents() -> List[Dict]:
    """Load all documents from CSV files."""
    all_docs = []
    
    all_docs.extend(load_products())
    all_docs.extend(load_repairs())
    all_docs.extend(load_blogs())
    
    print(f"\nTotal documents loaded: {len(all_docs)}")
    return all_docs


def save_documents_to_json(documents: List[Dict], output_path: str = None):
    """Save documents to JSON for inspection."""
    if output_path is None:
        output_path = os.path.join(DATA_DIR, 'ingested_documents.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Documents saved to {output_path}")


if __name__ == '__main__':
    docs = load_all_documents()
    save_documents_to_json(docs)
