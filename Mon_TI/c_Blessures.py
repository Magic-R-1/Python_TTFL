import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    player_data = []
    
    # Parcourir les informations des joueurs et les stocker dans la liste player_data
    for i in range(0, len(all_players), 4):
        player_name = all_players[i].text.strip()
        player_returnDate = all_players[i+1].text.strip()
        player_status = all_players[i+2].text.strip()
        player_comment = all_players[i+3].text.strip()
        player_data.append([player_name, player_returnDate, player_status, player_comment])

    # Créer un DataFrame pandas à partir des données des joueurs
    df = pd.DataFrame(player_data, columns=['Joueur', 'Date de retour', 'Statut', 'Commentaire'])

    # Afficher le DataFrame
    print(df)

else:
    print("La requête a échoué avec le code de statut:", response.status_code)