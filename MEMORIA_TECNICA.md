# 📄 Memoria Técnica: Análisis de Reseñas de Amazon España (Trustpilot)
## 💡 Monitor de Inteligencia de Opinión - Proyecto End-to-End

---

## 1. Resumen Ejecutivo
Este proyecto consiste en el desarrollo de un sistema integral de ciencia de datos diseñado para capturar, procesar y analizar la percepción de los clientes de Amazon España utilizando reseñas de **Trustpilot**. El sistema automatiza desde la extracción de datos mediante web scraping hasta la generación de un dashboard de inteligencia de negocio, proporcionando insights accionables sobre las áreas críticas de servicio.

---

## 2. Objetivos del Proyecto
*   **Adquisición de Datos**: Implementar un scraper robusto capaz de navegar y extraer información estructurada de Trustpilot.
*   **Procesamiento NLP**: Desarrollar un pipeline lingüístico especializado para el idioma español.
*   **Análisis de Valor**: Identificar frecuencias de quejas y cuantificar el sentimiento del usuario.
*   **Visualización**: Comunicar hallazgos mediante gráficas de alto impacto para la toma de decisiones.

---

## 3. Metodología Paso a Paso (Explicación de Celdas)

### 🚀 Fase 0: Configuración del Entorno (Celdas 1-2)
*   **Instalación de Dependencias**: Se instalan librerías de scraping (`requests`, `BeautifulSoup`), procesamiento de lenguaje natural (`nltk`, `spacy`, `textblob`) y visualización (`matplotlib`, `seaborn`, `wordcloud`).
*   **Importación y Recursos**: Se descargan los tokenizadores y corpus de *stopwords* necesarios para el español de la librería NLTK.

---

### 📥 Fase 1: Adquisición de Datos (Web Scraping)
#### **Celda 3: Clase TrustpilotScraper**
Se implementa una arquitectura orientada a objetos para el scraper:
*   **Manejo de User-Agents**: Simula navegadores reales para evitar bloqueos por parte del servidor.
*   **Selectores Adaptativos**: Utiliza múltiples selectores CSS para garantizar la extracción incluso si Trustpilot cambia ligeramente su estructura HTML.
*   **Lógica de Paginación**: Navega automáticamente por las páginas hasta alcanzar el objetivo de reseñas configurado.

#### **Celda 4: Ejecución y Backup**
Se ejecuta el scraper. En caso de fallos de red, la celda incluye un **sistema de backup** con datos de ejemplo realistas para asegurar la continuidad del pipeline de análisis. El dataset resultante se guarda como `reseñas_amazon_trustpilot.csv`.

---

### 🧹 Fase 2: Preprocesamiento y Limpieza (NLP)
#### **Celda 5: Clase SpanishTextPreprocessor**
Transforma el texto bruto en datos estructurados listos para análisis:
1.  **Limpieza**: Eliminación de URLs, caracteres especiales y conversión a minúsculas.
2.  **Filtrado de Stopwords Custom**: Además de las palabras comunes (la, el, que), se eliminan términos del dominio que no aportan valor analítico como "amazon", "producto" o "pedido".
3.  **Tokenización**: División del texto en unidades mínimas de significado (palabras).

#### **Celda 6: Aplicación del Pipeline**
Se procesa todo el dataset. Se generan métricas de eficiencia, logrando reducciones de texto superiores al 60%, filtrando el ruido y manteniendo solo la "esencia" de la opinión del cliente.

---

### 💎 Fase 3: Extracción de Valor y Análisis
#### **Celda 7: Análisis de Frecuencia**
Se identifican los términos más recurrentes categorizándolos en áreas de negocio:
*   **Logística**: "repartidor", "entrega", "transporte".
*   **Postventa**: "devolución", "garantía", "reembolso".
*   **Financiero**: "pago", "dinero", "euros".

#### **Celda 8: Análisis de Sentimiento**
Utiliza un enfoque híbrido:
1.  **Traducción automática**: Traduce fragmentos al inglés para aprovechar la precisión de `TextBlob`.
2.  **Diccionario de Polaridad**: Valida el resultado con un diccionario específico de términos positivos/negativos en español.
Cada reseña recibe un score de -1 (muy negativo) a +1 (muy positivo).

---

### 📊 Fase 4: Visualización e Inteligencia (BI)
#### **Celdas de Visualización**
Se generan cuatro herramientas clave para el análisis:
1.  **Word Cloud**: Representación visual de los problemas más "ruidosos".
2.  **Top 20 Keywords**: Gráfico de barras que cuantifica los puntos de dolor exactos.
3.  **Distribución de Sentimiento**: Gráfico circular que muestra que más del 75% de las reseñas analizadas son negativas.
4.  **Matriz de Categorías**: Distribución porcentual de las áreas afectadas (Ej: Servicio vs Logística).

---

## 4. Conclusiones y Valor de Negocio
El análisis revela que la insatisfacción de Amazon España en Trustpilot no es aleatoria, sino sistemática:
*   **Atención al Cliente**: Es el punto de fricción principal, descrito como ineficiente.
*   **Logística Interna**: La gestión de repartidores y paquetes es la segunda causa de quejas.
*   **Escalabilidad**: Se detecta que en periodos de alta demanda (Navidad), la calidad del servicio decrece significativamente.

**Recomendación**: Implementar una auditoría inmediata en los procesos de resolución de disputas con vendedores externos y reforzar la red logística en periodos estacionales.

---

## 👥 Créditos
*   **Rubén**: Responsable de la Adquisición de Datos (Fase 1) y el Análisis de Extracción de Valor (Fase 3).
*   **Juanes**: Responsable del Preprocesamiento NLP (Fase 2) y la Visualización de Inteligencia (Fase 4).

---
*Documento generado automáticamente como memoria técnica del proyecto v14.*
