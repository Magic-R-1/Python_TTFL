import pandas as pd
from Gestion_SQL import *

def RecupererJoueurs(player_ids, engine):
    liste_joueurs = []
    for player_id in player_ids:
        try:
            # Écrire la requête SQL pour récupérer les informations du joueur
            query = f"SELECT * FROM player WHERE id = {player_id};"

            # Exécuter la requête et charger les résultats dans un DataFrame
            joueur_df = pd.read_sql(query, engine)

            # Spécifier l'équivalence des colonnes
            Player_DB_API_column_equivalences = {
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
            joueur_df.rename(columns=Player_DB_API_column_equivalences, inplace=True)
            liste_joueurs.append(joueur_df)
        except Exception as e:
            print("Erreur lors de la récupération du joueur avec l'ID :", player_id, "-", e)
    return pd.concat(liste_joueurs, ignore_index=True)

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    
    player_ids = [202681]

    # Création de l'engine
    engine = CreerEngineSQL()

    # Effectuer l'opération SQL
    joueurs_df = RecupererJoueurs(player_ids, engine)

    # Suppression de l'engine
    engine.dispose()

    print(joueurs_df)
