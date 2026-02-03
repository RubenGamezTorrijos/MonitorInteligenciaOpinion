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
from src.services.viz_engine import generate_authority_scatter, generate_refinement_comparison

def render_dashboard(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    """Orchestrates the rendering of horizontal tabs and their content."""
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar el dashboard.")
        return

    # Init figures storage
    if 'figures' not in st.session_state:
        st.session_state.figures = {}

    # Create Modern Horizontal Tabs
    tab_list = st.tabs(TABS)
    
    with tab_list[0]:
        _render_overview_tab(df)
        
    with tab_list[1]:
        _render_sentiment_tab(df)
        
    with tab_list[2]:
        _render_intel_tab(df)
        
    with tab_list[3]:
        _render_trends_tab(df)

    with tab_list[4]:
        _render_advanced_insights_tab(df)
        
    with tab_list[5]:
        _render_corr_tab(df)

    with tab_list[6]:
        if not df_comp.empty:
            _render_comparison_tab(df, df_comp)
        else:
            st.info("💡 **Tip:** Activa el 'Modo Comparativa' en el lateral para ver el benchmark entre dos marcas.")

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
                    color='Categoría', color_discrete_sequence=px.colors.qualitative.Prism,
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
                    color='sentimiento', color_discrete_map={'positivo':'#22c55e', 'negativo':'#ef4444', 'neutral':'#eab308'},
                    hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.session_state.figures['sentiment_pie'] = fig_pie
        
    with col2:
        fig_hist = px.histogram(df, x="sentimiento_score", nbins=20, title="Distribución de Intensidad (-1 a 1)",
                          color_discrete_sequence=['#22c55e'], labels={'sentimiento_score':'Score de Sentimiento'})
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
                          colormap='Greens', max_words=100).generate(text_for_cloud)
            
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
                        color='Frecuencia', color_continuous_scale='Greens')
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
                     color_discrete_sequence=['#22c55e'], markers=True)
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
                        color_discrete_map={'positivo':'#22c55e', 'negativo':'#ef4444', 'neutral':'#eab308'})
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
                            color_discrete_map={'Positivo':'#22c55e', 'Negativo':'#ef4444'})
        fig_drivers.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_drivers, use_container_width=True)
        st.session_state.figures['opinion_drivers'] = fig_drivers

    st.divider()
    st.write("### 🏗️ Arquitectura Híbrida y Veracidad del Modelo")
    
    col3, col4 = st.columns(2)
    with col3:
        st.info("📊 **Autoridad del Revisor (PageRank):** Muestra cómo el sistema pondera las reseñas basándose en la importancia de cada usuario en la red.")
        fig_auth = generate_authority_scatter(df)
        if fig_auth:
            st.pyplot(fig_auth)
            st.session_state.figures['authority_scatter'] = fig_auth
            
    with col4:
        st.info("🧪 **Refinamiento de Sentimiento:** Comparación entre el score base (TF-IDF) y el ajustado por Filtrado Colaborativo y Autoridad.")
        fig_refine = generate_refinement_comparison(df)
        if fig_refine:
            st.pyplot(fig_refine)
            st.session_state.figures['refinement_comparison'] = fig_refine

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

def _render_comparison_tab(df1: pd.DataFrame, df2: pd.DataFrame):
    dom1 = df1['domain'].iloc[0] if not df1.empty else "Marca 1"
    dom2 = df2['domain'].iloc[0] if not df2.empty else "Marca 2"
    
    st.subheader(f"⚔️ Benchmarking: {dom1} vs {dom2}")
    
    # 1. Comparative Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 🚩 KPI: {dom1}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Rating Medio", f"{df1['rating'].mean():.2f}")
        m2.metric("Sentimiento", f"{df1['sentimiento_score'].mean():.2f}")
        m3.metric("% Positivo", f"{(len(df1[df1['sentimiento']=='positivo'])/len(df1)):.1%}")

    with col2:
        st.write(f"### 🏁 KPI: {dom2}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Rating Medio", f"{df2['rating'].mean():.2f}")
        m2.metric("Sentimiento", f"{df2['sentimiento_score'].mean():.2f}")
        m3.metric("% Positivo", f"{(len(df2[df2['sentimiento']=='positivo'])/len(df2)):.1%}")

    st.divider()

    # 2. Visual Comparison
    st.write("### 📊 Distribución de Sentimiento Comparada")
    
    # Prepare data for comparison chart
    df1_dist = df1['sentimiento'].value_counts(normalize=True).reset_index()
    df1_dist.columns = ['Sentimiento', 'Proporción']
    df1_dist['Marca'] = dom1

    df2_dist = df2['sentimiento'].value_counts(normalize=True).reset_index()
    df2_dist.columns = ['Sentimiento', 'Proporción']
    df2_dist['Marca'] = dom2

    comp_df = pd.concat([df1_dist, df2_dist])

    fig_comp = px.bar(comp_df, x='Sentimiento', y='Proporción', color='Marca', barmode='group',
                     color_discrete_sequence=['#22c55e', '#636efa'],
                     title="Porcentaje de Sentimiento por Marca")
    st.plotly_chart(fig_comp, use_container_width=True)

    st.divider()

    # 3. Key Differences Table
    st.write("### 🔍 Análisis de Diferencias Críticas")
    
    # Simple word comparison
    tokens1 = set([t for sublist in df1['tokens'] for t in sublist])
    tokens2 = set([t for sublist in df2['tokens'] for t in sublist])
    
    unique1 = list(tokens1 - tokens2)[:10]
    unique2 = list(tokens2 - tokens1)[:10]
    
    diff_col1, diff_col2 = st.columns(2)
    with diff_col1:
        st.info(f"Temas únicos de **{dom1}**")
        st.write(", ".join(unique1))
    with diff_col2:
        st.info(f"Temas únicos de **{dom2}**")
        st.write(", ".join(unique2))

