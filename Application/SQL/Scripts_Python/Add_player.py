from sqlalchemy.exc import IntegrityError
from nba_api.stats.endpoints import commonplayerinfo
from Gestion_SQL import *

import pandas as pd

def addLinePlayers(player_ids, engine):
    for player_id in player_ids:
        try:
            # Charger votre DataFrame
            DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
            print(DF_joueur_info)


            df = pd.DataFrame(DF_joueur_info)

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

            # Renommer les colonnes du DataFrame en utilisant les correspondances spécifiées
            df = df.rename(columns=Player_API_DB_column_equivalences)

            # Stocker le DataFrame dans la base de données
            table_name = 'player'
            df.to_sql(table_name, engine, if_exists='append', index=False)
        except IntegrityError as e:
            print("Erreur d'intégrité lors de l'insertion dans la base de données pour le joueur avec l'ID :", player_id, "-", e)

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    
    player_ids = [2]  # Exemple de liste d'IDs de joueurs

    engine = CreerEngineSQL()

    # Effectuer l'opération SQL
    addLinePlayers(player_ids, engine)

    SupprimerEngineSQL(engine)
