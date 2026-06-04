import { productCatalog, type Product } from '../data/catalog';

const outOfScopeHint =
  'I only assist with refrigerator and dishwasher replacement parts for PartSelect. For other questions, please ask a support channel dedicated to general appliance sales.';

function normalize(text: string) {
  return text.trim().toLowerCase();
}

function findRelevantProducts(query: string): Product[] {
  const normalized = normalize(query);
  const matches = productCatalog
    .map((product) => {
      const score = [
        product.category.toLowerCase().includes(normalized) ? 3 : 0,
        product.partNumber.toLowerCase().includes(normalized) ? 4 : 0,
        product.title.toLowerCase().includes(normalized) ? 3 : 0,
        product.description.toLowerCase().includes(normalized) ? 2 : 0,
        product.compatibility.some((brand) => normalized.includes(brand.toLowerCase())) ? 2 : 0,
        product.useCases.some((useCase) => normalized.includes(useCase.toLowerCase())) ? 1 : 0,
      ].reduce((sum, value) => sum + value, 0);
      return { product, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .map(({ product }) => product);

  if (matches.length) {
    return matches.slice(0, 4);
  }

  return productCatalog.filter((product) => product.category === 'Refrigerator').slice(0, 2).concat(productCatalog.filter((product) => product.category === 'Dishwasher').slice(0, 2));
}

function isOverviewRequest(text: string) {
  return /(recommend|show|browse|find|search)/i.test(text);
}

function isOrderRequest(text: string) {
  return /(order|purchase|buy|track|status|shipping|invoice)/i.test(text);
}

function isOutOfScope(text: string) {
  return !/(refrigerator|fridge|dishwasher|part|water filter|ice maker|spray arm|latch|heater|pump|gasket|order|track|status)/i.test(text);
}

function createOrderResponse(query: string) {
  if (/(track|status)/i.test(query)) {
    return {
      reply:
        'I can help you track an existing appliance parts order. Please provide your order number or the last 4 digits used at checkout so I can verify the shipment status.',
      products: [],
    };
  }

  return {
    reply:
      'Need help ordering a part? Share your appliance make and model or the part number you need, and I’ll recommend compatible refrigerator or dishwasher components and next steps for checkout.',
    products: findRelevantProducts(query),
  };
}

export function generateAgentReply(query: string) {
  const text = query.trim();
  if (!text) {
    return {
      reply:
        'Send a question about refrigerator or dishwasher replacement parts. For example, ask for a water filter, ice maker, spray arm, or order tracking help.',
      products: [],
    };
  }

  if (isOutOfScope(text) && !isOrderRequest(text)) {
    return {
      reply: outOfScopeHint,
      products: [],
    };
  }

  if (isOrderRequest(text)) {
    return createOrderResponse(text);
  }

  const results = findRelevantProducts(text);
  const productCount = results.length;
  const categoryLabel = /dishwasher/i.test(text) ? 'dishwasher' : /refrigerator|fridge/i.test(text) ? 'refrigerator' : 'related';

  let reply = `Here are ${productCount} ${categoryLabel} parts that fit your request.`;
  if (/part number/i.test(text) || /\b\d{4,}\b/.test(text)) {
    reply = `I found these matches based on the part number and appliance information you provided.`;
  }
  if (isOverviewRequest(text) && !productCount) {
    reply = 'I found several refrigerator and dishwasher replacement parts that may fit your appliance. Review the cards below for compatibility details.';
  }

  return {
    reply,
    products: results,
  };
}
