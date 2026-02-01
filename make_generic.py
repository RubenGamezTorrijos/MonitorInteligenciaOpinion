import json
import os

filepath = r'c:\Users\ruben\UEM_SSII_MonitorInteligenciaOpinion\MonitorInteligenciaOpinion\notebooks\MONITOR_INTELIGENCIA_OPINION_FINAL.ipynb'

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'class TrustpilotScraper:' in ''.join(cell['source']):
        source = cell['source']
        new_source = []
        for line in source:
            # 1. Update docstring
            if 'Scraper especializado para Trustpilot.com (versión Amazon España)' in line:
                line = line.replace('(versión Amazon España)', '(Análisis Dinámico)')
            
            # 2. Remove hardcoded default in __init__
            if 'def __init__(self, base_url: str = "https://es.trustpilot.com/review/amazon.es",' in line:
                line = line.replace('base_url: str = "https://es.trustpilot.com/review/amazon.es"', 'base_url: str')
            
            new_source.append(line)
        cell['source'] = new_source

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Scraper class made generic.")
