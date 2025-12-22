import json

def rebuild_3_analisis():
    cells = []
    
    # 1. Header and Imports
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# FASE 3: Análisis de Valor\n", "Este notebook realiza el análisis de sentimiento y de inteligencia de usuarios."]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "from textblob import TextBlob\n",
            "from collections import Counter\n",
            "import os\n",
            "import json\n",
            "\n",
            "# Cargar datos\n",
            "df = pd.read_csv('../data/processed/dataset_clean.csv')\n",
            "print(f\"Datos cargados: {len(df)} reseñas\")\n"
        ]
    })
    
    # 2. Sentiment Analysis
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def analyze_sentiment(text):\n",
            "    analysis = TextBlob(str(text))\n",
            "    polarity = analysis.sentiment.polarity\n",
            "    subjectivity = analysis.sentiment.subjectivity\n",
            "    if polarity > 0.1: sentiment = 'Positivo'\n",
            "    elif polarity < -0.1: sentiment = 'Negativo'\n",
            "    else: sentiment = 'Neutral'\n",
            "    return polarity, subjectivity, sentiment\n",
            "\n",
            "print(\"Analizando sentimiento...\")\n",
            "df_sentiment = df.copy()\n",
            "res = df_sentiment['texto_limpio'].apply(analyze_sentiment)\n",
            "df_sentiment[['polarity', 'subjectivity', 'sentiment']] = pd.DataFrame(res.tolist(), index=df.index)\n"
        ]
    })
    
    # 3. Emotions and Metrics
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "emotion_lexicon = {\n",
            "    'positivas': {'bien', 'bueno', 'excelente', 'perfecto', 'genial', 'fantastico', 'recomiendo'},\n",
            "    'negativas': {'mal', 'malo', 'horrible', 'terrible', 'problema', 'error', 'queja'}\n",
            "}\n",
            "def detect_emotions(text):\n",
            "    text_lower = str(text).lower()\n",
            "    counts = {cat: sum(1 for w in words if w in text_lower) for cat, words in emotion_lexicon.items()}\n",
            "    if max(counts.values()) == 0: return 'neutral'\n",
            "    return max(counts, key=counts.get)\n",
            "\n",
            "df_sentiment['emocion_predominante'] = df_sentiment['texto_limpio'].apply(detect_emotions)\n",
            "df_sentiment['longitud_texto'] = df_sentiment['texto_limpio'].fillna('').str.len()\n",
            "df_sentiment['num_palabras'] = df_sentiment['texto_limpio'].apply(lambda x: len(str(x).split()))\n"
        ]
    })
    
    # 4. User Intelligence (Persona B)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print(\"Analizando inteligencia de usuarios...\")\n",
            "if 'num_resenas_usuario_total' in df_sentiment.columns:\n",
            "    bins = [0, 1, 3, 10, 1000]\n",
            "    labels = ['Nuevo (1)', 'Casual (2-3)', 'Frecuente (4-10)', 'Experto (>10)']\n",
            "    df_sentiment['segmento_usuario'] = pd.cut(df_sentiment['num_resenas_usuario_total'], bins=bins, labels=labels, include_lowest=True)\n",
            "\n",
            "print(\"✓ Análisis de usuarios completado.\")\n"
        ]
    })
    
    # 5. Saving Results
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "output_path = '../data/processed/reviews_with_sentiment.csv'\n",
            "df_sentiment.to_csv(output_path, index=False, encoding='utf-8-sig')\n",
            "print(f\"✓ Dataset guardado: {output_path}\")\n",
            "\n",
            "# Word frequency\n",
            "all_tokens = ' '.join(df_sentiment['texto_limpio'].dropna().astype(str)).split()\n",
            "word_freq = Counter(all_tokens)\n",
            "pd.DataFrame(word_freq.most_common(50), columns=['palabra', 'frecuencia']).to_csv('../data/processed/top_palabras.csv', index=False)\n"
        ]
    })

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    with open('notebooks/3_analisis.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook 3_analisis.ipynb rebuilt.")

if __name__ == "__main__":
    rebuild_3_analisis()
