import pandas as pd

from d_Back_to_back import *
from x_DataFrames_globaux import *
from x_Utilitaires import *

# ------------------------------
# Fonction pour obtenir le Game Log d'un joueur, en y ajoutant la différence en jours entre chaque match
def obtenir_stats_joueur_avec_delta_jours(joueur_id):
    # Obtenir le DF du joueur
    DF_joueur_1 = obtenir_PlayerGameLog_DF_globaux(joueur_id)

    # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
    DF_joueur = DF_joueur_1.copy()

    # Convertir la colonne 'GAME_DATE' en type de données datetime
    DF_joueur['GAME_DATE'] = pd.to_datetime(DF_joueur['GAME_DATE'], format='%b %d, %Y')

    # Tri des données par date
    DF_joueur = DF_joueur.sort_values(by='GAME_DATE')

    # Ajout d'une colonne avec le calcul du nombre de jours entre chaque match
    DF_joueur['jours_entre'] = DF_joueur['GAME_DATE'].diff().dt.days

    return DF_joueur

# ------------------------------
# Fonction pour obtenir le nombre de B2B d'un joueur
def obtenir_nombre_de_B2B(DF_joueur):

    # Filtrer les 2èmes jours et calculer le score TTFL moyen
    DF_2e_jour = DF_joueur[DF_joueur['jours_entre'] == 1]

    nombre_de_B2B = len(DF_2e_jour)

    return nombre_de_B2B

# ------------------------------
# Fonction pour calculer la moyenne TTFL d'un joueur pas en B2B
def obtenir_moyenne_TTFL_hors_B2B(DF_joueur):

    # Filtrer les matchs qui ne sont pas un deuxième jour consécutif
    DF_non_consecutifs = DF_joueur[DF_joueur['jours_entre'] != 1]

    # Calculer la moyenne TTFL pour ces matchs
    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        moyenne_TTFL_hors_B2B = DF_non_consecutifs.apply(calcul_score_TTFL, axis=1).mean().round(1)
    except AttributeError:
        moyenne_TTFL_hors_B2B = 0
    

    return moyenne_TTFL_hors_B2B

# ------------------------------
# Fonction pour calculer la moyenne TTFL d'un joueur en B2B
def obtenir_moyenne_TTFL_B2B(DF_joueur):

    # Filtrer les 2èmes jours et calculer le score TTFL moyen
    DF_2e_jour = DF_joueur[DF_joueur['jours_entre'] == 1]

    # Calculer le score TTFL moyen pour toutes les lignes de DF_2e_jour
    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        moyenne_TTFL_B2B = DF_2e_jour.apply(calcul_score_TTFL, axis=1).mean().round(1)
    except AttributeError:
        moyenne_TTFL_B2B = 0

    return moyenne_TTFL_B2B

# ------------------------------
# Fonction pour obtenir le delta en B2B d'un joueur
def obtenir_delta_B2B(DF_joueur):

    moyenne_TTFL_hors_B2B = obtenir_moyenne_TTFL_hors_B2B(DF_joueur)
    moyenne_B2B = obtenir_moyenne_TTFL_B2B(DF_joueur)

    # try-except pour les joueurs NBA et qui n'ont aucune donnée (plus en NBA, ou pas encore joué cette saison)
    try:
        delta_B2B = (moyenne_B2B - moyenne_TTFL_hors_B2B).round(1)
    except AttributeError:
        delta_B2B = 0
    
    return delta_B2B

# ------------------------------
# Fonction principale, pour obtenir l'impact d'un B2B pour un joueur
def obtenir_array_delta_nb_B2B(joueur_id, row):
    
    # Charger le DF_joueur, utilisé 3 fois par la suite dans des fonctions
    DF_joueur = obtenir_stats_joueur_avec_delta_jours(joueur_id)

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)
    
    if row[1]['B2B'] == 'O':
        delta_B2B = obtenir_delta_B2B(DF_joueur)
        nombre_de_B2B = obtenir_nombre_de_B2B(DF_joueur)
    else:
        delta_B2B = ''
        nombre_de_B2B = ''

    array_delta_nb_B2B = [joueur_nom, delta_B2B, nombre_de_B2B]

    return array_delta_nb_B2B        

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_impact_B2B(ids_joueurs, date_du_jour):

    # Créer le DataFrame final avec les colonnes nécessaires
    DF_impact_B2B = pd.DataFrame(columns=['Joueur', 'delta_B2B', 'nombre_de_B2B'])

    DF_back_to_back = obtenir_DF_back_to_back(ids_joueurs, date_du_jour)

    for joueur_id, row in zip(ids_joueurs, DF_back_to_back.iterrows()):
        array_delta_nb_B2B = obtenir_array_delta_nb_B2B(joueur_id, row)
        DF_impact_B2B.loc[len(DF_impact_B2B)] = array_delta_nb_B2B

    # Enlever les joueurs pour les besoins du TI global
    DF_impact_B2B = DF_impact_B2B.drop(columns=['Joueur'])

    return DF_impact_B2B

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste de joueurs
    ids_joueurs = [1630578,203952,203076,1630162,1630559,1628389,203078,1627742]
    date_du_jour = '23/02/2024'

    DF_impact_B2B = obtenir_DF_impact_B2B(ids_joueurs, date_du_jour)

    print(DF_impact_B2B)