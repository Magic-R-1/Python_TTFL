import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playernextngames, commonplayerinfo

def obtenir_equipe_joueur(joueur_id):
    try:
        joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        joueur_info = joueur_info.common_player_info.get_data_frame()
        id_equipe_joueur = joueur_info['TEAM_ID'].iloc[0]
        return id_equipe_joueur
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention de l'équipe du joueur {joueur_id}: {str(e)}")
        return None

def obtenir_prochains_matchs_joueurs(ids_joueurs, nb_matchs=5):
    tableau_prochains_matchs = pd.DataFrame()

    for joueur_id in ids_joueurs:
        joueur_info = players.find_player_by_id(joueur_id)
        joueur_nom = joueur_info['full_name']

        id_equipe_joueur = obtenir_equipe_joueur(joueur_id)

        if id_equipe_joueur is not None:
            prochains_matchs = playernextngames.PlayerNextNGames(player_id=joueur_id, number_of_games=nb_matchs)
            df_prochains_matchs = prochains_matchs.get_data_frames()[0]

            adversaires = []

            for i in range(1, nb_matchs + 1):
                if id_equipe_joueur == df_prochains_matchs.loc[i - 1, 'HOME_TEAM_ID']:
                    adversaires.append(df_prochains_matchs.loc[i - 1, 'VISITOR_TEAM_ABBREVIATION'])
                else:
                    adversaires.append(df_prochains_matchs.loc[i - 1, 'HOME_TEAM_ABBREVIATION'])

            colonnes_adversaires = [f'M+{i}' for i in range(1, nb_matchs + 1)]

            tableau_prochains_matchs = pd.concat([tableau_prochains_matchs, pd.DataFrame({
                'Joueur': [joueur_nom],
                **dict(zip(colonnes_adversaires, adversaires))
            })], ignore_index=True)

    return tableau_prochains_matchs

# Liste d'identifiants de joueurs
ids_joueurs = [1629029, 203081, 1628368, 1627734, 1628973, 203944, 1626157, 202695, 2544, 202331, 1630567, 201939, 1630595, 1627750, 201935, 203114, 204001, 1628398, 1629008, 201566, 1626179, 203952, 1630559, 1626156, 1627832, 202330]

# Nombre de prochains matchs à récupérer
nb_prochains_matchs = 5

# Obtient le tableau des prochains matchs pour la liste de joueurs
tableau_prochains_matchs = obtenir_prochains_matchs_joueurs(ids_joueurs, nb_prochains_matchs)

# Affiche le tableau
print(tableau_prochains_matchs)