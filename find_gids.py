import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1npKHQOuAqO_PqNcdemVtBoZc34DS7l_SURaTl4rP2XY/edit?usp=sharing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'[^a-zA-Z0-9](.?.?.?.?\w+gid\w*.?.?.?.?[^a-zA-Z0-9])', html[:200000])
    
    # Another approach: Find all strings like "Basic", "intermediate" and print surrounding 50 chars
    for s in ["Basic", "intermediate", "Intermediate"]:
        for match in re.finditer(s, html):
            start = max(0, match.start() - 100)
            end = min(len(html), match.end() + 100)
            print(f"Around {s}: {html[start:end]}")
            
except Exception as e:
    print(e)
