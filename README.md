# Monitor de Inteligencia de Opinión

Este proyecto implementa un sistema "End-to-End" para el análisis de opinión pública, simulando el flujo de trabajo de un equipo de Ciencia de Datos.

Proyecto de análisis de datos textuales a partir de reseñas de Trustpilot sobre Amazon España.

---

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

---

## 📁 Estructura del Proyecto

```
MonitorInteligenciaOpinion/
├── data/
│   ├── raw/                # Dataset original (dataset_raw.csv)
│   └── processed/          # Dataset limpio (dataset_clean.csv)
├── scripts/                # Esta parte sólo se hará si se termina bien el cuaderno Notebook
│   ├── scraper.py          # Script de extracción (Rubén)
│   ├── preprocessing.py    # Script de limpieza (Juanes)
│   ├── analysis.py         # Script de actualización de análisis (Juanes)
│   ├── app.py              # Dashboard Web (Rubén)
│   └── verify_project.py   # Script de validación de calidad (Rubén)
├── notebooks/
│   └── MONITOR_INTELIGENCIA_OPINION.ipynb  # Secciones:  # Fase 1: Extracción  (Rubén) 
│                                                         # Fase 2: NLP (Juanes)
│                                                         # Fase 3: Valor (Rubén)
│                                                         # Fase 4: Gráficos (Juanes)
├── visualizations/         # Exportación de gráficos e informes (Juanes) (Esta directorio no es para Notebooks)
├── requirements.txt        # Dependencias (Juanes)
├── INFORME_EJECUTIVO.md    # Reporte ejecutivo (Rubén)
├── INFORME_TECNICO.md      # Memoria Técnica Detallada (Rubén)
├── GUIA_RAPIDA.md          # Guía de instalación y uso (Rubén)
└── README.md               # Instrucciones del Proyecto (Rubén)
```
---

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

---

## Roles y Responsabilidades

*   **Rubén (Project Lead / Backend):** Scraper, Lógica de Análisis, Validación, Informe Final.
*   **Juanes (NLP Specialist / Visualization):** Preprocesamiento, Visualización, Dashboard, Dependencias.

## Ejecución

El proyecto puede ejecutarse de dos modos (Sólo para uso local con Python *.py):

1.  **Modo Automático ("End-to-End"):** Ejecuta `python run_pipeline.py`.
2.  **Modo Manual (Notebooks):** Ejecuta los notebooks en orden (1 al 4) en Google Colab o Jupyter.

Para más detalles, consulta la `GUIA_RAPIDA.md`.

---

## 📊 Resultados Principales
El sistema extrae automáticamente más de 100 reseñas, aplica técnicas de NLP en español y clasifica el sentimiento del cliente, permitiendo identificar rápidamente los "drivers" de satisfacción de la marca.