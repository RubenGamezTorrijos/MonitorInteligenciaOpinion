import json
import re

nb_path = r'c:\Users\ruben\UEM_SSII_MonitorInteligenciaOpinion\MonitorInteligenciaOpinion\notebooks\Analisis_Amazon_TrustPilot_v6_DeepSeek_Revisar.ipynb'

def patch():
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Update Scraper
    scraper_src = [
        "import requests, pandas as pd, re, time, random\n",
        "from datetime import datetime\n",
        "from bs4 import BeautifulSoup\n",
        "\n",
        "class TrustpilotScraper:\n",
        "    def __init__(self, url, max_pages=15):\n",
        "        self.url = url\n",
        "        self.max_pages = max_pages\n",
        "        self.session = requests.Session()\n",
        "        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})\n",
        "\n",
        "    def extract(self, el):\n",
        "        try:\n",
        "            t_el = el.select_one('[data-review-title-typography=\"true\"]')\n",
        "            c_el = el.select_one('[data-review-content-typography=\"true\"]')\n",
        "            r_c = el.select_one('[data-star-rating]')\n",
        "            rating = int(re.search(r'(\\d+)', r_c.find('img')['alt']).group(1)) if r_c else None\n",
        "            user = el.select_one('[data-consumer-name-typography=\"true\"]').get_text(strip=True)\n",
        "            return {\n",
        "                'usuario': user,\n",
        "                'puntuacion': rating,\n",
        "                'titulo': t_el.get_text(strip=True) if t_el else \"\",\n",
        "                'texto_comentario': c_el.get_text(strip=True) if c_el else \"\"\n",
        "            }\n",
        "        except: return None\n",
        "\n",
        "    def scrape_all_pages(self):\n",
        "        results = []\n",
        "        for p in range(1, self.max_pages + 1):\n",
        "            res = self.session.get(f\"{self.url}?page={p}\")\n",
        "            soup = BeautifulSoup(res.content, 'html.parser')\n",
        "            articles = soup.select('article[data-review-card-identifier]')\n",
        "            for a in articles:\n",
        "                data = self.extract(a)\n",
        "                if data: results.append(data)\n",
        "            if len(results) >= 100: break\n",
        "            time.sleep(2)\n",
        "        return pd.DataFrame(results)\n"
    ]

    # 2. Update Processing
    proc_src = [
        "import nltk\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.tokenize import word_tokenize\n",
        "import unicodedata\n",
        "\n",
        "class TextPreprocessor:\n",
        "    def __init__(self):\n",
        "        nltk.download('punkt', quiet=True)\n",
        "        nltk.download('stopwords', quiet=True)\n",
        "        self.stop = set(stopwords.words('spanish'))\n",
        "\n",
        "    def clean(self, text):\n",
        "        text = str(text).lower()\n",
        "        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')\n",
        "        tokens = word_tokenize(text)\n",
        "        return ' '.join([t for t in tokens if t.isalpha() and t not in self.stop])\n",
        "\n",
        "pre = TextPreprocessor()\n",
        "df_final = df_reviews_raw.copy()\n",
        "df_final['texto_limpio'] = df_final['texto_comentario'].apply(pre.clean)\n",
        "print('✅ Procesamiento completado')\n"
    ]

    # 3. Update Visuals
    viz_src = [
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "from wordcloud import WordCloud\n",
        "\n",
        "plt.figure(figsize=(15, 5))\n",
        "plt.subplot(1, 2, 1)\n",
        "sns.countplot(data=df_final, x='puntuacion', palette='magma')\n",
        "plt.title('Distribución de Estrellas')\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "wordcloud = WordCloud(background_color='white').generate(' '.join(df_final['texto_limpio']))\n",
        "plt.imshow(wordcloud)\n",
        "plt.axis('off')\n",
        "plt.title('Nube de Temas')\n",
        "plt.show()\n"
    ]

    for cell in nb['cells']:
        cid = cell.get('metadata', {}).get('id')
        if cid == 'clase-trustpilot-scraper': cell['source'] = scraper_src
        if cid == 'aplicacion-preprocesamiento': cell['source'] = proc_src
        if cid == 'ejecucion-visualizaciones': cell['source'] = viz_src

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
    print("Patched successfully")

if __name__ == '__main__':
    patch()
