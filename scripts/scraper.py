import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import re
import os

class TrustpilotScraper:
    def __init__(self):
        self.base_url = "https://es.trustpilot.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        }
        self.reviews_data = []
        
        # Setup session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
    def get_company_reviews(self, company_url, pages=3):
        """
        Extrae reseñas de una empresa en Trustpilot
        """
        print(f"Iniciando scraping de {company_url}")
        
        for page in range(1, pages + 1):
            print(f"Procesando página {page}...")
            
            url = company_url if page == 1 else f"{company_url}?page={page}"
            
            try:
                # Delay aleatorio ético
                time.sleep(random.uniform(2, 5))
                response = self.session.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # New selector: article[data-review-card-identifier]
                review_containers = soup.select('article[data-review-card-identifier]')
                
                if not review_containers:
                    # Fallback to generic article
                    review_containers = soup.find_all('article')
                
                if not review_containers:
                    print(f"⚠️ No se encontraron reseñas en la página {page}. Trustpilot podría haber cambiado la estructura.")
                    break
                
                for review in review_containers:
                    review_data = self.extract_review_data(review)
                    if review_data:
                        self.reviews_data.append(review_data)
                
                print(f"  → Extraídas {len(review_containers)} reseñas de la página {page}")
                
            except Exception as e:
                print(f"❌ Error al procesar página {page}: {str(e)}")
                continue
        
        print(f"\nTotal de reseñas extraídas: {len(self.reviews_data)}")
    
    def extract_review_data(self, review_element):
        """Extrae los datos individuales de una reseña con selectores actualizados"""
        try:
            # 1. Título de la reseña
            title_el = review_element.select_one('[data-review-title-typography="true"]')
            titulo = title_el.get_text(strip=True) if title_el else "Sin título"
            
            # 2. Cuerpo del comentario
            text_el = review_element.select_one('[data-review-content-typography="true"]')
            if text_el:
                texto_comentario = text_el.get_text(strip=True).replace("Ver más", "").strip()
            else:
                texto_comentario = "Texto no disponible"
            
            # 3. Puntuación (Rating)
            # selector: div[data-star-rating] img
            rating_container = review_element.select_one('[data-star-rating]')
            puntuacion = None
            if rating_container:
                rating_img = rating_container.find('img')
                if rating_img and 'alt' in rating_img.attrs:
                    match = re.search(r'(\d+)', rating_img['alt'])
                    puntuacion = int(match.group(1)) if match else None
            
            # 4. Fecha de la reseña
            date_element = review_element.find('time')
            fecha = date_element['datetime'] if date_element and 'datetime' in date_element.attrs else datetime.now().strftime("%Y-%m-%d")
            
            # 5. Usuario
            user_el = review_element.select_one('[data-consumer-name-typography="true"]')
            usuario = user_el.get_text(strip=True) if user_el else "Anónimo"
            
            # 6. Ubicación
            location_el = review_element.select_one('[data-consumer-country-typography="true"]')
            if not location_el:
                # Fallback to secondary location selector
                location_el = review_element.select_one('div[class*="styles_consumerExtraDetails"] span')
            ubicacion = location_el.get_text(strip=True) if location_el else "Desconocida"
            
            # 7. Total reseñas del usuario
            count_el = review_element.select_one('[data-consumer-reviews-count-typography="true"]')
            total_resenas_usuario = count_el.get_text(strip=True) if count_el else "0"
            
            return {
                'usuario': usuario,
                'ubicacion': ubicacion,
                'total_resenas_usuario': total_resenas_usuario,
                'puntuacion': puntuacion,
                'fecha': fecha,
                'titulo': titulo,
                'texto_comentario': texto_comentario,
                'fecha_sistema': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"⚠️ Error al extraer datos de reseña: {str(e)}")
            return None
    
    def save_to_csv(self, filename='data/raw/dataset_raw.csv'):
        """Guarda los datos en un archivo CSV asegurando que el directorio existe"""
        if not self.reviews_data:
            print("No hay datos para guardar")
            return None
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df = pd.DataFrame(self.reviews_data)
        
        # Eliminar duplicados
        df = df.drop_duplicates(subset=['usuario', 'texto_comentario', 'fecha'])
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Datos guardados en {filename}. Filas únicas: {len(df)}")
        return df

def main():
    """Función principal para ejecutar el scraper"""
    
    # URL de Amazon España
    amazon_url = "https://es.trustpilot.com/review/www.amazon.es"
    
    scraper = TrustpilotScraper()
    
    # Scrapear reseñas (Rubén & Juanes)
    scraper.get_company_reviews(amazon_url, pages=3)
    
    # Guardar datos (Fase 1)
    df = scraper.save_to_csv('data/raw/dataset_raw.csv')
    
    # Mostrar información básica
    if df is not None:
        print("\n" + "="*50)
        print("MUESTRA DEL DATASET EXTRAÍDO")
        print("="*50)
        print(f"Reseñas rescatadas: {len(df)}")
        print(df[['usuario', 'puntuacion', 'texto_comentario']].head(3))

if __name__ == "__main__":
    main()