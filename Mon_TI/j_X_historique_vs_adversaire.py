import pandas as pd
from z_Utilitaires import *
from z_DataFrames_globaux import *

def obtenir_adversaire_prochain_match(joueur_id):
    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)

    if id_equipe_joueur is not None:
        # prochain_match = player-nextngames.PlayerNextNGames(player_id=joueur_id, number_of_games=1)
        # df_prochain_match = prochain_match.get_data_frames()[0]
        df_prochain_match = obtenir_prochains_matchs_DF_globaux(joueur_id)

        home_team_id, visitor_team_id = df_prochain_match.loc[0, ['HOME_TEAM_ID', 'VISITOR_TEAM_ID']]

        adversaire_id = visitor_team_id if id_equipe_joueur == home_team_id else home_team_id

        return adversaire_id
    else:
        return None

def obtenir_X_historique_vs_adversaire(joueur_id, nombre_de_matchs_vs_adversaire):
    try:
        # Récupérer le nom du joueur
        joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

        adversaire_id = obtenir_adversaire_prochain_match(joueur_id)

        # Obtenir les statistiques de jeu pour la saison en cours (à adapter selon vos besoins)
        # game_log = player-gamelog.PlayerGameLog(player_id=joueur_id, season='2023')  
        # df_joueur = game_log.get_data_frames()[0]
        df_joueur = obtenir_game_log_DF_globaux(joueur_id)

        # Filtrer les matchs contre l'équipe spécifiée
        df_matchs_contre_equipe = df_joueur[df_joueur['MATCHUP'].str.contains(f'{obtenir_equipeABV_avec_equipeID(adversaire_id)}', case=False, na=False)]

        # Initialiser le DataFrame avec des colonnes vides
        df_historique_vs_adversaire = pd.DataFrame({'Joueur': [joueur_nom]})

        # Remplir les colonnes en fonction du nombre de matchs spécifié
        for i in range(nombre_de_matchs_vs_adversaire):
            col_prefix = f'M-{i+1}'
            if i < len(df_matchs_contre_equipe):
                vs_indicator = 'vs' if 'vs' in df_matchs_contre_equipe['MATCHUP'].iloc[i].lower() else '@'
                df_historique_vs_adversaire[f'{col_prefix}_vs'] = vs_indicator
                df_historique_vs_adversaire[f'{col_prefix}_score'] = calcul_score_TTFL(df_matchs_contre_equipe.iloc[i])
            else:
                df_historique_vs_adversaire[f'{col_prefix}_vs'] = '-'
                df_historique_vs_adversaire[f'{col_prefix}_score'] = '-'

        return df_historique_vs_adversaire

    except (ValueError, IndexError) as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Exemple d'utilisation
    joueurs_ids = [203999, 1630169]

    # Nombre de matchs contre l'adversaire que l'on souhaite avoir
    nombre_de_matchs_vs_adversaire = 3
    
    # Créer le DataFrame final
    df_historique_vs_adversaire = pd.DataFrame()

    for joueur_id in joueurs_ids:
        df_historique_vs_adversaire = pd.concat([df_historique_vs_adversaire, obtenir_X_historique_vs_adversaire(joueur_id, nombre_de_matchs_vs_adversaire)], ignore_index=True)

    # Enlever les joueurs
    # df_historique_vs_adversaire = df_historique_vs_adversaire.drop(columns=['Joueur'])

    if df_historique_vs_adversaire is not None:
        print(df_historique_vs_adversaire)