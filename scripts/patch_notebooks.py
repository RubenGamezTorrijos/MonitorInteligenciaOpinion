import json
import os

def patch_notebook(path, replacements):
    if not os.path.exists(path):
        print(f"Skipping {path}, not found.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            original = source
            for old, new in replacements.items():
                source = source.replace(old, new)
            if source != original:
                # Break into lines
                cell['source'] = [line + ("\n" if not line.endswith("\n") else "") for line in source.splitlines()]
                # remove trailing newline on last line if it wasn't there
                if cell['source'] and not original.endswith("\n") and cell['source'][-1].endswith("\n"):
                     cell['source'][-1] = cell['source'][-1].rstrip("\n")
                modified = True
                
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Patched {path}")

# Phase 1 Notebook replacements
patch_notebook('notebooks/1_scraping.ipynb', {
    'Persona A - Extracción': 'Persona A (Organizador) - Extracción',
    'texto': 'texto_comentario',
    'reviews_amazon_raw.csv': 'dataset_raw.csv'
})

# Phase 2 Notebook replacements
patch_notebook('notebooks/2_preprocesamiento.ipynb', {
    'dataset_raw.csv': 'dataset_raw.csv',
    'texto': 'texto_comentario',
    'reviews_preprocessed.csv': 'dataset_clean.csv'
})

# Phase 3 Notebook replacements
patch_notebook('notebooks/3_analisis.ipynb', {
    'Persona A - Análisis': 'Persona A (Organizador) - Análisis',
    'dataset_clean.csv': 'dataset_clean.csv',
    'reviews_for_analysis.csv': 'dataset_clean.csv',
    'texto_limpio': 'texto_limpio'
})

# Phase 4 Notebook replacements
patch_notebook('notebooks/4_visualizacion.ipynb', {
    'Persona B - Creación': 'Persona B (Colaborador) - Creación',
    'reviews_with_sentiment.csv': 'reviews_with_sentiment.csv'
})
