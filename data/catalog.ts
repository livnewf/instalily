export type Product = {
  id: string;
  title: string;
  category: 'Refrigerator' | 'Dishwasher';
  partNumber: string;
  description: string;
  price: string;
  compatibility: string[];
  useCases: string[];
};

export const productCatalog: Product[] = [
  {
    id: 'fridge-filter-4389107',
    title: 'Refrigerator Water Filter',
    category: 'Refrigerator',
    partNumber: '4389107',
    description: 'High-flow replacement water filter compatible with major refrigerator brands.',
    price: '$59.99',
    compatibility: ['Samsung', 'LG', 'Kenmore', 'Whirlpool'],
    useCases: ['Filtered water', 'Ice maker', 'Refrigerator repair'],
  },
  {
    id: 'fridge-ice-maker-241740801',
    title: 'Refrigerator Ice Maker Assembly',
    category: 'Refrigerator',
    partNumber: '241740801',
    description: 'Complete ice maker kit with motor and tray for popular refrigerator models.',
    price: '$129.00',
    compatibility: ['Frigidaire', 'Kenmore', 'Electrolux'],
    useCases: ['Ice production', 'Tray replacement', 'Cooling system maintenance'],
  },
  {
    id: 'fridge-door-gasket-wp4396188',
    title: 'Refrigerator Door Gasket',
    category: 'Refrigerator',
    partNumber: 'WP4396188',
    description: 'Flexible door seal designed to improve energy efficiency and prevent leaks.',
    price: '$44.50',
    compatibility: ['Whirlpool', 'KitchenAid', 'Maytag'],
    useCases: ['Door seal repair', 'Insulation improvement', 'Cold leak fix'],
  },
  {
    id: 'fridge-defrost-heater-5300jb1154g',
    title: 'Defrost Heater Assembly',
    category: 'Refrigerator',
    partNumber: '5300JB1154G',
    description: 'Reliable defrost heater to keep freezer coils clear and maintain consistent cooling.',
    price: '$67.95',
    compatibility: ['LG', 'GE', 'Samsung'],
    useCases: ['Ice build-up fix', 'Freezer maintenance', 'Cooling performance'],
  },
  {
    id: 'dishwasher-spray-arm-w10134119a',
    title: 'Dishwasher Spray Arm',
    category: 'Dishwasher',
    partNumber: 'W10134119A',
    description: 'Precision spray arm replacement for even cleaning coverage in most dishwasher models.',
    price: '$34.99',
    compatibility: ['GE', 'Hotpoint', 'Whirlpool'],
    useCases: ['Wash performance', 'Water distribution', 'Spinning arm replacement'],
  },
  {
    id: 'dishwasher-door-latch-8268676',
    title: 'Dishwasher Door Latch',
    category: 'Dishwasher',
    partNumber: '8268676',
    description: 'Strong door latch assembly ensures secure closing and prevents leaks during cycles.',
    price: '$28.75',
    compatibility: ['Kenmore', 'GE'],
    useCases: ['Door seal repair', 'Cycle start failure', 'Leak prevention'],
  },
  {
    id: 'dishwasher-heating-element-68016656',
    title: 'Dishwasher Heating Element',
    category: 'Dishwasher',
    partNumber: '68016656',
    description: 'Durable heating element for faster drying and better sanitization results.',
    price: '$52.40',
    compatibility: ['Bosch', 'KitchenAid', 'Whirlpool'],
    useCases: ['Drying issue fix', 'Sanitization cycles', 'Water heating replacement'],
  },
  {
    id: 'dishwasher-pump-assembly-12002169',
    title: 'Dishwasher Pump Assembly',
    category: 'Dishwasher',
    partNumber: '12002169',
    description: 'Complete pump and motor assembly to restore water circulation and drainage.',
    price: '$89.95',
    compatibility: ['Maytag', 'Whirlpool'],
    useCases: ['Drainage problem', 'Pump failure', 'Water circulation fix'],
  },
];
