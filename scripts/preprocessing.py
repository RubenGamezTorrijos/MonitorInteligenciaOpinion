# FASE 2: Preprocesamiento y Limpieza (NLP)
# Pipeline de limpieza: Desarrollado por Rubén
# Stopwords y estadísticas: Desarrollado por Juanes

import pandas as pd
import re
import string
from typing import List, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import unicodedata

class TextPreprocessor:
    def __init__(self, language='spanish'):
        self.language = language
        
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Descargando recursos de NLTK...")
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('punkt_tab')
        
        # Juanes: Investigación de stopwords en español
        
                
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        return word_tokenize(text, language=self.language)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words]
    
    def apply_stemming(self, tokens: List[str]) -> List[str]:
        """Stemming (Desarrollado por Juanes)"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess_pipeline(self, text: str) -> Dict[str, Any]:
        """Integración de pipeline (Desarrollado por Rubén)"""
        # 1. Limpieza (Rubén)
        cleaned_text = self.clean_text(text)
        
        # 2. Tokenización (Rubén)
        tokens = self.tokenize_text(cleaned_text)
        
        # 3. Eliminación de stopwords (Juanes)
                
        # 4. Resultado final
        text_clean = ' '.join(tokens_no_stop)
        
        return {
            'texto_limpio': text_clean,
            'texto_original': text, # Original uncleaned text
            'texto_sin_stopwords': text_clean,
            'texto_comentario_limpio': cleaned_text,
            'texto_comentario_sin_stopwords': text_clean,
            'tokens': tokens,
            'tokens_sin_stopwords': tokens_no_stop,
            'num_palabras': len(tokens),
            'num_palabras_limpias': len(tokens_no_stop)
        }

    def calculate_persona_b_metrics(self, df: pd.DataFrame):
        """Métricas adicionales implementadas por Juanes"""
        print("Calculando estadísticas avanzadas (Juanes)...")
        # Asegurar que las columnas existen
        df['longitud_comentario'] = df['texto_comentario'].fillna('').str.len()
        df['conteo_palabras_unicas'] = df['texto_limpio'].apply(lambda x: len(set(str(x).split())))
        
        # Procesar 'total_resenas_usuario' para convertirlo a número si es posible
        def clean_resenas_count(val):
            if pd.isna(val): return 0
            match = re.search(r'(\d+)', str(val))
            return int(match.group(1)) if match else 0
        
        if 'total_resenas_usuario' in df.columns:
            df['num_resenas_usuario_total'] = df['total_resenas_usuario'].apply(clean_resenas_count)
            
        return df

def main():
    print("Cargando dataset_raw.csv...")
    input_path = 'data/raw/dataset_raw.csv'
    try:
        df = pd.read_csv(input_path)
    except:
        df = pd.read_csv('../' + input_path)

    # Eliminar duplicados si no se hizo en scraping
    df = df.drop_duplicates(subset=['usuario', 'texto_comentario', 'fecha'])

    # Persona B: Estrategia de transformación (Combinar título y texto)
    # Si el título no es "Sin título", lo concatenamos al texto para capturar su sentimiento/temas
    print("Transformando datos (Combinación Título + Texto)...")
    def combine_title_text(row):
        title = str(row['titulo']) if pd.notna(row['titulo']) else ""
        text = str(row['texto_comentario']) if pd.notna(row['texto_comentario']) else ""
        
        if title.lower() == "sin titulo" or title.lower() == "nan":
            return text
        
        if text.lower() == "texto no disponible":
            return title
            
        return f"{title}. {text}"

    df['texto_para_analisis'] = df.apply(combine_title_text, axis=1)

    preprocessor = TextPreprocessor(language='spanish')
    
    # Procesar sobre la nueva columna combinada (Rubén)
    print("Aplicando preprocesamiento NLP...")
    results = df['texto_para_analisis'].apply(preprocessor.preprocess_pipeline)
    df_results = pd.DataFrame(list(results))
    
    # Unir resultados
    df_final = pd.concat([df.reset_index(drop=True), df_results.reset_index(drop=True)], axis=1)
    
    # Métricas avanzadas (Juanes)
    

if __name__ == "__main__":
    main()
