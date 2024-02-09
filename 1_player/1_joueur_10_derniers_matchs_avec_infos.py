import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo, playergamelog, teamgamelog
from nba_api.stats.static import players, teams

# Fonction pour obtenir l'équipe du joueur
def obtenir_equipe_joueur(joueur_id):
    try:
        # Obtenir les informations du joueur
        joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        joueur_info = joueur_info.common_player_info.get_data_frame()

        # Extraire l'équipe actuelle du joueur
        id_equipe = joueur_info['TEAM_ID'].iloc[0]

        return id_equipe
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# Fonction de calcul du score TTFL
def calcul_score_TTFL(row):
    return (
        row["PTS"] +
        row["REB"] +
        row["AST"] +
        row["STL"] +
        row["BLK"] -
        row["TOV"] +
        (row["FGM"] - (row["FGA"] - row["FGM"])) +
        (row["FG3M"] - (row["FG3A"] - row["FG3M"])) +
        (row["FTM"] - (row["FTA"] - row["FTM"]))
    )

def construire_tableau_10_derniers_matchs(joueur_id, dates_10_derniers_matchs):
    # Obtenir les statistiques de jeu pour les 10 derniers matchs
    game_log = playergamelog.PlayerGameLog(player_id=joueur_id, season='2023')
    df_joueur = game_log.get_data_frames()[0].head(10)

    # Fusionner avec la liste complète de dates
    df_joueur_complet = pd.DataFrame({'GAME_DATE': dates_10_derniers_matchs}).merge(df_joueur, how='left', on='GAME_DATE')

    # Créer le tableau avec les informations nécessaires
    tableau_matchs = pd.DataFrame({
        'Date': df_joueur_complet['GAME_DATE'],
        'Adversaire': df_joueur_complet['MATCHUP'],
        'Score_TTFL': df_joueur_complet.apply(calcul_score_TTFL, axis=1)
    })

    # Remplacer les valeurs NaN (match non joué) par 0 dans la colonne Score_TTFL
    tableau_matchs['Score_TTFL'] = tableau_matchs['Score_TTFL'].fillna(0)

    return tableau_matchs

# Exemple d'utilisation avec un ID de joueur
joueur_id = 1631105  # Remplacez cela par l'ID du joueur souhaité

# Obtenez l'équipe du joueur
id_equipe = obtenir_equipe_joueur(joueur_id)

if id_equipe:
    # Obtenez les statistiques de jeu pour l'équipe des Lakers
    team_log = teamgamelog.TeamGameLog(team_id=id_equipe, season='2023')
    df_team = team_log.get_data_frames()[0]

    # Obtenez les dates des 10 derniers matchs des Lakers
    dates_10_derniers_matchs = df_team.head(10)['GAME_DATE'].tolist()

    # Construisez le tableau des 10 derniers matchs
    tableau_10_derniers_matchs = construire_tableau_10_derniers_matchs(joueur_id, dates_10_derniers_matchs)

    # Affichez le tableau des 10 derniers matchs
    print(tableau_10_derniers_matchs)
else:
    print("Impossible d'obtenir l'équipe du joueur.")