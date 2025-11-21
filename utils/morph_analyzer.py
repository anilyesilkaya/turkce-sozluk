"""
Automated Morphological Analyzer (AMA)

Accepts any Turkish word in an inflected form (e.g., "gelemedim")
and decomposes it into its lemma plus individual suffixes:
    "gelemedim" → gel-(mek) + e + me + dim

Usage (flag style):
    python morph_analyzer.py --input turkish_lemmas.json --output analysis.json

Or, using positional arguments:
    python morph_analyzer.py turkish_lemmas.json analyzed.json

The analyzer’s JSON output can be fed into an interactive
“suffix explorer” to inspect each suffix and its grammatical role.
"""
import argparse
import json
from pathlib import Path
import re

def main() -> None:
    parser = argparse.ArgumentParser(description="Turkish morphological analyzer")
    parser.add_argument("--input", required=True, help="JSON file containing Turkish words")
    parser.add_argument("--output", required=True, help="Path for the analysis JSON")
    args = parser.parse_args()

    # Load the source JSON
    
    words = json.loads(Path(args.input).read_text(encoding="utf-8"))
    
    # Analyze words
    lemmas = {}
    for i, w in enumerate(words):
        # Since each element is not consist of single word,
        # split the w into each word
        w_end = re.split(' ', w)[-1]
        
        # If the word contains the post-fix 'mek'/'mak', use it since,
        # the common structure is verb + mek/mak
        w_mek = re.split('mek', w_end)
        w_mak = re.split('mak', w_end)
        if len(w_mek) == 2:
            # Record the entry
            lemmas[w_mek[0]] = 'mek'
        elif len(w_mak) == 2:
            # Record the entry
            lemmas[w_mak[0]] = 'mak'
        else:
            continue

    # Write the destination JSON
    Path(args.output).write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Analysis written to {args.output}")


if __name__ == "__main__":
    main()