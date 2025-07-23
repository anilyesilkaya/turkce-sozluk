import json

# # Open load the TDK Sozluk JSON file
# data = []
# with open('database_sozluk/v12/gts.json', 'r', encoding='utf-8') as file:
#     for line in file:
#         if line.strip(): # keep the none-empty lines
#             data.append(json.loads(line))
#-------
# TEST
#--------
data = []
with open('database_sozluk/test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    data = [data]
#-------
# TEST
#--------

# Process the data
anlamlar = []
ozellikler = []
ornekler = []

for entry in data:
    restructured = []
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
        assert len(anlam.get("ozelliklerListe", "")) < 2, "Length of the ozelliklerListe is not 1."
        if len(anlam.get("ozelliklerListe", "")):
            ozellikler.append(anlam.get("ozelliklerListe", "")[0].get("tam_adi", ""))
        else:
            ozellikler.append("")

        # Extract the examples for each anlam
        assert len(anlam.get("orneklerListe", "")) < 2, "Length of the orneklerListe is not 1."
        if len(anlam.get("orneklerListe", "")):
            ornekler.append(anlam.get("orneklerListe", "")[0].get("ornek", ""))
        else:
            ornekler.append("")

    # Append restructured data
    restructured.append({
        "madde": word,
        "lisan": language,
        "ozellik": ozellikler,
        "anlam": anlamlar,
        "ornek": ornekler
    })
    print(restructured)
    break