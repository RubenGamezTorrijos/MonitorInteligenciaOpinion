import pandas as pd
from typing import List, Dict

class StrategicAdvisor:
    """
    Generates data-driven strategic recommendations for business improvement.
    Uses sentiment patterns to identify key pain points and suggest actionable steps.
    """
    
    def __init__(self):
        self.recommendation_rules = {
            'Logística y Envío': {
                'action': 'Optimizar proveedores de última milla',
                'detail': 'Se detectan retrasos recurrentes. Evaluar cambio de carrier o implementación de tracking en tiempo real.'
            },
            'Servicio al Cliente': {
                'action': 'Capacitación en resolución de conflictos',
                'detail': 'El tono de las respuestas es un problema. Implementar guiones de empatía y reducir tiempos de espera.'
            },
            'Producto': {
                'action': 'Revisión de control de calidad',
                'detail': 'Fallas funcionales reportadas. Revisar lotes de fabricación y política de garantías.'
            },
            'Seguridad y Fraude': {
                'action': 'Auditoría de seguridad y transparencia',
                'detail': 'Los usuarios perciben riesgos. Publicar sellos de confianza y clarificar cargos.'
            },
            'Económico': {
                'action': 'Revisión de estrategia de precios',
                'detail': 'Percepción de bajo valor/costo. Validar competidores o lanzar ofertas de fidelización.'
            }
        }

    def generate_strategic_report(self, df: pd.DataFrame) -> List[Dict]:
        """Analyzes negative sentiment drivers and returns strategic advice."""
        if df.empty: return []
        
        # Filter negative reviews
        negative_df = df[df['sentimiento'] == 'negativo']
        if negative_df.empty: 
            return [{"area": "General", "action": "Mantenimiento de Excelencia", "detail": "El sentimiento es mayoritariamente positivo. Enfocarse en fidelización."}]

        # Analyze worst categories
        cat_counts = negative_df['categoria_predom'].value_counts()
        total_neg = len(negative_df)
        
        insights = []
        for cat, count in cat_counts.items():
            impact = count / total_neg
            if impact > 0.05: # Lower threshold to 5% for better visibility
                rule = self.recommendation_rules.get(cat, {
                    'action': f'Investigar área de {cat}',
                    'detail': 'Se detectan anomalías no categorizadas.'
                })
                
                # Dynamic context: Find specific themes for this cat
                cat_neg_reviews = negative_df[negative_df['categoria_predom'] == cat]
                cat_tokens = [t for sublist in cat_neg_reviews['tokens'] for t in sublist]
                top_terms = pd.Series(cat_tokens).value_counts().head(3).index.tolist()
                term_str = ", ".join(top_terms)
                
                insights.append({
                    "area": cat,
                    "impact": f"{impact:.1%}",
                    "action": rule['action'],
                    "detail": f"{rule['detail']} (Foco en: `{term_str}`)"
                })
                
        return insights[:3] # Returns top 3 priority actions

    def generate_comparative_advice(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict]:
        """Provides competitive benchmarking insights."""
        if df1.empty or df2.empty: return []
        
        name1 = df1['domain'].iloc[0]
        name2 = df2['domain'].iloc[0]
        
        score1 = df1['sentimiento_score'].mean()
        score2 = df2['sentimiento_score'].mean()
        
        benchmarks = []
        
        # Sentiment Gap
        if abs(score1 - score2) > 0.1:
            leader = name1 if score1 > score2 else name2
            laggard = name2 if score1 > score2 else name1
            benchmarks.append({
                "area": "Posicionamiento Global",
                "action": f"Cierre de brecha con {leader}",
                "detail": f"{laggard} tiene un score de {min(score1, score2):.2f} frente al {max(score1, score2):.2f} de su competencia. Se requiere acción inmediata en fidelización."
            })
            
        # Category Gap
        cat1 = df1['categoria_predom'].value_counts(normalize=True).idxmax()
        cat2 = df2['categoria_predom'].value_counts(normalize=True).idxmax()
        
        if cat1 != cat2:
            benchmarks.append({
                "area": " Diferenciación de Mercado",
                "action": "Explotar nicho de mercado",
                "detail": f"Mientras {name1} se centra en {cat1}, {name2} domina en {cat2}. Oportunidad de diversificación."
            })
            
        return benchmarks
