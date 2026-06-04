import ChatPanel from '../components/ChatPanel';

export default function Home() {
  return (
    <main className="page-shell">
      <header className="site-header">
        <div className="brand-row">
          <div className="brand-logo">
            <img src="/partselect-logo.png" alt="PartSelect logo" className="brand-logo-image" />
          </div>
        </div>
        <div className="header-icons">
          <a href="https://www.partselect.com" target="_blank" rel="noopener noreferrer" className="header-icon home-icon" aria-label="Visit PartSelect">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
          </a>
          <a href="tel:1-866-319-8402" className="header-icon phone-icon" aria-label="Call PartSelect">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
          </a>
        </div>
      </header>

      <section className="hero-card">
        <div>
          <span className="eyebrow">PartSelect Support</span>
          <h1>Refrigerator and Dishwasher Inquiries</h1>
          <p>
            Find replacement components, review compatibility, and get help with orders for refrigerator
            and dishwasher parts. The assistant stays focused on appliance parts so you get fast, reliable
            support.
          </p>
          <div className="hero-buttons">
            <a href="https://www.partselect.com/Find-Your-Model-Number/" target="_blank" rel="noopener noreferrer" className="hero-button secondary">
              Can't find your model number?
            </a>
            <a href="https://www.partselect.com/user/self-service/" target="_blank" rel="noopener noreferrer" className="hero-button secondary">
              Want to manage your order?
            </a>
          </div>
        </div>
      </section>
      <ChatPanel />
    </main>
  );
}
