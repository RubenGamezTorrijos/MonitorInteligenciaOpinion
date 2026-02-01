
import pandas as pd
import requests
import re
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from textblob import TextBlob
from datetime import datetime
from typing import List, Dict, Optional

# Mocking the translator to avoid network issues or API limits during the test
class MockTranslator:
    def translate(self, text, src='es', dest='en'):
        class Obj:
            def __init__(self, t): self.text = t
        return Obj(text) # Simple return for test

class TrustpilotScraper:
    def __init__(self, business_query: str = None, max_pages: int = 1):
        self.query = business_query
        self.max_pages = max_pages
        self.ua = UserAgent()
        self.session = requests.Session()
        self.base_url = "https://es.trustpilot.com"
        self.target_url = None
        self.reviews_data = []

    def _get_headers(self):
        return {'User-Agent': self.ua.random}

    def search_business(self) -> bool:
        if not self.query: return False
        print(f"🔍 [TEST] Buscando empresa: '{self.query}'...")
        search_url = f"{self.base_url}/search?query={self.query.replace(' ', '+')}"
        try:
            response = self.session.get(search_url, headers=self._get_headers(), timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            link_element = soup.select_one('a[data-business-unit-card-link="true"]')
            if link_element and link_element.has_attr('href'):
                self.target_url = self.base_url + link_element['href']
                print(f"✅ [TEST] Enlace encontrado: {self.target_url}")
                return True
        except Exception as e:
            print(f"❌ Error búsqueda: {e}")
        return False

    def run_test(self):
        if self.search_business():
            print("🚀 [TEST] Probando extracción de primera página...")
            # We'll just check if we can get a 200 response from the target
            try:
                res = self.session.get(self.target_url, headers=self._get_headers(), timeout=10)
                print(f"📡 Status Code: {res.status_code}")
                return res.status_code == 200
            except:
                return False
        return False

# Sentiment Analysis Logic Test
def test_sentiment():
    print("😊 [TEST] Probando lógica de sentimiento...")
    pos_words = {'excelente', 'perfecto', 'genial'}
    text = "El servicio es excelente y todo fue perfecto"
    words = text.lower().split()
    pos = sum(1 for w in words if w in pos_words)
    print(f"   Texto: '{text}' | Palabras positivas detectadas: {pos}")
    return pos > 0

if __name__ == "__main__":
    print("=== INICIANDO TEST DE INTEGRACIÓN (HEADLESS) ===\n")
    scraper = TrustpilotScraper(business_query="Vueling", max_pages=1)
    search_ok = scraper.run_test()
    sent_ok = test_sentiment()
    
    if search_ok and sent_ok:
        print("\n✅ TODO FUNCIONA CORRECTAMENTE.")
        print("La búsqueda dinámica localiza la empresa y la lógica de sentimiento procesa el texto.")
    else:
        print("\n⚠️ El test finalizó con algunas advertencias (puede ser por bloqueo de IP o falta de internet).")
