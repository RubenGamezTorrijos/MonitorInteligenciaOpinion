# Monitor de Inteligencia de Opinión

Proyecto de análisis de datos textuales a partir de reseñas de Trustpilot sobre Amazon España.

## 👥 Equipo y Roles

Este proyecto ha sido desarrollado siguiendo un plan de colaboración dividido en dos perfiles:

*   **Rubén (Organizador/Coordinador):**
    *   Gestión de repositorio y entorno.
    *   Desarrollo del script principal de scraping (`scraper.py`).
    *   Implementación del pipeline de limpieza NLP.
    *   Análisis de frecuencia y sentimiento en Notebooks.
    *   Generación del Informe Final.

*   **Juanes (Colaborador):**
    *   Investigación de librerías y estructura HTML.
    *   Creación de funciones auxiliares y validación de datos.
    *   Implementación de métricas estadísticas (longitud, palabras únicas).
    *   Desarrollo de visualizaciones avanzadas y dashboard interactivo.
    *   Creación de la lista de dependencias (`requirements.txt`).
    *   Documentación (`README.md`) y presentaciones.

## 📁 Estructura del Proyecto

```text
MonitorInteligenciaOpinion/
├── data/
│   ├── raw/                # Dataset original (dataset_raw.csv)
│   └── processed/          # Dataset limpio (dataset_clean.csv)
├── scripts/
│   ├── scraper.py          # Script de extracción (Rubén)
│   ├── preprocessing.py    # Script de limpieza (Rubén/Juanes)
│   └── verify_project.py   # Script de validación de calidad
├── notebooks/
│   ├── 1_scraping.ipynb    # Fase 1: Extracción  (Rubén)
│   ├── 2_preprocesamiento.ipynb # Fase 2: NLP (Juanes)
│   ├── 3_analisis.ipynb    # Fase 3: Valor (Rubén)
│   └── 4_visualizacion.ipynb # Fase 4: Gráficos (Juanes)
├── visualizations/         # Exportación de gráficos e informes (Juanes)
├── requirements.txt        # Dependencias (Juanes)
├── INFORME_FINAL.md        # Reporte ejecutivo (Rubén)
└── README.md               # Instrucciones (Rubén)
```

## 🛠️ Instalación y Uso

1.  **Configurar Entorno:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Ejecutar Pipeline Completo:**
    He desarrollado un script maestro para facilitar el testing:
    ```bash
    python run_pipeline.py
    ```

3.  **Ejecución Manual:**
    - Extraer datos: `python scripts/scraper.py`
    - Procesar: `python scripts/preprocessing.py`
    - Verificación: `python scripts/verify_project.py`

## 📊 Resultados Principales
El sistema extrae automáticamente más de 100 reseñas, aplica técnicas de NLP en español y clasifica el sentimiento del cliente, permitiendo identificar rápidamente los "drivers" de satisfacción de la marca.