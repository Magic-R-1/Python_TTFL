import pandas as pd

from f_Nombre_matchs_joues_X_derniers_jours import obtenir_array_nb_matchs_joues_derniers_X_jours
from h2_Scores_X_derniers_matchs import construire_DF_X_derniers_matchs_un_joueur
from x_DataFrames_globaux import *
from x_Utilitaires import obtenir_joueurNom_avec_joueurID

# ------------------------------
# Fonction principale pour construire la liste des intervalles pour un joueur
def obtenir_array_intervalles_derniers_X_jours(joueur_id,limite_1,limite_2,limite_3,nb_jours_matchs_joues):

    # Trouver le nom joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Calcul du nombre de matchs joués sur les X derniers jours
    nb_matchs_joues_X_derniers_jours = obtenir_array_nb_matchs_joues_derniers_X_jours(joueur_id, nb_jours_matchs_joues)[1]

    # Mettre le résultat dans un DF
    DF_X_derniers_matchs = construire_DF_X_derniers_matchs_un_joueur(joueur_id, nb_matchs_joues_X_derniers_jours)

    # Enlever les joueurs
    DF_X_derniers_matchs = DF_X_derniers_matchs.drop(columns=['Joueur'])

    # Compter le nombre de valeurs inférieures à la limite 1
    count_values_below_limite_1 = (DF_X_derniers_matchs < limite_1).sum().sum()
    count_values_below_limite_2 = ((DF_X_derniers_matchs >= limite_1) & (DF_X_derniers_matchs < limite_2)).sum().sum()
    count_values_below_limite_3 = ((DF_X_derniers_matchs >= limite_2) & (DF_X_derniers_matchs < limite_3)).sum().sum()
    count_values_above_limite_3 = (DF_X_derniers_matchs >= limite_3).sum().sum()

    array_intervalles_derniers_X_jours = [joueur_nom, count_values_below_limite_1,count_values_below_limite_2,count_values_below_limite_3,count_values_above_limite_3]

    return array_intervalles_derniers_X_jours

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_intervalles_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues, limite_1, limite_2, limite_3):

    #DF final
    DF_intervalles = pd.DataFrame(columns=['Joueur', f'<{limite_1}', f'{limite_1}-{limite_2-1}', f'{limite_2}-{limite_3-1}', f'{limite_3}+'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        DF_intervalles.loc[len(DF_intervalles)] = obtenir_array_intervalles_derniers_X_jours(joueur_id,limite_1,limite_2,limite_3,nb_jours_matchs_joues)

    # Enlever les joueurs pour les besoins du TI global
    DF_intervalles = DF_intervalles.drop(columns=['Joueur'])

    return DF_intervalles

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    #Variables
    # Liste de joueurs
    ids_joueurs = [203076, 1627742, 1628368, 1627734, 2544, 1627783, 202331, 203497, 1630567, 1630169, 1629627, 1630596]
    limite_1 = 20               # Limite du premier intervalle
    limite_2 = 30               # Limite du deuxième intervalle
    limite_3 = 40               # Limite du troisième intervalle
    nb_jours_matchs_joues = 30  # Nombre de jours sur lesquels obtenir le nombre de matchs joués

    # DF final
    DF_intervalles = obtenir_DF_intervalles_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues, limite_1, limite_2, limite_3)

    # Print du DF
    print(DF_intervalles)