# Professional Streamlit Opinion Intelligence Monitor - Scraper Service

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from typing import List, Dict, Optional
from datetime import datetime
from src.config.constants import TRUSTPILOT_BASE_URL, SCRAPE_REVIEWS_PER_PAGE, TRUSTPILOT_SELECTORS

class TrustpilotScraper:
    """Service specialized for Trustpilot.com (Dynamic Analysis) as implemented in Laboratory Mode."""
    
    def __init__(self, domain: str):
        self.domain = domain.lower().replace(" ", "").replace("https://", "").replace("http://", "").split('/')[0]
        self.base_url = f"{TRUSTPILOT_BASE_URL}{self.domain}"
        self.session = requests.Session()
        
        # Realistic headers form the notebook
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def safe_extract(self, element, selector: str, attribute: str = None, default: str = ""):
        """Safely extracts data from an HTML element."""
        try:
            found = element.select_one(selector)
            if not found:
                return default
            if attribute:
                return found.get(attribute, default)
            return found.get_text(strip=True)
        except Exception:
            return default

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extracts relevant keywords from review text (E-commerce focused)."""
        ecommerce_keywords = [
            'cliente', 'entrega', 'problema', 'servicio', 'pedido',
            'devolución', 'reembolso', 'atención', 'producto', 'contacto',
            'cancelación', 'retraso', 'garantía', 'envío', 'pago',
            'estafa', 'fraude', 'repartidor', 'locker', 'prime'
        ]
        text_lower = text.lower()
        found_keywords = [kw for kw in ecommerce_keywords if kw in text_lower]
        return found_keywords[:top_n]

    def scrape_reviews(self, max_reviews: int = 50) -> pd.DataFrame:
        """Executes full scraping across multiple pages."""
        all_reviews = []
        target_pages = (max_reviews // 20) + 1  # 20 per page average
        
        for page in range(1, target_pages + 1):
            url = f"{self.base_url}?page={page}"
            try:
                response = self.session.get(url, timeout=15)
                if response.status_code != 200:
                    break
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Use constants
                review_selectors = TRUSTPILOT_SELECTORS['review_card']
                
                page_reviews_elements = []
                for selector in review_selectors:
                    elements = soup.select(selector)
                    if elements:
                        page_reviews_elements = elements
                        break
                
                for element in page_reviews_elements:
                    review_data = self._extract_review_details(element)
                    if review_data:
                        all_reviews.append(review_data)
                        
                if len(all_reviews) >= max_reviews:
                    break
                    
                time.sleep(1.5) # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Error on page {page}: {e}")
                break
                
        df = pd.DataFrame(all_reviews)
        if not df.empty:
            df = df.head(max_reviews)
            df['longitud'] = df['text'].apply(lambda x: len(str(x).split()))
            df['timestamp_scraping'] = datetime.now().isoformat()
        return df

    def _extract_review_details(self, element) -> Optional[Dict]:
        """Extracts structured data from a single review element."""
        try:
            # Text selectors from constants
            text = ""
            for selector in TRUSTPILOT_SELECTORS['text']:
                text = self.safe_extract(element, selector)
                if text and len(text) > 10:
                    break
            
            if not text: return None

            # User selectors
            user_name = "Anónimo"
            for selector in TRUSTPILOT_SELECTORS['user']:
                user_name = self.safe_extract(element, selector)
                if user_name: break

            # Rating logic (Robust Multi-language)
            rating = 3 
            try:
                # 1. Check for 'alt' attribute in img (Standard)
                rating_img = element.select_one('img[alt*="estrellas"], img[alt*="stars"]')
                if rating_img:
                    alt_text = rating_img.get('alt', '')
                    # Matches "5 de 5", "5 estrellas", "Rated 5", "Valorado con 5"
                    rating_match = re.search(r'(\d)', alt_text)
                    if rating_match:
                        rating = int(rating_match.group(1))
                else:
                    # 2. Check for data-rating attribute
                    rating_div = element.select_one('div[data-rating]')
                    if rating_div:
                        rating = int(rating_div.get('data-rating', 3))
                    else:
                        # 3. Check for specific class names containing the number
                        star_div = element.select_one('div[class*="star-rating"]')
                        if star_div:
                            # Class might be like "star-rating_starRating__9_fBy"
                            # Attempt to find common numeric patterns in siblings/children
                            text_ref = star_div.get_text()
                            num_match = re.search(r'(\d)', text_ref)
                            if num_match:
                                rating = int(num_match.group(1))
            except Exception:
                pass

            # Date selectors
            date_str = ""
            for selector in TRUSTPILOT_SELECTORS['date']:
                date_str = self.safe_extract(element, selector, 'datetime')
                if date_str: break
            
            # Keywords
            keywords = self.extract_keywords(text)

            return {
                "user_id": user_name,  # Using name as ID for simplicity
                "user": user_name,
                "text": text,
                "rating": rating,
                "product_id": self.domain, # Using domain as item ID
                "date": date_str if date_str else datetime.now().strftime('%Y-%m-%d'),
                "keywords": ", ".join(keywords) if keywords else "Ninguna",
                "domain": self.domain
            }
        except Exception:
            return None
