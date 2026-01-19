import json

nb_path = r'c:\Users\ruben\UEM_SSII_MonitorInteligenciaOpinion\MonitorInteligenciaOpinion\notebooks\Analisis_Amazon_TrustPilot_v6_DeepSeek_Revisar.ipynb'

def patch():
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # First Cell: Safe dependencies for Colab
    s1 = [
        "import sys\n",
        "print('='*70)\n",
        "print('🔧 CONFIGURANDO ENTORNO EN COLAB')\n",
        "print('='*70)\n",
        "# Solo instalamos lo que NO viene en Colab para evitar conflictos\n",
        "print('📦 Instalando componentes adicionales...')\n",
        "!pip install -q googletrans==3.1.0a0 wordcloud\n",
        "import nltk\n",
        "nltk.download('punkt', quiet=True)\n",
        "nltk.download('stopwords', quiet=True)\n",
        "print('✅ Entorno listo')\n"
    ]

    # Scraper Cell: Robust 2026
    s2 = [
        "import requests, pandas as pd, re, time, random\n",
        "from bs4 import BeautifulSoup\n",
        "from datetime import datetime\n",
        "\n",
        "class TrustpilotScraper:\n",
        "    def __init__(self, url, max_pages=15):\n",
        "        self.url = url\n",
        "        self.max_pages = max_pages\n",
        "        self.session = requests.Session()\n",
        "        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})\n",
        "\n",
        "    def extract(self, el):\n",
        "        try:\n",
        "            r_c = el.select_one('[data-star-rating] img')\n",
        "            rating = int(re.search(r'(\\d+)', r_c['alt']).group(1)) if r_c else 0\n",
        "            title_el = el.select_one('[data-review-title-typography=\"true\"]')\n",
        "            content_el = el.select_one('[data-review-content-typography=\"true\"]')\n",
        "            user_el = el.select_one('[data-consumer-name-typography=\"true\"]')\n",
        "            \n",
        "            return {\n",
        "                'usuario': user_el.get_text(strip=True) if user_el else 'Anónimo',\n",
        "                'puntuacion': rating,\n",
        "                'titulo': title_el.get_text(strip=True) if title_el else '',\n",
        "                'texto_comentario': content_el.get_text(strip=True) if content_el else '',\n",
        "                'fecha': datetime.now().strftime('%Y-%m-%d')\n",
        "            }\n",
        "        except: return None\n",
        "\n",
        "    def scrape_all_pages(self):\n",
        "        data_list = []\n",
        "        print(f'🚀 Iniciando extracción en {self.url}')\n",
        "        for p in range(1, self.max_pages + 1):\n",
        "            res = self.session.get(f'{self.url}?page={p}')\n",
        "            soup = BeautifulSoup(res.content, 'html.parser')\n",
        "            articles = soup.select('article[data-review-card-identifier]')\n",
        "            if not articles: break\n",
        "            for a in articles:\n",
        "                d = self.extract(a)\n",
        "                if d: data_list.append(d)\n",
        "            print(f'   📄 Página {p} procesada ({len(data_list)} reseñas)')\n",
        "            if len(data_list) >= 100: break\n",
        "            time.sleep(random.uniform(1, 3))\n",
        "        return pd.DataFrame(data_list)\n"
    ]

    for cell in nb['cells']:
        cid = cell.get('metadata', {}).get('id', '')
        if cid == 'instalacion-dependencias':
            cell['source'] = s1
        if cid == 'clase-trustpilot-scraper':
            cell['source'] = s2

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print('Patched successfully')

if __name__ == '__main__':
    patch()
