# 📔 Manual de Uso: Trustpilot Monitor Inteligente (Unified)

Este documento detalla el funcionamiento del notebook unificado y las mejoras implementadas para garantizar la robustez del scraping y la profundidad de los análisis.

## 🏗️ Estructura del Proyecto

El notebook se divide en 4 fases críticas, diseñadas para ser ejecutadas secuencialmente:

### 📥 FASE 1: Adquisición de Datos (Scraper Inteligente)
- **Búsqueda Dinámica**: Permite ingresar el nombre de la empresa. El sistema consulta a Trustpilot y extrae automáticamente la URL de reviews.
- **Modo Stealth Pro**: 
  - **Rotación de User-Agents**: Utiliza `fake-useragent` para que cada petición parezca venir de un navegador distinto.
  - **Delays Aleatorios**: Entre 2 y 4 segundos entre páginas para evitar la detección por comportamiento robótico.
- **Selectores Adaptativos**: Implementa una lógica de fallback con múltiples selectores CSS para mitigar cambios en el HTML de Trustpilot.

### 🧹 FASE 2: Preprocesamiento NLP
- **Limpieza de Ruido**: Eliminación de caracteres especiales, emojis y números que no aportan al sentimiento.
- **Stopwords Personalizadas**: Se han incluido términos específicos de Amazon y e-commerce (e.g., "producto", "envío", "paquete") para que no sesguen los resultados de las nubes de palabras.

### 💎 FASE 3: Análisis de Sentimiento
- **Motor Híbrido**:
  - **Diccionarios locales**: Identificación rápida de palabras clave en español.
  - **Fallback a Traducción + TextBlob**: Si el texto es largo y el diccionario local es ambiguo, se traduce al inglés para usar el modelo de polaridad de TextBlob (más preciso en inglés).
- **Métricas de Confianza**: Se calcula una puntuación de confianza para cada análisis.

### 📊 FASE 4: Visualización BI
- **Dashboard Integral**:
  - **Nube de Palabras**: Temas dominantes.
  - **Distribución de Sentimiento**: Salud de la marca.
  - **Correlación Longitud-Score**: ¿Son las quejas más detalladas que los elogios?
  - **Evolución Temporal**: Tendencias de opinión en el tiempo.

## 🚀 Cómo Ejecutar en Google Colab

1. Sube el archivo `.ipynb` a Drive.
2. Abre con Colab.
3. Ejecuta la **Fase 0** para instalar dependencias.
4. En la **Fase 1**, cuando aparezca el campo de texto, escribe el nombre de la empresa (ej: `Vueling` o `IKEA`) y presiona Enter.

## 📁 Archivos Generados
- `reseñas_trustpilot_raw.csv`: Datos brutos post-scraping.
- `reseñas_trustpilot_final.csv`: Dataset enriquecido con sentimientos y limpieza NLP.
