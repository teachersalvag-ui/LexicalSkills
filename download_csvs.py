import urllib.request
import csv
from io import StringIO
import json

targets = {
    "Basic": 0,
    "Intermediate": 1825947842
}

results = {}

try:
    for sheet_name, gid in targets.items():
        csv_url = f"https://docs.google.com/spreadsheets/d/1npKHQOuAqO_PqNcdemVtBoZc34DS7l_SURaTl4rP2XY/export?format=csv&gid={gid}"
        req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read().decode('utf-8')
        
        reader = csv.reader(StringIO(data))
        rows = list(reader)
        
        words = []
        for r in rows[1:]: # skip header row
            if len(r) >= 2 and r[0].strip() != '':
                words.append({"en": r[0].strip(), "es": r[1].strip()})
        
        results[sheet_name] = words
        print(f"{sheet_name}: {len(words)} words downloaded")
        print(f"Sample: {words[:3]}")

    with open("words_extracted.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
except Exception as e:
    print(e)
