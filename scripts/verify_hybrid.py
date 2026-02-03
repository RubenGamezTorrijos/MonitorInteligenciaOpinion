import pandas as pd
from src.services.preprocessor import SpanishTextPreprocessor
from src.services.analyzer import SentimentAnalyzerES
import numpy as np

def test_pipeline():
    print("🚀 Iniciando Verificación del Sistema Híbrido...")
    
    # Sample Data
    data = [
        {"user_id": "User1", "text": "Excelente producto, me encanta la calidad y el servicio!", "rating": 5, "product_id": "test_domain"},
        {"user_id": "User2", "text": "Pésimo servicio, el pedido llegó tarde y roto.", "rating": 1, "product_id": "test_domain"},
        {"user_id": "User3", "text": "Es normal, ni bueno ni malo, pero cumple.", "rating": 3, "product_id": "test_domain"},
        {"user_id": "User1", "text": "Otra reseña del mismo usuario para probar autoridad.", "rating": 4, "product_id": "test_domain"}, # User1 interacts twice
    ]
    df_raw = pd.DataFrame(data)
    
    print("\n1. Preprocesamiento...")
    preprocessor = SpanishTextPreprocessor()
    processed = [preprocessor.process_pipeline(t) for t in df_raw['text']]
    df_proc = pd.DataFrame(processed)
    df_merged = pd.concat([df_raw, df_proc.drop(columns=['original'])], axis=1)
    print("✅ Preprocesamiento completado.")
    
    print("\n2. Análisis Híbrido (TF-IDF + PageRank + CF)...")
    analyzer = SentimentAnalyzerES()
    df_final = analyzer.analyze_batch(df_merged)
    
    print("\n--- RESULTADOS ---")
    cols_to_show = ['user_id', 'sentimiento', 'sentimiento_score', 'authority_level', 'categoria_predom']
    print(df_final[cols_to_show])
    
    # Validations
    assert 'sentimiento_score' in df_final.columns
    assert 'authority_level' in df_final.columns
    assert df_final['sentimiento_score'].min() >= -1.0
    assert df_final['sentimiento_score'].max() <= 1.0
    
    print("\n✅ Verificación lógica exitosa!")

if __name__ == "__main__":
    test_pipeline()
