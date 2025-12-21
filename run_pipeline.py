import subprocess
import sys
import os
import time

def print_step(message):
    print("\n" + "="*60)
    print(f"🚀 {message}")
    print("="*60)

def run_command(command, step_name):
    print(f"Ejecutando: {step_name}...")
    start_time = time.time()
    
    try:
        if "jupyter" in command:
             # For jupyter commands, we might need to handle shell=True differently depending on OS
             result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        else:
             result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
             
        duration = time.time() - start_time
        print(f"✅ {step_name} completado con éxito ({duration:.2f}s)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {step_name}")
        print(f"Código de salida: {e.returncode}")
        print(f"Error output:\n{e.stderr}")
        return False

def main():
    print_step("INICIANDO PIPELINE END-TO-END")
    
    # 0. Verificar entorno
    python_cmd = sys.executable
    jupyter_cmd = os.path.join(os.path.dirname(python_cmd), "jupyter")
    
    # Lista de pasos
    steps = [
        {
            "name": "FASE 1: Web Scraping (scraper.py)",
            "cmd": f'"{python_cmd}" scripts/scraper.py'
        },
        {
            "name": "FASE 2: Preprocesamiento NLP (preprocessing.py)",
            "cmd": f'"{python_cmd}" scripts/preprocessing.py'
        },
        {
            "name": "FASE 3: Análisis de Valor (Notebook 3)",
            "cmd": f'"{jupyter_cmd}" nbconvert --to notebook --execute --inplace notebooks/3_analisis.ipynb'
        },
        {
            "name": "FASE 4: Visualización e Inteligencia (Notebook 4)",
            "cmd": f'"{jupyter_cmd}" nbconvert --to notebook --execute --inplace notebooks/4_visualizacion.ipynb'
        }
    ]
    
    total_start = time.time()
    success = True
    
    for step in steps:
        if not run_command(step["cmd"], step["name"]):
            success = False
            print("\n⛔ DETENIENDO PIPELINE DEBIDO A UN ERROR")
            break
            
    total_duration = time.time() - total_start
    
    if success:
        print_step(f"🎉 PIPELINE COMPLETADO EXITOSAMENTE ({total_duration:.2f}s)")
        print("\nPuedes encontrar los resultados en:")
        print(" - Datos: data/processed/")
        print(" - Visualizaciones: visualizations/")
    else:
        print_step("⚠️ EL PIPELINE FINALIZÓ CON ERRORES")

if __name__ == "__main__":
    main()
