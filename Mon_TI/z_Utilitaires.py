import pandas as pd
from nba_api.stats.endpoints import commonteamroster
from z_DataFrames_globaux import *

import os
from datetime import datetime

def calcul_score_TTFL(row):
    Turnover = row.get("TOV", row.get("TO", 0))  # Si "TOV" n'existe pas, utilise "TO" ou 0 par défaut
    return (
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

# Obtenir le nom du joueur avec son ID
def obtenir_joueurNom_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_informations_joueur_DF_globaux(joueur_id)
        joueur_nom = joueur_info['DISPLAY_FIRST_LAST'].iloc[0]
        return joueur_nom
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention du nom du joueur {joueur_id}: {str(e)}")
        return None

# Obtenir l'ID de l'equipe du joueur avec son ID
def obtenir_equipeID_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_informations_joueur_DF_globaux(joueur_id)
        id_equipe_joueur = joueur_info['TEAM_ID'].iloc[0]
        return id_equipe_joueur
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention de l'équipe du joueur {joueur_id}: {str(e)}")
        return None
 
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
    
# Obtenir l'ID de l'equipe du joueur avec son ID
def obtenir_equipeABV_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_informations_joueur_DF_globaux(joueur_id)
        ABV_equipe_joueur = joueur_info['TEAM_ABBREVIATION'].iloc[0]
        return ABV_equipe_joueur
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention de l'équipe du joueur {joueur_id}: {str(e)}")
        return None

# Obtenir le poste du joueur avec son ID
def obtenir_joueurPoste_avec_joueurID(joueur_id):
    try:
        joueur_info = obtenir_informations_joueur_DF_globaux(joueur_id)
        joueur_poste = joueur_info['POSITION'].iloc[0]  # Utiliser .iloc[0] pour obtenir la valeur sans l'index
        return joueur_poste
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention du poste du joueur {joueur_id}: {str(e)}")
        return None
    
# Obtenir le poste du joueur avec son ID en format abrégé (par exemple, F-C devient F-C)
def obtenir_joueurPosteAbregee_avec_joueurID(joueur_id):
    poste_complet = obtenir_joueurPoste_avec_joueurID(joueur_id)
    
    if poste_complet is not None:
        poste_abrege = ""
        for pos in poste_complet.split("-"):
            poste_abrege += pos[0] + "-"

        return poste_abrege[:-1]  # Enlever le dernier "-"
    else:
        return None

# Fonction pour palier aux erreurs du endpoints nextgames
def obtenir_un_coequipier_dans_equipe_avec_joueurID(joueur_id):
    # Obtenir l'ID de l'équipe du joueur
    equipe_id = obtenir_equipeID_avec_joueurID(joueur_id)

    # Vérifier si l'ID de l'équipe est valide
    if equipe_id is not None:
        # Appeler l'endpoint commonteamroster pour obtenir la liste des joueurs dans l'équipe
        roster = commonteamroster.CommonTeamRoster(team_id=equipe_id)
        roster_data = roster.get_normalized_dict()

        # Extraire les identifiants des joueurs de l'équipe
        joueurs_ids = [player['PLAYER_ID'] for player in roster_data['CommonTeamRoster']]
        
        for joueur_id_actuel in joueurs_ids:
            if joueur_id_actuel != joueur_id:
                return joueur_id_actuel
        return None
    
    else:
        print("ID de l'équipe non valide.")
        return None

def obtenir_integralite_calendrier_joueur_avec_joueurID(joueur_id):
    try:
        # Obtenir l'id de l'équipe
        id_equipe = obtenir_equipeID_avec_joueurID(joueur_id)

        # Récupérer les dates des matchs précédents du joueur
        matchs_precedents = obtenir_equipe_derniers_matchs_DF_globaux(id_equipe)
        matchs_precedents = pd.to_datetime(matchs_precedents['GAME_DATE'], format='%b %d, %Y')

        # Récupérer les dates des matchs à venir du joueur
        matchs_a_venir = obtenir_prochains_matchs_DF_globaux(joueur_id)
        matchs_a_venir = pd.to_datetime(matchs_a_venir['GAME_DATE'], format='%b %d, %Y')

        # Concaténer les deux séries de dates
        liste_integralite_dates = pd.concat([matchs_precedents, matchs_a_venir], ignore_index=True)

        # Trier la liste de dates
        liste_integralite_dates = liste_integralite_dates.sort_values()

        return liste_integralite_dates

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# Génerer un fichier Excel
def exporter_vers_Excel_generique(df, file_name):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Projet_Python\env1\Python_TTFL\Excel'

    # Obtenez la date du jour
    date_du_jour = datetime.now().strftime('%y_%m_%d')

    # Créez le nom du fichier Excel
    nom_fichier_excel = f'{file_name}_{date_du_jour}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    df.to_excel(excel_writer=chemin_nom_excel, index=False)
    print('Fichier Excel enregistré : ',nom_fichier_excel)

# Génrer un fichier Excel
def exporter_vers_Excel_mon_TI(mon_TI, date_du_jour):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Projet_Python\env1\Python_TTFL\Excel\TI'

    # Récupération de la date du jour
    date_du_jour = datetime.strptime(date_du_jour, "%b %d, %Y") # Conversion en objet datetime
    date_du_jour = date_du_jour.strftime("%Y_%m_%d") # Formater la date

    # Créez le nom du fichier Excel
    nom_fichier_excel = f'Mon_TI_{date_du_jour}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    mon_TI.to_excel(excel_writer=chemin_nom_excel, index=False)
    print('Fichier Excel enregistré : ',nom_fichier_excel)

def exporter_vers_Excel_impact_poste(df_impact_poste):

    # Spécifiez le chemin du dossier
    chemin_fichier_excel = r'C:\Users\egretillat\Documents\Personnel\Projet_Python\env1\Python_TTFL\Excel\Impact_poste'

    # Obtenez la date du jour
    date_du_jour = datetime.now().strftime('%y_%m_%d')

    # Créez le nom du fichier Excel
    nom_fichier_excel = f'Impact_poste_{date_du_jour}.xlsx'

    # Utilisez os.path.join pour former le chemin complet du fichier
    chemin_nom_excel = os.path.join(chemin_fichier_excel, nom_fichier_excel)

    # Exporter le fichier
    df_impact_poste.to_excel(excel_writer=chemin_nom_excel, index=False)
    print('Fichier Excel enregistré : ',nom_fichier_excel)