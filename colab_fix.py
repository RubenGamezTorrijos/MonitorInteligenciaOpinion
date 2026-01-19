import json

nb_path = r'c:\Users\ruben\UEM_SSII_MonitorInteligenciaOpinion\MonitorInteligenciaOpinion\notebooks\Analisis_Amazon_TrustPilot_v6_DeepSeek_Revisar.ipynb'

def patch():
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. FIX DEPS CELL (Safe for Colab)
    deps_src = [
        "import sys\n",
        "import os\n",
        "\n",
        "print(\"=\" * 70)\n",
        "print(\"🔧 CONFIGURANDO ENTORNO EN GOOGLE COLAB\")\n",
        "print(\"=\" * 70)\n",
        "\n",
        "def install_if_needed():\n",
        "    print(\"\\n📦 Verificando y preparando librerías...\")\n",
        "    \n",
        "    # No actualizamos pandas/numpy/requests para no romper el entorno de Colab\n",
        "    packages = [\n",
        "        'beautifulsoup4', \n",
        "        'wordcloud', \n",
        "        'textblob', \n",
        "        'nltk',\n",
        "        'googletrans==4.0.0-rc1'\n",
        "    ]\n",
        "    \n",
        "    for pkg in packages:\n",
        "        pkg_name = pkg.split('==')[0]\n",
        "        try:\n",
        "            __import__(pkg_name)\n",
        "            # Si es googletrans, verificamos que no sea la versión vieja que rompe\n",
        "            if pkg_name == 'googletrans':\n",
        "                import googletrans\n",
        "                if not hasattr(googletrans, 'Translator'): raise ImportError\n",
        "        except ImportError:\n",
        "            print(f\"   📥 Instalando {pkg}...\")\n",
        "            !pip install {pkg} -q\n",
        "            \n",
        "    print(\"\\n✅ Librerías fundamentales verificadas\")\n",
        "    \n",
        "    # Descargas NLTK críticas\n",
        "    import nltk\n",
        "    print(\"📥 Descargando recursos NLTK...\")\n",
        "    nltk.download('punkt', quiet=True)\n",
        "    nltk.download('stopwords', quiet=True)\n",
        "    nltk.download('punkt_tab', quiet=True)\n",
        "\n",
        "if 'google.colab' in sys.modules:\n",
        "    install_if_needed()\n",
        "else:\n",
        "    print(\"⚠️ Entorno local detectado, asegúrate de tener instaladas las dependencias.\")\n",
        "\n",
        "print(\"\\n✅ Entorno listo\")\n",
        "print(\"=\" * 70)\n"
    ]

    # 2. Scraper Cell (Robust & Documented)
    scraper_src = [
        "import requests, pandas as pd, re, time, random\n",
        "from datetime import datetime\n",
        "from bs4 import BeautifulSoup\n",
        "from typing import List, Dict, Optional\n",
        "\n",
        "class TrustpilotScraper:\n",
        "    \"\"\"\n",
        "    Scraper optimizado para Trustpilot 2026.\n",
        "    \"\"\"\n",
        "    def __init__(self, url: str, max_pages: int = 15):\n",
        "        self.url = url\n",
        "        self.max_pages = max_pages\n",
        "        self.session = requests.Session()\n",
        "        self.session.headers.update({\n",
        "            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'\n",
        "        })\n",
        "\n",
        "    def extract(self, el) -> Optional[Dict]:\n",
        "        try:\n",
        "            # Selectores estables 2026\n",
        "            title_el = el.select_one('[data-review-title-typography=\"true\"]')\n",
        "            content_el = el.select_one('[data-review-content-typography=\"true\"]')\n",
        "            rating_el = el.select_one('[data-star-rating] img')\n",
        "            user_el = el.select_one('[data-consumer-name-typography=\"true\"]')\n",
        "            \n",
        "            rating = 0\n",
        "            if rating_el and 'alt' in rating_el.attrs:\n",
        "                match = re.search(r'(\\d+)', rating_el['alt'])\n",
        "                if match: rating = int(match.group(1))\n",
        "\n",
        "            return {\n",
        "                'usuario': user_el.get_text(strip=True) if user_el else \"Anónimo\",\n",
        "                'puntuacion': rating,\n",
        "                'titulo': title_el.get_text(strip=True) if title_el else \"\",\n",
        "                'texto_comentario': content_el.get_text(strip=True) if content_el else \"\",\n",
        "                'fecha': datetime.now().strftime(\"%Y-%m-%d\")\n",
        "            }\n",
        "        except: return None\n",
        "\n",
        "    def scrape_all_pages(self) -> pd.DataFrame:\n",
        "        all_data = []\n",
        "        print(f\"🚀 Iniciando scraping en {self.url}\")\n",
        "        \n",
        "        for page in range(1, self.max_pages + 1):\n",
        "            print(f\"   📄 Procesando página {page}...\", end=' ')\n",
        "            try:\n",
        "                r = self.session.get(f\"{self.url}?page={page}\", timeout=10)\n",
        "                soup = BeautifulSoup(r.content, 'html.parser')\n",
        "                articles = soup.select('article[data-review-card-identifier]')\n",
        "                \n",
        "                page_reviews = []\n",
        "                for a in articles:\n",
        "                    data = self.extract(a)\n",
        "                    if data: page_reviews.append(data)\n",
        "                \n",
        "                all_data.extend(page_reviews)\n",
        "                print(f\"({len(page_reviews)} reseñas encontradas)\")\n",
        "                \n",
        "                if not page_reviews or len(all_data) >= 120: break\n",
        "                time.sleep(random.uniform(1.5, 3.0))\n",
        "            except Exception as e:\n",
        "                print(f\"❌ Error: {e}\")\n",
        "                break\n",
        "        \n",
        "        df = pd.DataFrame(all_data)\n",
        "        print(f\"\\n✅ Scrape completo. Total único: {len(df)}\")\n",
        "        return df\n"
    ]

    # Update cells
    for cell in nb['cells']:
        cid = cell.get('metadata', {}).get('id')
        if cid == 'instalacion-dependencias': cell['source'] = deps_src
        if cid == 'clase-trustpilot-scraper': cell['source'] = scraper_src

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(\"Notebook fixed for Colab compatibility.\")

if __name__ == '__main__':
    patch()
