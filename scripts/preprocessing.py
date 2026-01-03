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

        # Investigación de stopwords en español (Juanes)
    
        stopwords_nltk = set(stopwords.words(self.language))

        def normalize_word(word):
            return ''.join(
                c for c in unicodedata.normalize('NFD', word)
                if unicodedata.category(c) != 'Mn'
            )

        stopwords_normalizadas = {normalize_word(w) for w in stopwords_nltk}

        stopwords_amazon = {
            "producto", "productos", "comprar", "compra", "amazon",
            "envio", "envíos", "pedido", "pedidos",
            "precio", "calidad", "marca",
            "llego", "llegó", "llegar",
            "dia", "días", "mes", "año",
            "muy", "mas", "menos", "todo", "toda"
        }

        self.stop_words = stopwords_normalizadas.union(stopwords_amazon)

        # Stemmer español
        self.stemmer = SnowballStemmer(self.language)

    def clean_text(self, text: str) -> str:
        text = str(text).lower()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(
            c for c in text if unicodedata.category(c) != 'Mn'
        )
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize_text(self, text: str) -> List[str]:
        return word_tokenize(text, language=self.language)

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words]

    def apply_stemming(self, tokens: List[str]) -> List[str]:
        """Stemming (Desarrollado por Juanes)"""
        return [self.stemmer.stem(token) for token in tokens]

    def preprocess_pipeline(self, text: str) -> Dict[str, Any]:
        """Integración de pipeline (Rubén + Juanes)"""

        # 1. Limpieza (Rubén)
        cleaned_text = self.clean_text(text)

        # 2. Tokenización (Rubén)
        tokens = self.tokenize_text(cleaned_text)

        # 3. Eliminación de stopwords (Juanes)
        tokens_no_stop = self.remove_stopwords(tokens)

        # 4. Resultado final
        text_clean = ' '.join(tokens_no_stop)

        return {
            'texto_limpio': text_clean,
            'texto_original': text,
            'texto_comentario_limpio': cleaned_text,
            'tokens': tokens,
            'tokens_sin_stopwords': tokens_no_stop,
            'num_palabras': len(tokens),
            'num_palabras_limpias': len(tokens_no_stop)
        }

    def calculate_persona_b_metrics(self, df: pd.DataFrame):
        """Métricas adicionales implementadas por Juanes"""
        print("Calculando estadísticas avanzadas (Juanes)...")

        df['longitud_comentario'] = df['texto_comentario'].fillna('').str.len()

        df['conteo_palabras_unicas'] = df['texto_limpio'].apply(
            lambda x: len(set(str(x).split()))
        )

        def clean_resenas_count(val):
            if pd.isna(val):
                return 0
            match = re.search(r'(\d+)', str(val))
            return int(match.group(1)) if match else 0

        if 'total_resenas_usuario' in df.columns:
            df['num_resenas_usuario_total'] = df['total_resenas_usuario'].apply(
                clean_resenas_count
            )

        return df


def main():
    print("Cargando dataset_raw.csv...")
    input_path = 'data/raw/dataset_raw.csv'

    try:
        df = pd.read_csv(input_path)
    except:
        df = pd.read_csv('../' + input_path)

    # Eliminar duplicados si no se hizo en scrapling
    df = df.drop_duplicates(subset=['usuario', 'texto_comentario', 'fecha'])

    #Persona B: Estrategia de transformación (Combinar título y texto)
    # Si el título no es "Sin título", lo concatenamos al texto para capturar su sentimiento/temas
    print("Transformando datos (Combinación Título + Texto)...")

    def combine_title_text(row):
        title = str(row['titulo']) if pd.notna(row['titulo']) else ""
        text = str(row['texto_comentario']) if pd.notna(row['texto_comentario']) else ""

        if title.lower() in ["sin titulo", "nan"]:
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
    df_final = pd.concat(
        [df.reset_index(drop=True), df_results.reset_index(drop=True)],
        axis=1
    )

    # Métricas avanzadas (Juanes)
    df_final = preprocessor.calculate_persona_b_metrics(df_final)

    # Guardar dataset procesado
    output_path = 'data/processed/dataset_procesado_final.csv'
    try:
        df_final.to_csv(output_path, index=False)
    except:
        df_final.to_csv('../' + output_path, index=False)

    print("Dataset procesado guardado correctamente.")


if __name__ == "__main__":
    main()

