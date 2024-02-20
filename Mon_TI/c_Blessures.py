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
    all_players = soup.find_all("td", class_=["col-name Table__TD", "col-stat Table__TD"])
    
    # col-name Table__TD / nom
    # col-pos Table__TD / poste
    # col-date Table__TD / date de retour
    # col-stat Table__TD / statut
    # col-desc Table__TD / commentaire

    # Afficher les informations sur les blessures
    for i in range(0, len(all_players), 2):  # Parcourir la liste par pas de 2 pour obtenir le nom et le statut
        player_name = all_players[i].text.strip()
        player_status = all_players[i+1].text.strip()
        print(f"Nom du joueur : {player_name}, Statut : {player_status}")

else:
    print("La requête a échoué avec le code de statut:", response.status_code)