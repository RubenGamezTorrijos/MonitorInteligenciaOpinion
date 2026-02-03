# 📄 Memoria Técnica: Análisis de Reseñas de Amazon España (Trustpilot)
## 💡 Monitor de Inteligencia de Opinión - Proyecto Híbrido Multidimensional v2.0

---

## 1. Resumen Ejecutivo
Este proyecto evoluciona de un análisis descriptivo básico a un **Sistema Híbrido Multidimensional** avanzado. El sistema integra modelos de Recuperación de Información (IR), algoritmos de autoridad (PageRank) y técnicas de Filtrado Colaborativo para proporcionar una medición del sentimiento extremadamente robusta, personalizada y ponderada por la veracidad del informante.

---

## 2. Objetivos del Proyecto (Evolución v2.0)
*   **Adquisición de Datos**: Scraper robusto con extracción de metadatos de usuario y calificaciones.
*   **Procesamiento IR (Modelo Vectorial)**: Implementación de un índice invertido y representación en espacio vectorial.
*   **Ponderación por Autoridad**: Aplicación de PageRank para priorizar voces expertas o influyentes.
*   **Predicción y Personalización**: Uso de Filtrado Colaborativo para llenar vacíos de información y predecir tendencias.
*   **Visualización Científica**: Dashboard avanzado con métricas de veracidad y refinamiento del modelo.

---

## 3. Metodología Paso a Paso (Arquitectura Híbrida)

### 🚀 Fase 0: Pipeline de Procesamiento NLP (Evolución)
*   **Limpieza Profunda**: Manejo extendido de flexiones verbales en español y eliminación de términos de dominio con IDF=0.
*   **Tokenización Multidimensional**: Preparación de datos para el motor de indexación invertida.

### 📥 Fase 1: Motor de Recuperación de Información (IR Engine)
#### **Implementación de Espacio Vectorial**
Se han implementado las fórmulas académicas de pesado para una discriminación óptima:
*   **TF (Term Frequency)**: $1 + \log_2(f_{ij})$
*   **IDF (Inverse Document Frequency)**: $\log_2(N/n_i)$
*   **Similitud**: El sentimiento se determina midiendo la **Distancia del Coseno** entre el vector de la reseña y vectores "semilla" de conceptos positivos/negativos.

### 🔗 Fase 2: Módulo de Autoridad del Revisor (PageRank)
#### **Algoritmo de Brin & Page**
El sistema modela a los usuarios como una red de interacción:
*   **Nodos**: Usuarios/Revisores.
*   **Enlaces**: Interacciones y contribuciones cruzadas.
*   **Factor de Amortiguación**: $d = 0.85$.
*   **Resultado**: Cada reseña se pondera por la "autoridad" calculada del emisor, reduciendo el ruido de cuentas spam o irrelevantes.

### 🤖 Fase 3: Predicción y Personalización (Filtrado Colaborativo)
Se aplican dos enfoques para la veracidad de los datos:
1.  **User-to-User**: Utiliza la **Correlación de Pearson** para predecir el score de un usuario basándose en perfiles similares.
2.  **Item-to-Item**: Ajusta la puntuación esperada basándose en la similitud intrínseca de las experiencias de producto.
Esto permite "llenar vacíos" en reseñas incompletas mediante la fórmula de predicción de scores $p_{u,i}$.

---

### 📊 Fase 4: Visualización e Inteligencia Avanzada
El Dashboard se ha optimizado con tres niveles de lectura:
1.  **Nivel de Autoridad vs. Intensidad**: Identifica si las opiniones más fuertes provienen de usuarios con alta o baja autoridad.
2.  **Efecto del Refinamiento**: Gráfico comparativo que muestra cómo el Pipeline Híbrido ajusta el score base (TF-IDF) tras aplicar CF y PageRank.
3.  **Drivers de Opinión**: Análisis bidireccional de términos que impulsan la polaridad.

---

## 4. Conclusiones y Valor de Negocio v2.0
La arquitectura híbrida permite:
*   **Reducción de Sesgo**: La autoridad del revisor filtra el "ruido emocional" no cualificado.
*   **Alta Precisión**: El motor vectorial con log2-scaling detecta matices que el análisis de diccionarios simple ignora.
*   **Escalabilidad IR**: El índice invertido permite buscar y categorizar miles de reseñas en milisegundos.

**Recomendación**: Utilizar el Score Híbrido como métrica principal de KPI de marca, ya que es la representación más veraz y menos ruidosa de la reputación real del servicio.

---

## 👥 Créditos
*   **Equipo de Arquitectura Antigravity**: Diseño e implementación del Motor IR, PageRank y Filtrado Colaborativo.
*   **Rubén / Juanes**: Concepto original y validación de drivers de negocio.

---
*Documento actualizado: Febrero 2026 | Sistema de Inteligencia de Opinión Multidimensional.*
