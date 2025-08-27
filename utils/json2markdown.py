#!/usr/bin/env python3
"""
json2markdown.py – Convert a Turkish dictionary‑style JSON file to one
Markdown file per entry, each containing YAML front‑matter.

USAGE
    python json2markdown.py sozluk.json output/     # writes *.md next to output folder

DEPENDENCIES
    pip install python-slugify pyyaml
"""

from __future__ import annotations
import json
from pathlib import Path
import argparse
import yaml  # pip install pyyaml
from slugify import slugify  # pip install python-slugify
from collections import Counter, defaultdict
from datetime import datetime

# Local function definitions

def safe_slug(term: str) -> str:
    """
    Return a cross-platform, ASCII-only slug suitable for a file name.
    Ensures Turkish characters are mapped, path separators are replaced,
    and output is lowercase with hyphens.
    """
    term = term.strip()  # remove leading/trailing spaces
    
    slug = slugify(
        term,
        lowercase=True,
        separator="-",
        replacements=[
            ("/", "-"), ("\\", "-"),
            ("ç", "c"), ("Ç", "c"),
            ("ğ", "g"), ("Ğ", "g"),
            ("ı", "i"), ("İ", "i"),
            ("ö", "o"), ("Ö", "o"),
            ("ş", "s"), ("Ş", "s"),
            ("ü", "u"), ("Ü", "u"),
        ],
        allow_unicode=False,
    )
    
    if not slug:  # If empty after slugification
        slug = "unnamed-" + slugify(term or "term", lowercase=True, allow_unicode=False)
    
    return slug


def to_md(term: str, fields: dict) -> str:
    """Build the Markdown text (front‑matter + trailing ---) for one term."""
    # Generate the metadata
    front_matter = {
        "layout": "term",
        "title": term,  # keep the original Turkish spelling in the meta‑data
        "slug": safe_slug(term),
        "letter": term[0].upper(),
        "processed_at" : datetime.now().isoformat(timespec="seconds"),
        **fields,
    }

    yaml_text = yaml.safe_dump(
        front_matter,
        allow_unicode=True,
        sort_keys=False,
        width=10_000,  # do not wrap long lines
    )

    return f"---\n{yaml_text}---\n"  # trailing newline lets you append body later


# Main function definition
def main() -> None:
    parser = argparse.ArgumentParser(description="Processed JSON to markdown")
    parser.add_argument("--input", required=True, help="JSON file containing processed dictionary items")
    parser.add_argument("--output", required=True, help="Processed markdown page file path")
    args = parser.parse_args()
    
    with open(Path(args.input), encoding="utf-8") as f:
        data: dict[str, dict] = json.load(f)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Slug collision detector (SCD)
    terms = [term for term in data.keys()]
    slugs = [safe_slug(term) for term in data.keys()]
    dupes = [s for s,c in Counter(slugs).items() if c > 1]
    
    # Determine which terms are colliding to what slug
    if dupes:
        dict_slug = defaultdict(list)
        for t in terms:
            dict_slug[safe_slug(t)].append(t)
        for d in dupes:
            print(f"✘ collision: {d} ← {dict_slug[d]}")
        print(f"number of collisions: {len(dupes)}")

    # Main processing loop
    # Use the following formatting for page title URL:
    # base-url/{slug}--{index}.html
    total_items = len(data)
    for i, (term, fields) in enumerate(data.items(), start=1):
        filename = f"{safe_slug(term)}--{fields['indeks']}.md"
        out_path = out_dir / filename
        out_path.write_text(to_md(term, fields), encoding="utf-8")
        print(f"✔︎ {i / total_items:.3%}  |  {filename}")

# Main function call
if __name__ == "__main__":
    main()
