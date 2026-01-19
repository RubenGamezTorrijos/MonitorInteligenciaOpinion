import pandas as pd
import os
import json
import sys

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def verify_structure():
    print_header("TEST 1: VERIFICACION DE ESTRUCTURA DEL PROYECTO")
    required_dirs = ['data/raw', 'data/processed', 'notebooks', 'scripts', 'visualizations']
    required_files = [
        'requirements.txt', 
        'notebooks/Analisis_Amazon_TrustPilot_v6_DeepSeek_Revisar.ipynb', 
        'scripts/scraper.py',
        'scripts/preprocessing.py'
    ]
    
    all_ok = True
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for directory in required_dirs:
        path = os.path.join(base_dir, directory)
        if os.path.exists(path):
            print(f"[OK] Directorio '{directory}' existe")
        else:
            print(f"[ERROR] Directorio '{directory}' NO encontrado")
            all_ok = False
            
    for file in required_files:
        path = os.path.join(base_dir, file)
        if os.path.exists(path):
            print(f"[OK] Archivo '{file}' existe")
        else:
            print(f"[ERROR] Archivo '{file}' NO encontrado")
            all_ok = False
            
    return all_ok

def verify_dataset():
    print_header("TEST 2: VERIFICACION DEL DATASET (FASE 1)")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'data', 'raw', 'dataset_raw.csv')
    try:
        if not os.path.exists(dataset_path):
            print(f"[ERROR] Archivo '{dataset_path}' NO existe")
            return False
            
        df_raw = pd.read_csv(dataset_path)
        print(f"[OK] Dataset raw cargado correctamente")
        print(f"  - Total resenas: {len(df_raw)}")
        print(f"  - Columnas: {list(df_raw.columns)}")
        
        if len(df_raw) >= 50:
            print(f"[OK] Cantidad de resenas suficiente (>= 50)")
        else:
            print(f"[WARN] Advertencia: Menos de 50 resenas ({len(df_raw)})")
            
        required_cols = ['texto_comentario', 'puntuacion']
        missing_cols = [col for col in required_cols if col not in df_raw.columns]
        
        if not missing_cols:
            print("[OK] Columnas criticas presentes")
            return True
        else:
            print(f"[ERROR] Faltan columnas: {missing_cols}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error verificando dataset raw: {e}")
        return False

def verify_preprocessing():
    print_header("TEST 3: VERIFICACION DE PREPROCESAMIENTO (FASE 2)")
    try:
        if not os.path.exists('data/processed/dataset_clean.csv'):
            print("[ERROR] Archivo 'data/processed/dataset_clean.csv' NO existe")
            return False
            
        df_proc = pd.read_csv('data/processed/dataset_clean.csv')
        print(f"[OK] Dataset procesado cargado")
        
        required_cols = ['texto_limpio', 'num_palabras']
        missing = [c for c in required_cols if c not in df_proc.columns]
        
        if not missing:
            print(f"[OK] Columnas de preprocesamiento presentes: {required_cols}")
            return True
        else:
            print(f"[ERROR] Faltan columnas de preprocesamiento: {missing}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error verificando preprocesamiento: {e}")
        return False

def verify_analysis():
    print_header("TEST 4: VERIFICACION DE ANALISIS (FASE 3)")
    try:
        if not os.path.exists('data/processed/reviews_with_sentiment.csv'):
            print("[ERROR] Archivo 'data/processed/reviews_with_sentiment.csv' NO existe")
            return False
            
        df_sent = pd.read_csv('data/processed/reviews_with_sentiment.csv')
        
        if 'sentiment' in df_sent.columns and 'polarity' in df_sent.columns:
            print("[OK] Analisis de sentimiento detectado (columnas 'sentiment', 'polarity')")
            print(f"  - Distribucion: {df_sent['sentiment'].value_counts().to_dict()}")
            return True
        else:
            print("[ERROR] Faltan columnas de analisis de sentimiento")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error verificando analisis: {e}")
        return False

def verify_visualizations():
    print_header("TEST 5: VERIFICACION DE VISUALIZACIONES (FASE 4)")
    viz_files = [
        'wordcloud.png', 
        'top10_palabras.png', 
        'distribucion_sentimientos.png',
        'informe_final.png',
        'dashboard_interactivo.html'
    ]
    
    found_count = 0
    for viz in viz_files:
        path = os.path.join('visualizations', viz)
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"[OK] {viz} existe ({size_kb:.1f} KB)")
            found_count += 1
        else:
            print(f"[ERROR] {viz} NO encontrado")
    
    if found_count == len(viz_files):
        print(f"\n[OK] Todas las visualizaciones clave ({len(viz_files)}) estan presentes")
        return True
    elif found_count >= 3:
        print(f"\n[WARN] Faltan algunas visualizaciones, pero se cumplen los minimos (3)")
        return True
    else:
        print(f"\n[ERROR] Faltan demasiadas visualizaciones")
        return False

def main():
    print("INICIANDO PROTOCOLO DE VERIFICACION DEL PROYECTO")
    print("Monitor de Inteligencia de Opinion")
    
    results = [
        verify_structure(),
        verify_dataset(),
        verify_preprocessing(),
        verify_analysis(),
        verify_visualizations()
    ]
    
    print_header("RESUMEN FINAL")
    if all(results):
        print("[OK] EL PROYECTO CUMPLE CON TODOS LOS REQUISITOS TECNICOS")
        print("   Se han superado todas las pruebas automaticas.")
    else:
        print("[WARN] SE HAN DETECTADO PROBLEMAS EN ALGUNAS FASES")
        print("   Revise los logs anteriores para mas detalles.")

if __name__ == "__main__":
    main()
