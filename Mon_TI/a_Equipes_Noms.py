import pandas as pd

from z_Utilitaires import obtenir_joueurNom_avec_joueurID, obtenir_equipeABV_avec_joueurID

def generer_df_quipe_nom(joueur_id):
    # Trouver le poste du joueur avec son ID
    joueur_equipe = obtenir_equipeABV_avec_joueurID(joueur_id)

    # Trouver le nom du joueur avec son ID
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Retourner les résultats sous forme de tuple
    return (joueur_equipe, joueur_nom)

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [203076, 203944, 2544]

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