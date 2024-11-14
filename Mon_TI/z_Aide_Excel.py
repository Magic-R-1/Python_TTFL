from x_Utilitaires import *

def obtenirIDjoueur():
    print(obtenir_joueurID_avec_joueurNom("John Collins"))

def obtenirListeIDsEquipes():
    ids_joueurs = [1630578, 1641708]

    for player_id in ids_joueurs:
        DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id).get_data_frames()[0]
        TEAM_CITY = DF_joueur_info['TEAM_CITY'].iloc[0]
        TEAM_NAME = DF_joueur_info['TEAM_NAME'].iloc[0]
        print(TEAM_CITY + " " + TEAM_NAME)

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    obtenirIDjoueur()
    #obtenirListeIDsEquipes()