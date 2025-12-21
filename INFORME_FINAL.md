# Informe Final: Monitor de Inteligencia de Opinión

## 1. Resumen del Proyecto
Este proyecto implementa un sistema "End-to-End" para el análisis de sentimientos y opiniones de usuarios en la plataforma Trustpilot sobre Amazon España. El objetivo es proporcionar una herramienta que permita a una marca monitorear su reputación online de manera automatizada.

## 2. Metodología

### FASE 1: Adquisición de Datos (Web Scraping)
- **Fuente:** Trustpilot (Amazon España).
- **Herramientas:** Python, `requests`, `BeautifulSoup4`.
- **Resultados:** Se extrajeron 140 reseñas incluyendo usuario, puntuación, fecha, título y texto del comentario. Los datos se almacenaron en `data/raw/reviews_amazon_raw.csv`.

### FASE 2: Preprocesamiento y Limpieza (NLP)
- **Tareas:** Normalización (minúsculas), eliminación de caracteres especiales, eliminación de stopwords y tokenización.
- **Herramientas:** `nltk`, `re`, `unicodedata`.
- **Resultados:** Un dataset procesado listo para el análisis, guardado en `data/processed/reviews_preprocessed.csv`.

### FASE 3: Extracción de Valor y Análisis
- **Análisis de Frecuencia:** Identificación de los términos más recurrentes.
- **Análisis de Sentimiento:** Clasificación de reseñas en Positivas, Negativas y Neutras usando la librería `TextBlob`.
- **Resultados:** Generación de métricas de polaridad y subjetividad.

### FASE 4: Visualización e Inteligencia (BI)
- **Resultados Visuales:** 
    - Nube de palabras (WordCloud).
    - Gráfico de barras de las 10 palabras más frecuentes.
    - Distribución porcentual de sentimientos.
    - Dashboard interactivo con `Plotly`.

## 3. Conclusiones
- **Sentimiento General:** La marca analizada presenta una distribución de sentimientos mixta, permitiendo identificar puntos críticos de dolor para el cliente.
- **Palabras Clave:** Los términos más frecuentes revelan los aspectos que más preocupan o satisfacen a los usuarios (ej: "entrega", "servicio", "precio").
- **Valor de Negocio:** La automatización permite una respuesta rápida a las tendencias de opinión, facilitando la toma de decisiones estratégicas.

---
**Desarrollado por:** Persona A y Persona B
**Fecha:** Diciembre 2025
