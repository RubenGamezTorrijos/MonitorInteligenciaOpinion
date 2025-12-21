import json

notebook_path = 'notebooks/4_visualizacion.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Iterate through cells to find the code block
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        # Join source to search
        source_text = ''.join(source)
        if "explode=[0.05, 0.05, 0.05]" in source_text:
            print("Found target cell, patching...")
            # Replace the line
            new_source = []
            for line in source:
                if "explode=[0.05, 0.05, 0.05]" in line:
                    # We need to change how explode is defined.
                    # It's inside the pie function call usually.
                    # Easier to just replace the fixed list with a variable if defined before,
                    # but here it is passed directly.
                    # We will replace the list with a valid list comprehension or multiplication.
                    # However, we need to know the length of sentiment_counts.
                    # The code 'sentiment_counts = df['sentiment'].value_counts()' runs before.
                    # So we can use [0.05] * len(sentiment_counts).
                    new_line = line.replace("explode=[0.05, 0.05, 0.05]", "explode=[0.05] * len(sentiment_counts)")
                    new_source.append(new_line)
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False) # indent 1 to minimize diff or standard nbformat

print("Notebook patched.")
