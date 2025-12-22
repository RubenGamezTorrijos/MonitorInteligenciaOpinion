# Desarrollado por Rubén

import json
import os

def patch_notebooks():
    # Patch 3_analisis.ipynb
    nb_path = 'notebooks/3_analisis.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} no encontrado.")
        return

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # 1. Remove previously appended user intelligence cell if it's at the end
    # We check the last cell source for our header
    if nb['cells'] and '4. ANÁLISIS DE INTELIGENCIA DE USUARIOS' in "".join(nb['cells'][-1]['source']):
        nb['cells'].pop()
        print("Removed misplaced cell at the end of Notebook 3.")

    # 2. Find the cell where data is saved and inject analysis BEFORE it
    # We look for df_sentiment.to_csv
    save_cell_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and any('df_sentiment.to_csv' in line for line in cell['source']):
            save_cell_idx = i
            break
    
    analisis_user_code = [
        "\n",
        "# 4. ANÁLISIS DE INTELIGENCIA DE USUARIOS (Persona B)\n",
        "print(\"\\n\" + \"=\"*60)\n",
        "print(\"4. ANÁLISIS DE INTELIGENCIA DE USUARIOS\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "# Usuarios más activos\n",
        "top_users = df_sentiment['usuario'].value_counts().head(10)\n",
        "print(\"\\nTop 10 usuarios más frecuentes en la muestra:\")\n",
        "for user, count in top_users.items():\n",
        "    print(f\"  {user:30s}: {count:2d} reseñas\")\n",
        "\n",
        "# Distribución geográfica\n",
        "if 'ubicacion' in df_sentiment.columns:\n",
        "    print(\"\\nDISTRIBUCIÓN GEOGRÁFICA (Top 10)\")\n",
        "    print(\"-\" * 40)\n",
        "    loc_counts = df_sentiment['ubicacion'].value_counts().head(10)\n",
        "    for loc, count in loc_counts.items():\n",
        "        print(f\"  {loc:10s}: {count:3d} reseñas\")\n",
        "\n",
        "# Segmentación por experiencia\n",
        "if 'num_resenas_usuario_total' in df_sentiment.columns:\n",
        "    print(\"\\nPERFIL DE EXPERIENCIA DEL USUARIO\")\n",
        "    print(\"-\" * 40)\n",
        "    \n",
        "    # Crear segmentos\n",
        "    bins = [0, 1, 3, 10, 1000]\n",
        "    labels = ['Nuevo (1)', 'Casual (2-3)', 'Frecuente (4-10)', 'Experto (>10)']\n",
        "    df_sentiment['segmento_usuario'] = pd.cut(df_sentiment['num_resenas_usuario_total'], bins=bins, labels=labels, include_lowest=True)\n",
        "    \n",
        "    segment_counts = df_sentiment['segmento_usuario'].value_counts()\n",
        "    for seg, count in segment_counts.items():\n",
        "        print(f\"  {seg:20s}: {count:3d} usuarios\")\n",
        "        \n",
        "    # Relación Segmento vs Sentimiento\n",
        "    seg_sent = df_sentiment.groupby('segmento_usuario', observed=False)['polarity'].mean()\n",
        "    print(\"\\nPolaridad promedio por segmento:\")\n",
        "    print(seg_sent)\n",
        "\n"
    ]

    if save_cell_idx != -1:
        # Insert before the save cell
        nb['cells'].insert(save_cell_idx, {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": analisis_user_code
        })
        print(f"Injected user analysis before data save (at cell index {save_cell_idx}).")
    else:
        # Fallback to appending if save cell not found (shouldn't happen)
        nb['cells'].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": analisis_user_code
        })
        print("Append user analysis at the end (could not find save cell).")
    
    # 3. Update the viz_data selection cell to include new columns
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and 'viz_data = df_sentiment[[' in "".join(cell['source']):
            # Find the list of columns and append new ones
            for i, line in enumerate(cell['source']):
                if "'longitud_texto', 'num_palabras'" in line:
                    cell['source'][i] = "    'longitud_texto', 'num_palabras', 'num_resenas_usuario_total', 'segmento_usuario', 'ubicacion'\n"
                    print("Updated viz_data column selection.")
                    break

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Notebook {nb_path} updated.")

if __name__ == "__main__":
    patch_notebooks()
