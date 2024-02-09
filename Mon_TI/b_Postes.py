import pandas as pd

from z_Utilitaires import obtenir_joueurNom_avec_joueurID, obtenir_joueurPosteAbregee_avec_joueurID

def generer_df_postes(joueur_id):
    # Trouver le nom du joueur avec son ID
    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

    # Trouver le poste du joueur avec son ID
    joueur_poste = obtenir_joueurPosteAbregee_avec_joueurID(joueur_id)

    # Retourner les résultats sous forme de tuple
    return (joueur_nom, joueur_poste)

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1630578,203952,203076,1630162,1630559,1628389,203078,1627742,1641706,1630595,1631096,1626156,203081,1628368,1627749,201942,1630217,1626164,1627734,1628378,1630596,1627832,203507,202330,1629630,1628973,1627750,201935,1628991,1628386,1627759,1628369,203924,202710,203954,1630228,203944,1626157,202695,201142,203114,204001,1628398,202681,1630163,1628374,2544,1629029,1629008,1628970,203999,202696,1631094,1627783,202331,1629628,203497,201566,1630567,1628983,201939,1626179,202699,1629027,1629639,1630169,1630178,1641705,203897,1629627]

    # Créer le DataFrame final avec les colonnes nécessaires
    df_postes = pd.DataFrame(columns=['Joueur', 'Poste'])

    # Boucle à l'extérieur de la fonction
    for joueur_id in ids_joueurs:
        resultats = generer_df_postes(joueur_id)
        df_postes.loc[len(df_postes)] = resultats

    # Enlever les joueurs
    # df_postes = df_postes.drop(columns=['Joueur'])

    # df_postes.to_excel('Postes_complet.xlsx', index=False)

    # Print du tableau
    print(df_postes)