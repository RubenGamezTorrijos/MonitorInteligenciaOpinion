# Professional Streamlit Opinion Intelligence Monitor - dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import seaborn as sns
import io
from src.config.constants import TABS, SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE

def render_dashboard(df: pd.DataFrame):
    """Orchestrates the rendering of horizontal tabs and their content."""
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar el dashboard.")
        return

    # Init figures storage
    if 'figures' not in st.session_state:
        st.session_state.figures = {}

    # Create Modern Horizontal Tabs
    tab_overview, tab_sentiment, tab_intel, tab_trends, tab_insights, tab_corr = st.tabs(TABS)
    
    with tab_overview:
        _render_overview_tab(df)
        
    with tab_sentiment:
        _render_sentiment_tab(df)
        
    with tab_intel:
        _render_intel_tab(df)
        
    with tab_trends:
        _render_trends_tab(df)

    with tab_insights:
        _render_advanced_insights_tab(df)
        
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
        
        # 1. WordCloud (Full Width)
        st.write("### ☁️ Nube de Palabras (WordCloud)")
        text_for_cloud = " ".join(all_tokens)
        if text_for_cloud:
            wc = WordCloud(width=1200, height=500, background_color='white', 
                          colormap='Blues', max_words=100).generate(text_for_cloud)
            
            fig_wc, ax = plt.subplots(figsize=(15, 6))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)
            st.session_state.figures['wordcloud'] = fig_wc
        else:
            st.info("No hay palabras suficientes para generar la nube.")
        
        st.divider()

        # 2. Key Metrics & Table (Two Columns Below)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write("### 🏆 Top 20 Palabras Clave")
            fig_words = px.bar(word_freq, y='Palabra', x='Frecuencia', orientation='h',
                        color='Frecuencia', color_continuous_scale='Blues')
            fig_words.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_words, use_container_width=True)
            st.session_state.figures['word_freq'] = fig_words
            
        with col2:
            st.write("### 💡 Datos de Extracción")
            st.info("Términos más recurrentes tras el filtrado profundo de Stopwords.")
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

def _render_advanced_insights_tab(df: pd.DataFrame):
    st.subheader("🧠 Análisis de Insights Avanzados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📏 Distribución de Longitud por Sentimiento")
        fig_box = px.box(df, x="sentimiento", y="palabras_original", color="sentimiento",
                        title="Boxplot: Longitud de Reseña vs Sentimiento",
                        color_discrete_map={'positivo':'#00B4D8', 'negativo':'#FF6B6B', 'neutral':'#94A3B8'})
        st.plotly_chart(fig_box, use_container_width=True)
        st.session_state.figures['boxplot_length'] = fig_box

    with col2:
        st.write("### 🎯 Drivers de Opinión: Positivo vs Negativo")
        # Extract keywords for positive and negative
        pos_tokens = [t for sublist in df[df['sentimiento'] == 'positivo']['tokens'] for t in sublist]
        neg_tokens = [t for sublist in df[df['sentimiento'] == 'negativo']['tokens'] for t in sublist]
        
        pos_freq = pd.Series(pos_tokens).value_counts().head(10)
        neg_freq = pd.Series(neg_tokens).value_counts().head(10)
        
        # Create a comparison dataframe
        comparison_df = pd.DataFrame({
            'Palabra': list(pos_freq.index) + list(neg_freq.index),
            'Frecuencia': list(pos_freq.values) + [-v for v in neg_freq.values],
            'Sentimiento': ['Positivo']*len(pos_freq) + ['Negativo']*len(neg_freq)
        })
        
        fig_drivers = px.bar(comparison_df, x='Frecuencia', y='Palabra', color='Sentimiento',
                            orientation='h', title="Top Drivers (Frecuencia Comparada)",
                            color_discrete_map={'Positivo':'#00B4D8', 'Negativo':'#FF6B6B'})
        fig_drivers.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_drivers, use_container_width=True)
        st.session_state.figures['opinion_drivers'] = fig_drivers

def _render_corr_tab(df: pd.DataFrame):
    st.subheader("📉 Matriz de Correlación")
    
    # Select numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Filter columns that are relevant
    relevant_cols = [c for c in numeric_cols if c in ['sentimiento_score', 'confianza', 'palabras_original', 'palabras_limpias']]
    
    if len(relevant_cols) > 1:
        corr_matrix = df[relevant_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hoverongaps = False))
        
        fig_corr.update_layout(title="Mapa de Calor de Correlaciones Numéricas")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.session_state.figures['correlation_matrix'] = fig_corr
        
        st.markdown("""
        **Guía de Interpretación:**
        - **1.0**: Correlación positiva perfecta.
        - **-1.0**: Correlación negativa perfecta.
        - **0.0**: Ausencia de correlación lineal.
        """)
    else:
        st.warning("No hay suficientes variables numéricas para realizar la matriz de correlación.")

