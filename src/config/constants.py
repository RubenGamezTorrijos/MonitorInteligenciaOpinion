# Professional Streamlit Opinion Intelligence Monitor - Constants

import os

# App Branding
APP_TITLE = "Monitor de Opinión Inteligente Trustpilot"
APP_SUBTITLE = "Professional Sentiment & Brand Analytics"
APP_ICON = "📊"
APP_VERSION = "3.0.3"

# Scraper Configuration
TRUSTPILOT_BASE_URL = "https://es.trustpilot.com/review/"
DEFAULT_DOMAIN = "amazon.es"
SCRAPE_MAX_REVIEWS = 50  # Increased for laboratory depth
SCRAPE_REVIEWS_PER_PAGE = 20

# Local Storage (Temporary)
DATA_DIR = "data"
ASSETS_DIR = "assets"

# Sentiment Settings
SENTIMENT_THRESHOLD_POSITIVE = 0.2
SENTIMENT_THRESHOLD_NEGATIVE = -0.2

# Export Filenames
CSV_RAW_SUFFIX = "_raw_scraped.csv"
CSV_PROCESSED_SUFFIX = "_processed.csv"
CSV_SENTIMENT_SUFFIX = "_sentiment_results.csv"
PNG_CHART_PREFIX = "chart_"
PDF_REPORT_SUFFIX = "_intelligence_report.pdf"
ZIP_PACKAGE_SUFFIX = "_complete_box.zip"

# UI Labels (ES)
TABS = ["📊 Resumen", "😊 Sentimiento", "☁️ Palabras Clave", "📈 Evolución", "🧠 Insights Pro", "📉 Correlación"]
SIDEBAR_HEADER = "⚙️ Panel de Control"
ANALYZE_BUTTON = "🚀 Iniciar Inteligencia de Opinión"

# Style Config
THEME_GLASSMORPHISM = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
</style>
"""
