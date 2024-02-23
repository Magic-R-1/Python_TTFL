from nba_api.stats.endpoints import playernextngames, playergamelog, teamgamelog, commonplayerinfo, boxscoretraditionalv2
from nba_api.stats.static import teams
from json.decoder import JSONDecodeError
import pickle

ma_saison = '2023'

prochains_matchs_data_dict = {}
game_log_data_dict = {}
equipe_derniers_matchs_dict = {}
cache_CommonPlayerInfo = {}
liste_equipes_dict = {}
cache_match_data = {}
cache_abv_equipes = {}

# --------------------------------------------------------------------------------------------
# Obtenir les prochains matchs d'un joueur
def obtenir_prochains_matchs_DF_globaux(joueur_id, nb_matchs=None):
    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from x_Utilitaires import obtenir_un_coequipier_dans_equipe_avec_joueurID, obtenir_joueurNom_avec_joueurID

    global prochains_matchs_data_dict
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)
    joueur_key = str(joueur_id) + '_' + joueur_nom

    if joueur_id in prochains_matchs_data_dict and prochains_matchs_data_dict[joueur_key] is not None:
        DF_prochains_matchs = prochains_matchs_data_dict[joueur_key].copy()
    else:
        try:
            prochains_matchs = playernextngames.PlayerNextNGames(player_id=joueur_id)
        except JSONDecodeError: # Erreur avec PlayerNextNGames sur certains joueurs, sans raison aparent, donc on prends l'id d'un coéquipier
            nouvel_id = obtenir_un_coequipier_dans_equipe_avec_joueurID(joueur_id)
            nouveau_nom = obtenir_joueurNom_avec_joueurID(nouvel_id)

            prochains_matchs = playernextngames.PlayerNextNGames(player_id=nouvel_id)
            print(f"{joueur_nom} ({joueur_id}) remplacé par {nouveau_nom} ({nouvel_id}) pour l'erreur de l'enpoint PlayerNextNGames")
        DF_prochains_matchs = prochains_matchs.get_data_frames()[0]
        prochains_matchs_data_dict[joueur_key] = DF_prochains_matchs

    if nb_matchs is not None:
        DF_prochains_matchs = DF_prochains_matchs.head(nb_matchs)

    return DF_prochains_matchs
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Obtenir les games log d'un joueur (matchs passés)
def obtenir_game_log_DF_globaux(joueur_id, nb_matchs=None):
    global game_log_data_dict

    if joueur_id in game_log_data_dict and game_log_data_dict[joueur_id] is not None:
        DF_joueur = game_log_data_dict[joueur_id].copy()
    else:
        game_log = playergamelog.PlayerGameLog(player_id=joueur_id, season=ma_saison)  
        DF_joueur = game_log.get_data_frames()[0]
        game_log_data_dict[joueur_id] = DF_joueur

    if nb_matchs is not None:
        DF_joueur = DF_joueur.head(nb_matchs)

    return DF_joueur
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Obtenir les games log d'une équipe
def obtenir_equipe_derniers_matchs_DF_globaux(id_equipe, nb_matchs=None):
    global equipe_derniers_matchs_dict

    if id_equipe in equipe_derniers_matchs_dict and equipe_derniers_matchs_dict[id_equipe] is not None:
        equipe_derniers_matchs = equipe_derniers_matchs_dict[id_equipe].copy()
    else:
        team_log = teamgamelog.TeamGameLog(team_id=id_equipe, season=ma_saison)
        equipe_derniers_matchs = team_log.get_data_frames()[0]
        equipe_derniers_matchs_dict[id_equipe] = equipe_derniers_matchs

    if nb_matchs is not None:
        equipe_derniers_matchs = equipe_derniers_matchs.head(nb_matchs)

    return equipe_derniers_matchs
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir la liste des objets équipes
def obtenir_liste_equipes_DF_globaux():
    global liste_equipes_dict

    if 'liste_equipes' in liste_equipes_dict and liste_equipes_dict['liste_equipes'] is not None:
        return liste_equipes_dict['liste_equipes']
    else:
        liste_equipes = teams.get_teams()
        liste_equipes_dict['liste_equipes'] = liste_equipes
        return liste_equipes
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir la liste des équipes avec leurs identifiants
def obtenir_liste_equipes_IDs_DF_globaux():
    liste_equipes = teams.get_teams()
    liste_equipes_ids = [equipe['id'] for equipe in liste_equipes]
    return liste_equipes_ids
# --------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------
def sauvegarder_cache_CommonPlayerInfo(cache_CommonPlayerInfo):
    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_CommonPlayerInfo.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_CommonPlayerInfo, file)

def charger_cache_CommonPlayerInfo():
    global cache_CommonPlayerInfo  # Pour accéder au dictionnaire global

    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_CommonPlayerInfo.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_CommonPlayerInfo = pickle.load(file)
    except FileNotFoundError:
        cache_CommonPlayerInfo = {}
    return cache_CommonPlayerInfo

# Construire un cache avec un dictionnaire qui contient l'id des matchs et leur log
def remplir_cache_CommonPlayerInfo(joueur_id):
    global cache_CommonPlayerInfo

    if joueur_id in cache_CommonPlayerInfo and cache_CommonPlayerInfo[joueur_id] is not None:
        return cache_CommonPlayerInfo[joueur_id]
    else:
        joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        joueur_info_data = joueur_info.get_data_frames()[0]
        cache_CommonPlayerInfo[joueur_id] = joueur_info_data
        return joueur_info_data

# Fonction pour simplier les appellations
def obtenir_CommonPlayerInfo_DF_globaux(joueur_id):
    
    charger_cache_CommonPlayerInfo()
    remplir_cache_CommonPlayerInfo(joueur_id)
    sauvegarder_cache_CommonPlayerInfo(cache_CommonPlayerInfo)

    return remplir_cache_CommonPlayerInfo(joueur_id)
# --------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------
def sauvegarder_cache_match_data(cache_match_data):
    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2_cache/cache_match_data.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_match_data, file)

def charger_cache_match_data():
    global cache_match_data  # Pour accéder au dictionnaire global

    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2_cache/cache_match_data.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_match_data = pickle.load(file)
    except FileNotFoundError:
        cache_match_data = {}
    return cache_match_data

# Construire un cache avec un dictionnaire qui contient l'id des matchs et leur log
def remplir_cache_match_data(match_id):
    global cache_match_data

    if match_id not in cache_match_data:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=match_id)
        boxscore_data = boxscore.get_data_frames()
        logs_match = boxscore_data[0]
        cache_match_data[match_id] = logs_match
    else:
        logs_match = cache_match_data[match_id]

    return logs_match
# --------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------
def sauvegarder_cache_equipe_abv(cache_equipe_abv):
    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_equipe_abv.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_equipe_abv, file)

def charger_cache_equipe_abv():
    global cache_equipe_abv  # Pour accéder au dictionnaire global

    # Générer le nom de fichier
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_equipe_abv.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_equipe_abv = pickle.load(file)
    except FileNotFoundError:
        cache_equipe_abv = {}
    return cache_equipe_abv

# Construire un cache avec un dictionnaire qui contient l'id des équipes et leur abbréviation
def remplir_cache_equipe_abv(equipe_id):
    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from x_Utilitaires import obtenir_equipeABV_avec_equipeID

    global cache_abv_equipes

    if equipe_id in cache_abv_equipes:
        abv_equipe = cache_abv_equipes[equipe_id]
    else:
        abv_equipe = obtenir_equipeABV_avec_equipeID(equipe_id)
        cache_abv_equipes[equipe_id] = abv_equipe

    return abv_equipe
# --------------------------------------------------------------------------------------------