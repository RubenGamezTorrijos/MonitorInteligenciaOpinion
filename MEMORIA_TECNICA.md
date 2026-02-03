# 📄 Memoria Técnica: Análisis de Reseñas E-commerce (Trustpilot)
## 💡 Monitor de Inteligencia de Opinión - Proyecto Híbrido Multidimensional v3.0

---

## 1. Resumen Ejecutivo
Este proyecto evoluciona de un análisis descriptivo básico a un **Sistema Híbrido Multidimensional** avanzado. El sistema integra modelos de Recuperación de Información (IR), algoritmos de autoridad (PageRank) y técnicas de Filtrado Colaborativo para proporcionar una medición del sentimiento extremadamente robusta, personalizada y ponderada por la veracidad del informante.

---

## 2. Objetivos del Proyecto (Evolución v3.0)
*   **Adquisición de Datos**: Scraper robusto con extracción de metadatos de usuario y calificaciones.
*   **Procesamiento IR (Modelo Vectorial)**: Implementación de un índice invertido y representación en espacio vectorial.
*   **Ponderación por Autoridad**: Aplicación de PageRank para priorizar voces expertas o influyentes.
*   **Predicción y Personalización**: Uso de Filtrado Colaborativo para llenar vacíos de información y predecir tendencias.
*   **Inteligencia Comparativa (Benchmarking)**: Módulo de confrontación directa entre marcas.
*   **Visualización Científica**: Dashboard avanzado con métricas de veracidad y refinamiento del modelo.

---

## 3. Metodología Paso a Paso (Arquitectura Híbrida)

### 🚀 Fase 0: Pipeline de Procesamiento NLP (Evolución)
*   **Limpieza Profunda**: Manejo extendido de flexiones verbales en español.
*   **Tokenización Multidimensional**: Preparación de datos para el motor de indexación invertida.
*   **Filtrado Dinámico de Branding**: El sistema identifica el nombre de la marca analizada y lo elimina dinámicamente de los tokens para evitar ruido léxico redundante.

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

### 🤖 Fase 3: Predicción y Personalización (Fórmula Híbrida v2.1)
Se ha implementado una arquitectura de consenso para evitar la neutralización de scores y asegurar la diferenciación entre marcas:

#### **Fórmula de Consenso Equilibrada**
El sistema calcula el **Score Final** mediante una ponderación tripartita:
1.  **Puntuación Explícita (50%)**: Se deriva directamente de las estrellas (1-5) normalizadas al rango $[-1, 1]$.
2.  **Análisis Semántico IR (30%)**: Basado en la similitud del coseno, ajustado por la **Autoridad del Revisor** (PageRank).
3.  **Filtrado Colaborativo (20%)**: Proporciona el componente de personalización social mediante la Correlación de Pearson.

$$\text{Final Score} = (\text{Rating Score} \times 0.5) + (\text{Base Score} \times \text{Auth}_{norm} \times 0.3) + (\text{CF Pred} \times 0.2)$$

### 📊 Fase 4: Visualización e Inteligencia Avanzada
El Dashboard se ha optimizado con tres niveles de lectura:
1.  **Nivel de Autoridad vs. Intensidad**: Identifica si las opiniones más fuertes provienen de usuarios con autoridad.
2.  **Efecto del Refinamiento**: Gráfico comparativo que muestra el ajuste del score tras aplicar el Pipeline Híbrido.
3.  **Drivers de Opinión**: Análisis bidireccional de términos que impulsan la polaridad.

### ⚔️ Fase 5: Módulo de Benchmarking (Lucha de Gigantes)
Se ha implementado una arquitectura de visualización dual que permite:
*   **KPIs Enfrentados**: Comparativa directa de Rating Trustpilot vs. Score Híbrido entre dos marcas.
*   **Distribución de Polaridad**: Gráficas de barras agrupadas para identificar qué marca domina en sentimientos positivos o negativos.
*   **Diferenciación Léxica**: Extracción de temas únicos para cada marca mediante teoría de conjuntos.

---

## 4. Conclusiones y Valor de Negocio
La arquitectura híbrida permite:
*   **Reducción de Sesgo**: La autoridad del revisor filtra el "ruido emocional" no cualificado.
*   **Benchmarking Preciso**: La capacidad de comparar marcas bajo la misma métrica híbrida revela la ventaja competitiva real.
*   **Escalabilidad IR**: El índice invertido permite procesar grandes volúmenes de datos en milisegundos.

---

## 👥 Créditos
*   **Equipo de Arquitectura Antigravity**: Diseño e implementación del Motor IR, PageRank, Filtrado Colaborativo y Módulo de Comparativa.
*   **Rubén / Juanes**: Concepto original y validación de drivers de negocio.

---
*Documento actualizado: Febrero 2026 | Sistema de Inteligencia de Opinión Multidimensional v3.0.*
