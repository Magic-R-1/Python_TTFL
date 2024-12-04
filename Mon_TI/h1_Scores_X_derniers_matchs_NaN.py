import pandas as pd

from x_DataFrames_globaux import *
from x_Utilitaires import *

# ------------------------------
# Fonction principale pour construire le tableau des x derniers matchs pour un joueur
def obtenir_DF_X_derniers_matchs_avec_NaN_un_joueur(joueur_id, nb_derniers_matchs):

    id_equipe = obtenir_equipeID_avec_joueurID(joueur_id)
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    if id_equipe:

        DF_obtenir_equipe_derniers_matchs_DF_globaux = obtenir_equipe_derniers_matchs_DF_globaux(id_equipe,nb_derniers_matchs)['GAME_DATE']

        DF_joueur = obtenir_PlayerGameLog_DF_globaux(joueur_id, nb_derniers_matchs)

        # Fusionner les DataFrames en utilisant la colonne 'GAME_DATE' comme clé de fusion
        DF_joueur_avec_dates_equipe = pd.merge(DF_obtenir_equipe_derniers_matchs_DF_globaux, DF_joueur, how='left', on='GAME_DATE')

        scores_TTFL_X_derniers = DF_joueur_avec_dates_equipe.apply(calcul_score_TTFL, axis=1)

        DF_X_derniers_matchs_avec_NaN_un_joueur = pd.DataFrame({'Joueur': [f"{joueur_nom}"]})
        DF_X_derniers_matchs_avec_NaN_un_joueur = pd.concat([DF_X_derniers_matchs_avec_NaN_un_joueur, pd.DataFrame({f'M-{i+1}': [score] for i, score in enumerate(scores_TTFL_X_derniers)})], axis=1)

        return DF_X_derniers_matchs_avec_NaN_un_joueur

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_X_derniers_matchs_avec_NaN(ids_joueurs, nb_derniers_matchs):
    
    # Initialiser une liste pour stocker les DataFrames temporaires
    liste_DF_X_derniers_matchs_avec_NaN = []

    # Parcourir la liste des identifiants de joueurs
    for joueur_id in ids_joueurs:
        # Construire le tableau des derniers matchs avec NaN pour le joueur actuel
        DF_X_derniers_matchs_avec_NaN_un_joueur = obtenir_DF_X_derniers_matchs_avec_NaN_un_joueur(joueur_id, nb_derniers_matchs)
        # Ajouter le DataFrame temporaire à la liste
        liste_DF_X_derniers_matchs_avec_NaN.append(DF_X_derniers_matchs_avec_NaN_un_joueur)

    # Concaténer tous les DataFrames temporaires en un seul
    DF_X_derniers_matchs_avec_NaN = pd.concat(liste_DF_X_derniers_matchs_avec_NaN, ignore_index=True)

    # Enlever les joueurs pour les besoins du TI global
    if __name__ != "__main__":
        DF_X_derniers_matchs_avec_NaN = DF_X_derniers_matchs_avec_NaN.drop(columns=['Joueur'])

        # Gestion des 0
        DF_X_derniers_matchs_avec_NaN = DF_X_derniers_matchs_avec_NaN.fillna(0)             # Trasnformer les NaN en 0
        DF_X_derniers_matchs_avec_NaN = DF_X_derniers_matchs_avec_NaN.round(0).astype(int)  # Convertir les valeurs en integer pour ne plus avoir de décimales
        DF_X_derniers_matchs_avec_NaN = DF_X_derniers_matchs_avec_NaN.replace(0,"-")        # Remplacer les 0 par des tirets pour la lisibilité

    return DF_X_derniers_matchs_avec_NaN

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    ids_joueurs = [203076, 2544, 203944]
    nb_derniers_matchs = 5

    DF_X_derniers_matchs_avec_NaN = obtenir_DF_X_derniers_matchs_avec_NaN(ids_joueurs, nb_derniers_matchs)

    # Print du tableau
    print(DF_X_derniers_matchs_avec_NaN)