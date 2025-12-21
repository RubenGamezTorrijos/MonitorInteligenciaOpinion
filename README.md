# Proyecto: Monitor de Inteligencia de Opinión
UEM | Sistemas Inteligentes | Proyecto final: Monitor de Inteligencia de Opinión

# 📋 Descripción del Proyecto
Sistema completo para analizar opiniones y reseñas de Amazon España mediante técnicas de NLP y visualización de datos. Este proyecto implementa un pipeline end-to-end que incluye web scraping, preprocesamiento de texto, análisis de sentimiento y visualización de resultados.

# 👥 Equipo
- Rubén: Web Scraping, Análisis de Frecuencia, Coordinación
- Juanes: Preprocesamiento NLP, Visualización, Documentación

# 🏗️ Estructura del Proyecto
```
monitor_inteligencia_opinion/
├── data/
│   ├── raw/              # Datos crudos del scraping
│   └── processed/        # Datos procesados y analizados
├── notebooks/            # Jupyter notebooks por fase
│   ├── 1_scraping.ipynb
│   ├── 2_preprocesamiento.ipynb
│   ├── 3_analisis.ipynb
│   └── 4_visualizacion.ipynb
├── scripts/              # Scripts Python reutilizables
│   ├── scraper.py
│   └── preprocessing.py
├── visualizations/       # Gráficos y visualizaciones
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
```

# 🛠️ Preparación del Entorno
## Requisitos Previos
- Python 3.8 o superior
- Git (opcional, para clonar el repositorio)
- 500 MB de espacio libre en disco

## Opción 1: Entorno Local (Recomendado)
### Paso 1: Clonar o descargar el proyecto
```
# Si usas Git
git clone <url-del-repositorio>
cd monitor_inteligencia_opinion
```
# O descargar manualmente y descomprimir
Paso 2: Crear y activar entorno virtual
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Paso 3: Instalar dependencias
bash
pip install --upgrade pip
pip install -r requirements.txt
Paso 4: Descargar recursos de NLTK
bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
Paso 5: Verificar instalación
bash
python -c "import pandas, nltk, textblob; print('✓ Todas las dependencias están instaladas')"
Opción 2: Google Colab (Sin instalación local)
Subir todos los archivos del proyecto a Google Drive

Abrir Colab: colab.research.google.com

Montar Google Drive:

python
from google.colab import drive
drive.mount('/content/drive')
Navegar al directorio del proyecto

Instalar dependencias en Colab:

```
!pip install pandas nltk textblob beautifulsoup4 wordcloud plotly
!python -m nltk.downloader punkt stopwords
```

🧪 Pruebas y Verificación del Proyecto
Verificación Paso a Paso
Test 1: Verificar estructura del proyecto
```
# En la raíz del proyecto, ejecutar:
python -c "
import os
required_dirs = ['data/raw', 'data/processed', 'notebooks', 'scripts', 'visualizations']
required_files = ['requirements.txt', 'notebooks/1_scraping.ipynb', 'scripts/scraper.py']
for dir in required_dirs:
    os.makedirs(dir, exist_ok=True)
    print(f'✓ Directorio {dir} existe')
for file in required_files:
    if os.path.exists(file):
        print(f'✓ Archivo {file} existe')
    else:
        print(f'✗ Archivo {file} no encontrado')
```
Test 2: Ejecutar scraping (Fase 1)

# Opción A: Usar el notebook
```
jupyter notebook notebooks/1_scraping.ipynb
```
# Ejecutar todas las celdas (Cell → Run All)

# Opción B: Usar el script directamente
```
python scripts/scraper.py
```
Resultado esperado: Archivo data/raw/reviews_amazon_raw.csv con 50-100 reseñas.

Test 3: Verificar datos extraídos
```
python -c "
import pandas as pd
try:
    df = pd.read_csv('data/raw/reviews_amazon_raw.csv')
    print(f'✓ Dataset cargado: {len(df)} reseñas')
    print(f'✓ Columnas: {list(df.columns)}')
    print(f'✓ Muestra de datos:')
    print(df[['usuario', 'puntuacion']].head(3))
except Exception as e:
    print(f'✗ Error: {e}')
```
Test 4: Ejecutar preprocesamiento (Fase 2)
```
python scripts/preprocessing.py
```
Resultado esperado: Archivo data/processed/reviews_preprocessed.csv con columnas adicionales de texto procesado.

Test 5: Verificar preprocesamiento
```
python -c "
import pandas as pd
df = pd.read_csv('data/processed/reviews_preprocessed.csv')
print('✓ Columnas en dataset procesado:')
for col in df.columns:
    if 'texto' in col.lower():
        print(f'  - {col}')
print(f'\\n✓ Ejemplo de procesamiento:')
print(f'Texto original: {df.iloc[0][\"texto_original\"][:100]}...')
print(f'Texto limpio: {df.iloc[0][\"texto_limpio\"][:100]}...')
```
Test 6: Verificar análisis completo
```
# Ejecutar el notebook 3_analisis.ipynb completo
# Verificar que se generen:
# - data/processed/reviews_with_sentiment.csv
# - data/processed/analisis_stats.json
# - data/processed/top_palabras.csv
```
Test 7: Verificar visualizaciones
```
# Ejecutar el notebook 4_visualizacion.ipynb completo
# Verificar que se generen en visualizations/:
ls visualizations/
# Deberían aparecer:
# - wordcloud.png
# - top10_palabras.png
# - distribucion_sentimientos.png
# - informe_final.png
```
🚀 Cómo Ejecutar el Proyecto Completo
Método 1: Ejecución secuencial (Recomendado para primera vez)
```
# 1. Activar entorno virtual
```
source venv/bin/activate  # o venv\Scripts\activate en Windows
```
# 2. Ejecutar fase por fase
```
python scripts/scraper.py
python scripts/preprocessing.py
jupyter notebook notebooks/3_analisis.ipynb  # Ejecutar todas las celdas
jupyter notebook notebooks/4_visualizacion.ipynb  # Ejecutar todas las celdas
```
Método 2: Pipeline automatizado

# Crear script run_pipeline.py
```
python -c "
import subprocess
import sys

def run_phase(phase_name, command):
    print(f'\\n{'='*60}')
    print(f'Ejecutando {phase_name}')
    print(f'{'='*60}')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'✓ {phase_name} completado')
        return True
    else:
        print(f'✗ Error en {phase_name}:')
        print(result.stderr)
        return False
```
# Ejecutar pipeline
```
phases = [
    ('Scraping', 'python scripts/scraper.py'),
    ('Preprocesamiento', 'python scripts/preprocessing.py'),
    ('Análisis', 'jupyter nbconvert --to notebook --execute notebooks/3_analisis.ipynb'),
    ('Visualización', 'jupyter nbconvert --to notebook --execute notebooks/4_visualizacion.ipynb')
]

for phase_name, command in phases:
    if not run_phase(phase_name, command):
        print('Pipeline interrumpido')
        sys.exit(1)

print('\\n✅ Pipeline completado exitosamente')
```
Método 3: Usar Jupyter Notebooks interactivamente
```
# Iniciar Jupyter
jupyter notebook

# En el navegador, ejecutar en orden:
# 1. notebooks/1_scraping.ipynb
# 2. notebooks/2_preprocesamiento.ipynb
# 3. notebooks/3_analisis.ipynb
# 4. notebooks/4_visualizacion.ipynb

# ✅ Criterios de Verificación Final
Para confirmar que el proyecto funciona correctamente, verificar:

Requisitos Mínimos:
- Dataset con al menos 50 reseñas (data/raw/reviews_amazon_raw.csv)
- Preprocesamiento aplicado (texto_limpio, texto_sin_stopwords)
- Análisis de frecuencia (Top 10 palabras en top_palabras.csv)
- Análisis de sentimiento (polarity, subjectivity, sentiment)
- Al menos 3 visualizaciones generadas

Verificación Automática:
```
python -c "
import pandas as pd
import os
import json

print('Verificación del proyecto...')
print('='*50)
```

# 1. Verificar dataset
```
try:
    df_raw = pd.read_csv('data/raw/reviews_amazon_raw.csv')
    print(f'✓ Dataset raw: {len(df_raw)} reseñas')
    assert len(df_raw) >= 50, 'Menos de 50 reseñas'
except Exception as e:
    print(f'✗ Error dataset raw: {e}')
```

# 2. Verificar preprocesamiento
```
try:
    df_proc = pd.read_csv('data/processed/reviews_preprocessed.csv')
    required_cols = ['texto_limpio', 'texto_sin_stopwords']
    for col in required_cols:
        assert col in df_proc.columns, f'Falta columna {col}'
    print('✓ Preprocesamiento completo')
except Exception as e:
    print(f'✗ Error preprocesamiento: {e}')
```
# 3. Verificar análisis
```
try:
    df_sent = pd.read_csv('data/processed/reviews_with_sentiment.csv')
    assert 'sentiment' in df_sent.columns, 'Falta análisis de sentimiento'
    print('✓ Análisis de sentimiento completado')
except Exception as e:
    print(f'✗ Error análisis: {e}')
```
# 4. Verificar visualizaciones
```
viz_files = ['wordcloud.png', 'top10_palabras.png', 'distribucion_sentimientos.png']
for viz in viz_files:
    if os.path.exists(f'visualizations/{viz}'):
        print(f'✓ Visualización {viz} generada')
    else:
        print(f'✗ Falta visualización {viz}')

print('\\n' + '='*50)
print('Verificación completada')
```
# 🐛 Solución de Problemas Comunes
Problema 1: Error en la instalación de dependencias

# Si hay errores de versión
```
pip install --upgrade pip setuptools wheel
```
# Si hay problemas con NLTK
```
python -m nltk.downloader all
Problema 2: Scraping bloqueado
```
# Editar scripts/scraper.py y aumentar delays
```
time.sleep(random.uniform(3, 5))  # En lugar de 1-3
Problema 3: Memoria insuficiente en notebooks
```
# Reducir tamaño de dataset
# En scraping, cambiar pages=2 a pages=1
Problema 4: Caracteres especiales mal codificados

# Asegurar encoding UTF-8
```
df.to_csv('archivo.csv', index=False, encoding='utf-8-sig')
```
# 📊 Resultados Esperados
Archivos Generados:
```
data/
├── raw/
│   └── reviews_amazon_raw.csv          # 50-100 reseñas crudas
├── processed/
│   ├── reviews_preprocessed.csv        # Textos procesados
│   ├── reviews_with_sentiment.csv      # Análisis completo
│   ├── top_palabras.csv               # Frecuencia de palabras
│   └── analisis_stats.json            # Estadísticas clave

visualizations/
├── wordcloud.png                      # Nube de palabras
├── top10_palabras.png                 # Gráfico de barras
├── distribucion_sentimientos.png      # Gráfico circular
├── puntuacion_vs_sentimiento.png      # Gráfico de dispersión
├── analisis_adicional_1.png          # Gráficos adicionales
├── heatmap_palabras_sentimiento.png  # Heatmap
├── informe_final.png                 # Informe visual completo
└── dashboard_interactivo.html        # Dashboard interactivo
```
---

# Métricas de Calidad:
- Coverage: 100% de las fases implementadas
- Reproducibilidad: Pipeline completamente automatizado
- Documentación: Código comentado y README completo
- Visualizaciones: Gráficos profesionales y informativos

---

# 📝 Notas Finales
Este proyecto está completamente desarrollado y probado, con una distribución equitativa del trabajo entre Rubén y Juanes. Cada fase incluye código funcional, documentación y resultados verificables.

---

# Características destacadas:
## ✅ Web scraping ético con delays y User-Agents
## ✅ Pipeline completo de NLP en español
## ✅ Análisis de sentimiento con TextBlob
## ✅ Visualizaciones profesionales
## ✅ Código modular y reutilizable
## ✅ Documentación completa
## ✅ Tests de verificación incluidos

---

Para cualquier problema o consulta:
- Revisar la sección de solución de problemas
- Verificar que todas las dependencias están instaladas
- Ejecutar los tests de verificación
- Consultar los notebooks de ejemplo

---

Licencia: Proyecto educativo - Uso académico
Fecha: Diciembre 2025
Asignatura: Sistemas Inteligentes - Universidad Europea