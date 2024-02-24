import pandas as pd

from x_Utilitaires import *
from x_DataFrames_globaux import *

# ------------------------------
# Fonction pour obtenir le prochain adversaire d'un joueur
def obtenir_adversaireID_prochain_match(joueur_id, date_du_jour):
    
    # Obtient l'ID de l'équipe du joueur
    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)

    # Vérifie si l'ID de l'équipe du joueur est valide
    if id_equipe_joueur is not None:
        
        # Obtenir le DF des prochains matchs du joueur
        DF_prochains_matchs_1 = obtenir_PlayerNextNGames_DF_globaux(joueur_id)

        # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
        DF_prochains_matchs = DF_prochains_matchs_1.copy()

        # Convertir la colonne 'GAME_DATE' en type de données datetime
        DF_prochains_matchs['GAME_DATE'] = pd.to_datetime(DF_prochains_matchs['GAME_DATE'], format='%b %d, %Y')

        # Filtrer pour ne garder que les dates après celle qui nous intéresse et reset l'index, pour que la boucle ci-dessous fonctionne
        DF_prochains_matchs = DF_prochains_matchs[DF_prochains_matchs['GAME_DATE'] >= date_du_jour].reset_index(drop=True)

        # Obtient l'ID de l'équipe à domicile et à l'extérieur pour le prochain match
        home_team_id, visitor_team_id = DF_prochains_matchs.loc[0, ['HOME_TEAM_ID', 'VISITOR_TEAM_ID']]

        # Détermine l'adversaire du prochain match en fonction de l'équipe du joueur
        adversaireID_prochain_match = visitor_team_id if id_equipe_joueur == home_team_id else home_team_id

        return adversaireID_prochain_match
    else:
        # Retourne None si l'ID de l'équipe du joueur n'est pas valide
        return None

# ------------------------------
# Fonction principale, pour construire le DF d'un joueur, avec son historique contre l'adversaire du soir
def obtenir_DF_historique_vs_adversaire_un_joueur(joueur_id, nombre_de_matchs_vs_adversaire, date_du_jour):
    
    # Récupérer le nom du joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    adversaireID_prochain_match = obtenir_adversaireID_prochain_match(joueur_id, date_du_jour)

    # Obtenir les statistiques de jeu pour la saison en cours (à adapter selon vos besoins)
    DF_joueur = obtenir_PlayerGameLog_DF_globaux(joueur_id)

    # Obtenez l'abréviation de l'équipe adverse
    equipe_adverseABV = obtenir_equipeABV_avec_equipeID(adversaireID_prochain_match)

    # Filtrer les matchs contre l'équipe spécifiée
    DF_matchs_contre_equipe = DF_joueur[DF_joueur['MATCHUP'].str.contains(f'{equipe_adverseABV}', case=False, na=False)]

    # Initialiser le DataFrame avec des colonnes vides
    DF_historique_vs_adversaire = pd.DataFrame({'Joueur': [joueur_nom]})

    # Compléter les colonnes en fonction du nombre de matchs spécifié
    for i in range(nombre_de_matchs_vs_adversaire):
        col_prefix = f'M-{i+1}'
        if i < len(DF_matchs_contre_equipe):
            vs_indicator = 'vs' if 'vs' in DF_matchs_contre_equipe['MATCHUP'].iloc[i].lower() else '@'
            DF_historique_vs_adversaire[f'{col_prefix}_vs'] = vs_indicator
            DF_historique_vs_adversaire[f'{col_prefix}_score'] = calcul_score_TTFL(DF_matchs_contre_equipe.iloc[i])
        else:
            DF_historique_vs_adversaire[f'{col_prefix}_vs'] = '-'
            DF_historique_vs_adversaire[f'{col_prefix}_score'] = '-'
    
    return DF_historique_vs_adversaire

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_historiques_vs_adversaires(ids_joueurs, nombre_de_matchs_vs_adversaire, date_du_jour):

    # Créer une liste pour stocker les DataFrames individuels de chaque joueur
    liste_DF_historique_vs_adversaire = []

    # Boucler à travers les identifiants des joueurs
    for joueur_id in ids_joueurs:
        # Obtenir le DataFrame pour l'historique des matchs contre l'adversaire pour ce joueur
        DF_historique_vs_adversaire = obtenir_DF_historique_vs_adversaire_un_joueur(joueur_id, nombre_de_matchs_vs_adversaire, date_du_jour)

        # Ajouter le DataFrame à la liste
        liste_DF_historique_vs_adversaire.append(DF_historique_vs_adversaire)

    # Concaténer tous les DataFrames de la liste en un seul DataFrame final
    DF_historiques_vs_adversaires = pd.concat(liste_DF_historique_vs_adversaire, ignore_index=True)
    
    # Supprimer la colonne 'Joueur' pour les besoins du traitement d'information global
    DF_historiques_vs_adversaires = DF_historiques_vs_adversaires.drop(columns=['Joueur'])

    return DF_historiques_vs_adversaires

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    date_du_jour = '26/02/2024'         # Date du jour qui nous intéresse
    ids_joueurs = [203999, 1630169]     # Liste de joueurs
    nombre_de_matchs_vs_adversaire = 3  # Nombre de matchs contre l'adversaire que l'on souhaite avoir dans l'historique
    
    DF_historiques_vs_adversaires = obtenir_DF_historiques_vs_adversaires(ids_joueurs, nombre_de_matchs_vs_adversaire, date_du_jour)

    print(DF_historiques_vs_adversaires)