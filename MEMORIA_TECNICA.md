# 📄 Memoria Técnica: Análisis de Reseñas E-commerce (Trustpilot)
## 💡 Monitor de Inteligencia de Opinión - Proyecto Híbrido Multidimensional v2.1

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

### 🤖 Fase 3: Predicción y Personalización (Fórmula Híbrida v2.1)
Se ha implementado una arquitectura de consenso para evitar la neutralización de scores y asegurar la diferenciación entre marcas:

#### **Fórmula de Consenso Equilibrada**
El sistema calcula el **Score Final** mediante una ponderación tripartita:
1.  **Puntuación Explícita (50%)**: Se deriva directamente de las estrellas (1-5) normalizadas al rango $[-1, 1]$. Es el núcleo de la veracidad del dato.
2.  **Análisis Semántico IR (30%)**: Basado en la similitud del coseno (Espacio Vectorial), ajustado por la **Autoridad del Revisor** (PageRank).
3.  **Filtrado Colaborativo (20%)**: Proporciona el componente de personalización y veracidad social mediante la Correlación de Pearson.

$$\text{Final Score} = (\text{Rating Score} \times 0.5) + (\text{Base Score} \times \text{Auth}_{norm} \times 0.3) + (\text{CF Pred} \times 0.2)$$

#### **Diferenciación de Marca**
Gracias a este re-equilibrio, el sistema detecta con precisión la brecha reputacional:
- **Dominios Críticos**: Marcas con promedios de 1.1 estrellas (ej. Amazon) muestran ahora perfiles claramente negativos, no contaminados por el "ruido léxico" común.
- **Dominios Saludables**: Marcas con valoraciones equilibradas mantienen sus KPIs positivos o neutrales según la realidad del dato.

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
