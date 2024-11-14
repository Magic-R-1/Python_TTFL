from x_Utilitaires import *

print(obtenir_joueurID_avec_joueurNom("John Collins"))

ids_joueurs = [1630578, 1641708]

for player_id in ids_joueurs:
    DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id).get_data_frames()[0]
    TEAM_CITY = DF_joueur_info['TEAM_CITY'].iloc[0]
    TEAM_NAME = DF_joueur_info['TEAM_NAME'].iloc[0]
    print(TEAM_CITY + " " + TEAM_NAME)