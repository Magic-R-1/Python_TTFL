import pandas as pd
import re
import sys
from datetime import datetime
import requests
from z_Utilitaires import *
from z_DataFrames_globaux import *
from bs4 import BeautifulSoup

# Fonction pour charger les caches des feuilles de matchs et des postes des joueurs
def charger_cache():
    global cache_noms_joueurs  # Accès aux caches globaux
    cache_noms_joueurs = charger_cache_noms_joueurs()  # Charger le cache des matchs

# Fonction pour Web Scrapp la page d'EPSN, et construire un DF avec la liste des blessés et leur statut
def obtenir_DF_blessures():

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'} # Faire croire au navigateur que l'on est humain, et pas un programme
    # https://www.scrapingbee.com/blog/python-curl/
    url = "https://www.espn.com/nba/injuries" # Envoyer une requête HTTP à l'URL de la page
    # https://www.data-transitionnumerique.com/beautifulsoup-scraping/

    response = requests.get(url, headers=headers) # Obtenir la page web

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:

        html_content = response.content # Extraire le contenu HTML de la réponse

        soup = BeautifulSoup(html_content, "html.parser") # Analyser le HTML avec BeautifulSoup

        # Trouver tous les éléments de la page avec les classes "col-name Table__TD" et "col-stat Table__TD"
        all_players = soup.find_all("td", class_=["col-name Table__TD","col-date Table__TD", "col-stat Table__TD","col-desc Table__TD"])
        
        # Initialiser une liste pour stocker les données des joueurs
        liste_data_blessure_joueurs = []
        
        # Parcourir les informations des joueurs et les stocker dans la liste liste_data_blessure_joueurs
        for i in range(0, len(all_players), 4):
            player_name = all_players[i].text.strip()
            player_id = obtenir_joueurID_avec_joueurNom(player_name)
            player_returnDate = all_players[i+1].text.strip()
                # player_returnDate_1 = transformer_date_retour(player_returnDate)
            player_status = all_players[i+2].text.strip()
            player_comment = all_players[i+3].text.strip()
                # player_comment_1 = transformer_date_commentaire(player_comment)
            liste_data_blessure_joueurs.append([player_name, player_id, player_returnDate, player_status, player_comment])

        # Créer un DataFrame pandas à partir des données des joueurs
        DF_data_blessure_joueurs = pd.DataFrame(liste_data_blessure_joueurs, columns=['Joueur', 'ID', 'Date de retour', 'Statut', 'Commentaire'])

        # Afficher le DataFrame
        return DF_data_blessure_joueurs

    else:
        print("La requête a échoué avec le code de statut:", response.status_code)

# Fonction pour transformer la date de retour en un format pertinent
def transformer_date_retour(date_str):
    # Obtenez la date actuelle
    today = datetime.now()

    # Analysez le mois et le jour de la date_str
    try:
        date_obj = datetime.strptime(date_str, "%b %d")
    except ValueError as e:
        # Si la date donnée n'est pas valide, remplacez-la par le 28 février
        if date_str == 'Feb 29':
            date_obj = datetime(today.year, 2, 29)# + timedelta(days=1)
        else:
            print(f"Erreur sur la gestion de : {date_str}")
            sys.exit()

    # Remplacez l'année par la prochaine occurrence de la date par rapport à aujourd'hui
    next_year = today.year if (date_obj.month, date_obj.day) >= (today.month, today.day) else today.year + 1

    # Créez un objet datetime avec la nouvelle année
    date_obj = date_obj.replace(year=next_year)

    # Formatter la date au format "23/02/2024"
    date_formatted = date_obj.strftime("%d/%m/%Y")

    return date_formatted

# Fonction pour transformer la date contenue dans le commentaire en un format pertinent
def transformer_date_commentaire(commentaire):
    # Trouver la date dans le commentaire en utilisant une expression régulière
    match = re.search(r"([A-Z][a-z]{2}\s\d{1,2})", commentaire)
    if match:
        # Extraire la date trouvée
        date_str = match.group(1)

        # Ajouter l'année correspondant à la dernière fois que cette date a été rencontrée depuis aujourd'hui
        today = datetime.now()
        last_occurrence_year = today.year - 1
        last_occurrence_date = datetime.strptime(date_str, "%b %d").replace(year=last_occurrence_year)

        # Formatter la date au format "12/02/2024"
        date_formatted = last_occurrence_date.strftime("%d/%m/%Y")

        # Remplacer la date dans le commentaire
        commentaire_formate = re.sub(r"([A-Z][a-z]{2}\s\d{1,2})", date_formatted, commentaire)
        return commentaire_formate
    else:
        return commentaire

# Filtrer le tableau pour ne conserver que les lignes contenant des joueurs présent dans la liste d'input d'IDs de joueurs
def obtenir_DF_filtered(DF_data_blessure_joueurs, ids_joueurs):
    DF_filtered = DF_data_blessure_joueurs[DF_data_blessure_joueurs['ID'].isin(ids_joueurs)]
    return DF_filtered

def obtenir_DF_joueurs_status(ids_joueurs):

    # Obtenez le DataFrame complet avec toutes les blessures
    DF_complet = obtenir_DF_blessures()

    # Créez un DataFrame avec toutes les lignes correspondant aux joueurs dans ids_joueurs
    DF_joueurs_status = pd.DataFrame({'ID': ids_joueurs})

    # Filtrez le DataFrame complet pour ne conserver que les lignes avec les IDs présents dans ids_joueurs
    DF_filtered = obtenir_DF_filtered(DF_complet, ids_joueurs)

    # Fusionnez le DataFrame final avec le DataFrame filtré pour obtenir les statuts des joueurs
    DF_joueurs_status = DF_joueurs_status.merge(DF_filtered[['ID', 'Statut']], on='ID', how='left')

    # Remplissez les valeurs manquantes dans la colonne 'Statut' avec une chaîne vide
    DF_joueurs_status['Statut'] = DF_joueurs_status['Statut'].fillna('')
    
    # Charger le cache
    charger_cache()

    # Ajouter la colonne 'poste' en utilisant les postes abrégés des joueurs
    DF_joueurs_status['Joueur'] = DF_joueurs_status['ID'].apply(remplir_cache_noms_joueurs)

    # Sauvegarder le cache des matchs
    sauvegarder_cache_noms_joueurs(cache_noms_joueurs)

    # Réorganisez les colonnes pour avoir 'Joueur' en premier
    DF_joueurs_status = DF_joueurs_status[['Joueur', 'Statut']]

    # Enlever les joueurs pour les besoins du TI global
    DF_joueurs_status = DF_joueurs_status.drop(columns=['Joueur'])

    return DF_joueurs_status

def obtenir_nom_joueur_avec_id(id_joueur):
    # Insérez ici le code pour obtenir le nom du joueur à partir de son ID
    # Par exemple, vous pouvez utiliser une base de données ou une API pour obtenir cette information
    Nom = obtenir_joueurNom_avec_joueurID(id_joueur)
    return Nom

if __name__ == "__main__":

    ids_joueurs = [1628384, 203076, 1628983, 1627742, 1628368, 1626164, 1627759, 203944, 1630163, 1628374, 1631094, 202331, 1630567, 1630169, 1629627, 203078, 1641706, 1630595, 1630166, 1628978, 1630596, 1630532, 1631105, 1627750, 201935, 1628386, 1628398, 1629008, 1629628, 201566, 202699, 1630178, 1641705, 203952, 1630559, 1626156, 1627832, 202330]

    DF_joueurs_status = obtenir_DF_joueurs_status(ids_joueurs)

    print(DF_joueurs_status)