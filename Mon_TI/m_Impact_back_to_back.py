import pandas as pd
from d_Back_to_back import obtenir_df_back_to_back
from z_DataFrames_globaux import obtenir_game_log_DF_globaux
from z_Utilitaires import calcul_score_TTFL, obtenir_joueurNom_avec_joueurID

def obtenir_stats_joueur_avec_delta_jours(joueur_id):
    # Obtenir le DF du joueur
    df_joueur = obtenir_game_log_DF_globaux(joueur_id)

    # Convertir la colonne 'GAME_DATE' en type de données datetime
    df_joueur['GAME_DATE'] = pd.to_datetime(df_joueur['GAME_DATE'], format='%b %d, %Y')

    # Tri des données par date
    df_joueur = df_joueur.sort_values(by='GAME_DATE')

    # Ajout d'une colonne avec le calcul du nombre de jours entre chaque match
    df_joueur['jours_entre'] = df_joueur['GAME_DATE'].diff().dt.days

    return df_joueur

def obtenir_nombre_de_B2B(joueur_id):
    df_joueur = obtenir_stats_joueur_avec_delta_jours(joueur_id)

    # Filtrer les 2èmes jours et calculer le score TTFL moyen
    df_2e_jour = df_joueur[df_joueur['jours_entre'] == 1]

    nombre_de_B2B = len(df_2e_jour)

    return nombre_de_B2B

def obtenir_moyenne_TTFL_hors_B2B(joueur_id):
    df_joueur = obtenir_stats_joueur_avec_delta_jours(joueur_id)

    # Filtrer les matchs qui ne sont pas un deuxième jour consécutif
    df_non_consecutifs = df_joueur[df_joueur['jours_entre'] != 1]

    # Calculer la moyenne TTFL pour ces matchs
    moyenne_TTFL_hors_B2B = df_non_consecutifs.apply(calcul_score_TTFL, axis=1).mean().round(1)

    return moyenne_TTFL_hors_B2B

def obtenir_moyenne_TTFL_B2B(joueur_id):
    df_joueur = obtenir_stats_joueur_avec_delta_jours(joueur_id)

    # Filtrer les 2èmes jours et calculer le score TTFL moyen
    df_2e_jour = df_joueur[df_joueur['jours_entre'] == 1]

    # Calculer le score TTFL moyen pour toutes les lignes de df_2e_jour
    moyenne_TTFL_B2B = df_2e_jour.apply(calcul_score_TTFL, axis=1).mean().round(1)

    return moyenne_TTFL_B2B

def obtenir_delta_B2B(joueur_id):
    moyenne_TTFL_hors_B2B = obtenir_moyenne_TTFL_hors_B2B(joueur_id)
    moyenne_B2B = obtenir_moyenne_TTFL_B2B(joueur_id)

    delta_B2B = (moyenne_B2B - moyenne_TTFL_hors_B2B).round(1)

    return delta_B2B

def obtenir_resultats_impact_B2B(ids_joueurs, date_du_jour):

    # Créer le DataFrame final avec les colonnes nécessaires
    df_impact_B2B = pd.DataFrame(columns=['Joueur', 'delta_B2B', 'nombre_de_B2B'])

    df_back_to_back = obtenir_df_back_to_back(ids_joueurs, date_du_jour)

    print(df_back_to_back)

    for joueur_id, row in zip(ids_joueurs, df_back_to_back.iterrows()):
        joueur_nom = obtenir_joueurNom_avec_joueurID(joueur_id)
        if row[1]['B2B'] == 'O':
            delta_B2B = obtenir_delta_B2B(joueur_id)
            nombre_de_B2B = obtenir_nombre_de_B2B(joueur_id)
        else:
            delta_B2B = ''
            nombre_de_B2B = ''

        # Utiliser la fonction pd.concat pour ajouter une nouvelle ligne au DataFrame
        df_impact_B2B.loc[len(df_impact_B2B)] = [joueur_nom, delta_B2B, nombre_de_B2B]
    
    # Enlever les joueurs pour les besoins du TI global
    df_impact_B2B = df_impact_B2B.drop(columns=['Joueur'])

    return df_impact_B2B

# N'exécuter que si appelé ici directement
if __name__ == "__main__":

    # Liste de joueurs
    ids_joueurs = [2544, 201935, 202695, 202331, 1630567, 1628398, 203076, 1628983, 1627742, 1628368, 1626164]
    date_du_jour = '09/02/2024'

    df_impact_B2B = obtenir_resultats_impact_B2B(ids_joueurs, date_du_jour)

    print(df_impact_B2B)