import pandas as pd

from z_Utilitaires import obtenir_joueurNom_avec_joueurID
from f_Nombre_matchs_joues_X_derniers_jours import get_games_played_last_X_days
from h2_Scores_X_derniers_matchs import construire_tableau_X_derniers_matchs

def generer_intervalles_last_X_days(joueur_id,limite_1,limite_2,limite_3,number_of_days_matchs_joues):

    # Trouver le nom joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    games_played_last_30_days = get_games_played_last_X_days(joueur_id, number_of_days_matchs_joues)[1]

    tableau_X_derniers_matchs = construire_tableau_X_derniers_matchs(joueur_id, games_played_last_30_days)
    # Enlever les joueurs
    tableau_X_derniers_matchs = tableau_X_derniers_matchs.drop(columns=['Joueur'])

    df = pd.DataFrame(tableau_X_derniers_matchs)

    # Compter le nombre de valeurs inférieures à la limite 1
    count_values_below_limite_1 = (df < limite_1).sum().sum()
    count_values_below_limite_2 = ((df >= limite_1) & (df < limite_2)).sum().sum()
    count_values_below_limite_3 = ((df >= limite_2) & (df < limite_3)).sum().sum()
    count_values_above_limite_3 = (df >= limite_3).sum().sum()

    return [joueur_nom, count_values_below_limite_1,count_values_below_limite_2,count_values_below_limite_3,count_values_above_limite_3]

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    #Variables
    ids_joueurs = [1626164,  2544]

    limite_1 = 20
    limite_2 = 30
    limite_3 = 40

    number_of_days_matchs_joues = 30

    #DF final
    df_intervalles = pd.DataFrame(columns=['Joueur', f'<{limite_1}', f'{limite_1}-{limite_2-1}', f'{limite_2}-{limite_3-1}', f'{limite_3}+'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        df_intervalles.loc[len(df_intervalles)] = generer_intervalles_last_X_days(joueur_id,limite_1,limite_2,limite_3,number_of_days_matchs_joues)

    # Enlever les joueurs
    df_intervalles = df_intervalles.drop(columns=['Joueur'])

    # Print du tableau
    print(df_intervalles)