# Professional Streamlit Opinion Intelligence Monitor - dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.config.constants import TABS

def render_dashboard(df: pd.DataFrame):
    """Orchestrates the rendering of horizontal tabs and their content."""
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar el dashboard.")
        return

    # Init figures storage
    if 'figures' not in st.session_state:
        st.session_state.figures = {}

    # Create Modern Horizontal Tabs
    tab_overview, tab_sentiment, tab_intel, tab_trends, tab_corr = st.tabs(TABS)
    
    with tab_overview:
        _render_overview_tab(df)
        
    with tab_sentiment:
        _render_sentiment_tab(df)
        
    with tab_intel:
        _render_intel_tab(df)
        
    with tab_trends:
        _render_trends_tab(df)
        
    with tab_corr:
        _render_corr_tab(df)

def _render_overview_tab(df: pd.DataFrame):
    st.subheader("📈 Resumen Ejecutivo")
    
    col1, col2, col3, col4 = st.columns(4)
    avg_score = df['sentimiento_score'].mean()
    total_reviews = len(df)
    pos_perc = (len(df[df['sentimiento'] == 'positivo']) / total_reviews) * 100
    
    col1.metric("Sentimiento Promedio", f"{avg_score:.2f}")
    col2.metric("Total Reseñas", total_reviews)
    col3.metric("% Positivo", f"{pos_perc:.1f}%")
    col4.metric("Confianza Media", f"{df['confianza'].mean():.1%}")
    
    st.markdown("---")
    
    # Category Distribution
    st.write("### 🏷️ Distribución por Categorías Temáticas")
    cat_counts = df['categoria_predom'].value_counts().reset_index()
    cat_counts.columns = ['Categoría', 'Cantidad']
    fig_cat = px.bar(cat_counts, x='Categoría', y='Cantidad', 
                    color='Categoría', color_discrete_sequence=px.colors.qualitative.Safe,
                    title="Temas recurrentes en opiniones")
    st.plotly_chart(fig_cat, use_container_width=True)
    st.session_state.figures['overview'] = fig_cat

    st.write("### 🔍 Muestra de Datos Analizados")
    st.dataframe(df[['text', 'sentimiento', 'categoria_predom', 'keywords']].head(10), use_container_width=True)

def _render_sentiment_tab(df: pd.DataFrame):
    st.subheader("😊 Análisis de Sentimiento")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_pie = px.pie(df, names='sentimiento', title='Polaridad Global (Donut)',
                    color='sentimiento', color_discrete_map={'positivo':'#00B4D8', 'negativo':'#FF6B6B', 'neutral':'#94A3B8'},
                    hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.session_state.figures['sentiment_pie'] = fig_pie
        
    with col2:
        fig_hist = px.histogram(df, x="sentimiento_score", nbins=20, title="Distribución de Intensidad (-1 a 1)",
                          color_discrete_sequence=['#00B4D8'], labels={'sentimiento_score':'Score de Sentimiento'})
        st.plotly_chart(fig_hist, use_container_width=True)
        st.session_state.figures['sentiment_hist'] = fig_hist

def _render_intel_tab(df: pd.DataFrame):
    st.subheader("☁️ Inteligencia de Palabras")
    
    all_tokens = [t for sublist in df['tokens'] for t in sublist]
    if all_tokens:
        word_freq = pd.Series(all_tokens).value_counts().head(20).reset_index()
        word_freq.columns = ['Palabra', 'Frecuencia']
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("### 🏆 Top 20 Palabras Clave")
            fig_words = px.bar(word_freq, y='Palabra', x='Frecuencia', orientation='h',
                        color='Frecuencia', color_continuous_scale='Blues')
            fig_words.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_words, use_container_width=True)
            st.session_state.figures['word_freq'] = fig_words
            
        with col2:
            st.write("### 💡 Insights de Extracción")
            st.info("Términos más recurrentes tras el vaciado de Stopwords (400+ términos).")
            st.dataframe(word_freq, use_container_width=True)
    else:
        st.warning("No hay suficientes datos para la analítica de palabras.")

def _render_trends_tab(df: pd.DataFrame):
    st.subheader("📈 Evolución Temporal")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df_trends = df.sort_values('date')
        fig_trends = px.line(df_trends, x='date', y='sentimiento_score', title="Tendencia de Sentimiento en el Tiempo",
                     color_discrete_sequence=['#00B4D8'], markers=True)
        fig_trends.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_trends, use_container_width=True)
        st.session_state.figures['trends'] = fig_trends
    else:
        st.error("No se detectaron datos temporales válidos.")

def _render_corr_tab(df: pd.DataFrame):
    st.subheader("📉 Análisis de Correlación")
    fig_corr = px.scatter(df, x="palabras_original", y="sentimiento_score", color="sentimiento", 
                    title="Relación: Longitud de Reseña vs Sentiment",
                    labels={'palabras_original': 'Número de Palabras', 'sentimiento_score': 'Sentimiento Score'},
                    color_discrete_map={'positivo':'#00B4D8', 'negativo':'#FF6B6B', 'neutral':'#94A3B8'})
    st.plotly_chart(fig_corr, use_container_width=True)
    st.session_state.figures['correlation'] = fig_corr
