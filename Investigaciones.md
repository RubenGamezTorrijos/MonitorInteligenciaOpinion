## Investigación de bibliotecas de Web Scraping ##

El web scraping es una técnica fundamental para la adquisición automática de datos desde páginas web. En este proyecto se ha evaluado el uso de distintas bibliotecas de Python para la extracción de opiniones desde sitios web públicos, como Amazon España.

# BeautifulSoup

BeautifulSoup es una librería de parsing HTML/XML que permite navegar, buscar y extraer información de documentos web de forma sencilla.

- Ventajas:

Fácil de aprender y usar.

Ideal para proyectos académicos y scraping sencillo.

Funciona bien con páginas HTML estáticas.

Gran comunidad y documentación.

- Desventajas:

No ejecuta JavaScript.

No está pensada para scraping masivo o concurrente.

# Selenium

Selenium es una herramienta de automatización de navegadores que permite interactuar con páginas web dinámicas que dependen de JavaScript.

- Ventajas:

Permite renderizar JavaScript.

Simula la interacción de un usuario real.

Útil para webs complejas y protegidas.

- Desventajas:

Mucho más lenta que BeautifulSoup.

Mayor consumo de recursos.

Configuración más compleja (drivers, navegadores).

# Scrapy

Scrapy es un framework completo de scraping orientado a proyectos grandes y escalables.

- Ventajas:

Muy eficiente y rápido.

Manejo automático de peticiones y pipelines.

Ideal para scraping a gran escala.

- Desventajas:

Curva de aprendizaje más elevada.

Excesivo para proyectos pequeños o académicos.

## Investigación de librerías NLP ##

El procesamiento de lenguaje natural (NLP) permite analizar y transformar texto para extraer información relevante. Se han analizado las principales librerías de NLP en Python para seleccionar las más adecuadas al proyecto.

# NLTK (Natural Language Toolkit)

NLTK es una de las librerías de NLP más antiguas y utilizadas en el ámbito académico.

- Ventajas:

Amplia colección de herramientas NLP.

Soporte para tokenización, stopwords, stemming.

Ideal para aprendizaje y experimentación.

Excelente soporte para español.

- Desventajas:

Menos eficiente que librerías modernas.

Requiere descargas manuales de recursos.

# spaCy

spaCy es una librería moderna orientada a rendimiento y aplicaciones en producción.

Ventajas:

Muy rápida y eficiente.

Modelos preentrenados.

Ideal para proyectos industriales.

Desventajas:

Mayor complejidad.

Menor flexibilidad para aprendizaje básico.

Requiere más recursos.

# TextBlob

TextBlob es una librería de alto nivel orientada a facilitar tareas comunes de NLP, como el análisis de sentimiento.

Ventajas:

Muy fácil de usar.

API sencilla para análisis de sentimiento.

Ideal para prototipos rápidos.

Desventajas:

Menos configurable.

Resultados más genéricos.

## Investigación de librerías de visualización ##

La visualización de datos es clave para transformar resultados técnicos en información comprensible para usuarios no técnicos.

# Matplotlib

Matplotlib es la librería base de visualización en Python.

- Ventajas:

Muy flexible.

Control total sobre los gráficos.

Base de muchas otras librerías.

- Desventajas:

Sintaxis más extensa.

Menos estética por defecto.

🔹 Seaborn

Seaborn es una librería construida sobre Matplotlib, orientada a visualizaciones estadísticas.

- Ventajas:

Gráficos más estéticos.

Integración directa con pandas.

Ideal para análisis exploratorio y BI.

- Desventajas:

Menos control fino que Matplotlib.

🔹 WordCloud

WordCloud permite generar nubes de palabras basadas en la frecuencia de términos.

- Ventajas:

Visualización intuitiva.

Muy útil para análisis textual.

Fácil interpretación por usuarios no técnicos.

- Desventajas:

No cuantitativa por sí sola.

Requiere preprocesamiento previo.

#----- CONCLUSIÓN GENERAL-----#

Las tecnologías seleccionadas permiten construir un sistema completo de monitorización de opinión, desde la adquisición de datos hasta la visualización final, equilibrando simplicidad, potencia analítica y claridad conceptual.