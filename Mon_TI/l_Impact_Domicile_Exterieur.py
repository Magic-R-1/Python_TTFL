import pandas as pd

from x_Utilitaires import *
from x_DataFrames_globaux import *

# ------------------------------
# Prochain match_domicile_ou_exterieur
def obtenir_prochain_match_domicile_ou_exterieur(joueur_id):
    DF_prochain_match = obtenir_prochains_matchs_DF_globaux(joueur_id,1)

    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)
    home_team_id = DF_prochain_match.loc[0, 'HOME_TEAM_ID']

    vs_or_at = 'vs' if id_equipe_joueur == home_team_id else '@'

    return vs_or_at

# ------------------------------
# Moyenne gloabale
def obtenir_moyenne_globale(DF_joueur):
    moyenne_globale = DF_joueur.apply(calcul_score_TTFL, axis=1).mean().round(1)
    return moyenne_globale

# ------------------------------
# Moyenne domicile/extérieur
def obtenir_moyenne_domicile_ou_exterieur(DF_joueur, vs_or_at):

    # Filtrer les matchs sur domicile ou extérieur
    DF_domicile_ou_exterieur = DF_joueur[DF_joueur['MATCHUP'].str.contains(vs_or_at, case=False, na=False)]

    # Calculer la moyenne
    moyenne_domicile_ou_exterieur = DF_domicile_ou_exterieur.apply(calcul_score_TTFL, axis=1).mean().round(1)

    return moyenne_domicile_ou_exterieur

# ------------------------------
# Delta
def obtenir_array_delta_domicile_ou_exterieur(joueur_id):
    # Obtenir le nom du joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Obtenir si le prochain match est à domicile ou à l'extérieur
    vs_or_at = obtenir_prochain_match_domicile_ou_exterieur(joueur_id)

    # Obtenir les statistiques de jeu pour la saison en cours
    DF_joueur = obtenir_game_log_DF_globaux(joueur_id)

    # Calculer la moyenne globale
    moyenne_globale = obtenir_moyenne_globale(DF_joueur)
    
    # Calculer la moyenne à domicile ou à l'extérieur
    moyenne_domicile_ou_exterieur = obtenir_moyenne_domicile_ou_exterieur(DF_joueur, vs_or_at)

    # Calculer la différence entre la moyenne à domicile ou à l'extérieur et la moyenne globale
    delta_domicile_ou_exterieur = (moyenne_domicile_ou_exterieur - moyenne_globale).round(1)

    # Créer un tableau avec le nom du joueur, si le prochain match est à domicile ou à l'extérieur, et le delta
    array_delta_domicile_ou_exterieur = [joueur_nom, vs_or_at, delta_domicile_ou_exterieur]
    
    return array_delta_domicile_ou_exterieur

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_impact_domicile_ou_exterieurs(ids_joueurs):

     # Créer le DataFrame final avec les colonnes nécessaires
    DF_impact_domicile_ou_exterieurs = pd.DataFrame(columns=['Joueur', 'vs or @','Delta'])

    for joueur_id in ids_joueurs:
            # Ajouter une nouvelle ligne au DF
            array_delta_domicile_ou_exterieur = obtenir_array_delta_domicile_ou_exterieur(joueur_id)
            DF_impact_domicile_ou_exterieurs.loc[len(DF_impact_domicile_ou_exterieurs)] = array_delta_domicile_ou_exterieur
    
    # Enlever les joueurs pour les besoins du TI global
    DF_impact_domicile_ou_exterieurs = DF_impact_domicile_ou_exterieurs.drop(columns=['Joueur'])

    return DF_impact_domicile_ou_exterieurs   

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    ids_joueurs = [201142, 1630169, 2544]

    DF_impact_domicile_ou_exterieurs = obtenir_DF_impact_domicile_ou_exterieurs(ids_joueurs)

    # Print
    print(DF_impact_domicile_ou_exterieurs)