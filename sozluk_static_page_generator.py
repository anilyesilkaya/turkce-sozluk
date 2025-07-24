import os
import json

os.makedirs("_terms", exist_ok=True)

# Load sozluk
with open("database_sozluk/processed_sozluk.json", "r", encoding="utf-8") as f:
    sozluk = json.load(f)


for word, content in sozluk.items():
    filename = f"_terms/{word.replace(' ', '_')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"layout: term\n")
        f.write(f"turkish: {word}\n")
        f.write(f"lisan: {content['lisan']}\n")
        f.write("title: " + word + "\n")
        f.write("categories:\n")
        f.write("  - Otomatik\n")  # or custom categories
        f.write("---\n\n")

        for i, anlam in enumerate(content["anlam"], start=1):
            f.write(f"**{i}. Anlam:** {anlam}\n")
            if content["ozellik"][i-1]:
                f.write(f"\n**Özellikler:** {', '.join(content['ozellik'][i-1])}\n")
            if content["ornek"][i-1]:
                f.write(f"\n**Örnek(ler):** {', '.join(content['ornek'][i-1])}\n")
            f.write("\n\n")
