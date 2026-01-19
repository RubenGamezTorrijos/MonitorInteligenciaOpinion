import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://es.trustpilot.com/review/amazon.es'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

containers = soup.select('article[data-service-review-card-paper="true"]')
print(f"Containers found: {len(containers)}")

for i, container in enumerate(containers[:3]):
    print(f"\n--- Review {i+1} ---")
    user = container.select_one('[data-consumer-name-typography="true"]')
    print(f"User: {user.get_text() if user else 'None'}")
    
    date = container.find('time')
    print(f"Date: {date.get('datetime') if date else 'None'}")
    
    text = container.select_one('p[data-service-review-text-typography="true"], p[data-relevant-review-text-typography="true"]')
    print(f"Text Snippet: {text.get_text()[:50] if text else 'None'}...")
    
    title = container.select_one('h2[data-service-review-title-typography="true"]')
    print(f"Title: {title.get_text() if title else 'None'}")
    
    rating_img = container.find('img', alt=lambda x: x and 'estrella' in x.lower())
    print(f"Rating Alt: {rating_img.get('alt') if rating_img else 'None'}")
