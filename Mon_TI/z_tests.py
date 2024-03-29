from nba_api.stats.endpoints import playernextngames, playergamelog, teamgamelog, commonplayerinfo, boxscoretraditionalv2
from nba_api.stats.static import teams

from x_Utilitaires import *

# print(obtenir_joueurID_avec_joueurNom("Cam Thomas"))

DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=2544).get_data_frames()[0]
exporter_vers_Excel_generique(DF_joueur_info,"DF_joueur_info")