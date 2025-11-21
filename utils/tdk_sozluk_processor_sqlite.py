# %%
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json

# %%
# Connect to the database
conn = sqlite3.connect(Path("utils/database_sozluk/v12/v12.gts.sqlite3.db"))

# Get all the table names
cursor = conn.cursor()
cursor.execute("SELECT name from sqlite_master WHERE type='table';")
tables = cursor.fetchall()


# %%
# Read all tables into a dictionary of DataFrames#
dfs = {}
for table_name in tables:
    table = table_name[0]
    print(f"- Reading table: {table}")
    dfs[table] = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    print(f"    ✔ Rows: {len(dfs[table])}, Columns: {len(dfs[table].columns)}")
conn.close()

# %%
dfs['ornek'][:10]

# %%
dfs['anlam'][:10]

# %%
dfs['anlam_ozellik'][:10]

# %%
dfs['atasozu'][:10]

# %%
dfs['madde'][:10]

# %%
dfs['ozellik'][:20]

# %%
dfs['yazar'][:10]

# %%
dfs['madde_atasozu'][:10]

# %%
def xind(indices):
    '''This function enhances pandas isin method'''
    if isinstance(indices, int) or isinstance(indices, np.int64):
        return [indices]
    elif isinstance(indices, list) or isinstance(indices, np.ndarray):
        return indices
    else:
        raise TypeError("Expected indices to be an int or a list.")

# %%
'''
Creation of the structure using the tables

Structure:
----------
Madde (Entry/Word)
├── Anlam (Meaning)
│   ├── [Özellik 1, Özellik 2] Anlam 1
│   │   └── Örnek 1 - Yazar 1
│   └── [Özellik 3] Anlam 2
│       └── Örnek 2 - Yazar 2
└── Madde atasözü (if exists)

Components:
-----------
- Madde: Main dictionary entry/word
- Anlam: Meaning/definition (can have multiple)
- Özellikler: Properties/attributes for each meaning
- Örnek: Example sentence/usage
- Yazar: Author/source of the example
- Madde öntakı: Related prefix entry for a proverb (optional)
'''

# Initialization
sozluk = {}

# %%
# Processing loop
for i in range(len(dfs['madde'])):
# for i in range(100): # SANITY CHECK

    # 0. Extract basic madde information
    madde = dfs['madde'].iloc[i]
    madde_id = madde['madde_id'].item() # np.int64
    madde_name = madde['madde']
    madde_birlesikler = '' if madde['birlesikler'] is None else madde['birlesikler']
    
    # 1. More detailed information
    # 1.1 Fetch the language
    madde_lisan = madde['lisan'] if madde['lisan'] != '' else 'Türkçe'

    # 1.2. Fetch the on_taki field for the proverb madde (if exists)
    is_atasozu_or_deyim =  madde_id in dfs['atasozu']['madde_id'].tolist()
    
    if is_atasozu_or_deyim:
        on_taki = ''.join(dfs['atasozu'].loc[dfs['atasozu']['on_taki'] == madde_id, 'on_taki'].tolist()) + ' '
    else:
        on_taki = ''
    madde_name_ext = on_taki + madde_name

    # 1.2. Fetch the anlam and ozellik fields for the entry
    madde_anlam = dfs['anlam'].loc[dfs['anlam']['madde_id'] == madde_id, 'anlam'].tolist()
    madde_anlam_id = dfs['anlam'].loc[dfs['anlam']['madde_id'] == madde_id, 'anlam_id'].tolist()
    madde_num_anlam = len(madde_anlam)
    
    # 2.1 Fetch the ozellik ornek, and yazar associated with each anlam
    anlam_dict = {}
    for j, anlam in enumerate(madde_anlam):
        # 2.2 Fetch anlam_ozellik
        # Flow: anlam -> anlam_id -> anlam_ozellik_id -> anlam_ozellik
        anlam_id = madde_anlam_id[j]
        anlam_ozellik_id = dfs['anlam_ozellik'].loc[dfs['anlam_ozellik']['anlam_id'].isin(xind(anlam_id)), 'ozellik_id'].tolist()
        anlam_ozellik = ', '.join(dfs['ozellik'].loc[dfs['ozellik']['ozellik_id'].isin(xind(anlam_ozellik_id)), 'tam_adi'].tolist())

        # 2.3 ornek and yazar fields for the given anlam
        # anlam_ornek -> anlam_ornek_yazar_id -> anlam_ornek_yazar
        anlam_ornek = [orn for orn in dfs['ornek'].loc[dfs['ornek']['anlam_id'].isin(xind(anlam_id)), 'ornek'].tolist() if orn]
        anlam_ornek_yazar_id = [int(yid) for yid in dfs['ornek'].loc[dfs['ornek']['anlam_id'].isin(xind(anlam_id)), 'yazar_id'].fillna('').tolist() if yid]
        anlam_ornek_yazar = [yaz for yaz in dfs['yazar'].loc[dfs['yazar']['yazar_id'].isin(xind(anlam_ornek_yazar_id)), 'tam_adi'].tolist() if yaz]
        
        # 2.4 Save the anlam-ozellik-ornek-yazar data
        anlam_dict[f"{madde_id}_{anlam_id}"] = (anlam, anlam_ozellik, anlam_ornek, anlam_ornek_yazar)
        
    # Save the dictionary item
    sozluk[f"{madde_name}_{madde_id}"] = {
        "madde_id": madde_id,
        "madde_lisan": madde_lisan,
        "madde_name": madde_name,
        "madde_name_extended": madde_name_ext,
        "is_atasozu_or_deyim": is_atasozu_or_deyim,
        "on_taki": on_taki,
        "madde_birlesikler": madde_birlesikler,
        "madde_num_anlam": madde_num_anlam,
        "anlam_id:": anlam_id,
        "anlam": anlam_dict        
    }

    # Status update
    print(f"    ({100*i/len(dfs['madde']):.2f}%) [{madde_name}] has been processed...")

# %%
# Write in a JSON file
out_file = "gts_sqlite_processed"
file_path = Path("utils/database_sozluk/v12/processed") / f"{out_file}.json"
with open(file_path, "w+", encoding="utf-8") as f:
    json.dump(sozluk, f, ensure_ascii=False, indent=2)


