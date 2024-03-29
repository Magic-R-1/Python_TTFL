import pandas as pd
import psycopg2
from psycopg2 import Error
from Gestion_SQL import *
from nba_api.stats.endpoints import commonplayerinfo

def addLinePlayers(player_ids, conn):
    try:
        cursor = conn.cursor()

        for player_id in player_ids:
            # Charger les nouvelles données du joueur depuis l'API NBA
            DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]

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
            DF_joueur_info = DF_joueur_info.rename(columns=Player_API_DB_column_equivalences)

            # Convertir les valeurs de type numpy.int64 en int
            DF_joueur_info = DF_joueur_info.map(lambda x: int(x) if isinstance(x, pd.Series) else x)

            # pop prends la valeur et supprime
            colonne_a_deplacer = DF_joueur_info.pop('id')

            # Réinsérer la colonne à la dernière position
            DF_joueur_info.insert(len(DF_joueur_info.columns), colonne_a_deplacer.name, colonne_a_deplacer)

            print(DF_joueur_info)

            # Construire la requête SQL UPDATE
            sql_query = """UPDATE player SET
                            first_name = %s,
                            last_name = %s,
                            display_first_last = %s,
                            display_last_comma_first = %s,
                            display_fi_last = %s,
                            player_slug = %s,
                            birthdate = %s,
                            school = %s,
                            country = %s,
                            last_affiliation = %s,
                            height = %s,
                            weight = %s,
                            season_exp = %s,
                            jersey = %s,
                            position = %s,
                            rosterstatus = %s,
                            games_played_current_season_flag = %s,
                            team_id = %s,
                            team_name = %s,
                            team_abbreviation = %s,
                            team_code = %s,
                            team_city = %s,
                            playercode = %s,
                            from_year = %s,
                            to_year = %s,
                            dleague_flag = %s,
                            nba_flag = %s,
                            games_played_flag = %s,
                            draft_year = %s,
                            draft_round = %s,
                            draft_number = %s,
                            greatest_75_flag = %s
                            WHERE id = %s"""

            # Convertir le DataFrame en liste de tuples pour l'exécution de la requête
            values = [tuple(row) for row in DF_joueur_info.values.tolist()]

            print(values)

            cursor.executemany(sql_query, values)
            conn.commit()

    except Error as e:
        print("Erreur PostgreSQL lors de la mise à jour des données :", e)

    finally:
        if conn:
            cursor.close()

# Point d'entrée du programme
if __name__ == "__main__":
    player_ids = [2]  # Exemple de liste d'IDs de joueurs

    try:
        # Se connecter à la base de données PostgreSQL
        conn = OuvrirConnSQL()

        # Effectuer l'opération SQL pour chaque joueur
        addLinePlayers(player_ids, conn)

    except Error as e:
        print("Erreur PostgreSQL lors de la connexion à la base de données :", e)

    finally:
        if conn:
            conn.close()
