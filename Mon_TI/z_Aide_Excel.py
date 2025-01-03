from x_Utilitaires import *

def obtenirIDjoueur():
    try:
        player_name="Cameron Johnson"
        print(obtenir_joueurID_avec_joueurNom(player_name))
    except Exception as e:
        print(f"Le joueur {player_name} est introuvable")

def obtenirListeIDsEquipes():
    ids_joueurs = [1630578, 1641708, 203952, 203076, 1630162, 1630559, 1628389, 203992, 203078, 1627742, 1641706, 1630595, 1630560, 1629661, 1631096, 1626156, 1642261, 203081, 1629636, 1628368, 1629028, 1627749, 201942, 1630166, 1630217, 1626164, 1627734, 1628378, 1628978, 1630596, 1630532, 1627832, 203507, 1629630, 1628973, 1631105, 1630224, 1630552, 1631114, 1627750, 201935, 1628991, 1628386, 1627759, 1628369, 203924, 202710, 203954, 1628381, 1630228, 203944, 1626157, 202695, 201142, 203114, 204001, 1628398, 202681, 1630163, 1628374, 2544, 1629029, 1629008, 1628970, 1629651, 203999, 202696, 1631094, 1627783, 202331, 1629628, 203497, 1629060, 201566, 1630567, 1628983, 201939, 202699, 1629027, 1629639, 1630169, 1630178, 1641705, 203897, 1629627]

    for player_id in ids_joueurs:
        DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id).get_data_frames()[0]
        TEAM_CITY = DF_joueur_info['TEAM_CITY'].iloc[0]
        TEAM_NAME = DF_joueur_info['TEAM_NAME'].iloc[0]
        print(TEAM_CITY + " " + TEAM_NAME)

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":
    #obtenirIDjoueur()
    obtenirListeIDsEquipes()