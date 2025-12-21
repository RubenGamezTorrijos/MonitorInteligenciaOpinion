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
        """
        Inicializa el preprocesador de texto
        
        Args:
            language: Idioma para stopwords y stemming ('spanish' o 'english')
        """
        self.language = language
        
        # Descargar recursos de NLTK (si no están disponibles)
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Descargando recursos de NLTK...")
            nltk.download('punkt')
            nltk.download('stopwords')
        
        # Configurar stopwords
        if language == 'spanish':
            self.stop_words = set(stopwords.words('spanish'))
            self.stemmer = SnowballStemmer('spanish')
        else:
            self.stop_words = set(stopwords.words('english'))
            self.stemmer = SnowballStemmer('english')
        
        # Añadir stopwords personalizadas
        self.custom_stopwords = {
            'si', 'sí', 'no', 'ya', 'ver', 'vez', 'tan', 'así', 'solo',
            'sólo', 'aún', 'incluso', 'siempre', 'hace', 'hacer', 'puede',
            'cada', 'mas', 'más', 'menos', 'mucho', 'poco', 'gran'
        }
        self.stop_words.update(self.custom_stopwords)
        
    def clean_text(self, text: str) -> str:
        """
        Limpieza básica del texto
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not isinstance(text, str):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar acentos
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        
        # Eliminar URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Eliminar menciones (@) y hashtags (#)
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Eliminar números
        text = re.sub(r'\d+', '', text)
        
        # Eliminar caracteres especiales y puntuación
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokeniza el texto en palabras individuales
        
        Args:
            text: Texto a tokenizar
            
        Returns:
            Lista de tokens
        """
        return word_tokenize(text, language=self.language)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Elimina stopwords de una lista de tokens
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de tokens sin stopwords
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def apply_stemming(self, tokens: List[str]) -> List[str]:
        """
        Aplica stemming a una lista de tokens
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de tokens con stemming aplicado
        """
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess_pipeline(self, text: str, stem: bool = True) -> Dict[str, Any]:
        """
        Pipeline completo de preprocesamiento
        
        Args:
            text: Texto a procesar
            stem: Si aplicar stemming o no
            
        Returns:
            Diccionario con diferentes versiones del texto procesado
        """
        # Paso 1: Limpieza básica
        cleaned_text = self.clean_text(text)
        
        # Paso 2: Tokenización
        tokens = self.tokenize_text(cleaned_text)
        
        # Paso 3: Eliminar stopwords
        tokens_no_stopwords = self.remove_stopwords(tokens)
        
        # Paso 4: Aplicar stemming (opcional)
        if stem and tokens_no_stopwords:
            tokens_stemmed = self.apply_stemming(tokens_no_stopwords)
            text_stemmed = ' '.join(tokens_stemmed)
        else:
            tokens_stemmed = tokens_no_stopwords
            text_stemmed = ' '.join(tokens_no_stopwords)
        
        # Texto sin stopwords pero sin stemming
        text_no_stopwords = ' '.join(tokens_no_stopwords)
        
        # Texto tokenizado original (para análisis)
        text_tokenized = ' '.join(tokens)
        
        return {
            'texto_original': text,
            'texto_limpio': cleaned_text,
            'texto_tokenizado': text_tokenized,
            'texto_sin_stopwords': text_no_stopwords,
            'texto_stemmed': text_stemmed,
            'tokens': tokens,
            'tokens_sin_stopwords': tokens_no_stopwords,
            'tokens_stemmed': tokens_stemmed,
            'num_palabras_original': len(tokens),
            'num_palabras_sin_stopwords': len(tokens_no_stopwords)
        }
    
    def process_dataframe(self, df: pd.DataFrame, text_column: str = 'texto') -> pd.DataFrame:
        """
        Procesa todas las filas de un DataFrame
        
        Args:
            df: DataFrame con textos a procesar
            text_column: Nombre de la columna con el texto
            
        Returns:
            DataFrame con columnas adicionales de texto procesado
        """
        print(f"Procesando {len(df)} textos...")
        
        # Aplicar pipeline a cada texto
        processed_data = []
        for idx, row in df.iterrows():
            if idx % 10 == 0:
                print(f"  Procesados {idx}/{len(df)} textos...")
            
            text = row[text_column]
            result = self.preprocess_pipeline(text)
            result['id'] = idx
            processed_data.append(result)
        
        # Crear DataFrame de resultados
        processed_df = pd.DataFrame(processed_data)
        
        # Combinar con datos originales
        original_df = df.reset_index(drop=True)
        final_df = pd.concat([original_df, processed_df], axis=1)
        
        print(f"Preprocesamiento completado. Columnas añadidas: {len(processed_df.columns)}")
        
        return final_df
    
    def calculate_text_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula métricas adicionales para cada texto
        
        Args:
            df: DataFrame con textos procesados
            
        Returns:
            DataFrame con métricas adicionales
        """
        print("Calculando métricas de texto...")
        
        # Métricas básicas
        df['longitud_texto_original'] = df['texto_original'].apply(lambda x: len(str(x)))
        df['longitud_texto_limpio'] = df['texto_limpio'].apply(len)
        df['num_palabras_original'] = df['texto_original'].apply(lambda x: len(str(x).split()))
        df['num_palabras_limpio'] = df['texto_limpio'].apply(lambda x: len(x.split()))
        
        # Densidad léxica (palabras únicas / total palabras)
        def lexical_density(text):
            words = text.split()
            if not words:
                return 0
            unique_words = set(words)
            return len(unique_words) / len(words)
        
        df['densidad_lexica'] = df['texto_sin_stopwords'].apply(lexical_density)
        
        # Longitud promedio de palabras
        def avg_word_length(text):
            words = text.split()
            if not words:
                return 0
            return sum(len(word) for word in words) / len(words)
        
        df['longitud_promedio_palabra'] = df['texto_sin_stopwords'].apply(avg_word_length)
        
        print(f"Métricas calculadas para {len(df)} textos")
        
        return df

def main():
    """Función principal para probar el preprocesador"""
    # Cargar datos de ejemplo
    print("Cargando datos...")
    input_path = 'data/raw/reviews_amazon_raw.csv'
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        # Intentar con ruta relativa si se ejecuta desde scripts/
        df = pd.read_csv('../' + input_path)

    
    # Mostrar información inicial
    print(f"Dataset cargado: {len(df)} reseñas")
    print(f"Columnas: {list(df.columns)}")
    
    # Inicializar preprocesador
    preprocessor = TextPreprocessor(language='spanish')
    
    # Procesar textos
    df_processed = preprocessor.process_dataframe(df, text_column='texto')
    
    # Calcular métricas
    df_processed = preprocessor.calculate_text_metrics(df_processed)
    
    # Guardar dataset procesado
    output_path = 'data/processed/reviews_preprocessed.csv'
    try:
        df_processed.to_csv(output_path, index=False, encoding='utf-8')
    except OSError:
        # Intentar con ruta relativa
        output_path = '../' + output_path
        df_processed.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\nDataset guardado en: {output_path}")
    print(f"Número total de columnas: {len(df_processed.columns)}")
    
    # Mostrar información de las nuevas columnas
    new_columns = [col for col in df_processed.columns if col not in df.columns]
    print(f"Columnas añadidas: {new_columns}")
    
    # Mostrar ejemplo de procesamiento
    print("\nEJEMPLO DE PROCESAMIENTO:")
    sample_idx = 0
    print(f"\nTexto original (reseña {sample_idx}):")
    print(df_processed.loc[sample_idx, 'texto_original'][:200] + "...")
    print(f"\nTexto limpio:")
    print(df_processed.loc[sample_idx, 'texto_limpio'][:200] + "...")
    print(f"\nTexto sin stopwords:")
    print(df_processed.loc[sample_idx, 'texto_sin_stopwords'][:200] + "...")
    print(f"\nNúmero de palabras original: {df_processed.loc[sample_idx, 'num_palabras_original']}")
    print(f"Número de palabras sin stopwords: {df_processed.loc[sample_idx, 'num_palabras_sin_stopwords']}")
    
    return df_processed

if __name__ == "__main__":
    df_processed = main()