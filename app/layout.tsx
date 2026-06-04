import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PartSelect Chat Agent',
  description: 'Interactive refrigerator and dishwasher parts assistant for PartSelect.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
