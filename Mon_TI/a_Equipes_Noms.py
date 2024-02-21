import pandas as pd

from z_DataFrames_globaux import *

from z_Utilitaires import obtenir_joueurNom_avec_joueurID, obtenir_equipeABV_avec_joueurID

# Fonction pour charger les caches des feuilles de matchs et des postes des joueurs
def charger_cache():
    global cache_noms_joueurs   # Accès aux caches globaux
    cache_noms_joueurs = charger_cache_noms_joueurs()   # Charger le cache des matchs

def generer_df_quipe_nom(joueur_id):

    # Charger le cache
    charger_cache()

    # Trouver le poste du joueur avec son ID
    joueur_equipe = obtenir_equipeABV_avec_joueurID(joueur_id)

    # Trouver le nom du joueur avec son ID
    joueur_nom = remplir_cache_noms_joueurs(joueur_id)

    # Sauvegarder le cache des matchs
    sauvegarder_cache_noms_joueurs(cache_noms_joueurs)

    # Retourner les résultats sous forme de tuple
    return (joueur_equipe, joueur_nom)

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1628384, 203076, 1628983, 1627742, 1628368, 1626164, 1627759, 203944, 1630163, 1628374, 1631094, 202331, 1630567, 1630169, 1629627, 203078, 1641706, 1630595, 1630166, 1628978, 1630596, 1630532, 1631105, 1627750, 201935, 1628386, 1628398, 1629008, 1629628, 201566, 202699, 1630178, 1641705, 203952, 1630559, 1626156, 1627832, 202330]

    # Créer le DataFrame final avec les colonnes nécessaires
    df_equipes_noms = pd.DataFrame(columns=['Equipe', 'Joueur'])

    # Boucle à l'extérieur de la fonction
    for joueur_id in ids_joueurs:
        resultats = generer_df_quipe_nom(joueur_id)
        df_equipes_noms.loc[len(df_equipes_noms)] = resultats

    # Enlever les joueurs
    # df_postes = df_equipe_nom.drop(columns=['Joueur'])

    # Print du tableau
    print(df_equipes_noms)