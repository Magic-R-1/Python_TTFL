import pandas as pd
from datetime import datetime, timedelta

from x_Utilitaires import *

# ------------------------------
# Fonction pour obtenir le fait que le joueur soit en B2B ou non
def obtenir_array_B2B(joueur_id, date_du_jour):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id) # Nom du joueur avec son ID

    # Obtenir l'intégralité des dates du joueurs
    DF_liste_integralite_dates = obtenir_integralite_calendrier_joueur_avec_joueurID(joueur_id)

    # Vérifier si le joueur a joué la veille
    veille = (date_du_jour - timedelta(days=1)) in DF_liste_integralite_dates.values

    # Test d'attribution du B2B ou non
    joueur_B2B = 'O' if veille else ''

    array_B2B = [joueur_nom, joueur_B2B]

    return array_B2B

# ------------------------------
# Fonction pour convertir la date
def convertir_date_du_jour(date_du_jour):
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y')  # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y")           # Formater la date
    date_du_jour = pd.Timestamp(date_du_jour)                   # Convertir date_du_jour en Timestamp
    return date_du_jour

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_back_to_back(ids_joueurs, date_du_jour):
    
    # Conversion de la date du jour
    date_du_jour = convertir_date_du_jour(date_du_jour)

    # Créer le DataFrame final avec les colonnes nécessaires
    DF_back_to_back = pd.DataFrame(columns=['Joueur', 'B2B'])

    # Boucler sur les joueurs
    for joueur_id in ids_joueurs:
        array_B2B = obtenir_array_B2B(joueur_id, date_du_jour)  # Obtention de l'array
        DF_back_to_back.loc[len(DF_back_to_back)] = array_B2B   # Ajout en dernière ligne du DF
    
    # Enlever les joueurs pour les besoins du TI global
    DF_back_to_back = DF_back_to_back.drop(columns=['Joueur'])

    return DF_back_to_back

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste d'identifiants de joueurs
    ids_joueurs = [1628378, 203507, 203954, 203999, 1630578, 1630162, 1627742, 201942, 1628369, 202710, 1630228, 1626157, 202695, 1628374, 2544, 1631094, 203497, 1630567, 201939, 1629027, 1630169, 1629627, 1641708, 203992, 203078, 1641706, 1630595, 1631096, 1629028, 1630166, 1630596, 1630532, 1631105, 1630552, 1627750, 201935, 1628991, 203114, 204001, 1628398, 1629008, 1628970, 202696, 1629628, 1629060, 201566, 1626179, 202699]
    date_du_jour = '14/04/2024'

    DF_back_to_back = obtenir_DF_back_to_back(ids_joueurs, date_du_jour)

    print(DF_back_to_back)