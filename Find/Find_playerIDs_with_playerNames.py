from nba_api.stats.static import players

def print_ids_joueurs(noms_joueurs):
    # Parcourir la liste des noms de joueurs
    for nom_joueur in noms_joueurs:
        # Trouver le joueur par nom
        joueur_info = players.find_players_by_full_name(nom_joueur)

        if joueur_info:
            # Imprimer l'ID du joueur
            print(joueur_info[0]['id'])
        else:
            # Si le nom n'est pas valide, imprimer un message d'erreur
            print(f"Nom {nom_joueur} non valide")

# Exemple d'utilisation avec la liste de noms que vous avez fournie
liste_noms = [
    "DeMar DeRozan", "Desmond Bane", "Devin Booker",
    "Donovan Mitchell",
    "Fred VanVleet",
    "Ja Morant", "Jalen Brunson", "Jamal Murray", "James Harden", "Jaren Jackson Jr.", "Jarrett Allen",
    "Jayson Tatum", "Jerami Grant", "Jimmy Butler",
    "Julius Randle", "Karl-Anthony Towns", "Kawhi Leonard", "Kevin Durant", "Khris Middleton", "Kristaps Porzingis", "Kyle Kuzma", "Kyrie Irving", "LaMelo Ball", "Lauri Markkanen",
    "Luka Doncic", "Michael Porter Jr.", "Nikola Jokic", "Nikola Vucevic", "Paolo Banchero", "Pascal Siakam", "Paul George", "Rudy Gobert", "Russell Westbrook", "Scottie Barnes", "Shai Gilgeous-Alexander", "Stephen Curry", "Terry Rozier", "Trae Young", "Tyler Herro",
    "Tyrese Maxey", "Victor Wembanyama", "Zach LaVine"]

# Appeler la fonction pour imprimer les IDs des joueurs
print_ids_joueurs(liste_noms)
