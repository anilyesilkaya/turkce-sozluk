import pathlib, io
from datetime import datetime


# Turkish alphabet with 29 elements

letters = ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L",
            "M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"]
TEMPLATE = """---
layout: letter
title: "{L} harfiyle başlayan sözcükler"
letter: "{L}"
permalink: "/liste/{L}.html"
processed_at: "{processed_at}"
---
"""

pathlib.Path("../_pages/liste").mkdir(parents=True, exist_ok=True)
for L in letters:
    with io.open(f"_pages/liste/{L}.md", "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(L=L, processed_at=datetime.now().isoformat(timespec="seconds")))
        print(f"✔︎ {L}.md")