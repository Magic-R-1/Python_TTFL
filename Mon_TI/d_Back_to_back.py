import pandas as pd
from datetime import datetime, timedelta
from z_Utilitaires import obtenir_joueurNom_avec_joueurID, obtenir_integralite_calendrier_joueur_avec_joueurID

def est_en_back_to_back(joueur_id, date_du_jour):

    try:
        # Trouver le nom joueur
        joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

        # Obtenir l'intégralité des dates du joueurs
        df_liste_integralite_dates = obtenir_integralite_calendrier_joueur_avec_joueurID(joueur_id)

        # Convertir date_du_jour en Timestamp
        date_du_jour = pd.Timestamp(date_du_jour)

        # Vérifier si le joueur a joué la veille
        veille = (date_du_jour - timedelta(days=1)) in df_liste_integralite_dates.values

        if veille:
            return joueur_nom,'O'
        else:
            return joueur_nom,''
    
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1628398]

    date_du_jour = '09/02/2024'
    # Conversion de la date du jour
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y') # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y") # Formater la date

    # Créer le DataFrame final avec les colonnes nécessaires
    df_back_to_back = pd.DataFrame(columns=['Joueur', 'B2B'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        # Ajouter une nouvelle ligne directement avec loc
        df_back_to_back.loc[len(df_back_to_back)] = est_en_back_to_back(joueur_id, date_du_jour)

    # Enlever les joueurs
    # df_back_to_back = df_back_to_back.drop(columns=['Joueur'])

    print(df_back_to_back)