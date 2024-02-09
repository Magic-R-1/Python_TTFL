import pandas as pd
from datetime import datetime
from z_Utilitaires import obtenir_joueurNom_avec_joueurID, obtenir_equipeID_avec_joueurID
from z_DataFrames_globaux import obtenir_prochains_matchs_DF_globaux

def obtenir_prochains_matchs_joueurs(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour):

    joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)
    id_equipe_joueur = obtenir_equipeID_avec_joueurID(joueur_id)

    if id_equipe_joueur is not None:
        df_prochains_matchs = obtenir_prochains_matchs_DF_globaux(joueur_id)

        # Convertir la colonne 'GAME_DATE' en type de données datetime
        df_prochains_matchs['GAME_DATE'] = pd.to_datetime(df_prochains_matchs['GAME_DATE'], format='%b %d, %Y')

        # Filtrer pour ne garder que les dates après cellequi nous intéresse et reset l'index, pour que la boucle ci-dessous fonctionne
        df_prochains_matchs = df_prochains_matchs[df_prochains_matchs['GAME_DATE'] >= date_du_jour].reset_index(drop=True)

        data = {'Joueur': [joueur_nom]}
        for i in range(1 + nb_matchs_a_sauter, nb_prochains_matchs + 1 + nb_matchs_a_sauter):

            home_team_id = df_prochains_matchs.loc[i - 1, 'HOME_TEAM_ID']

            if id_equipe_joueur == home_team_id:
                adversaire_type = 'vs'
                adversaire = df_prochains_matchs.loc[i - 1, 'VISITOR_TEAM_ABBREVIATION']
            else:
                adversaire_type = '@'
                adversaire = df_prochains_matchs.loc[i - 1, 'HOME_TEAM_ABBREVIATION']
            
            data[f'M+{i}_H_A'] = adversaire_type
            data[f'M+{i}_team'] = adversaire

        # Création du DataFrame avec les données
        df_X_prochains_matchs = pd.DataFrame(data)

        return df_X_prochains_matchs
    else:
        return None

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Date du jour qui nous intéresse
    date_du_jour = '09/02/2024'
    date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y') # Convertir la chaîne en objet datetime
    date_du_jour = date_du_jour.strftime("%b %d, %Y") # Formater la date

    # Liste d'identifiants de joueurs
    # joueurs_ids = [2544, 1629029]
    joueurs_ids = [1630595]

    # Nombre de prochains matchs à récupérer
    nb_prochains_matchs = 4

    # Nombre de matchs à sauter
    nb_matchs_a_sauter = 1

    # Créer le DataFrame final
    df_X_prochains_matchs = pd.DataFrame()

    for joueur_id in joueurs_ids:
        df_X_prochains_matchs = pd.concat([df_X_prochains_matchs, obtenir_prochains_matchs_joueurs(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)], ignore_index=True)

    # Enlever les joueurs
    # df_X_prochains_matchs = df_X_prochains_matchs.drop(columns=['Joueur'])

    # Print du tableau
    print(df_X_prochains_matchs)