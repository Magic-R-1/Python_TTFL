import pandas as pd
from sqlalchemy.exc import IntegrityError

from nba_api.stats.endpoints import commonplayerinfo

from Gestion_SQL import *

import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL')
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Application')
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Application/Python')
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Application/SQL')
from Python.x_Utilitaires import *

def addLinePlayers(player_ids, engine):
    for player_id in player_ids:
        
        try:
            # Chargement du DF CommonPlayerInfo
            DF_joueur_CommonPlayerInfo = pd.DataFrame(commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0])

            # Spécifier l'équivalence des colonnes
            Player_API_DB_column_equivalences = {
                'PERSON_ID': 'id',
                'FIRST_NAME': 'first_name',
                'LAST_NAME': 'last_name',
                'DISPLAY_FIRST_LAST': 'display_first_last',
                'DISPLAY_LAST_COMMA_FIRST': 'display_last_comma_first',
                'DISPLAY_FI_LAST': 'display_fi_last',
                'PLAYER_SLUG': 'player_slug',
                'BIRTHDATE': 'birthdate',
                'SCHOOL': 'school',
                'COUNTRY': 'country',
                'LAST_AFFILIATION': 'last_affiliation',
                'HEIGHT': 'height',
                'WEIGHT': 'weight',
                'SEASON_EXP': 'season_exp',
                'JERSEY': 'jersey',
                'POSITION': 'position',
                'ROSTERSTATUS': 'rosterstatus',
                'GAMES_PLAYED_CURRENT_SEASON_FLAG': 'games_played_current_season_flag',
                'TEAM_ID': 'team_id',
                'TEAM_NAME': 'team_name',
                'TEAM_ABBREVIATION': 'team_abbreviation',
                'TEAM_CODE': 'team_code',
                'TEAM_CITY': 'team_city',
                'PLAYERCODE': 'playercode',
                'FROM_YEAR': 'from_year',
                'TO_YEAR': 'to_year',
                'DLEAGUE_FLAG': 'dleague_flag',
                'NBA_FLAG': 'nba_flag',
                'GAMES_PLAYED_FLAG': 'games_played_flag',
                'DRAFT_YEAR': 'draft_year',
                'DRAFT_ROUND': 'draft_round',
                'DRAFT_NUMBER': 'draft_number',
                'GREATEST_75_FLAG': 'greatest_75_flag'
            }

            # Renommer les colonnes du DF CommonPlayerInfo en utilisant les correspondances spécifiées
            DF_joueur_CommonPlayerInfo = DF_joueur_CommonPlayerInfo.rename(columns=Player_API_DB_column_equivalences)

            # Stocker le DataFrame dans la base de données
            table_name = 'player'
            DF_joueur_CommonPlayerInfo.to_sql(table_name, engine, if_exists='append', index=False)

        except IntegrityError as e:
            error_message = "\n" + str(e)[:160] # "\n" pour revenir à la ligne, puis n'afficher que le début de l'erreur (160 premiers caractères)
            print("Erreur d'intégrité lors de la mise à jour des données pour le joueur avec l'ID :", player_id, error_message)

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    
    # Liste d'IDs de joueurs
    player_ids = [203076]

    engine = CreerEngineSQL()

    # Effectuer l'opération SQL
    addLinePlayers(player_ids, engine)

    engine.dispose()
