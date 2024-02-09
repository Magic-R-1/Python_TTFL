import pandas as pd
# from nba_api.stats.endpoints import player-gamelog ,player-nextngames
from z_Utilitaires import calcul_score_TTFL, obtenir_joueurNom_avec_joueurID, obtenir_equipeID_avec_joueurID
from z_DataFrames_globaux import obtenir_prochains_matchs_DF_globaux, obtenir_game_log_DF_globaux

# ------------------------------
# Prochain match_domicile_ou_exterieur
def obtenir_prochain_match_domicile_ou_exterieur(joueur_id):
    df_prochain_match = obtenir_prochains_matchs_DF_globaux(joueur_id,1)

    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)
    home_team_id = df_prochain_match.loc[0, 'HOME_TEAM_ID']

    vs_or_at = 'vs' if id_equipe_joueur == home_team_id else '@'

    return vs_or_at

# ------------------------------
# Moyenne gloabale
def obtenir_moyenne_globale(df_joueur):
    moyenne_globale = df_joueur.apply(calcul_score_TTFL, axis=1).mean().round(1)
    return moyenne_globale

# ------------------------------
# Moyenne domicile/extérieur
def obtenir_moyenne_domicile_ou_exterieur(df_joueur, vs_or_at):

    # Filtrer les matchs contre l'équipe spécifiée
    df_domicile_ou_exterieur = df_joueur[df_joueur['MATCHUP'].str.contains(vs_or_at, case=False, na=False)]

    # Calculer la moyenne
    moyenne_domicile_ou_exterieur = df_domicile_ou_exterieur.apply(calcul_score_TTFL, axis=1).mean().round(1)

    return moyenne_domicile_ou_exterieur

# ------------------------------
# Delta
def obtenir_delta_globale_domicile_ou_exterieur(joueur_id):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    vs_or_at = obtenir_prochain_match_domicile_ou_exterieur(joueur_id)

    # Obtenir les statistiques de jeu pour la saison en cours (à adapter selon vos besoins)
    # game_log = player-gamelog.PlayerGameLog(player_id=joueur_id, season='2023')  
    # df_joueur = game_log.get_data_frames()[0]
    df_joueur = obtenir_game_log_DF_globaux(joueur_id)

    moyenne_globale = obtenir_moyenne_globale(df_joueur)
    moyenne_domicile_ou_exterieur = obtenir_moyenne_domicile_ou_exterieur(df_joueur, vs_or_at)

    delta_globale_domicile_ou_exterieur = (moyenne_domicile_ou_exterieur-moyenne_globale).round(1)

    return joueur_nom, vs_or_at, delta_globale_domicile_ou_exterieur

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    joueurs_ids = [201142, 1630169, 2544]

    # Créer le DataFrame final avec les colonnes nécessaires
    df_impact_domicile_ou_exterieurs = pd.DataFrame(columns=['Joueur', 'vs or @','Delta'])

    for joueur_id in joueurs_ids:
            # Ajouter une nouvelle ligne directement avec loc
            df_impact_domicile_ou_exterieurs.loc[len(df_impact_domicile_ou_exterieurs)] = obtenir_delta_globale_domicile_ou_exterieur(joueur_id)

    # Enlever les joueurs
    # df_impact_domicile_ou_exterieurs = df_impact_domicile_ou_exterieurs.drop(columns=['Joueur'])

    # Print
    print(df_impact_domicile_ou_exterieurs)