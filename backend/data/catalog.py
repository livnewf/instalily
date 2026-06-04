from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: str
    title: str
    category: str
    part_number: str
    description: str
    price: str
    compatibility: List[str]
    use_cases: List[str]

product_catalog = [
    Product(
        id='fridge-filter-4389107',
        title='Refrigerator Water Filter',
        category='Refrigerator',
        part_number='4389107',
        description='High-flow replacement water filter compatible with major refrigerator brands.',
        price='$59.99',
        compatibility=['Samsung', 'LG', 'Kenmore', 'Whirlpool'],
        use_cases=['Filtered water', 'Ice maker', 'Refrigerator repair'],
    ),
    Product(
        id='fridge-ice-maker-241740801',
        title='Ice Maker Assembly',
        category='Refrigerator',
        part_number='241740801',
        description='Complete ice maker kit with motor and tray for popular refrigerator models.',
        price='$129.00',
        compatibility=['Frigidaire', 'Kenmore', 'Electrolux'],
        use_cases=['Ice production', 'Tray replacement', 'Cooling system maintenance'],
    ),
    Product(
        id='fridge-door-gasket-wp4396188',
        title='Refrigerator Door Gasket',
        category='Refrigerator',
        part_number='WP4396188',
        description='Flexible door seal designed to improve energy efficiency and prevent leaks.',
        price='$44.50',
        compatibility=['Whirlpool', 'KitchenAid', 'Maytag'],
        use_cases=['Door seal repair', 'Insulation improvement', 'Cold leak fix'],
    ),
    Product(
        id='dishwasher-spray-arm-w10134119a',
        title='Dishwasher Spray Arm',
        category='Dishwasher',
        part_number='W10134119A',
        description='Precision spray arm replacement for even cleaning coverage in most dishwasher models.',
        price='$34.99',
        compatibility=['GE', 'Hotpoint', 'Whirlpool'],
        use_cases=['Wash performance', 'Water distribution', 'Spinning arm replacement'],
    ),
    Product(
        id='dishwasher-door-latch-8268676',
        title='Dishwasher Door Latch',
        category='Dishwasher',
        part_number='8268676',
        description='Strong door latch assembly ensures secure closing and prevents leaks during cycles.',
        price='$28.75',
        compatibility=['Kenmore', 'GE'],
        use_cases=['Door seal repair', 'Cycle start failure', 'Leak prevention'],
    ),
    Product(
        id='dishwasher-heating-element-68016656',
        title='Dishwasher Heating Element',
        category='Dishwasher',
        part_number='68016656',
        description='Durable heating element for faster drying and better sanitization results.',
        price='$52.40',
        compatibility=['Bosch', 'KitchenAid', 'Whirlpool'],
        use_cases=['Drying issue fix', 'Sanitization cycles', 'Water heating replacement'],
    ),
]

support_documents = [
    {
        'id': 'order-support',
        'text': (
            'PartSelect supports order tracking, shipping questions, and returns for replacement parts. '
            'Provide the order number or last 4 digits of the payment method to look up your order status.'
        ),
        'metadata': {'type': 'support', 'topic': 'order'},
    },
    {
        'id': 'compatibility-help',
        'text': (
            'For refrigerator and dishwasher parts, compatibility is based on brand, model, and part number. '
            'Always verify your appliance make and model before selecting a replacement part.'
        ),
        'metadata': {'type': 'support', 'topic': 'compatibility'},
    },
]
