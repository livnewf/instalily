from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

url = 'https://www.partselect.com/Refrigerator-Parts.htm'

playwright = sync_playwright().start()
# Try with headless=False
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(
    user_agent=(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    ),
    extra_http_headers={
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
)
page = context.new_page()

try:
    time.sleep(2)
    page.goto(url, wait_until='networkidle', timeout=45000)
    time.sleep(3)
    html = page.content()
    
    soup = BeautifulSoup(html, 'lxml')
    print(f"Title: {soup.title.string if soup.title else 'NO TITLE'}")
    print(f"Total <a> tags: {len(soup.find_all('a'))}")
    print(f"first 5 .htm links:")
    count = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.htm') and count < 5:
            print(f"  {href[:100]}")
            count += 1
    
finally:
    context.close()
    browser.close()
    playwright.stop()
