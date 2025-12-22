# Desarrollado por Rubén

import requests
from bs4 import BeautifulSoup
from collections import Counter

url = "https://es.trustpilot.com/review/www.amazon.es"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check for potential review containers
    articles = soup.find_all('article')
    print(f"Number of 'article' tags: {len(articles)}")
    
    classes = []
    for art in articles:
        if 'class' in art.attrs:
            classes.append(' '.join(art['class']))
            
    with open('debug_log.txt', 'w', encoding='utf-8') as f:
        f.write("\nArticle classes found:\n")
        for cls, count in Counter(classes).most_common(5):
            f.write(f"  {cls}: {count}\n")

        if articles:
            f.write("\nStructure of first article:\n")
            first_art = articles[0]
            # Recursively print tags with classes to identify structure
            for child in first_art.recursiveChildGenerator():
                if child.name and child.name in ['p', 'h2', 'div', 'span', 'time', 'img', 'a']:
                    cls = child.get('class', [])
                    txt = child.get_text(strip=True)[:30]
                    if cls or txt:
                        f.write(f"Tag: {child.name} | Class: {cls} | Text: {txt}\n")
                        if child.name == 'img':
                             f.write(f"  Alt: {child.get('alt', 'No alt')}\n")
                        if child.name == 'time':
                             f.write(f"  Datetime: {child.get('datetime', 'No datetime')}\n")


except Exception as e:
    print(f"Error: {e}")
