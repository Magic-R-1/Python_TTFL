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
    
    # Créer le DataFrame final avec les colonnes nécessaires
    DF_equipes_noms = pd.DataFrame(columns=['Equipe', 'Joueur'])

    # Boucle sur les joueurs
    for joueur_id in ids_joueurs:
        array_equipe_nom = obtenir_array_equipe_nom(joueur_id)          # Obtention de l'array
        DF_equipes_noms.loc[len(DF_equipes_noms)] = array_equipe_nom    # Ajout en dernière ligne du DF
    
    return DF_equipes_noms

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1628384, 203076, 1628983, 1627742, 1628368, 1626164, 1627759, 203944, 1630163, 1628374, 1631094, 202331, 1630567, 1630169, 1629627, 203078, 1641706, 1630595, 1630166, 1628978, 1630596, 1630532, 1631105, 1627750, 201935, 1628386, 1628398, 1629008, 1629628, 201566, 202699, 1630178, 1641705, 203952, 1630559, 1626156, 1627832, 202330]

    # Appel de la fonction
    DF_equipes_noms = obtenir_DF_equipes_noms(ids_joueurs)

    # Print du tableau
    print(DF_equipes_noms)