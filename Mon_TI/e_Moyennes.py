import pandas as pd
# from nba_api.stats.endpoints import player-gamelog
from z_DataFrames_globaux import obtenir_game_log_DF_globaux

from z_Utilitaires import calcul_score_TTFL, obtenir_joueurNom_avec_joueurID

def generer_df_moyennes(joueur_id):
    
    # Trouver le nom joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Obtenir les statistiques de jeu pour la saison 2023
    # game_log = player-gamelog.PlayerGameLog(player_id=joueur_id, season='2023')
    # df_joueur = game_log.get_data_frames()[0]
    df_joueur = obtenir_game_log_DF_globaux(joueur_id)

    # Calculer les moyennes
    moyenne_5_premieres = df_joueur.head(5).apply(calcul_score_TTFL, axis=1).mean().round(1)
    moyenne_15_premieres = df_joueur.head(15).apply(calcul_score_TTFL, axis=1).mean().round(1)
    moyenne_totale = df_joueur.apply(calcul_score_TTFL, axis=1).mean().round(1)

    # Retourner les moyennes
    return [joueur_nom, moyenne_5_premieres, moyenne_15_premieres, moyenne_totale]

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [203076, 203944, 2544]

    # Créer le DataFrame final avec les colonnes nécessaires
    df_moyennes = pd.DataFrame(columns=['Joueur', '5 matchs', '15 matchs', 'Saison'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        df_moyennes.loc[len(df_moyennes)] = generer_df_moyennes(joueur_id) #ajouter le résultat en dernière ligne

    # Tri du tableau par ordre décroissant de la colonne "Saison"
    # df_moyennes = df_moyennes.sort_values(by='Saison', ascending=False)

    # Enlever les joueurs
    df_moyennes = df_moyennes.drop(columns=['Joueur'])

    # Print du tableau
    print(df_moyennes)