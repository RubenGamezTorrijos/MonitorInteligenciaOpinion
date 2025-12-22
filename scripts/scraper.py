# FASE 1: Web Scraping
# Desarrollado por: Rubén (Organizador)
# Apoyo en funciones auxiliares: Juanes (Colaborador)

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
                # Petición HTTP con delay aleatorio (Implementado por Juanes para ser ético)
                time.sleep(random.uniform(2, 4))
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                # Parsear HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Encontrar todos los contenedores de reseñas (Juanes: Investigar estructura HTML)
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
        """Extrae los datos individuales de una reseña (Rubén)"""
        try:
            # Extraer texto del comentario (texto_comentario)
            # Usar selectores precisos identificados por auditoría
            text_el = review_element.select_one('[data-service-review-text-typography="true"]')
            if text_el:
                texto_comentario = text_el.get_text(strip=True).replace("Ver más", "").strip()
            else:
                # Fallback a selectores anteriores o genéricos
                text_div = review_element.find('p', class_=lambda x: x and 'reviewText' in x)
                texto_comentario = text_div.get_text(strip=True) if text_div else "Texto no disponible"
            
            # Extraer puntuación
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
            
            # Extraer usuario y metadatos del usuario (Persona B: Estudio de usuarios)
            user_el = review_element.select_one('[data-consumer-name-typography="true"]')
            usuario = user_el.get_text(strip=True) if user_el else "Anónimo"
            
            location_el = review_element.select_one('[data-consumer-country-typography="true"]')
            ubicacion = location_el.get_text(strip=True) if location_el else "Desconocida"
            
            count_el = review_element.select_one('[data-consumer-reviews-count-typography="true"]')
            total_resenas_usuario = count_el.get_text(strip=True) if count_el else "0"
            
            # Extraer título de la reseña
            title_el = review_element.select_one('[data-review-title-typography="true"]')
            if not title_el:
                 title_el = review_element.find(['h2', 'a'], class_=lambda x: x and ('title' in x or 'heading' in x))
            
            titulo = title_el.get_text(strip=True) if title_el else "Sin título"
            
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
            print(f"Error al extraer datos de reseña: {str(e)}")
            return None
    
    def save_to_csv(self, filename='data/raw/dataset_raw.csv'):
        """Guarda los datos en un archivo CSV (Rubén)"""
        if not self.reviews_data:
            print("No hay datos para guardar")
            return
        
        df = pd.DataFrame(self.reviews_data)
        
        # Eliminar duplicados (Persona B: Limpieza de datos)
        # Un duplicado real tiene mismo usuario, mismo texto y misma fecha
        df = df.drop_duplicates(subset=['usuario', 'texto_comentario', 'fecha'])
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Datos guardados en {filename}. Filas únicas: {len(df)}")
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