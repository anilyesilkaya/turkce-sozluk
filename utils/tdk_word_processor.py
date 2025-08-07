import json
import copy
import sys
from pathlib import Path

def main(source_file: Path, destin_file: Path) -> None:
    # Open load the TDK Sozluk JSON file
    data = []
    with source_file.open('r', encoding='utf-8') as file:
        for line in file:
            if line.strip(): # keep the none-empty lines and remove any spacing and line breaking
                data.append(json.loads(line))

    # Process the data
    sozluk = {}
    anlamlar = []
    ozellikler = []
    ornekler = []
    orneklerkaynak = []
    o_tmp = []
    e_tmp = []
    s_tmp = []
    print(f'(Progress...0%)') # initial progress display
    for i, entry in enumerate(data, start=1):
        # Reset the states
        word = []
        pword = []
        language = []
        anlamlar.clear()
        ozellikler.clear()
        ornekler.clear()
        orneklerkaynak.clear()
        
        word = entry.get("madde","") # fetch the word
        if not word: # if the word is empty, skip
            continue

        # Extract language ("lisan" could be empty)
        language = entry.get("lisan", "")

        if not language: # if the language is empty, fill it with "Türkçe"
            language = "Türkçe"

        # Loop for each meaning
        for anlam in entry.get("anlamlarListe", ""):
            # Extract meanings from meanings list
            anlam_text = anlam.get("anlam", "").strip()
            if anlam_text: # if the meaning is empty, empty string
                if anlam_text[0] == "►": # remove the ► character from anlam_text
                    anlamlar.append(anlam_text[2::])
                else:
                    anlamlar.append(anlam_text)
            else:
                anlamlar.append("")

            # Extract features for each anlam
            if word != pword:
                o_tmp.clear()
            if len(anlam.get("ozelliklerListe", "")) > 0:
                for o in anlam.get("ozelliklerListe", ""):
                    o_tmp.append(o.get("tam_adi", ""))
            else:
                o_tmp.append("")
            ozellikler.append(o_tmp.copy())

            # Extract the examples for each anlam
            e_tmp.clear()
            s_tmp.clear()
            if len(anlam.get("orneklerListe", "")) > 0:
                for e in anlam.get("orneklerListe", ""):
                    e_tmp.append(e.get("ornek", ""))
                    # If the yazar_id is different than 0 fetch the name of the author
                    if e.get("yazar",""):
                        s_tmp.append(e.get("yazar", "")[0].get("tam_adi", ""))
                    else:
                        s_tmp.append("")
            else:
                e_tmp.append("")
                s_tmp.append("")
            ornekler.append(e_tmp.copy())
            orneklerkaynak.append(s_tmp.copy())

            
            # Update the word pointer
            pword = word
            
        # Create a dictionary using populated values, key is the word itself
        sozluk[word] = {
            "lisan": language,
            "anlamlar": copy.deepcopy(anlamlar),
            "ozellikler": copy.deepcopy(ozellikler),
            "ornekler": copy.deepcopy(ornekler),
            "orneklerkaynak": copy.deepcopy(orneklerkaynak)
        }

        
        # Show progress
        print(f'(Progress...{100*i/len(data)}%)')

    # Save processed sozluk
    with destin_file.open('w', encoding='utf-8') as f:
        json.dump(sozluk, f, ensure_ascii=False, indent=2)
    
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: tdk_word_processor.py <input-json-file> <output-json-file>")

    source_json = Path(sys.argv[1])
    destin_json = Path(sys.argv[2])

    main(source_json, destin_json)
