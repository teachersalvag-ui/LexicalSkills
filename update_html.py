import json
import re

# Load words
with open("words_extracted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

basic_list = data["Intermediate"] # Intermediate words go into BASIC array (data-cat="basic")
inter_list = data["Basic"] # Basic words go into INTER array (data-cat="inter")

v_basic = len(basic_list)
v_inter = len(inter_list)
v_total = v_basic + v_inter

# Stringify
basic_str = json.dumps(basic_list, ensure_ascii=False)
inter_str = json.dumps(inter_list, ensure_ascii=False)

# Read HTML
html_path = "LexicalSkills.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace Arrays
html = re.sub(r'const BASIC = \[.*?\];', f'const BASIC = {basic_str};', html)
html = re.sub(r'const INTER = \[.*?\];', f'const INTER = {inter_str};', html)

# Replace Counts
html = re.sub(r'657( palabras · Opci)', f'{v_total}\\1', html)
html = re.sub(r'490( palabras · Phrasal)', f'{v_basic}\\1', html)
html = re.sub(r'167( palabras · Adjetivos)', f'{v_inter}\\1', html)
html = re.sub(r'657( palabras · Basic)', f'{v_total}\\1', html)

# Write HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated successfully! New counts Basic:{v_inter}, Intermediate:{v_basic}, Total:{v_total}")
