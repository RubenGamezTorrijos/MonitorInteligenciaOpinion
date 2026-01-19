import pandas as pd
import re
import string
from typing import List, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import unicodedata
import os


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

        # Cache stopwords
        try:
            stopwords_nltk = set(stopwords.words(self.language))
        except:
            nltk.download('stopwords')
            stopwords_nltk = set(stopwords.words(self.language))

        def normalize_word(word):
            return ''.join(
                c for c in unicodedata.normalize('NFD', word)
                if unicodedata.category(c) != 'Mn'
            ).lower()

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
        self.stemmer = SnowballStemmer(self.language)

    def clean_text(self, text: str) -> str:
        if pd.isna(text) or text == "Texto no disponible":
            return ""
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
        if not text: return []
        return word_tokenize(text, language=self.language)

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]

    def apply_stemming(self, tokens: List[str]) -> List[str]:
        return [self.stemmer.stem(token) for token in tokens]

    def preprocess_pipeline(self, text: str) -> Dict[str, Any]:
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize_text(cleaned_text)
        tokens_no_stop = self.remove_stopwords(tokens)
        text_clean = ' '.join(tokens_no_stop)

        return {
            'texto_limpio': text_clean,
            'texto_original': text,
            'tokens': tokens_no_stop,
            'num_palabras': len(tokens),
            'num_palabras_limpias': len(tokens_no_stop)
        }

    def calculate_metrics(self, df: pd.DataFrame):
        print("Calculando estadísticas avanzadas...")
        df['longitud_comentario'] = df['texto_comentario'].fillna('').str.len()
        df['conteo_palabras_unicas'] = df['texto_limpio'].apply(
            lambda x: len(set(str(x).split())) if pd.notna(x) else 0
        )

        def clean_resenas_count(val):
            if pd.isna(val): return 0
            match = re.search(r'(\d+)', str(val))
            return int(match.group(1)) if match else 0

        if 'total_resenas_usuario' in df.columns:
            df['num_resenas_usuario_total'] = df['total_resenas_usuario'].apply(clean_resenas_count)

        return df


def main():
    # Caminos relativos seguros
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'raw', 'dataset_raw.csv')
    output_path = os.path.join(base_dir, 'data', 'processed', 'dataset_clean.csv')

    print(f"Cargando dataset desde: {input_path}")
    if not os.path.exists(input_path):
        print(f"❌ Error: No se encuentra el archivo {input_path}")
        return

    df = pd.read_csv(input_path)
    df = df.drop_duplicates(subset=['usuario', 'texto_comentario', 'fecha'])

    print("Transformando datos...")
    def combine_title_text(row):
        title = str(row['titulo']) if pd.notna(row['titulo']) and str(row['titulo']).lower() != "sin título" else ""
        text = str(row['texto_comentario']) if pd.notna(row['texto_comentario']) and str(row['texto_comentario']) != "Texto no disponible" else ""
        return f"{title}. {text}".strip('. ')

    df['texto_para_analisis'] = df.apply(combine_title_text, axis=1)

    preprocessor = TextPreprocessor(language='spanish')
    print("Aplicando preprocesamiento NLP...")
    
    results = df['texto_para_analisis'].apply(preprocessor.preprocess_pipeline)
    df_results = pd.DataFrame(list(results))

    df_final = pd.concat([df.reset_index(drop=True), df_results.reset_index(drop=True)], axis=1)
    df_final = preprocessor.calculate_metrics(df_final)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ Dataset procesado guardado en: {output_path}")


if __name__ == "__main__":
    main()

