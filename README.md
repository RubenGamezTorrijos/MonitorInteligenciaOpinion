# 📊 Monitor de Opinión Inteligente Trustpilot

Plataforma profesional de análisis de sentimientos y reputación online optimizada para **Trustpilot**. Esta herramienta transforma reseñas masivas en insights accionables mediante NLP (Procesamiento de Lenguaje Natural) y visualizaciones interactivas.

MonitorOpinionInteligente_Portada.jpg

## 🚀 Características Principales

- **Dashboard Interactivo**: 5 niveles de análisis (Resumen, Sentimiento, Inteligencia de Palabras, Tendencias y Correlación).
- **Procesamiento Avanzado (NLP)**:
    - Preprocesamiento robusto en español (400+ Stopwords).
    - Análisis híbrido de sentimiento (TextBlob + Diccionario Local).
    - Categorización automática de feedback (Servicio, Logística, Quejas, etc.).
- **Suite de Exportación Pro**:
    - **Excel (XLSX)**: Dataset limpio y formateado.
    - **PDF Pro**: Informe ejecutivo con gráficas integradas.
    - **Pack ZIP**: Todo el material analítico en un solo archivo.

## 🛠️ Instalación Local

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/RubenGamezTorrijos/MonitorInteligenciaOpinion.git
    cd MonitorInteligenciaOpinion
    ```

2.  **Configurar entorno**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Ejecutar**:
    ```bash
    streamlit run app.py
    ```

## ☁️ Despliegue en Streamlit Cloud

1. Sube el código a un repositorio de GitHub.
2. Conecta tu cuenta en [share.streamlit.io](https://share.streamlit.io).
3. Selecciona `app.py` como punto de entrada.
4. ¡Listo! Tu monitor estará accesible vía web.

## 📁 Estructura del Proyecto

- `src/services/`: Motores de scraping, NLP y exportación.
- `src/views/`: Componentes de UI y estilos CSS.
- `src/config/`: Constantes y branding.
- `notebooks/`: Versión original de laboratorio (Jupyter).

---
**Desarrollado para el Máster SSII - Monitor de Inteligencia de Opinión**