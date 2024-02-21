import pandas as pd
from datetime import datetime, timedelta
from z_Utilitaires import *

def obtenir_df_back_to_back(ids_joueurs, date_du_jour):

    date_du_jour = convertir_date_du_jour(date_du_jour) # Conversion de la date du jour

    # Créer le DataFrame final avec les colonnes nécessaires
    df_back_to_back = pd.DataFrame(columns=['Joueur', 'B2B'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:

        try:
            # Trouver le nom joueur
            joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)

            # Obtenir l'intégralité des dates du joueurs
            df_liste_integralite_dates = obtenir_integralite_calendrier_joueur_avec_joueurID(joueur_id)

            # Vérifier si le joueur a joué la veille
            veille = (date_du_jour - timedelta(days=1)) in df_liste_integralite_dates.values

            # Test d'attribution du B2B ou non
            joueur_B2B = 'O' if veille else ''
            
            # Ajouter une nouvelle ligne directement avec loc
            df_back_to_back.loc[len(df_back_to_back)] = joueur_nom, joueur_B2B
        
        except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"
    
    # Enlever les joueurs pour les besoins du TI global
    df_back_to_back = df_back_to_back.drop(columns=['Joueur'])

    return df_back_to_back

def convertir_date_du_jour(date_du_jour):
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y')  # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y")           # Formater la date
    date_du_jour = pd.Timestamp(date_du_jour)                   # Convertir date_du_jour en Timestamp
    return date_du_jour

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [2544, 201935, 202695, 202331, 1630567, 1628398, 203076, 1628983, 1627742, 1628368, 1626164]
    date_du_jour = '09/02/2024'

    df_back_to_back = obtenir_df_back_to_back(ids_joueurs, date_du_jour)

    print(df_back_to_back)