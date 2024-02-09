import pandas as pd
# from nba_api.stats.endpoints import player-gamelog
from z_DataFrames_globaux import obtenir_game_log_DF_globaux
from z_Utilitaires import calcul_score_TTFL, obtenir_equipeID_avec_joueurID, obtenir_joueurNom_avec_joueurID

# Fonction pour construire le tableau des x derniers matchs pour un joueur
def construire_tableau_X_derniers_matchs(joueur_id, nb_matchs):
    id_equipe = obtenir_equipeID_avec_joueurID(joueur_id)
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    if id_equipe:
        df_joueur = obtenir_game_log_DF_globaux(joueur_id, nb_matchs)

        scores_TTFL_X_derniers = df_joueur.apply(calcul_score_TTFL, axis=1)

        tableau_matchs = pd.DataFrame({'Joueur': [f"{joueur_nom}"]})
        tableau_matchs = pd.concat([tableau_matchs, pd.DataFrame({f'M-{i+1}': [score] for i, score in enumerate(scores_TTFL_X_derniers)})], axis=1)

        return tableau_matchs

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [2544]
    nb_matchs = 10

    # Créer le DataFrame final
    df_x_derniers_matchs = pd.DataFrame()

    # Parcourir la liste des identifiants de joueurs
    for joueur_id in ids_joueurs:
        tableau_X_derniers_matchs = construire_tableau_X_derniers_matchs(joueur_id, nb_matchs)
        df_x_derniers_matchs = pd.concat([df_x_derniers_matchs, tableau_X_derniers_matchs], ignore_index=True)

    # Enlever les joueurs
    # df_x_derniers_matchs = df_x_derniers_matchs.drop(columns=['Joueur'])

    # Print du tableau
    print(df_x_derniers_matchs)