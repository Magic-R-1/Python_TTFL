import pandas as pd
import time
import os
from datetime import datetime

from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static  import players

from x_DataFrames_globaux import *

# --------------------------------------------------------------------------------------------
# Fonction de calcul du score TTFL d'un joueur sur un match
def calcul_score_TTFL(row):
    Turnover = row.get("TOV", row.get("TO", 0))  # Si "TOV" n'existe pas, utilise "TO" ou 0 par défaut
    
    score_TTFL = (
        row["PTS"] +
        row["REB"] +
        row["AST"] +
        row["STL"] +
        row["BLK"] -
        Turnover +
        (row["FGM"] - (row["FGA"] - row["FGM"])) +
        (row["FG3M"] - (row["FG3A"] - row["FG3M"])) +
        (row["FTM"] - (row["FTA"] - row["FTM"]))
    )

    return score_TTFL

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir l'ID d'un joueur avec son nom
def obtenir_joueurID_avec_joueurNom(joueur_nom):
    player_dict = players.get_players()
    # print(f"Appel à l'API players")
    player =[player for player in player_dict if player['full_name']==joueur_nom][0]
    return player['id']

# --------------------------------------------------------------------------------------------
# Fonction pour obtenir la liste des IDs de tous les joueurs de la NBA
def obtenir_liste_joueurs_NBA():
    # Obtenir la liste des joueurs
    liste_joueurs = players.get_players()
    
    # Créer une liste pour stocker les joueurs avec leurs informations
    liste_joueursIDs = []
    
    # Ajouter les informations de chaque joueur à la liste
    for joueur in liste_joueurs:
        # Vérifier si le statut du joueur est actif
        if joueur['is_active']:
            liste_joueursIDs.append(joueur['id'])
    
    return liste_joueursIDs

# #######################################################
# Obtentions avec joueur_ID

# --------------------------------------------------------------------------------------------
# Obtenir le nom du joueur avec son ID
def obtenir_joueurNom_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_CommonPlayerInfo_DF_globaux(joueur_id)
        joueur_nom = joueur_info['DISPLAY_FIRST_LAST'].iloc[0]
        return joueur_nom
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention du nom du joueur {joueur_id}: {str(e)}")
        return None
    
# --------------------------------------------------------------------------------------------
# Obtenir l'ID de l'equipe du joueur avec son ID
def obtenir_equipeID_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_CommonPlayerInfo_DF_globaux(joueur_id)
        id_equipe_joueur = joueur_info['TEAM_ID'].iloc[0]
        return id_equipe_joueur
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention de l'équipe du joueur {joueur_id}: {str(e)}")
        return None
    
# --------------------------------------------------------------------------------------------    
# Obtenir l'ID de l'equipe du joueur avec son ID
def obtenir_equipeABV_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_CommonPlayerInfo_DF_globaux(joueur_id)
        ABV_equipe_joueur = joueur_info['TEAM_ABBREVIATION'].iloc[0]
        return ABV_equipe_joueur
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention de l'équipe du joueur {joueur_id}: {str(e)}")
        return None

# --------------------------------------------------------------------------------------------
# Obtenir le poste du joueur avec son ID
def obtenir_joueurPoste_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_CommonPlayerInfo_DF_globaux(joueur_id)
        joueur_poste = joueur_info['POSITION'].iloc[0]  # Utiliser .iloc[0] pour obtenir la valeur sans l'index
        return joueur_poste
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention du poste du joueur {joueur_id}: {str(e)}")
        return None

# --------------------------------------------------------------------------------------------
# Obtenir le poste du joueur avec son ID en format abrégé (par exemple, Forward-Center devient F-C)
def obtenir_joueurPosteAbregee_avec_joueurID(joueur_id):
    poste_complet = obtenir_joueurPoste_avec_joueurID(joueur_id)
    
    if poste_complet is not None:
        poste_abrege = ""
        for pos in poste_complet.split("-"):
            poste_abrege += pos[0] + "-"
        
        poste_abrege = poste_abrege[:-1] # Enlever le dernier "-"

        # Retraiter le poste du joueur parmis un liste de joueurs spécifique
        poste_reprocessed = retraitement_poste_joueurs_specifiques(joueur_id)
        if poste_reprocessed is not None:
            triplette_poste = poste_reprocessed
        else : # Si pas de traitement spécifique, obtenir le poste parmis la triplette
            triplette_poste = trouver_equivalence_triplette_poste(poste_abrege)

        return triplette_poste
    else:
        return None

# --------------------------------------------------------------------------------------------
# Fonction pour retraiter le poste de certains joueurs (comme Lauri Markkanen, que l'on veut en F et pas en C)
# 1628374
def retraitement_poste_joueurs_specifiques(joueur_id):
    equivalence = {
        1628374: 'F', # Lauri Markkanen
    }
    return equivalence.get(joueur_id)

# --------------------------------------------------------------------------------------------
# Fonction pour transformer l'abbréviation du poste du joueur vers une des 3 possibilités : G, F, C
def trouver_equivalence_triplette_poste(position):
    # Création du tableau d'équivalence
    equivalence = {
        'G': 'G',
        'G-F': 'G',
        'F-G': 'F',
        'F': 'F',
        'F-C': 'C',
        'C-F': 'C',
        'C': 'C'
    }
    return equivalence.get(position)

# --------------------------------------------------------------------------------------------
# Fonction pour palier aux erreurs du endpoints nextgames
def obtenir_un_coequipier_dans_equipe_avec_joueurID(joueur_id):
    # Obtenir l'ID de l'équipe du joueur
    equipe_id = obtenir_equipeID_avec_joueurID(joueur_id)

    # Vérifier si l'ID de l'équipe est valide
    if equipe_id is not None:
        # Obtenir la liste des joueurs dans l'équipe
        roster = commonteamroster.CommonTeamRoster(team_id=equipe_id)
        # print(f"Appel à l'API CommonTeamRoster")
        roster_data = roster.get_normalized_dict()

        # Extraire les identifiants des joueurs de l'équipe
        ids_joueurs = [player['PLAYER_ID'] for player in roster_data['CommonTeamRoster']]
        
        for joueur_id_actuel in ids_joueurs:
            if joueur_id_actuel != joueur_id:
                return joueur_id_actuel
        return None
    
    else:
        print("ID de l'équipe non valide.")
        return None

# --------------------------------------------------------------------------------------------
def obtenir_integralite_calendrier_joueur_avec_joueurID(joueur_id):
    try:
        
        # Obtenir le DF des matchs joués par le joueur
        DF_joueur_1 = obtenir_PlayerGameLog_DF_globaux(joueur_id)

        # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
        DF_joueur = DF_joueur_1.copy()

        # Convertir la colonne 'GAME_DATE' en type de données datetime
        matchs_precedents = pd.to_datetime(DF_joueur['GAME_DATE'], format='%b %d, %Y')

        # Récupérer les dates des matchs à venir du joueur
        matchs_a_venir = obtenir_PlayerNextNGames_DF_globaux(joueur_id)
        matchs_a_venir = pd.to_datetime(matchs_a_venir['GAME_DATE'], format='%b %d, %Y')

        # Concaténer les deux séries de dates
        liste_integralite_dates = pd.concat([matchs_precedents, matchs_a_venir], ignore_index=True)

        # Trier la liste de dates
        liste_integralite_dates = liste_integralite_dates.sort_values()

        return liste_integralite_dates

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# #######################################################



# --------------------------------------------------------------------------------------------
def obtenir_equipeID_avec_equipeNom(nom_equipe):
    try:
            liste_equipes = obtenir_liste_equipes_DF_globaux()
            equipe_info = next((equipe for equipe in liste_equipes if equipe['full_name'] == nom_equipe), None)

            if equipe_info:
                id_equipe = equipe_info['id']
                return id_equipe
            else:
                print(f"2 Aucune équipe trouvée avec l'ID {nom_equipe}.")
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération du nom de l'équipe avec l'ID {nom_equipe}: {str(e)}")
        return None

# #######################################################
# Obtentions avec joueur_ID

# --------------------------------------------------------------------------------------------
def obtenir_equipeNom_avec_equipeID(id_equipe):
    try:
            liste_equipes = obtenir_liste_equipes_DF_globaux()
            equipe_info = next((equipe for equipe in liste_equipes if equipe['id'] == int(id_equipe)), None)

            if equipe_info:
                nom_equipe = equipe_info['full_name']
                return nom_equipe
            else:
                print(f"1 Aucune équipe trouvée avec l'ID {id_equipe}.")
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération du nom de l'équipe avec l'ID {id_equipe}: {str(e)}")
        return None

# --------------------------------------------------------------------------------------------
def obtenir_equipeABV_avec_equipeID(id_equipe):
    try:
        liste_equipes = obtenir_liste_equipes_DF_globaux()
        equipe_info = next((equipe for equipe in liste_equipes if equipe['id'] == int(id_equipe)), None)

        if equipe_info:
            ABV_equipe = equipe_info['abbreviation']
            return ABV_equipe
        else:
            raise ValueError(f"Aucune équipe trouvée avec l'ID {id_equipe}.")
    except Exception as e:
        print(f"Erreur lors de la récupération de l'abbréviation de l'équipe avec l'ID {id_equipe}: {str(e)}")
        return None

# #######################################################



# --------------------------------------------------------------------------------------------
# Génerer un fichier Excel
def exporter_vers_Excel_generique(DF, file_name):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Python_TTFL\Excel'

    # Obtenez la date du jour
    date_du_jour = datetime.now().strftime('%y_%m_%d')

    # Créez le nom du fichier Excel
    nom_fichier_excel = f'{file_name}_{date_du_jour}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    DF.to_excel(excel_writer=chemin_nom_excel, index=False)
    print()
    print('Fichier Excel enregistré : ',nom_fichier_excel)

# --------------------------------------------------------------------------------------------
# Génerer un fichier Excel
def exporter_vers_Excel_mon_TI(mon_TI, date_du_jour, suffixe):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Python_TTFL\Excel\TI'

    # Conversion de la date du jour
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y')  # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%Y_%m_%d")            # Formater la date

    if suffixe == "":
        # Créez le nom du fichier Excel
        nom_fichier_excel = f'Mon_TI_{date_du_jour}.xlsx'
    else :
        nom_fichier_excel = f'Mon_TI_{date_du_jour}_{suffixe}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    mon_TI.to_excel(excel_writer=chemin_nom_excel, index=False)
    print()
    print('Fichier Excel enregistré : ',nom_fichier_excel)

# --------------------------------------------------------------------------------------------
def exporter_vers_Excel_impact_poste(DF_impact_poste, suffixe=None):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Python_TTFL\Excel\Impact_poste'

    # Obtenez la date du jour
    date_du_jour = datetime.now().strftime('%Y_%m_%d')

    # Créez le nom du fichier Excel
    if suffixe is not None:
        nom_fichier_excel = f'Impact_poste_{date_du_jour}{suffixe}.xlsx'
    else:
        nom_fichier_excel = f'Impact_poste_{date_du_jour}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    DF_impact_poste.to_excel(excel_writer=chemin_nom_excel, index=False)
    print()
    print('Fichier Excel enregistré : ',nom_fichier_excel)

# ------------------------------
# Fonction pour charger le cache
def charger_cache() :
    charger_cache_BoxScoreTraditionalV2()
    charger_cache_CommonPlayerInfo()

# ------------------------------
# Fonction pour sauvegarder le cache
def sauvegarder_cache():
    sauvegarder_cache_BoxScoreTraditionalV2()
    sauvegarder_cache_CommonPlayerInfo()

# --------------------------------------------------------------------------------------------
def print_message_de_confirmation(temps_debut):
    temps_fin = time.time()  # Enregistrer le temps de fin d'exécution
    duree_execution = temps_fin - temps_debut  # Calculer la durée d'exécution
    minutes = int(duree_execution // 60)  # Convertir la durée en minutes
    secondes = int(duree_execution % 60)  # Calculer les secondes restantes

    pluriel_minutes = "s" if minutes > 1 else ""
    pluriel_secondes = "s" if secondes > 1 else ""

    if minutes != 0:
        if secondes != 0:
            print(f"Le code a pris {minutes} minute{pluriel_minutes} et {secondes} seconde{pluriel_secondes} pour s'exécuter.")
        else:
            print(f"Le code a pris {minutes} minute{pluriel_minutes} pour s'exécuter.")
    elif secondes != 0:
        print(f"Le code a pris {secondes} seconde{pluriel_secondes} pour s'exécuter.")