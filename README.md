# Proyecto: Monitor de Inteligencia de Opinión
UEM | Sistemas Inteligentes | Proyecto final: Monitor de Ingeligencia de Opinión

## 📋 Descripción del Proyecto
Sistema completo para analizar opiniones y reseñas de Amazon España mediante técnicas de NLP y visualización de datos.

## 👥 Equipo
- **Rubén Gámez Torrijos**: Web Scraping, Análisis de Frecuencia, Coordinación
- **Juán Esteban Torres Carreño**: Preprocesamiento NLP, Visualización, Documentación

## 🏗️ Estructura del Proyecto

```
monitor_inteligencia_opinion/
├── data/
│ ├── raw/ # Datos crudos del scraping
│ └── processed/ # Datos procesados y analizados
├── notebooks/ # Jupyter notebooks por fase
├── scripts/ # Scripts Python reutilizables
├── visualizations/ # Gráficos y visualizaciones
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo
```


## 🚀 Cómo Ejecutar el Proyecto

### 1. Configurar entorno
```bash
# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar recursos de NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Fase 1: Web Scraping
jupyter notebook notebooks/1_scraping.ipynb

# Fase 2: Preprocesamiento
jupyter notebook notebooks/2_preprocesamiento.ipynb

# Fase 3: Análisis
jupyter notebook notebooks/3_analisis.ipynb

# Fase 4: Visualización
jupyter notebook notebooks/4_visualizacion.ipynb



---

## **ENTREGA FINAL**

### **Archivos a entregar:**
1. **Notebooks completos** (`notebooks/`):
   - `1_scraping.ipynb`
   - `2_preprocesamiento.ipynb`
   - `3_analisis.ipynb`
   - `4_visualizacion.ipynb`

2. **Scripts Python** (`scripts/`):
   - `scraper.py`
   - `preprocessing.py`

3. **Dataset generado** (`data/`):
   - `raw/reviews_amazon_raw.csv`
   - `processed/reviews_with_sentiment.csv`

4. **Visualizaciones** (`visualizations/`):
   - `wordcloud.png`
   - `top10_palabras.png`
   - `distribucion_sentimientos.png`
   - `informe_final.png`

5. **Documentación**:
   - `requirements.txt`
   - `README.md`

### **Cómo verificar que funciona:**
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar notebooks en orden numérico
3. Verificar que se generan todos los archivos CSV
4. Comprobar que las visualizaciones se crean correctamente
5. Confirmar que el análisis incluye:
   - Mínimo 50 reseñas
   - Preprocesamiento completo (limpieza, stopwords, tokenización)
   - Análisis de frecuencia (top palabras)
   - Análisis de sentimiento
   - 3+ visualizaciones informativas

Este proyecto está completamente desarrollado y probado, con una distribución equitativa del trabajo entre Rubén y Juanes. Cada fase incluye código funcional, documentación y resultados verificables.