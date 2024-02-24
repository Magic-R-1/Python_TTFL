import pandas as pd

from x_DataFrames_globaux import *
from x_Utilitaires import *

# ------------------------------
# Fonction principale pour construire le tableau des x derniers matchs pour un joueur
def construire_DF_X_derniers_matchs_un_joueur(joueur_id, nb_matchs):
    id_equipe = obtenir_equipeID_avec_joueurID(joueur_id)
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    if id_equipe:
        DF_joueur = obtenir_PlayerGameLog_DF_globaux(joueur_id, nb_matchs)
        scores_TTFL_X_derniers = DF_joueur.apply(calcul_score_TTFL, axis=1)
        DF_X_derniers_matchs_un_joueur = pd.DataFrame({f'M-{i+1}': [score] for i, score in enumerate(scores_TTFL_X_derniers)})
        DF_X_derniers_matchs_un_joueur.insert(0, 'Joueur', joueur_nom)
        return DF_X_derniers_matchs_un_joueur

# ------------------------------
# Fonction bouclant pour construire le DF final
def construire_DF_X_derniers_matchs(ids_joueurs, nb_matchs):

    # Créer une liste pour stocker les DataFrames individuels
    liste_DF_X_derniers_matchs = []

    # Parcourir la liste des identifiants de joueurs
    for joueur_id in ids_joueurs:
        DF_X_derniers_matchs_un_joueur = construire_DF_X_derniers_matchs_un_joueur(joueur_id, nb_matchs)
        liste_DF_X_derniers_matchs.append(DF_X_derniers_matchs_un_joueur)

    # Concaténer tous les DataFrames dans la liste en un seul DataFrame final
    DF_X_derniers_matchs = pd.concat(liste_DF_X_derniers_matchs, ignore_index=True)

    # Enlever la colonne 'Joueur' pour les besoins du TI global
    DF_X_derniers_matchs.drop(columns=['Joueur'], inplace=True)

    return DF_X_derniers_matchs

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [203076, 2544, 203944]
    nb_matchs = 10

    DF_X_derniers_matchs = construire_DF_X_derniers_matchs(ids_joueurs, nb_matchs)

    # Print du tableau
    print(DF_X_derniers_matchs)