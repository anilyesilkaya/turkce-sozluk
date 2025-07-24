import requests
import yaml
import os
import re
import time

def slugify(text):
    return re.sub(r"[^a-z0-9\-]", "", text.lower().replace(" ", "-"))

def scrape_word(word):
    url = f"https://sozluk.gov.tr/gts?ara={word}"
    headers =   {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
                }
    response = requests.get(url, headers=headers, timeout=10)
    time.sleep(0.5) # timeout between requests

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] Error fetching {word}: {e}")
        return

    if not data or isinstance(data, dict):
        print(f"[!] Not found: {word}")
        return
    
    try:
        data = response.json()
    except ValueError:
        print(f"[!] Invalid JSON for {word}")
        return

    entry = data[0]
    meanings = entry.get("anlamlarListe", [])
    english_equiv = entry.get("karsilik", "")
    examples = []

    definitions = []
    for m in meanings:
        defn = m.get("anlam", "")
        definitions.append(defn)
        for e in m.get("orneklerListe", []):
            examples.append(e.get("ornek"))

    # Build Markdown content
    filename = slugify(entry["madde"]) + ".md"
    frontmatter = {
        "layout": "term",
        "turkish": entry["madde"],
        "english": english_equiv,
        "definition": definitions[0] if definitions else "",
        "examples": examples,
        "categories": [],  # can fill later
        "origin": entry.get("lisan", "")
    }

    os.makedirs("terms", exist_ok=True)
    with open(os.path.join("terms", filename), "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True)
        f.write("---\n\n")
        f.write(f"## Anlamlar\n\n")
        for i, d in enumerate(definitions, 1):
            f.write(f"{i}. {d}\n")
        if examples:
            f.write("\n## Örnekler\n")
            for ex in examples:
                f.write(f"> {ex}\n")

    print(f"[+] Saved: {entry['madde']}")


words_to_scrape = ["jeton"]
for word in words_to_scrape:
    scrape_word(word)
