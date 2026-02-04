# Professional Streamlit Opinion Intelligence Monitor - app.py (v3.1.0-DEPLOYMENT-FIX)

import streamlit as st
import pandas as pd
import os
import sys

# Diagnostic Print for Streamlit Cloud Logs
print("\n>>> STARTING MONITOR INTELLIGENCIA OPINION v3.1.2 (DEPLOYMENT FIXED) <<<")

import os
import sys

# Ensure the root directory is in sys.path for robust imports on Streamlit Cloud
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Internal Imports
from src.config.constants import APP_TITLE, APP_ICON, DATA_DIR, APP_SUBTITLE_TEMPLATE
from src.views.styles import apply_custom_styles
from src.views.sidebar import render_sidebar
from src.views.dashboard import render_dashboard
from src.services.scraper import TrustpilotScraper
from src.services.preprocessor import SpanishTextPreprocessor
from src.services.analyzer import SentimentAnalyzerES
from src.services.storage import ReviewRepository

# --- Optimized Service Helpers with Caching ---
# Removing cache for pipeline to ensure latest data is saved/loaded
# caching should happen at the data loading level if needed, but for now we want fresh save
def run_analysis_pipeline(domain: str, max_rev: int):
    """Pipeline with Persistence: Scrape -> Save -> Load History -> Analyze."""
    repo = ReviewRepository()
    
    # 1. Scraping (Try to get new data)
    scraper = TrustpilotScraper(domain)
    df_new = scraper.scrape_reviews(max_reviews=max_rev)
    
    # 2. Persistence (Save new data)
    new_count = 0
    if not df_new.empty:
        new_count = repo.save_reviews(domain, df_new)
        
    # 3. Load Cumulative History (The "Learning" Step)
    # We analyze the full history, not just the new batch
    df_history = repo.load_history(domain)
    
    if df_history.empty:
        return None
        
    # 4. Preprocessing (Dynamic Noise Filtering)
    # Apply to full history
    preprocessor = SpanishTextPreprocessor()
    # We re-process everything to ensure consistency (or we could store processed)
    # For now, re-processing ensures latest stopwords/logic are applied
    processed_results = [preprocessor.process_pipeline(text, domain=domain) for text in df_history['text']]
    df_proc = pd.DataFrame(processed_results)
    
    # Merge results
    df_merged = pd.concat([df_history.reset_index(drop=True), df_proc.drop(columns=['original'])], axis=1)
    
    # 5. Global Learning / Sentiment Analysis
    # In a full ML system, we would load a global model here. 
    # For now, TF-IDF fits on the specific domain history, which is "cumulative learning" for that domain.
    analyzer = SentimentAnalyzerES()
    
    # Optional: Load Global Corpus for better IDF (if performance allows)
    # global_corpus = repo.get_global_corpus() 
    # For now, we use the domain history as the "learning base" which is safer for performance
    # But to answer the user's request for "Global Learning", we can enable it:
    
    global_corpus = []
    # Only load global if we have enough data to make it worth it, or if user requested deep learning
    # For this implementation, we use the domain history + potential other domains
    # To be safe and fast, let's just use the df_merged text as the training set, 
    # but IF we want "Global", we would uncomment:
    # global_corpus = repo.get_global_corpus()
    
    # We pass the full history as the "corpus" to train on. 
    # The analyzer will use this to build the vocabulary and IDF.
    # Note: analyze_batch already uses the input df to build the index.
    # If we want to add *extra* context from other domains, we pass it as 'global_corpus'.
    # Let's try to get a broader context if available.
    extra_context = repo.get_global_corpus()
    # Filter out texts already in df_merged to avoid double counting if we were strict, 
    # but InvertedIndex with negative IDs handles separation.
    
    df_final = analyzer.analyze_batch(df_merged, global_corpus=extra_context)
    
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
    comp_dom = st.session_state.get('compare_domain_name', None)
    df_comp = st.session_state.get('df_comp', pd.DataFrame())
    
    display_text = active_dom
    if not df_comp.empty and comp_dom:
        display_text = f"{active_dom} ⚔️ {comp_dom}"
        
    st.markdown(APP_SUBTITLE_TEMPLATE.format(domains=f"`{display_text}`"))
    
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
