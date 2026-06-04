from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://www.partselect.com/Refrigerator-Parts.htm'

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=True)
context = browser.new_context(
    user_agent=(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    )
)
page = context.new_page()

try:
    page.goto(url, wait_until='domcontentloaded', timeout=30000)
    html = page.content()
    
    soup = BeautifulSoup(html, 'lxml')
    
    print(f"Total <a> tags: {len(soup.find_all('a'))}")
    print(f"\nFirst 10 <a> tags:")
    for i, a in enumerate(soup.find_all('a')[:10]):
        href = a.get('href', 'NO HREF')
        text = a.get_text(strip=True)[:50]
        print(f"  {i+1}. href={href[:80]} | text={text}")
    
    print(f"\n<a> tags ending in .htm:")
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.htm'):
            print(f"  {href[:100]}")
    
    print(f"\nPage title: {soup.title.string if soup.title else 'NO TITLE'}")
    print(f"Page has {len(soup.find_all('h1'))} <h1> tags")
    print(f"Page has {len(soup.find_all('h2'))} <h2> tags")
    
finally:
    context.close()
    browser.close()
    playwright.stop()
