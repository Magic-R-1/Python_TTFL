import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Mon_TI')

import pandas as pd
from k_Impact_poste import *

# print(obtenir_delta_ttfl_postes())

# Votre DataFrame initial
data = obtenir_delta_ttfl_postes()

# Création du DataFrame à partir des données
df = pd.DataFrame(data)

# Sélection des colonnes d'intérêt (Poste et les scores pour chaque équipe)
df_selected = df[["index", "0"]]

# Renommer les colonnes pour correspondre au format souhaité
df_selected.columns = ["Team", "Value"]

# Filtrer les lignes pour exclure les en-têtes (Poste, TTFL, Minutes, Moyenne)
df_selected = df_selected[df_selected["Team"].isin([
    "ATL", "BOS", "CLE", "NOP", "CHI", "DAL", "DEN", "GSW", "HOU", "LAC", "LAL", 
    "MIA", "MIL", "MIN", "BKN", "NYK", "ORL", "IND", "PHI", "PHX", "POR", 
    "SAC", "SAS", "OKC", "TOR", "UTA", "MEM", "WAS", "DET", "CHA"
])]

# Réinitialiser l'index
df_selected.reset_index(drop=True, inplace=True)

# Afficher le DataFrame résultant
print(df_selected)
