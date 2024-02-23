import pandas as pd

from x_DataFrames_globaux import *
from x_Utilitaires import *

# ------------------------------
# Fonction pour obtenir les moyennes du joueur
def obtenir_array_moyennes(joueur_id):

    # Trouver le nom joueur
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Obtenir les statistiques de jeu pour la saison 2023
    DF_joueur = obtenir_game_log_DF_globaux(joueur_id)

    # Calculer les moyennes
    moyenne_5_premieres = DF_joueur.head(5).apply(calcul_score_TTFL, axis=1).mean().round(1)
    moyenne_15_premieres = DF_joueur.head(15).apply(calcul_score_TTFL, axis=1).mean().round(1)
    moyenne_totale = DF_joueur.apply(calcul_score_TTFL, axis=1).mean().round(1)

    array_moyennes = [joueur_nom, moyenne_5_premieres, moyenne_15_premieres, moyenne_totale]

    return array_moyennes

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_moyennes(ids_joueurs):
    
    # Créer le DataFrame final avec les colonnes nécessaires
    DF_moyennes = pd.DataFrame(columns=['Joueur', '5M', '15M', 'Saison'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
         # Ajouter le résultat en dernière ligne
        array_moyennes = obtenir_array_moyennes(joueur_id)
        DF_moyennes.loc[len(DF_moyennes)] = array_moyennes

    # Enlever les joueurs pour les besoins du TI global
    DF_moyennes = DF_moyennes.drop(columns=['Joueur'])

    # Retourner les moyennes
    return DF_moyennes

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [203076, 203944, 2544]

    DF_moyennes = obtenir_DF_moyennes(ids_joueurs)

    # Tri du tableau par ordre décroissant de la colonne "Saison"
    # DF_moyennes = DF_moyennes.sort_values(by='Saison', ascending=False)

    # Print du tableau
    print(DF_moyennes)