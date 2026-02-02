# 🛠️ Scripts de Utilidad

Esta carpeta contiene herramientas para la gestión, mantenimiento y ejecución independiente de las fases del monitor de opinión.

## 📋 Guía de Scripts

### 🚀 Herramientas de Ejecución (CLI)
*   **`scraper.py`**: Versión de terminal del extractor de reseñas. Permite bajar datos sin abrir Streamlit.
*   **`preprocessing.py`**: Realiza la limpieza NLP y transformación de datos raw a procesados de forma independiente.

### 🔧 Mantenimiento y Notebooks
*   **`verify_project.py`**: Protocolo de verificación que chequea si la estructura, archivos y datos del proyecto son correctos.
*   **`rebuild_analysis.py`**: Reconstruye el Notebook de análisis (`3_analisis.ipynb`) desde cero.
*   **`patch_notebooks.py`**: Aplica parches de código a los notebooks existentes para corregir errores comunes de visualización.
*   **`update_user_analysis.py`**: Inyecta celdas de análisis de "Inteligencia de Usuario" en los notebooks de trabajo.

### 🧩 Otros
*   **`verify_exporter.py`** (antes `test_exporter.py`): Verifica que la generación de PDF y Excel funcione correctamente sin errores de rutas.

---
> [!NOTE]
> Estos scripts son herramientas de soporte. El funcionamiento principal de la aplicación web reside en la carpeta `src/`.
