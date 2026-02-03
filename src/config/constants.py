# Professional Streamlit Opinion Intelligence Monitor - Constants

import os

# App Branding
APP_TITLE = "Monitor de Opinión Inteligente Trustpilot"
APP_SUBTITLE = "Professional Sentiment & Brand Analytics"
APP_ICON = "📊"
APP_VERSION = "3.0.6"
APP_SUBTITLE_TEMPLATE = "Analítica Profesional de Reputación Online | Dominio analizado: {domains}"

# Scraper Configuration
TRUSTPILOT_BASE_URL = "https://es.trustpilot.com/review/"
DEFAULT_DOMAIN = "dominio.com"
DEFAULT_COMPARE_DOMAIN = "competencia.com"
SCRAPE_MAX_REVIEWS = 50  # Increased for laboratory depth
SCRAPE_REVIEWS_PER_PAGE = 20

# CSS Selectors (Maintenance)
TRUSTPILOT_SELECTORS = {
    'review_card': [
        'article[data-service-review-card-paper="true"]',
        'article[data-service-review]',
        'div.review-card'
    ],
    'text': [
        'p[data-service-review-text-typography="true"]',
        'p[data-relevant-review-text-typography="true"]',
        'p[data-review-content-typography="true"]'
    ],
    'user': [
        'span[data-consumer-name-typography="true"]',
        'div[data-consumer-name-typography="true"]',
        'span.typography_appearance-default__D9m_F.typography_color-inherit__D_i_t'
    ],
    'date': ['time', 'span[data-service-review-date-time-ago]', 'div.review-date']
}

# Local Storage (Temporary)
DATA_DIR = "data"
ASSETS_DIR = "assets"

# Sentiment Settings
SENTIMENT_THRESHOLD_POSITIVE = 0.1
SENTIMENT_THRESHOLD_NEGATIVE = -0.1

# Export Filenames
CSV_RAW_SUFFIX = "_raw_scraped.csv"
CSV_PROCESSED_SUFFIX = "_processed.csv"
CSV_SENTIMENT_SUFFIX = "_sentiment_results.csv"
PNG_CHART_PREFIX = "chart_"
PDF_REPORT_SUFFIX = "_intelligence_report.pdf"
ZIP_PACKAGE_SUFFIX = "_complete_box.zip"

# UI Labels (ES)
TABS = ["📊 Resumen", "😊 Sentimiento", "☁️ Palabras Clave", "📈 Evolución", "🧠 Insights Pro", "📉 Correlación", "⚔️ Comparativa"]
SIDEBAR_HEADER = "⚙️ Panel de Control"
ANALYZE_BUTTON = "🚀 Iniciar Análisis"

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
