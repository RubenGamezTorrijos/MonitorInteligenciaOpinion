import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import re

class TrustpilotScraper:
    def __init__(self):
        self.base_url = "https://es.trustpilot.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
        }
        self.reviews_data = []
        
    def get_company_reviews(self, company_url, pages=3):
        """
        Extrae reseñas de una empresa en Trustpilot
        
        Args:
            company_url: URL de la página de reseñas de la empresa
            pages: Número de páginas a scrapear
        """
        print(f"Iniciando scraping de {company_url}")
        
        for page in range(1, pages + 1):
            print(f"Procesando página {page}...")
            
            # Construir URL de la página
            if page == 1:
                url = company_url
            else:
                url = f"{company_url}?page={page}"
            
            try:
                # Petición HTTP con delay aleatorio
                time.sleep(random.uniform(1, 3))
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                # Parsear HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Encontrar todos los contenedores de reseñas
                review_containers = soup.find_all('article')
                
                if not review_containers:
                    print("No se encontraron reseñas en esta página")
                    break
                
                # Extraer datos de cada reseña
                for review in review_containers:
                    review_data = self.extract_review_data(review)
                    if review_data:
                        self.reviews_data.append(review_data)
                
                print(f"  → Extraídas {len(review_containers)} reseñas de la página {page}")
                
            except Exception as e:
                print(f"Error al procesar página {page}: {str(e)}")
                continue
        
        print(f"\nTotal de reseñas extraídas: {len(self.reviews_data)}")
    
    def extract_review_data(self, review_element):
        """Extrae los datos individuales de una reseña"""
        try:
            # Extraer texto del comentario
            # Buscamos div con clase que contenga 'reviewText'
            text_div = review_element.find('div', class_=lambda x: x and 'reviewText' in x)
            if text_div:
                text_p = text_div.find('p')
                texto = text_p.get_text(strip=True) if text_p else text_div.get_text(strip=True)
            else:
                texto = "Texto no disponible"
            
            # Extraer puntuación (estrellas)
            # Buscamos img con alt que contenga 'estrellas' o 'stars'
            rating_img = review_element.find('img', alt=lambda x: x and ('estrellas' in x or 'stars' in x))
            if rating_img:
                alt_text = rating_img['alt']
                match = re.search(r'(\d+)', alt_text)
                puntuacion = int(match.group(1)) if match else None
            else:
                puntuacion = None
            
            # Extraer fecha
            date_element = review_element.find('time')
            fecha = date_element['datetime'] if date_element else datetime.now().strftime("%Y-%m-%d")
            
            # Extraer usuario
            user_element = review_element.find(['span', 'div'], class_=lambda x: x and 'consumerName' in x)
            usuario = user_element.get_text(strip=True) if user_element else "Anónimo"
            
            # Extraer título de la reseña
            title_element = review_element.find('h2')
            if not title_element:
                 # A veces el título está en un a con clase typography_heading-s
                 title_element = review_element.find('a', class_=lambda x: x and 'heading-s' in x)
            
            titulo = title_element.get_text(strip=True) if title_element else "Sin título"
            
            return {
                'titulo': titulo,
                'texto': texto,
                'puntuacion': puntuacion,
                'fecha': fecha,
                'usuario': usuario,
                'timestamp_extraccion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"Error al extraer datos de reseña: {str(e)}")
            return None
    
    def save_to_csv(self, filename='data/raw/reviews_raw.csv'):
        """Guarda los datos en un archivo CSV"""
        if not self.reviews_data:
            print("No hay datos para guardar")
            return
        
        df = pd.DataFrame(self.reviews_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Datos guardados en {filename}")
        return df

def main():
    """Función principal para ejecutar el scraper"""
    
    # URLs de empresas para scrapear (ejemplos)
    empresas = [
        "https://es.trustpilot.com/review/www.amazon.es",
        "https://es.trustpilot.com/review/www.booking.com",
        "https://es.trustpilot.com/review/www.elcorteingles.es"
    ]
    
    scraper = TrustpilotScraper()
    
    # Scrapear reseñas de Amazon como ejemplo
    scraper.get_company_reviews(empresas[0], pages=2)
    
    # Guardar datos
    df = scraper.save_to_csv('data/raw/reviews_amazon_raw.csv')
    
    # Mostrar información básica
    if df is not None:
        print("\n" + "="*50)
        print("INFORMACIÓN DEL DATASET")
        print("="*50)
        print(f"Número de reseñas: {len(df)}")
        print(f"Columnas: {', '.join(df.columns)}")
        print("\nPrimeras 3 reseñas:")
        print(df[['usuario', 'puntuacion', 'texto']].head(3))
        print("\nDistribución de puntuaciones:")
        print(df['puntuacion'].value_counts().sort_index())

if __name__ == "__main__":
    main()