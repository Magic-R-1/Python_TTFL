import pandas as pd

from x_DataFrames_globaux import *
from x_Utilitaires import *

# ------------------------------
# Fonction pour obtenir le nom et l'équipe d'un joueur
def obtenir_array_equipe_nom(joueur_id):

    joueur_equipe = obtenir_equipeABV_avec_joueurID(joueur_id)  # Poste du joueur avec son ID
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)     # Nom du joueur avec son ID

    array_equipe_nom = [joueur_equipe, joueur_nom]  # Construction de la liste

    return array_equipe_nom

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_equipes_noms(ids_joueurs):
    
    charger_cache_CommonPlayerInfo()

    # Créer le DataFrame final avec les colonnes nécessaires
    DF_equipes_noms = pd.DataFrame(columns=['Equipe', 'Joueur'])

    # Boucle sur les joueurs
    for joueur_id in ids_joueurs:
        array_equipe_nom = obtenir_array_equipe_nom(joueur_id)          # Obtention de l'array
        DF_equipes_noms.loc[len(DF_equipes_noms)] = array_equipe_nom    # Ajout en dernière ligne du DF
    
    sauvegarder_cache_CommonPlayerInfo()
    
    return DF_equipes_noms

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1628384, 203076, 1628983, 1627742, 1628368, 1626164]
    
    # Appel de la fonction
    DF_equipes_noms = obtenir_DF_equipes_noms(ids_joueurs)

    # Print du tableau
    print(DF_equipes_noms)