import pandas as pd

from x_Utilitaires import *
from x_DataFrames_globaux import *

# ------------------------------
# Fonction pour convertir la date
def convertir_date(date_du_jour):
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y')  # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y")           # Formater la date
    return date_du_jour

# ------------------------------
# Prochain match_domicile_ou_exterieur
def obtenir_prochain_match_domicile_ou_exterieur(joueur_id, date_du_jour):

    # Obtenir le DF des prochains matchs du joueur
    DF_prochains_matchs_1 = obtenir_PlayerNextNGames_DF_globaux(joueur_id)

    # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
    DF_prochains_matchs = DF_prochains_matchs_1.copy()

    # Convertir la colonne 'GAME_DATE' en type de données datetime
    DF_prochains_matchs['GAME_DATE'] = pd.to_datetime(DF_prochains_matchs['GAME_DATE'], format='%b %d, %Y')

    # Filtrer pour ne garder que les dates après celle qui nous intéresse et reset l'index, pour que la boucle ci-dessous fonctionne
    DF_prochains_matchs = DF_prochains_matchs[DF_prochains_matchs['GAME_DATE'] >= date_du_jour].reset_index(drop=True)

    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)
    home_team_id = DF_prochains_matchs.loc[0, 'HOME_TEAM_ID']

    vs_or_at = 'vs' if id_equipe_joueur == home_team_id else '@'

    return vs_or_at

# ------------------------------
# Moyenne gloabale
def obtenir_moyenne_globale(DF_joueur):
    
    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        moyenne_globale = DF_joueur.apply(calcul_score_TTFL, axis=1).mean().round(1)
    except AttributeError:
        moyenne_globale = 0

    return moyenne_globale

# ------------------------------
# Moyenne domicile/extérieur
def obtenir_moyenne_domicile_ou_exterieur(DF_joueur, vs_or_at):

    # Filtrer les matchs sur domicile ou extérieur
    DF_domicile_ou_exterieur = DF_joueur[DF_joueur['MATCHUP'].str.contains(vs_or_at, case=False, na=False)]

    # Calculer la moyenne
    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        moyenne_domicile_ou_exterieur = DF_domicile_ou_exterieur.apply(calcul_score_TTFL, axis=1).mean().round(1)
    except AttributeError:
        moyenne_domicile_ou_exterieur = 0

    return moyenne_domicile_ou_exterieur

# ------------------------------
# Delta
def obtenir_array_delta_domicile_ou_exterieur(joueur_id, date_du_jour):
    # Obtenir le nom du joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Obtenir si le prochain match est à domicile ou à l'extérieur
    vs_or_at = obtenir_prochain_match_domicile_ou_exterieur(joueur_id, date_du_jour)

    # Obtenir les statistiques de jeu pour la saison en cours
    DF_joueur = obtenir_PlayerGameLog_DF_globaux(joueur_id)

    # Calculer la moyenne globale
    moyenne_globale = obtenir_moyenne_globale(DF_joueur)
    
    # Calculer la moyenne à domicile ou à l'extérieur
    moyenne_domicile_ou_exterieur = obtenir_moyenne_domicile_ou_exterieur(DF_joueur, vs_or_at)

    # Calculer la différence entre la moyenne à domicile ou à l'extérieur et la moyenne globale
    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        delta_domicile_ou_exterieur = (moyenne_domicile_ou_exterieur - moyenne_globale).round(1)
    except AttributeError:
        delta_domicile_ou_exterieur = 0

    # Créer un tableau avec le nom du joueur, si le prochain match est à domicile ou à l'extérieur, et le delta
    array_delta_domicile_ou_exterieur = [joueur_nom, vs_or_at, delta_domicile_ou_exterieur]
    
    return array_delta_domicile_ou_exterieur

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_impact_domicile_ou_exterieurs(ids_joueurs, date_du_jour):

     # Créer le DataFrame final avec les colonnes nécessaires
    DF_impact_domicile_ou_exterieurs = pd.DataFrame(columns=['Joueur', 'vs or @','Delta'])

    date_du_jour = convertir_date(date_du_jour)

    for joueur_id in ids_joueurs:
            # Ajouter une nouvelle ligne au DF
            array_delta_domicile_ou_exterieur = obtenir_array_delta_domicile_ou_exterieur(joueur_id, date_du_jour)
            DF_impact_domicile_ou_exterieurs.loc[len(DF_impact_domicile_ou_exterieurs)] = array_delta_domicile_ou_exterieur
    
    # Enlever les joueurs pour les besoins du TI global
    DF_impact_domicile_ou_exterieurs = DF_impact_domicile_ou_exterieurs.drop(columns=['Joueur'])

    return DF_impact_domicile_ou_exterieurs   

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    ids_joueurs = [1627759, 203944, 1631094, 203497, 1630595, 1628978, 1630532, 1631105]
    date_du_jour = '24/02/2024' # Date du jour qui nous intéresse

    DF_impact_domicile_ou_exterieurs = obtenir_DF_impact_domicile_ou_exterieurs(ids_joueurs, date_du_jour)

    # Print
    print(DF_impact_domicile_ou_exterieurs)