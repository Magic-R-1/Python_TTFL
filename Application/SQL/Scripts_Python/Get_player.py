import pandas as pd
from Gestion_SQL import *

def joueurExisteBDD(player_id):
    
    # Création de l'engine
    engine = CreerEngineSQL()

    # Écrire la requête SQL pour récupérer les informations du joueur
    query = f"SELECT * FROM player WHERE id = {player_id};"

    # Exécuter la requête et charger les résultats dans un DataFrame
    DF_joueur_info = pd.read_sql(query, engine)

    # Suppression de l'engine
    engine.dispose()

    if DF_joueur_info.empty:
        return False
    else:
        return DF_joueur_info

def RecupererJoueur(player_id):
    
    DF_joueur_info = joueurExisteBDD(player_id)

    if DF_joueur_info is not False:
        
        # Spécifier l'équivalence des colonnes
        player_db_api_column_equivalences = {
            'id': 'PERSON_ID',
            'first_name': 'FIRST_NAME',
            'last_name': 'LAST_NAME',
            'display_first_last': 'DISPLAY_FIRST_LAST',
            'display_last_comma_first': 'DISPLAY_LAST_COMMA_FIRST',
            'display_fi_last': 'DISPLAY_FI_LAST',
            'player_slug': 'PLAYER_SLUG',
            'birthdate': 'BIRTHDATE',
            'school': 'SCHOOL',
            'country': 'COUNTRY',
            'last_affiliation': 'LAST_AFFILIATION',
            'height': 'HEIGHT',
            'weight': 'WEIGHT',
            'season_exp': 'SEASON_EXP',
            'jersey': 'JERSEY',
            'position': 'POSITION',
            'rosterstatus': 'ROSTERSTATUS',
            'games_played_current_season_flag': 'GAMES_PLAYED_CURRENT_SEASON_FLAG',
            'team_id': 'TEAM_ID',
            'team_name': 'TEAM_NAME',
            'team_abbreviation': 'TEAM_ABBREVIATION',
            'team_code': 'TEAM_CODE',
            'team_city': 'TEAM_CITY',
            'playercode': 'PLAYERCODE',
            'from_year': 'FROM_YEAR',
            'to_year': 'TO_YEAR',
            'dleague_flag': 'DLEAGUE_FLAG',
            'nba_flag': 'NBA_FLAG',
            'games_played_flag': 'GAMES_PLAYED_FLAG',
            'draft_year': 'DRAFT_YEAR',
            'draft_round': 'DRAFT_ROUND',
            'draft_number': 'DRAFT_NUMBER',
            'greatest_75_flag': 'GREATEST_75_FLAG'
        }

        # Renommer les colonnes
        DF_joueur_info.rename(columns=player_db_api_column_equivalences, inplace=True)

    return DF_joueur_info

def Crer_DF_liste_joueurs_info(player_ids):
    
    # Créer une liste pour stocker les DataFrames des joueurs
    liste_df_joueurs_info = []
    
    for player_id in player_ids:
        # Récupérer les informations du joueur
        DF_joueur_info = RecupererJoueur(player_id)
        
        if DF_joueur_info is not False:
            # Ajouter le DataFrame du joueur à la liste
            liste_df_joueurs_info.append(DF_joueur_info)

    if liste_df_joueurs_info:
        # Concaténer tous les DataFrames des joueurs en un seul DataFrame
        df_liste_joueurs_info = pd.concat(liste_df_joueurs_info, ignore_index=True)
        return df_liste_joueurs_info
    else:
        print("Aucun joueur trouvé pour l'ID donnée.")

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    # Liste d'IDs de joueurs
    player_ids = [2544]

    # Création de l'engine
    # engine = CreerEngineSQL()

    # Effectuer l'opération SQL
    df_liste_joueurs_info = Crer_DF_liste_joueurs_info(player_ids)

    # Suppression de l'engine
    # engine.dispose()

    print(df_liste_joueurs_info)