#!/usr/bin/env python3
"""
json2markdown.py – Convert a Turkish dictionary‑style JSON file to one
Markdown file per entry, each containing YAML front‑matter.

USAGE
    python json2markdown.py sozluk.json            # writes *.md next to JSON
    python json2markdown.py sozluk.json output/     # writes into output/

DEPENDENCIES
    pip install python-slugify pyyaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml  # pip install pyyaml
from slugify import slugify  # pip install python-slugify

# ──────────────────────────────────────────────────────────────────────────────

def safe_slug(term: str) -> str:
    """Return a cross‑platform, ASCII‑only slug suitable for a file name."""
    slug = slugify(
        term,
        lowercase=True,
        separator="-",
        replacements=[("/", "-"), ("\\", "-")],  # replace path separators
        allow_unicode=False,
    )
    return slug or "unnamed"


def to_md(term: str, fields: dict) -> str:
    """Build the Markdown text (front‑matter + trailing ---) for one term."""
    front_matter = {
        "layout": "term",
        "title": term,  # keep the original Turkish spelling in the meta‑data
        **fields,
    }

    yaml_text = yaml.safe_dump(
        front_matter,
        allow_unicode=True,
        sort_keys=False,
        width=10_000,  # do not wrap long lines
    )

    return f"---\n{yaml_text}---\n"  # trailing newline lets you append body later


# ──────────────────────────────────────────────────────────────────────────────

def main(source: Path, out_dir: Path) -> None:
    with source.open(encoding="utf-8") as f:
        data: dict[str, dict] = json.load(f)

    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(data)
    for i, (term, fields) in enumerate(data.items(), 1):
        filename = f"{safe_slug(term)}.md"
        out_path = out_dir / filename
        out_path.write_text(to_md(term, fields), encoding="utf-8")
        print(f"✔︎ {i / total:.1%}  |  {filename}")


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: json2markdown.py <json-file> [output-dir]")

    json_file = Path(sys.argv[1])
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else json_file.parent

    main(json_file, destination)
