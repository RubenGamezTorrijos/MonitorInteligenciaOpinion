import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

def generate_sentiment_pie(df):
    counts = df['sentimiento'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    # Standard Sentiment Colors
    colors_map = {
        'positivo': '#22c55e', 
        'neutral': '#eab308', 
        'negativo': '#ef4444'
    }
    
    chart_colors = [colors_map.get(str(x).lower(), '#cbd5e1') for x in counts.index]
    
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', 
           colors=chart_colors,
           startangle=140, explode=[0.05]*len(counts))
    ax.set_title("Distribución de Sentimiento")
    return fig

def generate_category_chart(df):
    counts = df['categoria_predom'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    # Using a professional palette that doesn't conflict with sentiment colors
    sns.barplot(x=counts.index, y=counts.values, palette='viridis', ax=ax)
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
    all_text = " ".join(df['texto_limpio'].fillna('').astype(str))
    tokens = [t for t in all_text.split() if len(t) > 2]
    if not tokens: return None
    
    word_freq = pd.Series(tokens).value_counts().head(20).reset_index()
    word_freq.columns = ['Palabra', 'Frecuencia']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Matching dashboard's Greens scale
    sns.barplot(data=word_freq, x='Frecuencia', y='Palabra', palette='Greens_r', ax=ax)
    ax.set_title("Top 20 Palabras Clave")
    return fig

def generate_evolution_chart(df):
    df_ev = df.copy()
    if 'date' not in df_ev.columns:
        return None
        
    df_ev['date'] = pd.to_datetime(df_ev['date'])
    df_ev = df_ev.set_index('date').sort_index()
    df_ev = df_ev.resample('D')['sentimiento_score'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_ev['date'], df_ev['sentimiento_score'], marker='o', linestyle='-', color='#22c55e')
    ax.fill_between(df_ev['date'], df_ev['sentimiento_score'], alpha=0.2, color='#22c55e')
    ax.set_title("Evolución del Sentimiento Score")
    ax.set_ylim(-1.1, 1.1)
    plt.xticks(rotation=45)
    return fig

def generate_boxplot_insight(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_map = {
        'positivo': '#22c55e', 
        'neutral': '#eab308', 
        'negativo': '#ef4444'
    }
    sns.boxplot(data=df, x='sentimiento', y='palabras_limpias', 
                palette=colors_map, ax=ax)
    ax.set_title("Longitud de Reseña por Sentimiento")
    return fig

def generate_correlation_heatmap(df):
    numeric_cols = ['sentimiento_score', 'confianza', 'palabras_original', 'palabras_limpias']
    cols = [c for c in numeric_cols if c in df.columns]
    
    if len(cols) > 1:
        # Avoid NaN errors by dropping constant columns
        df_corr = df[cols].copy()
        valid_cols = [c for c in cols if df_corr[c].std() > 0]
        
        if len(valid_cols) > 1:
            corr = df_corr[valid_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, ax=ax)
            ax.set_title("Matriz de Correlación")
            return fig
    return None

def generate_wordcloud_static(df):
    """Generates a wordcloud with colors based on the average sentiment of each word."""
    all_tokens_reviews = []
    for _, row in df.iterrows():
        tokens = row.get('tokens', [])
        score = row.get('sentimiento_score', 0)
        for t in tokens:
            all_tokens_reviews.append((t, score))
            
    if not all_tokens_reviews: return None
    
    # Calculate average sentiment per word
    word_scores = {}
    word_counts = {}
    for word, score in all_tokens_reviews:
        word_scores[word] = word_scores.get(word, 0) + score
        word_counts[word] = word_counts.get(word, 0) + 1
        
    avg_word_sentiment = {w: word_scores[w] / word_counts[w] for w in word_scores}
    frequencies = word_counts
    
    # Custom color function: Red (Neg) -> Orange -> Ochre (Neu) -> Green -> Forest Green (Pos)
    def sentiment_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        sentiment = avg_word_sentiment.get(word, 0)
        # Custom palette for better contrast (Premium Look)
        if sentiment > 0.4:
            return "#15803d" # Forest Green (Very Good)
        elif sentiment > 0.1:
            return "#22c55e" # Green (Good)
        elif sentiment > -0.1:
            return "#a16207" # Dark Yellow / Ochre (Neutral)
        elif sentiment > -0.4:
            return "#ea580c" # Orange (Bad)
        else:
            return "#991b1b" # Dark Red (Critical)

    wc = WordCloud(width=1200, height=600, background_color='white', 
                  max_words=100, color_func=sentiment_color_func).generate_from_frequencies(frequencies)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Nube de Inteligencia Semántica (Color por Sentimiento)")
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
    colors_map = {'Positivo': '#22c55e', 'Negativo': '#ef4444'}
    sns.barplot(data=comparison_df, x='Frecuencia', y='Palabra', hue='Sentimiento', 
                dodge=False, palette=colors_map, ax=ax)
    ax.set_title("Top Drivers (Frecuencia Comparada)")
    ax.axvline(0, color='black', linewidth=0.8)
    return fig

def generate_authority_scatter(df):
    if 'authority_level' not in df.columns: return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    # Diverging map that matches the Green-Yellow-Red aesthetic
    sc = ax.scatter(df['sentimiento_score'], df['authority_level'], 
                    alpha=0.6, c=df['sentimiento_score'], cmap='RdYlGn')
    ax.set_title("Nivel de Autoridad vs. Intensidad de Sentimiento")
    ax.set_xlabel("Score de Sentimiento")
    ax.set_ylabel("Nivel de Autoridad (Normalizado)")
    plt.colorbar(sc, ax=ax, label="Sentimiento")
    return fig

def generate_refinement_comparison(df):
    if 'base_score' not in df.columns: return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    samples = df.head(15)
    x = np.arange(len(samples))
    width = 0.35
    
    ax.bar(x - width/2, samples['base_score'], width, label='Base (TF-IDF)', color='#cbd5e1')
    ax.bar(x + width/2, samples['sentimiento_score'], width, label='Final (Híbrido)', color='#22c55e')
    
    ax.set_title("Efecto del Refinamiento Multidimensional (Híbrido)")
    ax.set_ylabel("Score")
    ax.set_xticks(x)
    ax.set_xticklabels([f"R{i+1}" for i in x], rotation=45)
    ax.legend()
    return fig

def generate_time_series_comparison(df1, df2, label1, label2):
    """Generates a comparison line chart for sentiment evolution."""
    def process_series(df, label):
        if 'date' not in df.columns: return None
        d = df.copy()
        d['date'] = pd.to_datetime(d['date'])
        d = d.set_index('date').sort_index()
        # Monthly or weekly resampling to smooth data
        return d.resample('W')['sentimiento_score'].mean().reset_index()

    s1 = process_series(df1, label1)
    s2 = process_series(df2, label2)
    
    if s1 is None or s2 is None: return None
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot Series 1 (Green)
    ax.plot(s1['date'], s1['sentimiento_score'], marker='o', linestyle='-', color='#22c55e', label=label1)
    # Plot Series 2 (Blue)
    ax.plot(s2['date'], s2['sentimiento_score'], marker='s', linestyle='--', color='#3b82f6', label=label2)
    
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax.set_title(f"Evolución Comparada: {label1} vs {label2}")
    ax.set_ylim(-1.1, 1.1)
    ax.legend()
    plt.xticks(rotation=45)
    return fig

def generate_sentiment_comparison_bar(df1, df2, label1, label2):
    """Generates a grouped bar chart for sentiment distribution comparison."""
    def get_dist(df, label):
        d = df['sentimiento'].value_counts(normalize=True).reset_index()
        d.columns = ['Sentimiento', 'Proporción']
        d['Marca'] = label
        return d

    comp_df = pd.concat([get_dist(df1, label1), get_dist(df2, label2)])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=comp_df, x='Sentimiento', y='Proporción', hue='Marca', 
                palette=['#22c55e', '#3b82f6'], ax=ax)
    
    ax.set_title("Distribución de Sentimiento Comparada (%)")
    ax.set_ylim(0, 1.0)
    return fig

def generate_category_comparison_bar(df1, df2, label1, label2):
    """Generates a grouped bar chart for category distribution comparison."""
    def get_dist(df, label):
        d = df['categoria_predom'].value_counts(normalize=True).reset_index()
        d.columns = ['Categoría', 'Proporción']
        d['Marca'] = label
        return d

    comp_df = pd.concat([get_dist(df1, label1), get_dist(df2, label2)])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=comp_df, x='Categoría', y='Proporción', hue='Marca', 
                palette=['#22c55e', '#3b82f6'], ax=ax)
    
    ax.set_title("Distribución de Temas Comparada (%)")
    plt.xticks(rotation=45)
    return fig
