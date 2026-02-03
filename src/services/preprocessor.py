# Professional Streamlit Opinion Intelligence Monitor - Preprocessor Service

import spacy
import nltk
from nltk.corpus import stopwords
import re
import unicodedata
from typing import List, Optional, Dict
import pandas as pd

class SpanishTextPreprocessor:
    """Service specialized for NLP preprocessing of Spanish e-commerce reviews."""
    
    def __init__(self):
        # NLTK Stopwords
        try:
            self.stop_words = set(stopwords.words('spanish'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('spanish'))
            
        # Add comprehensive industries/domain specific Stopwords from notebook
        extra_stopwords = {
            'amazon', 'amazones', 'temu', 'elcorteingles', 'pccomponentes',
            'producto', 'productos', 'servicio', 'servicios', 'envío', 'envios',
            'pedido', 'pedidos', 'cliente', 'clientes', 'comprar', 'compra',
            'calidad', 'precio', 'tiempo', 'entrega', 'entregas', 'empresa',
            'atención', 'recomiendo', 'recomendación', 'recomendaciones',
            'problema', 'problemas', 'cosa', 'cosas', 'vez', 'veces', 'año',
            'años', 'día', 'días', 'semana', 'semanas', 'mes', 'meses',
            'hora', 'horas', 'minuto', 'minutos', 'momento',
            'también', 'además', 'incluso', 'aunque', 'porque', 'pues',
            'entonces', 'ahora', 'luego', 'después', 'antes', 'siempre',
            'nunca', 'jamás', 'solo', 'solamente', 'quizás', 'tal', 'vez',
            'hacer', 'hace', 'hice', 'hicieron', 'hecho', 'decir', 'dice',
            'dijo', 'dijeron', 'poder', 'puede', 'puedo', 'podemos', 'poner',
            'pone', 'puesto', 'ver', 'veo', 'visto', 'dar', 'da', 'dado',
            'saber', 'sé', 'sabe', 'supuesto', 'querer', 'quiere', 'quería',
            'tenía', 'tenían', 'teniendo', 'tengo', 'tienes', 'tiene', 'tenemos',
            'había', 'habían', 'habiendo', 'hay', 'hubo', 'estaba', 'estaban',
            'ser', 'sido', 'siendo', 'soy', 'eres', 'es', 'somos', 'son',
            'fue', 'fueron', 'era', 'eran', 'ir', 'voy', 'va', 'vamos', 'van',
            'fui', 'fuimos', 'iba', 'iban'
        }
        self.stop_words.update(extra_stopwords)

    def clean_text(self, text: str) -> str:
        """Limpieza completa del texto manteniendo significado en español."""
        if not isinstance(text, str) or not text.strip():
            return ""
        
        text = text.lower()
        # Remove URLs/mentions
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)
        # Preserve only Spanish letters, spaces, ñ, and accents
        text = re.sub(r'[^a-záéíóúüñ\s]', ' ', text)
        # Remove extra spaces
        text = ' '.join(text.split())
        return text

    def remove_stopwords(self, text: str, domain: Optional[str] = None) -> str:
        """Removes stopwords, short words, and optionally domain-specific noise."""
        if not text: return ""
        tokens = text.split()
        
        current_stops = self.stop_words.copy()
        if domain:
            # Aggressive domain filtering (e.g., 'amazon.es' -> 'amazon', 'es', 'amazones')
            # 1. Split domain parts
            parts = re.split(r'[.-]', domain.lower())
            current_stops.update(parts)
            
            # 2. Add full clean name
            main_name = parts[0]
            current_stops.add(main_name)
            
            # 3. Add variations (plurals, common misspellings if needed)
            current_stops.add(main_name + 'es') # e.g., amazones
            current_stops.add(main_name + 's')  # e.g., amazons
            
        filtered = [w for w in tokens if w not in current_stops and len(w) > 2]
        return ' '.join(filtered)

    def process_pipeline(self, text: str, domain: Optional[str] = None) -> Dict:
        """Executes full NLP pipeline with optional domain filtering."""
        cleaned = self.clean_text(text)
        no_stopwords = self.remove_stopwords(cleaned, domain=domain)
        tokens = no_stopwords.split()
        
        return {
            'original': text,
            'texto_limpio': cleaned,
            'texto_sin_stopwords': no_stopwords,
            'tokens': tokens,
            'palabras_original': len(str(text).split()),
            'palabras_limpias': len(tokens)
        }
