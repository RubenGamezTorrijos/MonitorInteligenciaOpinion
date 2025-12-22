import json
import os

def add_cell_to_notebook(nb_path, cell_content, target_header=None, position='end'):
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} no encontrado.")
        return
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in cell_content.splitlines()]
    }
    
    if position == 'end':
        nb['cells'].append(new_cell)
    elif position == 'after_header' and target_header:
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'markdown' and any(target_header in line for line in cell['source']):
                nb['cells'].insert(i + 1, new_cell)
                break
        else:
            nb['cells'].append(new_cell)
            
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Notebook {nb_path} actualizado exitosamente.")

# --- Contenido para Notebook 3 (Análisis) ---
analisis_user_code = """
# %%
# 4. ANÁLISIS DE INTELIGENCIA DE USUARIOS (Persona B)
print("\\n" + "="*60)
print("4. ANÁLISIS DE INTELIGENCIA DE USUARIOS")
print("="*60)

# Usuarios más activos
top_users = df_sentiment['usuario'].value_counts().head(10)
print("\\nTop 10 usuarios más frecuentes en la muestra:")
for user, count in top_users.items():
    print(f"  {user:30s}: {count:2d} reseñas")

# Distribución geográfica
if 'ubicacion' in df_sentiment.columns:
    print("\\nDISTRIBUCIÓN GEOGRÁFICA (Top 10)")
    print("-" * 40)
    loc_counts = df_sentiment['ubicacion'].value_counts().head(10)
    for loc, count in loc_counts.items():
        print(f"  {loc:10s}: {count:3d} reseñas")

# Segmentación por experiencia
if 'num_resenas_usuario_total' in df_sentiment.columns:
    print("\\nPERFIL DE EXPERIENCIA DEL USUARIO")
    print("-" * 40)
    
    # Crear segmentos
    bins = [0, 1, 3, 10, 1000]
    labels = ['Nuevo (1)', 'Casual (2-3)', 'Frecuente (4-10)', 'Experto (>10)']
    df_sentiment['segmento_usuario'] = pd.cut(df_sentiment['num_resenas_usuario_total'], bins=bins, labels=labels, include_lowest=True)
    
    segment_counts = df_sentiment['segmento_usuario'].value_counts()
    for seg, count in segment_counts.items():
        print(f"  {seg:20s}: {count:3d} usuarios")
        
    # Relación Segmento vs Sentimiento
    seg_sent = df_sentiment.groupby('segmento_usuario', observed=False)['polarity'].mean()
    print("\\nPolaridad promedio por segmento:")
    print(seg_sent)
"""

# --- Contenido para Notebook 4 (Visualización) ---
visualizacion_user_code = """
# %%
# VISUALIZACIÓN DE INTELIGENCIA DE USUARIOS (Persona B)
import seaborn as sns
import matplotlib.pyplot as plt

def plot_user_intelligence(df):
    plt.figure(figsize=(15, 10))
    
    # 1. Top Ubicaciones
    plt.subplot(2, 2, 1)
    if 'ubicacion' in df.columns:
        df['ubicacion'].value_counts().head(10).plot(kind='bar', color='skyblue')
        plt.title('Top 10 Ubicaciones de los Usuarios')
        plt.ylabel('Cantidad de Reseñas')
    
    # 2. Segmentos de Usuario
    plt.subplot(2, 2, 2)
    if 'segmento_usuario' in df.columns:
        df['segmento_usuario'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        plt.title('Distribución de Segmentos de Usuario')
        plt.ylabel('')
    
    # 3. Polaridad por Segmento
    plt.subplot(2, 2, 3)
    if 'segmento_usuario' in df.columns:
        sns.barplot(x='segmento_usuario', y='polarity', data=df, palette='viridis', errorbar=None)
        plt.title('Polaridad Media por Segmento de Usuario')
        plt.xticks(rotation=45)
    
    # 4. Relación Experiencia vs Puntuación
    plt.subplot(2, 2, 4)
    if 'num_resenas_usuario_total' in df.columns:
        plt.scatter(df['num_resenas_usuario_total'], df['puntuacion'], alpha=0.5)
        plt.title('Experiencia (Total Reseñas) vs Puntuación')
        plt.xlabel('Reseñas totales del usuario')
        plt.ylabel('Estrellas')
        plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig('../visualizations/user_intelligence_dashboard.png')
    plt.show()

# Ejecutar visualización si existen los datos
if 'segmento_usuario' in df.columns or 'ubicacion' in df.columns:
    plot_user_intelligence(df)
else:
    print("Datos de usuario no encontrados para visualizar. Ejecuta el pipeline completo.")
"""

if __name__ == "__main__":
    add_cell_to_notebook('notebooks/3_analisis.ipynb', analisis_user_code, target_header="ANÁLISIS ADICIONALES DE VALOR", position='after_header')
    add_cell_to_notebook('notebooks/4_visualizacion.ipynb', visualizacion_user_code, position='end')
