# OK pour une équipe

import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Python_TTFL/Mon_TI')

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import boxscoretraditionalv2
from x_Utilitaires import obtenir_equipeID_avec_equipeNom, obtenir_joueurPosteAbregee_avec_joueurID, calcul_score_TTFL, obtenir_equipeABV_avec_equipeID
from x_DataFrames_globaux import obtenir_equipe_derniers_matchs_DF_globaux

def obtenir_liste_ids_matchs_equipe(equipe_id):
    equipe_matchs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)
    DF_matchs_equipe = equipe_matchs[['Game_ID']]
    return DF_matchs_equipe

def obtenir_logs_match_avec_matchID(match_id, equipe_id):
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=match_id)
    boxscore_data = boxscore.get_data_frames()
    logs_match = boxscore_data[0]
    logs_equipe = logs_match.loc[logs_match['TEAM_ID'] != equipe_id]
    logs_equipe = logs_equipe.loc[logs_match['MIN'].notnull()]
    logs_equipe['poste'] = logs_equipe['PLAYER_ID'].apply(obtenir_joueurPosteAbregee_avec_joueurID)
    logs_equipe['Score_TTFL'] = logs_equipe.apply(calcul_score_TTFL, axis=1).astype(int)
    logs_equipe['MIN'] = logs_equipe['MIN'].str.extract(r'(\d+)').astype(int)
    logs_equipe['Score_TTFL_MIN'] = logs_equipe['MIN'] * logs_equipe['Score_TTFL']
    return logs_equipe

def obtenir_DF_moyenne_par_poste(match_id, equipe_id):
    logs_equipe = obtenir_logs_match_avec_matchID(match_id, equipe_id)
    DF_postes = pd.DataFrame(['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'], columns=['Poste'])
    sommes_TTFL = []
    sommes_MIN = []

    for poste in DF_postes['Poste']:
        lignes_poste = logs_equipe[logs_equipe['poste'] == poste]
        somme_score_ttfl = lignes_poste['Score_TTFL_MIN'].sum()
        somme_minutes = lignes_poste['MIN'].sum()
        sommes_TTFL.append(somme_score_ttfl)
        sommes_MIN.append(somme_minutes)

    DF_postes['Somme_TTFL'] = sommes_TTFL
    DF_postes['Somme_MIN'] = sommes_MIN

    return DF_postes

equipe_nom = 'Los Angeles Lakers'
equipe_id = obtenir_equipeID_avec_equipeNom(equipe_nom)
equipe_ABV = obtenir_equipeABV_avec_equipeID(equipe_id)
DF_matchs_equipe = obtenir_liste_ids_matchs_equipe(equipe_id)
total_matchs = len(DF_matchs_equipe)

# Création d'un DataFrame pour stocker les résultats
DF_resultat = pd.DataFrame(columns=['Poste'])

# Initialisation des listes pour stocker les sommes totales
somme_ttfl_par_poste = []
somme_min_par_poste = []

# Boucle sur chaque match dans DF_matchs_equipe
for index, match_id in enumerate(DF_matchs_equipe['Game_ID'], start=1):

    progression = (index / total_matchs) * 100
    message = f"Match {index} sur {total_matchs} ({progression:.2f}%)"
    sys.stdout.write('\r' + message)
    sys.stdout.flush()

    # Obtention des statistiques par poste pour ce match
    DF_statistiques_match = obtenir_DF_moyenne_par_poste(match_id, equipe_id)

    # Somme des valeurs de Somme_TTFL et Somme_MIN par poste
    somme_ttfl_par_poste.append(DF_statistiques_match['Somme_TTFL'].values)
    somme_min_par_poste.append(DF_statistiques_match['Somme_MIN'].values)

# Somme des valeurs par poste sur tous les matchs
somme_ttfl_totale_par_poste = np.sum(somme_ttfl_par_poste, axis=0)
somme_min_totale_par_poste = np.sum(somme_min_par_poste, axis=0)
moyenne_ttfl_ponderee = np.round(somme_ttfl_totale_par_poste / somme_min_totale_par_poste, 1)

# Création du DataFrame final
DF_final = pd.DataFrame({
    'Poste': ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'],
    'Somme_TTFL': somme_ttfl_totale_par_poste,
    'Somme_MIN': somme_min_totale_par_poste,
    f'{equipe_ABV}': moyenne_ttfl_ponderee
})

# Aller à la ligne après l'affichage de la progression
print()
print(DF_final)