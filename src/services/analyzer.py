# Professional Streamlit Opinion Intelligence Monitor - Analyzer Service

from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from src.config.constants import SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE

class SentimentAnalyzerES:
    """Service specialized for sentiment analysis and categorization of Spanish reviews."""
    
    def __init__(self):
        self.translator = Translator()
        self.positive_words_es = {
            'excelente', 'perfecto', 'genial', 'maravilloso', 'fantástico',
            'recomiendo', 'satisfecho', 'contento', 'feliz', 'agradecido',
            'rápido', 'eficiente', 'útil', 'valioso', 'agradable', 'fácil',
            'bueno', 'buena', 'correcto', 'adecuado', 'perfectamente',
            'cumple', 'funciona', 'resolvió', 'solucionó', 'ayudó',
            'profesional', 'amable', 'atento', 'respetuoso', 'educado'
        }

        self.negative_words_es = {
            'pésimo', 'horrible', 'terrible', 'decepcionado', 'decepción',
            'problema', 'error', 'defectuoso', 'malo', 'mala', 'lento',
            'difícil', 'complicado', 'frustrante', 'inútil', 'pobre',
            'desastre', 'estafa', 'fraude', 'estafadores', 'mentira',
            'engañado', 'timado', 'abusivo', 'abusadores', 'desleal',
            'irresponsable', 'negligente', 'incompetente', 'ineficiente',
            'desorganizado', 'caótico', 'catastrófico',
            'insatisfecho', 'enfadado', 'molesto', 'indignado', 'furia'
        }

        # Category mapping from notebook
        self.categorias_palabras = {
            'cliente': 'Servicio', 'atención': 'Servicio', 'servicio': 'Servicio',
            'contacto': 'Comunicación', 'respuesta': 'Comunicación', 'llamada': 'Comunicación',
            'entrega': 'Logística', 'pedido': 'Logística', 'envío': 'Logística',
            'repartidor': 'Logística', 'transporte': 'Logística', 'locker': 'Logística',
            'problema': 'Queja', 'decepción': 'Queja', 'error': 'Queja', 'fallo': 'Queja',
            'estafa': 'Fraude', 'fraude': 'Fraude', 'estafadores': 'Fraude',
            'devolución': 'Postventa', 'reembolso': 'Postventa', 'garantía': 'Postventa',
            'tiempo': 'Tiempo', 'espera': 'Tiempo', 'retraso': 'Tiempo', 'urgente': 'Tiempo'
        }

    def analyze_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processes a full DataFrame and adds sentiment/category columns."""
        results = df['texto_sin_stopwords'].apply(lambda x: self._get_combined_sentiment(x))
        sentiment_df = pd.DataFrame(results.tolist())
        
        # Add labels to categories
        df = pd.concat([df, sentiment_df], axis=1)
        df['categoria_predom'] = df['tokens'].apply(self._get_dominant_category)
        return df

    def _get_dominant_category(self, tokens: List[str]) -> str:
        """Identifies the most frequent category in a review."""
        cats = [self.categorias_palabras.get(w) for w in tokens if w in self.categorias_palabras]
        if not cats: return "Otros"
        return max(set(cats), key=cats.count)

    def _get_combined_sentiment(self, text: str) -> Dict:
        """Hybrid sentiment logic from notebook."""
        if not text or len(str(text).strip()) < 5:
            return {'sentimiento_score': 0, 'sentimiento': 'neutral', 'confianza': 0}

        # 1. TextBlob Approach (via Translation)
        try:
            translated = self.translator.translate(text, src='es', dest='en')
            blob = TextBlob(translated.text)
            score = blob.sentiment.polarity
            confidence = abs(score)
            
            if confidence > 0.4: # Threshold from notebook logic
                label = 'positivo' if score > 0.2 else ('negativo' if score < -0.2 else 'neutral')
                return {'sentimiento_score': score, 'sentimiento': label, 'confianza': confidence}
        except:
            pass

        # 2. Dictionary Approach (Fallback)
        words = str(text).lower().split()
        pos_count = sum(1 for w in words if w in self.positive_words_es)
        neg_count = sum(1 for w in words if w in self.negative_words_es)
        
        total = pos_count + neg_count
        if total == 0:
            return {'sentimiento_score': 0, 'sentimiento': 'neutral', 'confianza': 0}
            
        dict_score = (pos_count - neg_count) / total
        label = 'positivo' if dict_score > 0.3 else ('negativo' if dict_score < -0.3 else 'neutral')
        
        return {
            'sentimiento_score': dict_score,
            'sentimiento': label,
            'confianza': min(abs(dict_score) * 1.5, 1.0)
        }
