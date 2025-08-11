import argparse
import json
import copy
from pathlib import Path

# Local function calls

# Replace the matcing string with a replace string
def replace_if_exist(in_str, match_str, rep_str):
    if in_str == match_str:
        return rep_str
    else:
        return in_str

# Drop the arrow character from each meaning
def drop_arrow_char(word):
    if word[0] == "►":
        return word[2::]
    else:
        return word

# Morphological analyzer
def morphological_analyzer(word):
    return 0

def main() -> None:
    parser = argparse.ArgumentParser(description="TDK dictionary JSON analyzer")
    parser.add_argument("--input", required=True, help="JSON file path containing Turkish dictionary items")
    parser.add_argument("--output", required=True, help="Processed JSON file path")
    parser.add_argument("--morph", required=False, default=False, help="Word level morphological analysis")
    args = parser.parse_args()

    # Open load the Turk Dil Kurumu (TDK) Sozluk JSON file
    data = []
    with open(Path(args.input), 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip(): # keep the none-empty lines and remove any spacing and line breaking
                data.append(json.loads(line))
            else:
                print("Empty")

    # Process the data
    sozluk = {}
    anlamlar = []
    ozellikler = []
    ozellikler_tmp = []
    ornekler = []
    yazarlar = []
    
    # Main entry loop
    print(f'(Progress...0%)') # initial progress display
    for i, entry in enumerate(data, start=1):
        # Reset the states for each entry
        word = []
        language = []
        anlamlar.clear()
        ozellikler.clear()
        ozellikler_tmp.clear()
        ornekler.clear()
        yazarlar.clear()
        
        # Initial validation
        word = entry.get("madde","") # fetch the word
        if not word: # if the word is empty, skip
            continue
        elif args.morph:
            word = morphological_analyzer(word)

        # Extract language ("lisan" could be empty)
        language = entry.get("lisan", "")

        if not language: # if the language is empty, fill it with "Türkçe"
            language = "Türkçe"

        # Extract meaning(s)
        for j in range(len(entry.get("anlamlarListe", ""))):
            anlam_tmp = entry.get("anlamlarListe")[j]
            if anlam_tmp.get("anlam", ""): # if anlam is empty, skip the processing
                anlam_text = drop_arrow_char(anlam_tmp.get("anlam", ""))
                anlamlar.append(anlam_text)
            else:
                break

            # Extract features for each anlam
            for ozellik in anlam_tmp.get("ozelliklerListe", ""):
                ozellik_text = ozellik.get("tam_adi")
                # Replace 'ağızlardan' with 'halk ağzında'
                ozellikler_tmp.append(replace_if_exist(ozellik_text,  'ağızlardan', 'halk ağzında'))
            ozellikler.append(ozellikler_tmp)
            
            # Extract examples for each anlam
            for ornek in anlam_tmp.get("orneklerListe", ""):
                ornek_text = ornek.get("ornek", "")
                ornekler.append(ornek_text)
                for yazar in ornek.get("yazar", ""):
                    yazar_text = yazar.get("tam_adi", "")
                    yazarlar.append(yazar_text)

        # Create a dictionary using populated values, key is the word itself
        if anlamlar: # if anlamlar is empty, skip the entry
            sozluk[word] = {
                "indeks": i,
                "lisan": language,
                "anlamlar": copy.deepcopy(anlamlar),
                "ozellikler": copy.deepcopy(ozellikler),
                "ornekler": copy.deepcopy(ornekler),
                "orneklerkaynak": copy.deepcopy(yazarlar)
            }

        # Show progress
        print(f'(Progress...{100*i/len(data):.4f}%)')

    # Save processed sozluk
    with open(Path(args.output), 'w', encoding='utf-8') as f:
        json.dump(sozluk, f, ensure_ascii=False, indent=2)
    
# Main function call
if __name__ == "__main__":
    main()