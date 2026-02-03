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
from src.services.viz_engine import generate_authority_scatter, generate_refinement_comparison, generate_time_series_comparison

def render_dashboard(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    """Orchestrates the rendering of horizontal tabs and their content."""
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar el dashboard.")
        return

    # Init figures storage
    if 'figures' not in st.session_state:
        st.session_state.figures = {}

    # Dynamic Tabs Configuration
    final_tabs = TABS.copy()
    if df_comp.empty:
        if "⚔️ Comparativa" in final_tabs:
            final_tabs.remove("⚔️ Comparativa")
            
    tab_list = st.tabs(final_tabs)
    
    # 1. Overview
    with tab_list[0]:
        _render_overview_tab(df, df_comp)
        
    # 2. Sentiment
    with tab_list[1]:
        _render_sentiment_tab(df, df_comp)
        
    # 3. Intel
    with tab_list[2]:
        _render_intel_tab(df, df_comp)
        
    # 4. Trends
    with tab_list[3]:
        _render_trends_tab(df, df_comp)
        
    # 5. Advanced Insights
    with tab_list[4]:
        _render_advanced_insights_tab(df, df_comp)
        
    # 6. Correlation
    with tab_list[5]:
        _render_corr_tab(df, df_comp)
        
    # 7. Comparison (Only if active)
    if not df_comp.empty and len(tab_list) > 6:
        with tab_list[6]:
            _render_comparison_tab(df, df_comp)

def _render_overview_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("📈 Resumen Ejecutivo")
    
    # helper to render metrics
    def render_row(d, label):
        c_dom, c1, c2, c3, c4 = st.columns([2, 2, 2, 2, 2])
        avg_score = d['sentimiento_score'].mean()
        total_reviews = len(d)
        pos_perc = (len(d[d['sentimiento'] == 'positivo']) / total_reviews) * 100
        
        with c_dom:
            st.markdown(f"### 🏷️ {label}")
            st.caption("Dominio Analizado")
            
        c1.metric("Sentimiento", f"{avg_score:.2f}")
        c2.metric("Total Reseñas", total_reviews)
        c3.metric("% Positivo", f"{pos_perc:.1f}%")
        c4.metric("Confianza", f"{d['confianza'].mean():.1%}")

    if not df_comp.empty:
        nom1 = df['domain'].iloc[0]
        nom2 = df_comp['domain'].iloc[0]
        
        # Row 1: Main Domain
        st.markdown(f"##### 🟦 Dominio Principal")
        render_row(df, nom1)
        st.divider()
        
        # Row 2: Comparison Domain
        st.markdown(f"##### 🟧 Comparativa")
        render_row(df_comp, nom2)
        
    else:
        # Single mode: Standard Layout
        render_row(df, df['domain'].iloc[0])
    
    st.markdown("---")
    st.write("### 🏷️ Distribución por Temas")

    def get_cat_fig(d, title, color_seq):
        cat_counts = d['categoria_predom'].value_counts().reset_index()
        cat_counts.columns = ['Categoría', 'Cantidad']
        return px.bar(cat_counts, x='Categoría', y='Cantidad', 
                     color='Categoría', color_discrete_sequence=color_seq,
                     title=title)

    if not df_comp.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{df['domain'].iloc[0]}**")
            st.plotly_chart(get_cat_fig(df, "", px.colors.qualitative.Prism), use_container_width=True)
        with c2:
            st.markdown(f"**{df_comp['domain'].iloc[0]}**")
            st.plotly_chart(get_cat_fig(df_comp, "", px.colors.qualitative.Pastel), use_container_width=True)
    else:
        fig_cat = get_cat_fig(df, "Temas recurrentes", px.colors.qualitative.Prism)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.session_state.figures['overview'] = fig_cat

    if df_comp.empty:
        st.write("### 🔍 Muestra de Datos")
        st.dataframe(df[['text', 'sentimiento', 'categoria_predom', 'keywords']].head(5), use_container_width=True)

def _render_sentiment_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("😊 Análisis de Sentimiento")
    
    if not df_comp.empty:
        # Comparative View
        # Row 1: Donut Charts Side-by-Side with headers
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🟦 {df['domain'].iloc[0]}")
            fig_pie1 = px.pie(df, names='sentimiento', 
                        color='sentimiento', color_discrete_map={'positivo':'#22c55e', 'negativo':'#ef4444', 'neutral':'#eab308'},
                        hole=0.4)
            st.plotly_chart(fig_pie1, use_container_width=True)
            
        with c2:
            st.markdown(f"#### 🟧 {df_comp['domain'].iloc[0]}")
            fig_pie2 = px.pie(df_comp, names='sentimiento', 
                        color='sentimiento', color_discrete_map={'positivo':'#22c55e', 'negativo':'#ef4444', 'neutral':'#eab308'},
                        hole=0.4)
            st.plotly_chart(fig_pie2, use_container_width=True)

        st.divider()
        st.write("### 📊 Intensidad Emocional Comparada")
        
        # Overlay histograms (Scipy-free version)
        import plotly.graph_objects as go
        
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(x=df['sentimiento_score'], name=df['domain'].iloc[0], 
                                      marker_color='#22c55e', opacity=0.75))
        fig_dist.add_trace(go.Histogram(x=df_comp['sentimiento_score'], name=df_comp['domain'].iloc[0], 
                                      marker_color='#f97316', opacity=0.75))
        
        fig_dist.update_layout(barmode='overlay', title="Distribución de Sentimiento (Superpuesta)",
                             xaxis_title="Score de Sentimiento", yaxis_title="Frecuencia")
        st.plotly_chart(fig_dist, use_container_width=True)
        
    else:
        # Standard Single View
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

def _render_intel_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("☁️ Inteligencia de Palabras")
    
    # Helper for WordCloud
    def render_cloud(d, title):
        all_tokens = [t for sublist in d['tokens'] for t in sublist]
        if all_tokens:
            text_for_cloud = " ".join(all_tokens)
            wc = WordCloud(width=800, height=400, background_color='white', 
                          colormap='Greens', max_words=100).generate(text_for_cloud)
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(title)
            st.pyplot(fig_wc)
        else:
            st.info(f"Sin datos para {title}")

    if not df_comp.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🟦 {df['domain'].iloc[0]}")
            render_cloud(df, "Palabras Clave")
        with c2:
            st.markdown(f"#### 🟧 {df_comp['domain'].iloc[0]}")
            render_cloud(df_comp, "Palabras Clave")
    else:
        # Standard Single View
        all_tokens = [t for sublist in df['tokens'] for t in sublist]
        if all_tokens:
            word_freq = pd.Series(all_tokens).value_counts().head(20).reset_index()
            word_freq.columns = ['Palabra', 'Frecuencia']
            
            st.write("### ☁️ Nube de Palabras (WordCloud)")
            text_for_cloud = " ".join(all_tokens)
            if text_for_cloud:
                wc = WordCloud(width=1200, height=500, background_color='white', 
                              colormap='Greens', max_words=100).generate(text_for_cloud)
                
                fig_wc, ax = plt.subplots(figsize=(15, 6))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig_wc)
                text_for_cloud = " ".join(all_tokens)
            
            st.divider()
    
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

def _render_trends_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("📈 Evolución Temporal")
    
    if not df_comp.empty:
        nom1 = df['domain'].iloc[0]
        nom2 = df_comp['domain'].iloc[0]
        st.markdown(f"#### 🆚 Comparativa: **{nom1}** vs **{nom2}**")
        
        # Use new comparative viz function
        fig_evol = generate_time_series_comparison(df, df_comp, nom1, nom2)
        if fig_evol:
            st.pyplot(fig_evol)
        else:
            st.warning("No se pudieron generar las series temporales comparadas.")
            
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df_trends = df.sort_values('date')
        fig_trends = px.line(df_trends, x='date', y='sentimiento_score', title="Tendencia de Sentimiento en el Tiempo",
                     color_discrete_sequence=['#22c55e'], markers=True)
        fig_trends.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_trends, use_container_width=True)
        st.session_state.figures['trends'] = fig_trends
    else:
        st.error("No se detectaron datos temporales válidos.")

def _render_advanced_insights_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("🧠 Análisis de Insights Avanzados")
    
    if not df_comp.empty:
        st.info("⚠️ Mostrando insights comparativos simplificados")
        nom1 = df['domain'].iloc[0]
        nom2 = df_comp['domain'].iloc[0]
        
        # 1. Authority Scatter Comparison
        st.write(f"### 📊 Autoridad del Revisor: {nom1} vs {nom2}")
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"Autoridad: {nom1}")
            fig1 = generate_authority_scatter(df)
            if fig1: st.pyplot(fig1)
        with c2:
            st.caption(f"Autoridad: {nom2}")
            fig2 = generate_authority_scatter(df_comp)
            if fig2: st.pyplot(fig2)
            
        st.divider()
        
        # 2. Refinement Comparison
        st.write(f"### 🧪 Efecto del Refinamiento Híbrido")
        c3, c4 = st.columns(2)
        with c3:
            fig_ref1 = generate_refinement_comparison(df)
            if fig_ref1: st.pyplot(fig_ref1)
        with c4:
            fig_ref2 = generate_refinement_comparison(df_comp)
            if fig_ref2: st.pyplot(fig_ref2)
            
    else:
        # Standard Single View
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
        st.write("### 🤖 Asesor Estratégico (AI-Driven)")
        
        from src.services.advisor import StrategicAdvisor
        advisor = StrategicAdvisor()
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown(f"#### 💡 Recomendaciones para {df['domain'].iloc[0]}")
            insights = advisor.generate_strategic_report(df)
            for insight in insights:
                st.warning(f"**{insight['area']}**: {insight['action']}")
                st.caption(insight['detail'])
                
        with col_adv2:
            if not df_comp.empty:
                st.markdown(f"#### 💡 Recomendaciones para {df_comp['domain'].iloc[0]}")
                insights_comp = advisor.generate_strategic_report(df_comp)
                for insight in insights_comp:
                    st.warning(f"**{insight['area']}**: {insight['action']}")
                    st.caption(insight['detail'])
            else:
                st.info("Añade un competidor para ver recomendaciones comparadas.")

        st.divider()
        st.write("### 🗣️ Consenso de Opinión (Frases Recurrentes)")
        st.caption("Patrones verbales de 3 palabras más repetidos (Trigramas)")
        
        from src.services.preprocessor import SpanishTextPreprocessor
        pre = SpanishTextPreprocessor()
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown(f"**{df['domain'].iloc[0]}** - Patrones")
            phrases = pre.extract_common_phrases(df['text'], n=3, top_k=5)
            for p, count in phrases:
                st.write(f"- *'{p}'* ({count} veces)")
                
        with c_p2:
            if not df_comp.empty:
                st.markdown(f"**{df_comp['domain'].iloc[0]}** - Patrones")
                phrases_comp = pre.extract_common_phrases(df_comp['text'], n=3, top_k=5)
                for p, count in phrases_comp:
                    st.write(f"- *'{p}'* ({count} veces)")
                    
        st.divider()
        st.write("### 🛡️ Veracidad de la Información (User Authority)")
        st.info("Métrica basada en PageRank: Evalúa la credibilidad de los autores basada en su historial e impacto.")
        
        av1 = df['authority_level'].mean()
        delta_val = None
        if not df_comp.empty:
            av2 = df_comp['authority_level'].mean()
            delta_val = av1 - av2
            
        st.metric(label=f"Índice de Veracidad Promedio ({df['domain'].iloc[0]})", value=f"{av1:.2f}", delta=f"{delta_val:.2f}" if delta_val else None)
        
        fig_auth = generate_authority_scatter(df)
        if fig_auth: st.pyplot(fig_auth)

def _render_corr_tab(df: pd.DataFrame, df_comp: pd.DataFrame = pd.DataFrame()):
    st.subheader("📉 Matriz de Correlación")
    
    if not df_comp.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### 🟦 {df['domain'].iloc[0]}")
            _plot_correlation(df)
        with col2:
            st.markdown(f"#### 🟧 {df_comp['domain'].iloc[0]}")
            _plot_correlation(df_comp)
    else:
        _plot_correlation(df)

def _plot_correlation(df_in: pd.DataFrame):
    """Helper to plot correlation matrix for a given dataframe."""
    # Select numeric columns for correlation
    numeric_cols = df_in.select_dtypes(include=[np.number]).columns.tolist()
    # Filter columns that are relevant
    relevant_cols = [c for c in numeric_cols if c in ['sentimiento_score', 'confianza', 'palabras_original', 'palabras_limpias', 'rating_score', 'user_authority']]
    
    if len(relevant_cols) > 1:
        corr_matrix = df_in[relevant_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hoverongaps = False))
        
        fig_corr.update_layout(title=f"Matriz de Correlación: {df_in['domain'].iloc[0] if not df_in.empty else ''}")
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning(f"No hay suficientes variables numéricas para realizar la matriz en {df_in['domain'].iloc[0] if not df_in.empty else 'dominio'}.")

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

