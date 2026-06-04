'use client';

import { useEffect, useMemo, useState } from 'react';
import { Product } from '../data/catalog';
import ProductCard from './ProductCard';

type ChatMessage = {
  role: 'assistant' | 'user';
  text: string;
  products?: Product[];
};

const quickActions = [
  'How can I install part number PS11752778?',
  'Is this part compatible with my WDT780SAEM1 model?',
  'The ice maker on my Whirlpool fridge is not working. How can I fix it?',
  'Help me find a replacement part',
];

export default function ChatPanel() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const welcome = useMemo<ChatMessage[]>(
    () => [
      {
        role: 'assistant',
        text:
          'Hello! I’m your PartSelect assistant for refrigerator and dishwasher parts. Ask me about compatible replacement parts, order support, or product recommendations.',
      },
    ],
    []
  );

  useEffect(() => {
    setMessages(welcome);
  }, [welcome]);

  async function submitMessage(messageText: string) {
    if (!messageText.trim()) return;
    const userMessage: ChatMessage = { role: 'user', text: messageText };
    setMessages((current) => [...current, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: messageText }),
      });

      const data = await response.json();
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        text: data.reply,
        products: data.products,
      };
      setMessages((current) => [...current, assistantMessage]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          text: 'Something went wrong while fetching support. Please try again in a moment.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    submitMessage(input);
  }

  return (
    <div className="chat-shell">
      <div className="chat-window">
        <div className="message-panel">
          {messages.map((message, index) => (
            <div key={`${message.role}-${index}`} className={`message-row ${message.role}`}>
              <div className={`bubble ${message.role}`}>
                {message.text}
                {message.products && message.products.length > 0 && (
                  <div className="product-grid">
                    {message.products.map((product) => (
                      <ProductCard key={product.id} product={product} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="composer">
          <div className="quick-actions">
            {quickActions.map((label) => (
              <button
                key={label}
                type="button"
                className="quick-action"
                onClick={() => submitMessage(label)}
              >
                {label}
              </button>
            ))}
          </div>
          <form onSubmit={handleSubmit}>
            <textarea
              aria-label="Ask the PartSelect assistant"
              placeholder="Ask about refrigerator or dishwasher parts..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              {loading ? 'Thinking...' : 'Send message'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
