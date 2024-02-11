from nba_api.stats.endpoints import playernextngames, playergamelog, teamgamelog, commonplayerinfo, boxscoretraditionalv2
from nba_api.stats.static import teams
from json.decoder import JSONDecodeError
import pickle
from datetime import date

ma_saison = '2023'

prochains_matchs_data_dict = {}
game_log_data_dict = {}
equipe_derniers_matchs_dict = {}
joueur_info_dict = {}
liste_equipes_dict = {}
cache_match_data = {}
cache_postes_joueurs = {}
cache_abv_equipes = {} # Définir un dictionnaire global pour stocker les abréviations des équipes

# ----------------------------------------
# Obtenir les prochains matchs d'un joueur
def obtenir_prochains_matchs_DF_globaux(joueur_id, nb_matchs=None):
    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from z_Utilitaires import obtenir_un_coequipier_dans_equipe_avec_joueurID, obtenir_joueurNom_avec_joueurID

    global prochains_matchs_data_dict

    if joueur_id in prochains_matchs_data_dict and prochains_matchs_data_dict[joueur_id] is not None:
        df_prochains_matchs = prochains_matchs_data_dict[joueur_id].copy()
    else:
        try:
            prochains_matchs = playernextngames.PlayerNextNGames(player_id=joueur_id)
        except JSONDecodeError: # Erreur avec PlayerNextNGames sur certains joueurs, sans raison aparent, donc on prends l'id d'un coéquipier
            nouvel_id = obtenir_un_coequipier_dans_equipe_avec_joueurID(joueur_id)
            nouveau_nom = obtenir_joueurNom_avec_joueurID(nouvel_id)
            joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

            prochains_matchs = playernextngames.PlayerNextNGames(player_id=nouvel_id)
            print(f" {joueur_nom} ({joueur_id}) remplacé par {nouveau_nom} ({nouvel_id}) pour l'enpoint PlayerNextNGames")
        df_prochains_matchs = prochains_matchs.get_data_frames()[0]
        prochains_matchs_data_dict[joueur_id] = df_prochains_matchs

    if nb_matchs is not None:
        df_prochains_matchs = df_prochains_matchs.head(nb_matchs)

    return df_prochains_matchs

# ----------------------------------------
# Obtenir les games log d'un joueur (matchs passés)
def obtenir_game_log_DF_globaux(joueur_id, nb_matchs=None):
    global game_log_data_dict

    if joueur_id in game_log_data_dict and game_log_data_dict[joueur_id] is not None:
        df_joueur = game_log_data_dict[joueur_id].copy()
    else:
        game_log = playergamelog.PlayerGameLog(player_id=joueur_id, season=ma_saison)  
        df_joueur = game_log.get_data_frames()[0]
        game_log_data_dict[joueur_id] = df_joueur

    if nb_matchs is not None:
        df_joueur = df_joueur.head(nb_matchs)

    return df_joueur

# ----------------------------------------
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

# ----------------------------------------
# Obtenir les informations d'un joueur
def obtenir_informations_joueur_DF_globaux(joueur_id):
    global joueur_info_dict

    if joueur_id in joueur_info_dict and joueur_info_dict[joueur_id] is not None:
        return joueur_info_dict[joueur_id]
    else:
        joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        joueur_info_data = joueur_info.get_data_frames()[0]
        joueur_info_dict[joueur_id] = joueur_info_data
        return joueur_info_data

# Fonction pour obtenir la liste des équipes
def obtenir_liste_equipes_DF_globaux():
    global liste_equipes_dict

    if 'liste_equipes' in liste_equipes_dict and liste_equipes_dict['liste_equipes'] is not None:
        return liste_equipes_dict['liste_equipes']
    else:
        liste_equipes = teams.get_teams()
        liste_equipes_dict['liste_equipes'] = liste_equipes
        return liste_equipes

# Fonction pour obtenir la liste des équipes avec leurs identifiants
def obtenir_liste_equipes_ids_DF_globaux():
    liste_equipes = teams.get_teams()
    liste_equipes_ids = [equipe['id'] for equipe in liste_equipes]
    return liste_equipes_ids

def sauvegarder_cache_match_data(cache_match_data):
    # Générer le nom de fichier avec la date du jour
    today = date.today().strftime("%Y_%m_%d")
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2_cache/cache_match_data_{today}.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_match_data, file)

def charger_cache_match_data():
    global cache_match_data  # Pour accéder au dictionnaire global

    # Générer le nom de fichier avec la date du jour
    today = date.today().strftime("%Y_%m_%d")
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/BoxScoreTraditionalV2_cache/cache_match_data_{today}.pkl"
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

def sauvegarder_cache_postes_joueurs(cache_postes_joueurs):
    # Générer le nom de fichier avec la date du jour
    today = date.today().strftime("%Y_%m_%d")
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_postes_joueurs_{today}.pkl"
    # Sauvegarder le cache dans le fichier
    with open(file_path, 'wb') as file:
        pickle.dump(cache_postes_joueurs, file)

def charger_cache_postes_joueurs():
    global cache_postes_joueurs  # Pour accéder au dictionnaire global

    # Générer le nom de fichier avec la date du jour
    today = date.today().strftime("%Y_%m_%d")
    file_path = f"C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Cache/CommonPlayerInfo_cache/cache_postes_joueurs_{today}.pkl"
    # Charger le cache depuis le fichier
    try:
        with open(file_path, 'rb') as file:
            cache_postes_joueurs = pickle.load(file)
    except FileNotFoundError:
        cache_postes_joueurs = {}
    return cache_postes_joueurs

# Construire un cache avec un dictionnaire qui contient l'id des joueurs et leur poste
def remplir_cache_poste_abrege_data(player_id):
    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from z_Utilitaires import obtenir_joueurPosteAbregee_avec_joueurID

    global cache_postes_joueurs

    if player_id in cache_postes_joueurs:
        poste = cache_postes_joueurs[player_id]
    else:
        poste = obtenir_joueurPosteAbregee_avec_joueurID(player_id)
        cache_postes_joueurs[player_id] = poste

    return poste

# Construire un cache avec un dictionnaire qui contient l'id des équipes et leur abbréviation
def remplir_cache_equipe_abv_data(equipe_id):
    # Importer le module à l'intérieur de la fonction pour éviter l'importation circulaire
    from z_Utilitaires import obtenir_equipeABV_avec_equipeID

    global cache_abv_equipes

    if equipe_id in cache_abv_equipes:
        abv_equipe = cache_abv_equipes[equipe_id]
    else:
        abv_equipe = obtenir_equipeABV_avec_equipeID(equipe_id)
        cache_abv_equipes[equipe_id] = abv_equipe

    return abv_equipe