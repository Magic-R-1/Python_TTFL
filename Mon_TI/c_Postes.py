import pandas as pd

from x_Utilitaires import *

# ------------------------------
# Fonction pour obtenir le poste du joueur
def obtenir_array_nom_poste(joueur_id):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)             # Nom du joueur avec son ID
    joueur_poste = obtenir_joueurPosteAbregee_avec_joueurID(joueur_id)  # Poste du joueur avec son ID

    array_nom_poste = [joueur_nom, joueur_poste]    # Construction de la liste

    return array_nom_poste

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_postes(ids_joueurs):

    # Créer le DataFrame final avec les colonnes nécessaires
    DF_postes = pd.DataFrame(columns=['Joueur', 'Poste'])

    # Boucle sur les joueurs
    for joueur_id in ids_joueurs:
        array_nom_poste = obtenir_array_nom_poste(joueur_id)    # Obtention de l'array
        DF_postes.loc[len(DF_postes)] = array_nom_poste         # Ajout en dernière ligne du DF

    # Enlever les joueurs pour les besoins du TI global
    if __name__ != "__main__":
        DF_postes = DF_postes.drop(columns=['Joueur'])

    return DF_postes

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1630578,203952,203076,1630162,1630559,1628389,203078,1627742]

    # Appel de la fonction
    DF_postes = obtenir_DF_postes(ids_joueurs)

    # Print du tableau
    print(DF_postes)