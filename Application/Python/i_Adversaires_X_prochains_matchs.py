import pandas as pd
from datetime import datetime

from x_Utilitaires import *
from x_DataFrames_globaux import *

# ------------------------------
# Fonction pour convertir la date
def convertir_date(date_du_jour):
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y')  # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y")           # Formater la date
    return date_du_jour

# ------------------------------
# Fonction pour obtenir les prochains matchs d'un joueur
def obtenir_DF_X_prochains_matchs_un_joueur(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)
    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)

    if id_equipe_joueur is not None:

        # Obtenir le DF des prochains matchs du joueur
        DF_prochains_matchs_1 = obtenir_PlayerNextNGames_DF_globaux(joueur_id)

        # Copie du DF, puisqu'il me semble que la conversion de la date la ligne suivante, impactait le DF_joueur dans d'autres modules...
        DF_prochains_matchs = DF_prochains_matchs_1.copy()

        # Convertir la colonne 'GAME_DATE' en type de données datetime
        DF_prochains_matchs['GAME_DATE'] = pd.to_datetime(DF_prochains_matchs['GAME_DATE'], format='%b %d, %Y')

        # Filtrer pour ne garder que les dates après celle qui nous intéresse et reset l'index, pour que la boucle ci-dessous fonctionne
        DF_prochains_matchs = DF_prochains_matchs[DF_prochains_matchs['GAME_DATE'] >= date_du_jour].reset_index(drop=True)

        # S'assurer qu'il reste assez de matchs pour en obtenir le nombre souhaité (problématique en fin de saison)
        nombreDeMatchsRestants = len(DF_prochains_matchs)
        indexMin = nb_matchs_a_sauter
        indexMax = min(nb_prochains_matchs + nb_matchs_a_sauter, nombreDeMatchsRestants)
        
        # Cas du dernier match de la saison
        if nombreDeMatchsRestants == 1:
            indexMax += 1

        array_tmp_prochains_matchs = {'Joueur': [joueur_nom]}

        # Gestion du dernier match de la saison, et d'un match à sauter (donc pas possible)
        if nombreDeMatchsRestants == 1 and nb_matchs_a_sauter>0:
            for i in range(0, 3):
                array_tmp_prochains_matchs[f'M+{i+1}_H_A'] = "-"
                array_tmp_prochains_matchs[f'M+{i+1}_team'] = "-"
        else:
            for i in range(indexMin, indexMax):

                home_team_id = DF_prochains_matchs.loc[i, 'HOME_TEAM_ID']

                if id_equipe_joueur == home_team_id:
                    adversaire_H_A = 'vs'
                    adversaireABV = DF_prochains_matchs.loc[i, 'VISITOR_TEAM_ABBREVIATION']
                else:
                    adversaire_H_A = '@'
                    adversaireABV = DF_prochains_matchs.loc[i, 'HOME_TEAM_ABBREVIATION']
                
                array_tmp_prochains_matchs[f'M+{i+1}_H_A'] = adversaire_H_A
                array_tmp_prochains_matchs[f'M+{i+1}_team'] = adversaireABV

                # Cas du dernier match de la saison, et pas de match à sauter
                if nombreDeMatchsRestants == 1:
                    break

        # Création du DataFrame avec les données
        DF_X_prochains_matchs_un_joueur = pd.DataFrame(array_tmp_prochains_matchs)

        return DF_X_prochains_matchs_un_joueur
    else:
        return None

# ------------------------------
# Fonction bouclant pour construire le DF final
def obtenir_DF_X_prochains_matchs(ids_joueurs, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour):

    date_du_jour = convertir_date(date_du_jour)

    # Créer une liste pour stocker les DataFrames de chaque joueur
    liste_DF_X_prochains_matchs = []

    for joueur_id in ids_joueurs:
        # Obtenir le DataFrame des prochains matchs pour un joueur
        DF_X_prochains_matchs_un_joueur = obtenir_DF_X_prochains_matchs_un_joueur(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)
        # Ajouter le DataFrame à la liste
        liste_DF_X_prochains_matchs.append(DF_X_prochains_matchs_un_joueur)

    # Concaténer tous les DataFrames de la liste en un seul DataFrame
    DF_X_prochains_matchs = pd.concat(liste_DF_X_prochains_matchs, ignore_index=True)

    # Gestion des 0 (en fin de saison)
    # DF_X_prochains_matchs = DF_X_prochains_matchs.fillna(0)             # Trasnformer les NaN en 0
    # DF_X_prochains_matchs = DF_X_prochains_matchs.round(0).astype(int)  # Convertir les valeurs en integer pour ne plus avoir de décimales
    # DF_X_prochains_matchs = DF_X_prochains_matchs.replace(0,"-")        # Remplacer les 0 par des tirets pour la lisibilité

    # Enlever les joueurs pour les besoins du TI global
    DF_X_prochains_matchs = DF_X_prochains_matchs.drop(columns=['Joueur'])

    # Retourner le DataFrame final
    return DF_X_prochains_matchs

# ------------------------------
# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Variables
    ids_joueurs = [1628378, 203507, 203954, 203999, 1630578, 1630162, 1627742, 201942, 1628369, 202710, 1630228, 1626157, 202695, 1628374, 2544, 1631094, 203497, 1630567, 201939, 1629027, 1630169, 1629627, 1641708, 203992, 203078, 1641706, 1630595, 1631096, 1629028, 1630166, 1630596, 1630532, 1631105, 1630552, 1627750, 201935, 1628991, 203114, 204001, 1628398, 1629008, 1628970, 202696, 1629628, 1629060, 201566, 1626179, 202699]
    nb_prochains_matchs = 1     # Nombre de prochains matchs à récupérer
    nb_matchs_a_sauter = 0      # Nombre de matchs à sauter
    date_du_jour = '14/04/2024' # Date du jour qui nous intéresse

    DF_X_prochains_matchs = obtenir_DF_X_prochains_matchs(ids_joueurs, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)

    # Print du tableau
    print(DF_X_prochains_matchs)