import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
from wordcloud import WordCloud

def generate_sentiment_pie(df):
    counts = df['sentimiento'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'positivo': '#22c55e', 'neutral': '#eab308', 'negativo': '#ef4444'}
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', 
           colors=[colors.get(x, '#cbd5e1') for x in counts.index],
           startangle=140, explode=[0.05]*len(counts))
    ax.set_title("Distribución de Sentimiento")
    return fig

def generate_category_chart(df):
    counts = df['categoria_predom'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values, palette='Greens_d', ax=ax)
    ax.set_title("Temas recurrentes en opiniones")
    ax.set_ylabel("Cantidad")
    plt.xticks(rotation=45)
    return fig

def generate_sentiment_hist(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df['sentimiento_score'], bins=20, kde=True, color='#22c55e', ax=ax)
    ax.set_title("Distribución de Intensidad de Sentimiento")
    ax.set_xlabel("Score de Sentimiento (-1 a 1)")
    return fig

def generate_word_freq_chart(df):
    from collections import Counter
    import re
    
    # Simple extraction for fallback
    all_text = " ".join(df['texto_limpio'].fillna('').astype(str))
    tokens = [t for t in all_text.split() if len(t) > 2]
    word_freq = pd.Series(tokens).value_counts().head(20).reset_index()
    word_freq.columns = ['Palabra', 'Frecuencia']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=word_freq, x='Frecuencia', y='Palabra', palette='Greens_r', ax=ax)
    ax.set_title("Top 20 Palabras Clave")
    return fig

def generate_evolution_chart(df):
    df_ev = df.copy()
    if 'date' not in df_ev.columns:
        return None
        
    df_ev['date'] = pd.to_datetime(df_ev['date'])
    df_ev = df_ev.set_index('date').resample('D')['sentimiento_score'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_ev['date'], df_ev['sentimiento_score'], marker='o', linestyle='-', color='#16a34a')
    ax.fill_between(df_ev['date'], df_ev['sentimiento_score'], alpha=0.2, color='#22c55e')
    ax.set_title("Evolución del Sentimiento Score")
    ax.set_ylim(-1.1, 1.1)
    plt.xticks(rotation=45)
    return fig

def generate_boxplot_insight(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='sentimiento', y='palabras_limpias', palette={'positivo':'#22c55e', 'negativo':'#ef4444', 'neutral':'#eab308'}, ax=ax)
    ax.set_title("Longitud de Reseña por Sentimiento")
    return fig

def generate_correlation_heatmap(df):
    numeric_cols = ['sentimiento_score', 'confianza', 'palabras_original', 'palabras_limpias']
    cols = [c for c in numeric_cols if c in df.columns]
    
    if len(cols) > 1:
        corr = df[cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='PRGn', center=0, ax=ax)
        ax.set_title("Matriz de Correlación")
        return fig
    return None

def generate_wordcloud_static(df):
    all_text = " ".join(df['texto_limpio'].fillna('').astype(str))
    if not all_text.strip(): return None
    
    wc = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Nube de Palabras")
    return fig

def generate_drivers_chart(df):
    pos_tokens = [t for sublist in df[df['sentimiento'] == 'positivo']['tokens'] for t in sublist]
    neg_tokens = [t for sublist in df[df['sentimiento'] == 'negativo']['tokens'] for t in sublist]
    
    pos_freq = pd.Series(pos_tokens).value_counts().head(10)
    neg_freq = pd.Series(neg_tokens).value_counts().head(10)
    
    comparison_df = pd.DataFrame({
        'Palabra': list(pos_freq.index) + list(neg_freq.index),
        'Frecuencia': list(pos_freq.values) + [-v for v in neg_freq.values],
        'Sentimiento': ['Positivo']*len(pos_freq) + ['Negativo']*len(neg_freq)
    })
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=comparison_df, x='Frecuencia', y='Palabra', hue='Sentimiento', 
                dodge=False, palette={'Positivo':'#22c55e', 'Negativo':'#ef4444'}, ax=ax)
    ax.set_title("Top Drivers (Frecuencia Comparada)")
    ax.axvline(0, color='black', linewidth=0.8)
    return fig

def generate_authority_scatter(df):
    """Shows the relationship between user authority and sentiment intensity."""
    if 'authority_level' not in df.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    sc = ax.scatter(df['sentimiento_score'], df['authority_level'], 
                    alpha=0.6, c=df['sentimiento_score'], cmap='RdYlGn')
    ax.set_title("Nivel de Autoridad vs. Intensidad de Sentimiento")
    ax.set_xlabel("Score de Sentimiento")
    ax.set_ylabel("Nivel de Autoridad (Normalizado)")
    plt.colorbar(sc, ax=ax, label="Sentimiento")
    return fig

def generate_refinement_comparison(df):
    """Compares base TF-IDF score with final hybrid score."""
    if 'base_score' not in df.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    samples = df.head(15) # Show first 15 for clarity
    x = np.arange(len(samples))
    width = 0.35
    
    ax.bar(x - width/2, samples['base_score'], width, label='Base (TF-IDF)', color='#94a3b8')
    ax.bar(x + width/2, samples['sentimiento_score'], width, label='Final (Híbrido)', color='#16a34a')
    
    ax.set_title("Efecto del Refinamiento Multidimensional (Personalización)")
    ax.set_ylabel("Score")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Reseña {i+1}" for i in x], rotation=45)
    ax.legend()
    return fig
