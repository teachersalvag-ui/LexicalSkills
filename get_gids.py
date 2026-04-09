import urllib.request
import re
import csv
from io import StringIO
import json

url = "https://docs.google.com/spreadsheets/d/1npKHQOuAqO_PqNcdemVtBoZc34DS7l_SURaTl4rP2XY/htmlview"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    gids = {}
    matches = re.finditer(r'\{gid:\s*\"?(\d+)\"?[^}]+name:\s*\"?([^\"]+)\"?\}', html)
    for m in matches:
        gids[m.group(2)] = m.group(1)
    if not gids:
        matches = re.finditer(r'\[\"([^\"]+)\",(\d+)\]', html)
        for m in matches:
            gids[m.group(1)] = m.group(2)
    print("GIDS:", gids)

    # Try exact or similar names
    targets = []
    for k in gids.keys():
        if 'basic' in k.lower() or 'intermediate' in k.lower():
            targets.append(k)
            
    print("Found target sheets:", targets)

    for sheet_name in targets:
        csv_url = f"https://docs.google.com/spreadsheets/d/1npKHQOuAqO_PqNcdemVtBoZc34DS7l_SURaTl4rP2XY/export?format=csv&gid={gids[sheet_name]}"
        csv_req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
        csv_data = urllib.request.urlopen(csv_req).read().decode('utf-8')
        reader = csv.reader(StringIO(csv_data))
        rows = list(reader)
        print(f"--- {sheet_name} ---")
        print(rows[:5])
        
        # Output as valid array format
        # If columns are just Word(EN) and Meaning(ES)
        words = []
        for row in rows[1:]: # skip header
            if len(row) >= 2 and row[0].strip() != '':
                words.append({"en": row[0].strip(), "es": row[1].strip()})
        print(f"Total words in {sheet_name}: {len(words)}")
        
        with open(f"{sheet_name}.json", "w", encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False)
except Exception as e:
    print(e)
