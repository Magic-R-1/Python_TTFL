import pandas as pd
from datetime import datetime, timedelta
# from nba_api.stats.endpoints import player-gamelog
from z_DataFrames_globaux import obtenir_game_log_DF_globaux

from z_Utilitaires import obtenir_joueurNom_avec_joueurID

def get_games_played_last_X_days(joueur_id,number_of_days_matchs_joues):
    
    # Variable
    number_of_games = (number_of_days_matchs_joues//2)+5

    # Trouver le nom joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Obtenez la date actuelle et la date d'il y a 30 jours
    start_date = datetime.now() - timedelta(days=30)

    # Utilisez l'endpoint player-gamelog pour obtenir les statistiques de jeu du joueur
    df_joueur = obtenir_game_log_DF_globaux(joueur_id)
    
    df_joueur['GAME_DATE'] = pd.to_datetime(df_joueur['GAME_DATE'], format='%b %d, %Y') # Conversion en DataFrame panda, avec spécification du format

    # Filtrer les dates supérieures ou égales à start_date
    dates_superieures_ou_egales = df_joueur['GAME_DATE'] >= start_date

    # Calculer le nombre de dates supérieures ou égales à start_date
    nombre_dates_superieures_ou_egales = dates_superieures_ou_egales.sum()

    return [joueur_nom, nombre_dates_superieures_ou_egales]

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [2544]

    # Nombre de matchs à considérer pour les 30 derniers jours
    number_of_days_matchs_joues = 30

    # Créer le DataFrame final avec les colonnes nécessaires
    df_matchs_joues_X_derniers_jours = pd.DataFrame(columns=['Joueur', 'GP'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        df_matchs_joues_X_derniers_jours.loc[len(df_matchs_joues_X_derniers_jours)] = get_games_played_last_X_days(joueur_id,number_of_days_matchs_joues)

    # Enlever les joueurs
    df_matchs_joues_X_derniers_jours = df_matchs_joues_X_derniers_jours.drop(columns=['Joueur'])

    # Print du tableau
    print(df_matchs_joues_X_derniers_jours)