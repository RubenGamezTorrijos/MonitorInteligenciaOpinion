# Professional Streamlit Opinion Intelligence Monitor - app.py
st.write("DEPLOY CHECK v3.0.0")

import streamlit as st
import pandas as pd
import os

# Internal Imports
from src.config.constants import APP_TITLE, APP_ICON, DATA_DIR
from src.views.styles import apply_custom_styles
from src.views.sidebar import render_sidebar
from src.views.dashboard import render_dashboard
from src.services.scraper import TrustpilotScraper
from src.services.preprocessor import SpanishTextPreprocessor
from src.services.analyzer import SentimentAnalyzerES

# --- Optimized Service Helpers with Caching ---
@st.cache_data(show_spinner=False)
def run_analysis_pipeline(domain: str, max_rev: int):
    """Cached pipeline to avoid redundant scraping and processing."""
    # 1. Scraping
    scraper = TrustpilotScraper(domain)
    df_raw = scraper.scrape_reviews(max_reviews=max_rev)
    
    if df_raw.empty:
        return None
        
    # 2. Preprocessing (Notebook Alignment)
    preprocessor = SpanishTextPreprocessor()
    processed_results = [preprocessor.process_pipeline(text) for text in df_raw['text']]
    df_proc = pd.DataFrame(processed_results)
    
    # Merge results (avoiding duplicate 'original' column)
    df_merged = pd.concat([df_raw, df_proc.drop(columns=['original'])], axis=1)
    
    # 3. Sentiment & Categorization Analysis
    analyzer = SentimentAnalyzerES()
    df_final = analyzer.analyze_batch(df_merged)
    
    return df_final

# Session State Initialization
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'data_ready' not in st.session_state:
    st.session_state.data_ready = False

def main():
    # Page Configuration
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
    
    # UI Styles
    apply_custom_styles()
    
    # Sidebar Navigation & Controls
    domain, max_rev, analyze_clicked = render_sidebar()
    
    # Analysis Execution
    if analyze_clicked:
        with st.spinner(f"🚀 Analizando {domain}..."):
            result_df = run_analysis_pipeline(domain, max_rev)
            if result_df is not None:
                st.session_state.df = result_df
                st.session_state.analyzed_domain = domain
                st.session_state.data_ready = True
                st.success(f"✅ Análisis completado para {domain}!")
            else:
                st.error("No se pudieron extraer reseñas. Verifica el dominio.")

    # Main Content Area
    st.title(f"{APP_ICON} {APP_TITLE}")
    active_dom = st.session_state.get('analyzed_domain', 'Ninguno')
    st.markdown(f"**Analítica Profesional de Reputación Online** | Dominio analizado: `{active_dom}`")
    
    if st.session_state.data_ready:
        render_dashboard(st.session_state.df)
    else:
        # Welcome Screen / Empty State
        st.info("👈 Introduce un dominio en el menú lateral e inicia el análisis.")
        
        # Performance/Architecture Note
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.markdown("### ⚡ Optimización\nUso de cache y procesamiento modular para máxima velocidad.")
        col2.markdown("### 🧩 Escalabilidad\nArquitectura de micro-servicios internos lista para producción.")
        col3.markdown("### 🔒 Privacidad\nExtracción segura y cumplimiento de políticas de visualización.")

if __name__ == "__main__":
    main()
