# 📊 Monitor de Inteligencia de Opinión

![Portada](images/MonitorOpinionInteligencia_Portada.jpg)

Este proyecto implementa un sistema **"End-to-End"** para el análisis de opinión pública, simulando el flujo de trabajo de un equipo profesional de Ciencia de Datos.

Proyecto de análisis de datos textuales a partir de reseñas de Trustpilot sobre Amazon España. Esta herramienta transforma reseñas masivas en insights accionables mediante NLP (Procesamiento de Lenguaje Natural) y visualizaciones interactivas premium.

## 👥 Equipo y Roles
Este proyecto ha sido desarrollado siguiendo un plan de colaboración dividido en dos perfiles:

### Rubén (Organizador/Coordinador)
- Gestión de repositorio y entorno.
- Desarrollo del script principal de scraping (`scraper.py`).
- Implementación del pipeline de limpieza NLP.
- Análisis de frecuencia y sentimiento en Notebooks.
- Desarrollado entorno web con Streamlit y Demo en Streamlit.app (Cloud Subdomain)
- Generación del Informe Final.

### Juanes (Colaborador)
- Investigación de librerías y estructura HTML.
- Creación de funciones auxiliares y validación de datos.
- Implementación de métricas estadísticas (longitud, palabras únicas).
- Desarrollo de visualizaciones avanzadas y dashboard interactivo.
- Creación de la lista de dependencias (`requirements.txt`).
- Documentación (`README.md`) y presentaciones.

## 🚀 Características Principales
- **Dashboard Interactivo**: 6 niveles de análisis (Resumen, Sentimiento, Inteligencia de Palabras, Tendencias, Insights Pro y Correlación).
- **Procesamiento Avanzado (NLP)**:
    - Preprocesamiento robusto en español (400+ Stopwords).
    - Análisis híbrido de sentimiento (TextBlob + Diccionario Local).
    - Categorización automática de feedback (Servicio, Logística, Quejas, etc.).
- **Suite de Exportación Pro**:
    - **Excel (XLSX)**: Dataset limpio y formateado.
    - **Informe PDF Pro**: Informe ejecutivo con gráficas integradas (Matplotlib).
    - **Pack ZIP**: Todo el material analítico e imágenes individuales.

## 📁 Estructura del Proyecto
```text
MonitorInteligenciaOpinion/
├── data/
│   ├── raw/                # Dataset original (dataset_raw.csv)
│   └── processed/          # Dataset limpio (dataset_clean.csv)
├── src/                    # Código fuente de la aplicación
│   ├── services/           # Motores de scraping, NLP y exportación
│   ├── views/              # Componentes de UI y estilos CSS
│   └── config/             # Constantes y branding
├── scripts/                # Herramientas de soporte
│   ├── scraper.py          # Script de extracción (Rubén)
│   ├── preprocessing.py    # Script de limpieza (Juanes)
│   ├── analysis.py         # Script de actualización de análisis (Juanes)
│   └── verify_project.py   # Script de validación de calidad (Rubén)
├── notebooks/
│   └── MONITOR_INTELIGENCIA_OPINION.ipynb  # Fase 1: Extracción (Rubén) | Fase 2: NLP (Juanes) | Fase 3: Valor (Rubén) | Fase 4: Gráficos (Juanes)
├── visualizations/         # Exportación de gráficos e informes (Juanes)
├── requirements.txt        # Dependencias (Juanes)
├── INFORME_EJECUTIVO.md    # Reporte ejecutivo (Rubén)
├── INFORME_TECNICO.md      # Memoria Técnica Detallada (Rubén)
├── GUIA_RAPIDA.md          # Guía de instalación y uso (Rubén)
├── app.py                  # Dashboard Web principal (Rubén)
└── README.md               # Instrucciones del Proyecto (Rubén)
```

## 🛠️ Instalación y Uso
1. **Configurar Entorno**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Linux/Mac
    pip install -r requirements.txt
    ```

2. **Ejecutar Pipeline Completo**: He desarrollado un script maestro para facilitar el testing:
    ```bash
    python run_pipeline.py
    ```

3. **Ejecución del Dashboard**:
    ```bash
    streamlit run app.py
    ```

4. **Ejecución Manual de Componentes**:
    - Extraer datos: `python scripts/scraper.py`
    - Procesar: `python scripts/preprocessing.py`
    - Verificación: `python scripts/verify_project.py`

## 📊 Resultados Principales
El sistema extrae automáticamente reseñas, aplica técnicas de NLP en español y clasifica el sentimiento del cliente, permitiendo identificar rápidamente los **"drivers"** de satisfacción de la marca.

---
**Desarrollado para la asignatura de SSIIRC - Monitor de Inteligencia de Opinión Trustpilot**