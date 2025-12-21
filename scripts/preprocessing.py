# FASE 2: Preprocesamiento y Limpieza (NLP)
# Pipeline de limpieza: Desarrollado por Persona A
# Stopwords y estadísticas: Desarrollado por Persona B

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
        
        # Persona B: Investigación de stopwords en español
        if language == 'spanish':
            self.stop_words = set(stopwords.words('spanish'))
            self.stemmer = SnowballStemmer('spanish')
        else:
            self.stop_words = set(stopwords.words('english'))
            self.stemmer = SnowballStemmer('english')
        
        self.custom_stopwords = {
            'amazon', 'producto', 'si', 'sí', 'no', 'ya', 'ver', 'vez', 'tan', 'así', 'solo',
            'sólo', 'aún', 'incluso', 'siempre', 'hace', 'hacer', 'puede',
            'cada', 'mas', 'más', 'menos', 'mucho', 'poco', 'gran'
        }
        self.stop_words.update(self.custom_stopwords)
        
    def clean_text(self, text: str) -> str:
        """Limpieza básica (Persona A)"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower() # minúsculas
        # Eliminar acentos
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        # Eliminar URLs, menciones y hashtags (Persona A)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+|#\w+', '', text)
        # Eliminar símbolos y puntuación
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        return word_tokenize(text, language=self.language)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words]
    
    def apply_stemming(self, tokens: List[str]) -> List[str]:
        """Stemming (Persona B)"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess_pipeline(self, text: str) -> Dict[str, Any]:
        """Integración de pipeline (Desarrollado por Persona A)"""
        # 1. Limpieza (Persona A)
        cleaned_text = self.clean_text(text)
        
        # 2. Tokenización (Persona A)
        tokens = self.tokenize_text(cleaned_text)
        
        # 3. Eliminación de stopwords (Persona B)
        tokens_no_stop = self.remove_stopwords(tokens)
        
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
        """Métricas adicionales implementadas por Persona B"""
        print("Calculando estadísticas avanzadas (Persona B)...")
        df['longitud_comentario'] = df['texto_comentario'].str.len()
        df['conteo_palabras_unicas'] = df['texto_limpio'].apply(lambda x: len(set(str(x).split())))
        return df

def main():
    print("Cargando dataset_raw.csv...")
    input_path = 'data/raw/dataset_raw.csv'
    try:
        df = pd.read_csv(input_path)
    except:
        df = pd.read_csv('../' + input_path)

    preprocessor = TextPreprocessor(language='spanish')
    
    # Procesar (Persona A)
    print("Aplicando preprocesamiento...")
    results = df['texto_comentario'].apply(preprocessor.preprocess_pipeline)
    df_results = pd.DataFrame(list(results))
    
    df_final = pd.concat([df, df_results], axis=1)
    
    # Métricas (Persona B)
    df_final = preprocessor.calculate_persona_b_metrics(df_final)
    
    output_path = 'data/processed/dataset_clean.csv'
    try:
        df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
    except:
        output_path = '../' + output_path
        df_final.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"Fase 2 completada exitosamente. Archivo: {output_path}")

if __name__ == "__main__":
    main()