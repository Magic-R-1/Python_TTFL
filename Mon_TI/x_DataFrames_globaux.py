from nba_api.stats.endpoints import playernextngames, playergamelog, teamgamelog, commonplayerinfo, boxscoretraditionalv2
from nba_api.stats.static import teams
from json.decoder import JSONDecodeError
import pickle

ma_saison = '2023'

liste_equipes = None
dictionnaire_TeamGameLog = {}
dictionnaire_PlayerNextNGames = {}
dictionnaire_PlayerGameLog = {}

cache_CommonPlayerInfo = {}
cache_BoxScoreTraditionalV2 = {}

# --------------------------------------------------------------------------------------------
# Obtenir les games log d'une équipe
def obtenir_equipe_derniers_matchs_DF_globaux(id_equipe, nb_matchs=None):
    global dictionnaire_TeamGameLog

    if id_equipe in dictionnaire_TeamGameLog and dictionnaire_TeamGameLog[id_equipe] is not None:
        equipe_derniers_matchs = dictionnaire_TeamGameLog[id_equipe].copy()
    else:
        team_log = teamgamelog.TeamGameLog(team_id=id_equipe, season=ma_saison)
        print(f"Appel à l'API TeamGameLog")
        equipe_derniers_matchs = team_log.get_data_frames()[0]
        dictionnaire_TeamGameLog[id_equipe] = equipe_derniers_matchs

    if nb_matchs is not None:
        equipe_derniers_matchs = equipe_derniers_matchs.head(nb_matchs)

    return equipe_derniers_matchs
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir la liste des objets équipes
def obtenir_liste_equipes_DF_globaux():
    global liste_equipes

    if liste_equipes is not None:
        return liste_equipes
    else:
        liste_equipes = teams.get_teams()
        print(f"Appel à l'API teams")
        return liste_equipes
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir la liste des équipes avec leurs identifiants
def obtenir_liste_equipes_IDs_DF_globaux():
    liste_equipes = obtenir_liste_equipes_DF_globaux()
    liste_equipes_ids = [equipe['id'] for equipe in liste_equipes]
    return liste_equipes_ids
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir les games log d'un joueur avec gestion du cache
def obtenir_PlayerGameLog_DF_globaux(joueur_id, nb_matchs=None):

    global dictionnaire_PlayerGameLog

    if joueur_id in dictionnaire_PlayerGameLog and dictionnaire_PlayerGameLog[joueur_id] is not None:
        return dictionnaire_PlayerGameLog[joueur_id]
    else:
        game_log = playergamelog.PlayerGameLog(player_id=joueur_id, season=ma_saison)
        print(f'Appel API PlayerGameLog pour {joueur_id}')
        DF_joueur = game_log.get_data_frames()[0]
        dictionnaire_PlayerGameLog[joueur_id] = DF_joueur

        if nb_matchs is not None:
            DF_joueur = DF_joueur.head(nb_matchs)

        return DF_joueur
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir prochains matchs d'un joueur avec gestion du cache
def obtenir_PlayerNextNGames_DF_globaux(joueur_id):

    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from x_Utilitaires import obtenir_un_coequipier_dans_equipe_avec_joueurID, obtenir_joueurNom_avec_joueurID

    global dictionnaire_PlayerNextNGames
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    if joueur_id in dictionnaire_PlayerNextNGames and dictionnaire_PlayerNextNGames[joueur_id] is not None:
        DF_prochains_matchs = dictionnaire_PlayerNextNGames[joueur_id].copy()
    else:
        try:
            prochains_matchs = playernextngames.PlayerNextNGames(player_id=joueur_id)
            print(f'Appel API PlayerNextNGames pour {joueur_nom} ({joueur_id})')
        except JSONDecodeError: # Erreur avec PlayerNextNGames sur certains joueurs, sans raison apparente, on prend donc l'id d'un coéquipier
            nouvel_id = obtenir_un_coequipier_dans_equipe_avec_joueurID(joueur_id)
            nouveau_nom = obtenir_joueurNom_avec_joueurID(nouvel_id)

            prochains_matchs = playernextngames.PlayerNextNGames(player_id=nouvel_id)
            print(f"Appel API PlayerNextNGames pour {joueur_nom} ({joueur_id}) remplacé par {nouveau_nom} ({nouvel_id})")
        DF_prochains_matchs = prochains_matchs.get_data_frames()[0]
        dictionnaire_PlayerNextNGames[joueur_id] = DF_prochains_matchs

    return DF_prochains_matchs
# --------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------
# À METTRE À JOUR APRÈS TRANSFERTS

# Fonction pour sauvegarder le cache
def sauvegarder_cache_CommonPlayerInfo():

    # Pour accéder au dictionnaire global
    global cache_CommonPlayerInfo

    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo/cache_CommonPlayerInfo.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_CommonPlayerInfo, file)

# Fonction pour charger le cache
def charger_cache_CommonPlayerInfo():

    # Pour accéder au dictionnaire global
    global cache_CommonPlayerInfo

    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo/cache_CommonPlayerInfo.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_CommonPlayerInfo = pickle.load(file)
    except FileNotFoundError:
        cache_CommonPlayerInfo = {}
    return cache_CommonPlayerInfo

# Construire un cache avec un dictionnaire qui contient l'id des matchs et leur log
def obtenir_CommonPlayerInfo_DF_globaux(joueur_id):
    
    # Pour accéder au dictionnaire global
    global cache_CommonPlayerInfo

    if joueur_id in cache_CommonPlayerInfo and cache_CommonPlayerInfo[joueur_id] is not None:
        return cache_CommonPlayerInfo[joueur_id]
    else:
        DF_joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        print(f"Appel à l'API CommonPlayerInfo")
        DF_joueur_info = DF_joueur_info.get_data_frames()[0]
        cache_CommonPlayerInfo[joueur_id] = DF_joueur_info
        return DF_joueur_info
# --------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------
# Fonction pour sauvegarder le cache
def sauvegarder_cache_BoxScoreTraditionalV2():
    
    # Pour accéder au dictionnaire global
    global cache_BoxScoreTraditionalV2

    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2/cache_BoxScoreTraditionalV2.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_BoxScoreTraditionalV2, file)

# Fonction pour charger le cache
def charger_cache_BoxScoreTraditionalV2():
    
    # Pour accéder au dictionnaire global
    global cache_BoxScoreTraditionalV2

    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2/cache_BoxScoreTraditionalV2.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_BoxScoreTraditionalV2 = pickle.load(file)
    except FileNotFoundError:
        cache_BoxScoreTraditionalV2 = {}
    return cache_BoxScoreTraditionalV2

# Construire un cache avec un dictionnaire qui contient l'id des matchs et leur log
def obtenir_BoxScoreTraditionalV2_DF_globaux(match_id):
    
    # Pour accéder au dictionnaire global
    global cache_BoxScoreTraditionalV2

    if match_id not in cache_BoxScoreTraditionalV2:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=match_id)
        print(f"Appel à l'API BoxScoreTraditionalV2")
        boxscore_data = boxscore.get_data_frames()
        DF_logs_match = boxscore_data[0]
        cache_BoxScoreTraditionalV2[match_id] = DF_logs_match
    else:
        DF_logs_match = cache_BoxScoreTraditionalV2[match_id]
    return DF_logs_match
# --------------------------------------------------------------------------------------------