from nba_api.stats.endpoints import commonplayerinfo

def obtenir_equipe_joueur(joueur_id):
    try:
        # Obtenir les informations du joueur
        joueur_info = commonplayerinfo.CommonPlayerInfo(player_id=joueur_id)
        joueur_info = joueur_info.common_player_info.get_data_frame()

        # Extraire l'équipe actuelle du joueur
        equipe_actuelle = joueur_info['POSITION'].iloc[0]

        return equipe_actuelle
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# Exemple d'utilisation avec un ID de joueur
joueur_id = 2544
equipe_joueur = obtenir_equipe_joueur(joueur_id)

# Afficher l'équipe du joueur
if equipe_joueur:
    print(f"La position du joueur {joueur_id} est : {equipe_joueur}")
else:
    print(f"Impossible d'obtenir le poste du joueur.")