# Professional Streamlit Opinion Intelligence Monitor - app.py

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
    """Cached pipeline with dynamic brand noise filtering."""
    # 1. Scraping
    scraper = TrustpilotScraper(domain)
    df_raw = scraper.scrape_reviews(max_reviews=max_rev)
    
    if df_raw.empty:
        return None
        
    # 2. Preprocessing (Dynamic Noise Filtering)
    preprocessor = SpanishTextPreprocessor()
    processed_results = [preprocessor.process_pipeline(text, domain=domain) for text in df_raw['text']]
    df_proc = pd.DataFrame(processed_results)
    
    # Merge results
    df_merged = pd.concat([df_raw, df_proc.drop(columns=['original'])], axis=1)
    
    # 3. Sentiment & Categorization Analysis
    analyzer = SentimentAnalyzerES()
    df_final = analyzer.analyze_batch(df_merged)
    
    return df_final

# Session State Initialization
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'df_comp' not in st.session_state:
    st.session_state.df_comp = pd.DataFrame()
if 'data_ready' not in st.session_state:
    st.session_state.data_ready = False

def main():
    # Page Configuration
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
    
    # UI Styles
    apply_custom_styles()
    
    # Sidebar Navigation & Controls
    domain, max_rev, analyze_clicked, compare_mode, compare_domain = render_sidebar()
    
    # Analysis Execution
    if analyze_clicked:
        with st.spinner(f"🚀 Analizando {domain}..."):
            result_df = run_analysis_pipeline(domain, max_rev)
            if result_df is not None:
                st.session_state.df = result_df
                st.session_state.analyzed_domain = domain
                st.session_state.data_ready = True
                
                # Comparison mode
                if compare_mode and compare_domain:
                    with st.spinner(f"⚔️ Comparando con {compare_domain}..."):
                        st.session_state.df_comp = run_analysis_pipeline(compare_domain, max_rev)
                        st.session_state.compare_domain_name = compare_domain
                else:
                    st.session_state.df_comp = pd.DataFrame()
                    
                st.success(f"✅ Análisis completado!")
            else:
                st.error("No se pudieron extraer reseñas. Verifica el dominio principal.")

    # Main Content Area
    st.title(f"{APP_ICON} {APP_TITLE}")
    active_dom = st.session_state.get('analyzed_domain', 'Ninguno')
    st.markdown(f"**Analítica Profesional de Reputación Online** | Dominio analizado: `{active_dom}`")
    
    if st.session_state.data_ready:
        render_dashboard(st.session_state.df, st.session_state.df_comp)
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
