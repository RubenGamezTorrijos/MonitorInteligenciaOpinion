# Desarrollado por Rubén

import json
import os

def fix_visualization_notebook():
    nb_path = 'notebooks/4_visualizacion.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} no encontrado.")
        return

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # We'll search for the problematic lines and replace them
    # target: for sentiment in ['positivo', 'neutral', 'negativo']:
    # also add a check for empty box_data_list
    
    cells_updated = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            new_source = []
            changed = False
            for line in source:
                # Fix lowercase strings to capitalized or handle both
                if "for sentiment in ['positivo', 'neutral', 'negativo']:" in line:
                    line = line.replace("['positivo', 'neutral', 'negativo']", "['Positivo', 'Neutral', 'Negativo']")
                    changed = True
                
                # Fix common mismatch in viz code
                if "sentiment in df['sentiment'].values" in line:
                    if "sentiment.lower()" not in line and "Positivo" not in line:
                        # If we already changed the loop to capitalized, this is fine
                        pass
                
                new_source.append(line)
            
            # Add safety check for boxplot if not present
            if "ax6.boxplot(box_data_list" in "".join(new_source) and "if box_data_list:" not in "".join(new_source):
                # We need to find where bp = ax6.boxplot is and indent it
                final_source = []
                in_loop = False
                for line in new_source:
                    if "bp = ax6.boxplot" in line:
                        final_source.append("    if box_data_list:\n")
                        final_source.append("        " + line)
                        changed = True
                    elif "colors_box =" in line and "bp['boxes']" in "".join(new_source):
                         final_source.append("        " + line)
                    elif "for patch, color in zip(bp['boxes']" in line:
                         final_source.append("        " + line)
                    elif "patch.set_facecolor(color)" in line:
                         final_source.append("        " + line)
                    else:
                        final_source.append(line)
                new_source = final_source

            if changed:
                cell['source'] = new_source
                cells_updated += 1

    if cells_updated > 0:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"Notebook {nb_path} updated. {cells_updated} cells modified.")
    else:
        print("No changes needed or could not find targets.")

if __name__ == "__main__":
    fix_visualization_notebook()
