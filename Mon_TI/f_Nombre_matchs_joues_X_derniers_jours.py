import pandas as pd
from datetime import datetime, timedelta

from x_DataFrames_globaux import *
from x_Utilitaires import obtenir_joueurNom_avec_joueurID

# ------------------------------
# Fonction pour obtenir le nombre de matchs joués par un joueur ces X derniers jours
def obtenir_array_nb_matchs_joues_derniers_X_jours(joueur_id,nb_jours_matchs_joues):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id) # Nom du joueur avec son ID

    # Obtenez la date actuelle et la date d'il y a 30 jours
    start_date = datetime.now() - timedelta(days=nb_jours_matchs_joues)

    # Obtenir le DF des matchs joués par le joueur
    DF_joueur_1 = obtenir_PlayerGameLog_DF_globaux(joueur_id)

    # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
    DF_joueur = DF_joueur_1.copy()

    # Convertir la colonne 'GAME_DATE' en type de données datetime
    DF_joueur['GAME_DATE'] = pd.to_datetime(DF_joueur['GAME_DATE'], format='%b %d, %Y')

    # Filtrer les dates supérieures ou égales à start_date
    dates_superieures_ou_egales = DF_joueur['GAME_DATE'] >= start_date

    # Calculer le nombre de dates supérieures ou égales à start_date
    nb_matchs_joues_derniers_X_jours = dates_superieures_ou_egales.sum()

    # Création de la liste
    array_nb_matchs_joues_derniers_X_jours = [joueur_nom, nb_matchs_joues_derniers_X_jours]
    
    return array_nb_matchs_joues_derniers_X_jours

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_nb_matchs_joues_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues):

    # Créer le DataFrame final avec les colonnes nécessaires
    DF_matchs_joues_X_derniers_jours = pd.DataFrame(columns=['Joueur', 'GP'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        array_nb_matchs_joues_derniers_X_jours = obtenir_array_nb_matchs_joues_derniers_X_jours(joueur_id,nb_jours_matchs_joues)
        DF_matchs_joues_X_derniers_jours.loc[len(DF_matchs_joues_X_derniers_jours)] = array_nb_matchs_joues_derniers_X_jours
    
    # Enlever les joueurs
    DF_matchs_joues_X_derniers_jours = DF_matchs_joues_X_derniers_jours.drop(columns=['Joueur'])

    return DF_matchs_joues_X_derniers_jours

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [2544]

    # Nombre de jours sur lesquels obtenir le nombre de matchs joués
    nb_jours_matchs_joues = 30

    DF_matchs_joues_X_derniers_jours = obtenir_DF_nb_matchs_joues_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues)

    # Print du tableau
    print(DF_matchs_joues_X_derniers_jours)