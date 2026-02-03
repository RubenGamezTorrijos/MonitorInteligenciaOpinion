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
            if impact > 0.1: # Threshold: >10% of complaints
                rule = self.recommendation_rules.get(cat, {
                    'action': f'Investigar área de {cat}',
                    'detail': 'Se detectan anomalías no categorizadas.'
                })
                
                insights.append({
                    "area": cat,
                    "impact": f"{impact:.1%}",
                    "action": rule['action'],
                    "detail": rule['detail']
                })
                
        return insights[:3] # Returns top 3 priority actions
