# Informe Ejecutivo: Monitor de Inteligencia de Opinión
**Persona A (Organizador)**

## 1. Resumen Ejecutivo
Este proyecto presenta una solución integral para el monitoreo de reputación online. Mediante el uso de técnicas avanzadas de procesamiento de lenguaje natural (NLP) y scraping de datos en tiempo real, se ha logrado transformar opiniones desestructuradas en métricas de negocio accionables.

## 2. Metodología Aplicada
Bajo la coordinación de Persona A, el equipo ha desarrollado un pipeline dividido en 4 fases críticas:
*   **Adquisición:** Scraping de Trustpilot (Amazon ES) con manejo de paginación y delays.
*   **Preprocesamiento:** Limpieza profunda de texto (minúsculas, caracteres especiales, stopwords).
*   **Análisis:** Cálculo de polaridad de sentimientos y modelado de gramas.
*   **Inteligencia:** Generación de dashboards y visualizaciones para BI.

## 3. Hallazgos Principales (Persona A & B)
1.  **Sentimiento:** El análisis revela una polaridad promedio de -0.02 (Neutral), con 210 reseñas procesadas. La mayoría de los comentarios se clasifican como neutrales (204) o negativos (6), indicando un clima de opinión cauteloso.
2.  **Temas Recurrentes:** Las palabras clave más frecuentes están asociadas a "cliente", "atencion", "entrega" y "pedido", lo que sugiere que la calidad del soporte y la logística son los principales drivers de opinión.
3.  **Relación Estrellas-Texto:** Se observa una correlación positiva débil (0.05) entre la puntuación otorgada y la polaridad calculada, lo que implica que los usuarios expresan sus frustraciones de manera matizada.

## 4. Conclusiones y Recomendaciones
*   Se recomienda implementar este monitor de forma continua para alertar sobre caídas bruscas en el sentimiento.
*   El uso de "dataset_clean.csv" permite análisis posteriores de Machine Learning para predicción de fuga de clientes (Churn).

---
**Firma:** Persona A (Coordinador de Proyecto)
**Fecha:** Diciembre 2025
