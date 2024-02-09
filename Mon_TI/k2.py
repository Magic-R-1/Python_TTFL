# Code donnant la somme TTFL et minutes par match pour tous les matchs pour une équipe

import pandas as pd
from nba_api.stats.endpoints import boxscoretraditionalv2
from z_Utilitaires import obtenir_equipeID_avec_equipeNom, obtenir_joueurPosteAbregee_avec_joueurID, calcul_score_TTFL
from z_DataFrames_globaux import obtenir_equipe_derniers_matchs_DF_globaux

def obtenir_liste_ids_matchs_equipe(equipe_id):
    equipe_matchs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)
    df_matchs_equipe = equipe_matchs[['Game_ID']]
    return df_matchs_equipe

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

def obtenir_df_moyenne_par_poste(match_id, equipe_id):
    logs_equipe = obtenir_logs_match_avec_matchID(match_id, equipe_id)
    df_postes = pd.DataFrame(['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'], columns=['Poste'])
    sommes_TTFL = []
    sommes_MIN = []

    for poste in df_postes['Poste']:
        lignes_poste = logs_equipe[logs_equipe['poste'] == poste]
        somme_score_ttfl = lignes_poste['Score_TTFL_MIN'].sum()
        somme_minutes = lignes_poste['MIN'].sum()
        sommes_TTFL.append(somme_score_ttfl)
        sommes_MIN.append(somme_minutes)

    df_postes['Somme_TTFL'] = sommes_TTFL
    df_postes['Somme_MIN'] = sommes_MIN

    return df_postes

equipe_nom = 'Los Angeles Lakers'
equipe_id = obtenir_equipeID_avec_equipeNom(equipe_nom)
df_matchs_equipe = obtenir_liste_ids_matchs_equipe(equipe_id)

# Création d'un DataFrame pour stocker les résultats
df_resultat = pd.DataFrame(columns=['Poste'])

# Boucle sur chaque match dans df_matchs_equipe
for i, match_id in enumerate(df_matchs_equipe['Game_ID'], start=1):

    if i == 1:
        logs_equipe = obtenir_logs_match_avec_matchID(match_id, equipe_id)
        print(logs_equipe)
        break

    # Obtention des statistiques par poste pour ce match
    df_statistiques_match = obtenir_df_moyenne_par_poste(match_id, equipe_id)
    # Renommage des colonnes pour ce match
    df_statistiques_match.columns = [f'{col}_Match_{i}' if col not in ['Poste'] else col for col in df_statistiques_match.columns]
    # Concaténation des résultats avec le DataFrame global
    df_resultat = pd.concat([df_resultat, df_statistiques_match], axis=1)

print(df_resultat)
df_resultat.to_excel('nom_du_fichier.xlsx', index=False)