# Professional Streamlit Opinion Intelligence Monitor - Analyzer Service

from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from src.config.constants import SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE

from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from src.config.constants import SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE

# New service imports
from src.services.ir_engine import InvertedIndex, VectorSpaceModel
from src.services.authority import UserAuthorityService
from src.services.recommender import CollaborativeFilteringService

class SentimentAnalyzerES:
    """Hybrid Multidimensional Sentiment Analysis System."""
    
    def __init__(self):
        self.translator = Translator()
        self.positive_seed = [
            'excelente', 'perfecto', 'genial', 'maravilloso', 'fantástico',
            'recomiendo', 'satisfecho', 'contento', 'feliz', 'bueno', 'buena',
            'rápido', 'eficiente', 'útil', 'valioso', 'perfectamente', 'cumple',
            'funciona', 'amable', 'atento'
        ]
        self.negative_seed = [
            'pésimo', 'horrible', 'terrible', 'decepcionado', 'decepción',
            'malo', 'mala', 'lento', 'difícil', 'inútil', 'desastre', 'estafa',
            'fraude', 'irresponsable', 'negligente', 'incompetente', 'insatisfecho',
            'molesto', 'error', 'defectuoso'
        ]
        
        # Services
        self.authority_service = UserAuthorityService()
        self.cf_service = CollaborativeFilteringService()
        self.ir_model = None

    def analyze_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processes reviews using the hybrid pipeline."""
        if df.empty: return df

        # 1. Build IR Engine
        idx = InvertedIndex()
        for i, row in df.iterrows():
            idx.add_document(i, row['tokens'])
        
        self.ir_model = VectorSpaceModel(idx)
        pos_query_vec = self.ir_model.vectorize(self.positive_seed)
        neg_query_vec = self.ir_model.vectorize(self.negative_seed)

        # 2. Base Sentiment (TF-IDF + Cosine Similarity)
        df['base_score'] = df['tokens'].apply(
            lambda x: self.ir_model.analyze_sentiment(self.ir_model.vectorize(x), pos_query_vec, neg_query_vec)
        )

        # 3. User Authority (PageRank)
        interactions = self._generate_simulated_interactions(df)
        self.authority_service.calculate_authority(interactions)
        df['user_authority'] = df['user_id'].apply(self.authority_service.get_user_weight)

        # 4. Collaborative Filtering (Pearson)
        # Re-balanced temp_score: 50% explicit rating, 50% base semantic score
        # Rating normalized to [-1, 1]: (rating - 3) / 2
        df['rating_score'] = (df['rating'] - 3) / 2
        df['temp_score'] = (df['base_score'] * 0.5) + (df['rating_score'] * 0.5)
        
        self.cf_service.fit(df.rename(columns={'temp_score': 'sentimiento_score'}))
        
        # 5. Hybrid Calculation
        final_results = []
        for _, row in df.iterrows():
            # CF prediction for personalization
            cf_pred = self.cf_service.predict_user_item(row['user_id'], row['product_id'])
            
            # Normalize authority to influence the semantic part
            auth_norm = row['user_authority'] / df['user_authority'].mean() if not df.empty else 1.0
            
            # Hybrid Formula v2.1:
            # 50% normalized rating + 30% semantic text (weighted by auth) + 20% CF personalization
            final_score = (row['rating_score'] * 0.50) + (row['base_score'] * auth_norm * 0.30) + (cf_pred * 0.20)
            
            # Constraints
            final_score = max(-1.0, min(1.0, final_score))
            
            # Adjusted Thresholds for Trustpilot ecosystem (more sensitive)
            if final_score >= 0.05:
                label = 'positivo'
            elif final_score <= -0.05:
                label = 'negativo'
            else:
                label = 'neutral'
                
            confidence = abs(final_score)
            
            final_results.append({
                'sentimiento_score': final_score,
                'sentimiento': label,
                'confianza': confidence,
                'authority_level': auth_norm
            })

        res_df = pd.DataFrame(final_results)
        df = pd.concat([df.reset_index(drop=True), res_df], axis=1)
        
        # Category classification (Existing logic)
        df['categoria_predom'] = df['tokens'].apply(self._get_dominant_category)
        
        return df

    def _generate_simulated_interactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simulates a user network based on same-item reviews to enable PageRank."""
        interactions = []
        # Users reviewing the same product create "influence" links (simplified)
        for prod in df['product_id'].unique():
            users = df[df['product_id'] == prod]['user_id'].unique()
            for i in range(len(users)):
                for j in range(i + 1, len(users)):
                    interactions.append({'source_user': users[i], 'target_user': users[j]})
        
        if not interactions:
            return pd.DataFrame(columns=['source_user', 'target_user'])
        return pd.DataFrame(interactions)

    def _get_dominant_category(self, tokens: List[str]) -> str:
        categorias_palabras = {
            'cliente': 'Servicio al Cliente', 'atención': 'Servicio al Cliente', 'servicio': 'Servicio al Cliente',
            'soporte': 'Servicio al Cliente', 'ayuda': 'Servicio al Cliente', 'amabilidad': 'Servicio al Cliente',
            'entrega': 'Logística y Envío', 'pedido': 'Logística y Envío', 'envío': 'Logística y Envío',
            'transporte': 'Logística y Envío', 'retraso': 'Logística y Envío', 'paquete': 'Logística y Envío',
            'problema': 'Incidencias', 'error': 'Incidencias', 'fallo': 'Incidencias', 'roto': 'Incidencias',
            'estafa': 'Seguridad y Fraude', 'fraude': 'Seguridad y Fraude', 'engaño': 'Seguridad y Fraude',
            'precio': 'Económico', 'dinero': 'Económico', 'coste': 'Económico', 'barato': 'Económico',
            'calidad': 'Producto', 'material': 'Producto', 'funciona': 'Producto', 'útil': 'Producto',
            'devolución': 'Postventa', 'reembolso': 'Postventa', 'garantía': 'Postventa'
        }
        cats = [categorias_palabras.get(w) for w in tokens if w in categorias_palabras]
        if not cats: return "Opinión General"
        return max(set(cats), key=cats.count)
