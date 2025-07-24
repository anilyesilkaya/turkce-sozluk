import json
import copy

# Open load the TDK Sozluk JSON file
data = []
with open('database_sozluk/test2.json', 'r', encoding='utf-8') as file:
    for line in file:
        if line.strip(): # keep the none-empty lines
            data.append(json.loads(line))

# #-------
# # TEST
# #--------
# data = []
# sozluk = {}
# with open('database_sozluk/test.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#     data = [data]
# #-------
# # TEST
# #--------

# Process the data
sozluk = {}
anlamlar = []
ozellikler = []
ornekler = []
o_tmp = []
e_tmp = []
print(f'(Progress...0%)') # initial progress display
for i, entry in enumerate(data, start=1):
    # Reset the states
    word = []
    pword = []
    language = []
    anlamlar.clear()
    ozellikler.clear()
    ornekler.clear()
    
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
        if word != pword:
            e_tmp.clear()
        if len(anlam.get("orneklerListe", "")) > 0:
            for e in anlam.get("orneklerListe", ""):
                e_tmp.append(e.get("ornek", ""))
        else:
            e_tmp.append("")
        ornekler.append(e_tmp.copy())

        # Create a dictionary using populated values, key is the word itself
        sozluk[word] = {
            "lisan": language,
            "anlamlar": copy.deepcopy(anlamlar),
            "ozellikler": copy.deepcopy(ozellikler),
            "ornekler": copy.deepcopy(ornekler)
        }
        pword = word

    
    # Show progress
    print(f'(Progress...{100*i/len(data)}%)')

# Save processed sozluk
with open("database_sozluk/processed_sozluk.json", "w", encoding="utf-8") as f:
    json.dump(sozluk, f, ensure_ascii=False, indent=2)
