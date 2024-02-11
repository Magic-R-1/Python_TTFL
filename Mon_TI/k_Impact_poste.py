import pandas as pd
import numpy as np
import sys
import time
from z_Utilitaires import *
from z_DataFrames_globaux import *

def obtenir_liste_ids_matchs_equipe(equipe_id):
    equipe_matchs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)
    df_matchs_equipe = equipe_matchs[['Game_ID']]
    return df_matchs_equipe

# Fonction pour obtenir les logs d'un match avec un match_id spécifique et l'identifiant d'une équipe
def obtenir_logs_match_avec_matchID(match_id, equipe_id):
    global cache_match_data  # Pour accéder au dictionnaire global
    global cache_postes_joueurs # Pour accéder au dictionnaire global

    # Obtenir les logs du match
    logs_match = remplir_cache_match_data(match_id)

    # Filtrer les données pour l'équipe spécifiée
    logs_equipe = logs_match.loc[logs_match['TEAM_ID'] != equipe_id]
    logs_equipe = logs_equipe.loc[logs_match['MIN'].notnull()]
    logs_equipe['poste'] = logs_equipe['PLAYER_ID'].apply(remplir_cache_poste_abrege_data)
    logs_equipe['Score_TTFL'] = logs_equipe.apply(calcul_score_TTFL, axis=1).astype(int)
    logs_equipe['MIN'] = logs_equipe['MIN'].str.extract(r'(\d+)').astype(int)
    logs_equipe['Score_TTFL_MIN'] = logs_equipe['MIN'] * logs_equipe['Score_TTFL']
    
    return logs_equipe

# Fonction pour obtenir les statistiques moyennes par poste pour un match donné et une équipe donnée
def obtenir_df_moyenne_par_poste(match_id, equipe_id):
    logs_equipe = obtenir_logs_match_avec_matchID(match_id, equipe_id)
    df_postes = pd.DataFrame(['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'], columns=['Poste'])
    sommes_TTFL = []
    sommes_MIN = []

    for poste in df_postes['Poste']:
        lignes_poste = logs_equipe[logs_equipe['poste'] == poste]
        somme_score_ttfl = lignes_poste['Score_TTFL_MIN'].sum()
        somme_minutes = lignes_poste['MIN'].sum()
        sommes_TTFL.append(somme_score_ttfl)
        sommes_MIN.append(somme_minutes)

    df_postes['Somme_TTFL'] = sommes_TTFL
    df_postes['Somme_MIN'] = sommes_MIN

    return df_postes

# Fonction principale pour obtenir les moyennes pondérées TTFL par poste pour chaque équipe
def obtenir_moyennes_ttfl_par_equipe():

    # Tout début de fonction, on commence par charger le cache des feuilles de matchs
    global cache_match_data  # Pour accéder au dictionnaire global
    global cache_postes_joueurs  # Pour accéder au dictionnaire global
    # charger_le_cache_global()
    cache_match_data = charger_cache_match_data()
    cache_postes_joueurs = charger_cache_postes_joueurs()

    # Obtenir la liste des identifiants des équipes
    # liste_equipes_id = [1610612747, 1610612738]  # Utilisation d'une liste ordonnée
    liste_equipes_id = obtenir_liste_equipes_ids_DF_globaux()
    total_equipes = len(liste_equipes_id)

    # Initialisation d'un dictionnaire pour stocker les résultats par équipe
    resultats_par_equipe = {}

    # Initialisation des listes pour stocker les sommes totales
    somme_ttfl_totale = np.zeros(7)
    somme_min_totale = np.zeros(7)
    moyenne_ttfl_ponderee_totale = np.zeros(7)

    # Boucle sur chaque équipe
    for equipe_id in liste_equipes_id:
        equipe_ABV = remplir_cache_equipe_abv_data(equipe_id)
        df_matchs_equipe = obtenir_liste_ids_matchs_equipe(equipe_id)
        total_matchs = len(df_matchs_equipe)

        # Initialisation des listes pour stocker les sommes totales
        somme_ttfl_par_poste = []
        somme_min_par_poste = []

        # Afficher la progression du match
        for match_index, match_id in enumerate(df_matchs_equipe['Game_ID'], start=1):
            match_progression = (match_index + total_matchs - len(df_matchs_equipe)) / total_matchs * 100

            equipe_index = liste_equipes_id.index(equipe_id)+1
            equipe_abv = obtenir_equipeABV_avec_equipeID(equipe_id)
            equipe_progression = (equipe_index/total_equipes)*100

            match_message = f"\r Équipe {equipe_abv} {equipe_index}/{total_equipes} ({equipe_progression:.2f}%) - Match {match_index} sur {total_matchs} ({match_progression:.2f}%)"
            sys.stdout.write(match_message + ' ' * (len(match_message) - 1))  # Effacer la ligne précédente
            sys.stdout.flush()

            # Obtention des statistiques par poste pour ce match
            df_statistiques_match = obtenir_df_moyenne_par_poste(match_id, equipe_id)

            # Somme des valeurs de Somme_TTFL et Somme_MIN par poste
            somme_ttfl_par_poste.append(df_statistiques_match['Somme_TTFL'].values)
            somme_min_par_poste.append(df_statistiques_match['Somme_MIN'].values)

        # Somme des valeurs par poste sur tous les matchs pour cette équipe
        somme_ttfl_totale_par_poste = np.sum(somme_ttfl_par_poste, axis=0)
        somme_min_totale_par_poste = np.sum(somme_min_par_poste, axis=0)
        moyenne_ttfl_ponderee = np.round(somme_ttfl_totale_par_poste / somme_min_totale_par_poste, 1)

        # Somme des valeurs totales pour toutes les équipes
        somme_ttfl_totale += somme_ttfl_totale_par_poste
        somme_min_totale += somme_min_totale_par_poste

        # Ajouter les résultats de cette équipe au dictionnaire
        resultats_par_equipe[equipe_ABV] = moyenne_ttfl_ponderee

    # Fin de boucle, donc on commence par sauvegarder le cache des feuilles de matchs
    # sauvegarder_le_cache_global()
    sauvegarder_cache_match_data(cache_match_data)
    sauvegarder_cache_postes_joueurs(cache_postes_joueurs)

    # Création du DataFrame final à partir du dictionnaire
    df_impact_poste = pd.DataFrame(resultats_par_equipe)

    # Conversion en integer
    somme_ttfl_totale = somme_ttfl_totale.astype(int)
    somme_min_totale = somme_min_totale.astype(int)

    # Ajout de la colonne 'Poste' en première position
    df_impact_poste.insert(0, 'Poste', ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'])
    
    # Ajout des colonnes de somme totale
    df_impact_poste.insert(1, 'TTFL', somme_ttfl_totale)
    df_impact_poste.insert(2, 'Minutes', somme_min_totale)
    moyenne_ttfl_ponderee_totale = np.round(somme_ttfl_totale / somme_min_totale,1)
    df_impact_poste.insert(3, 'Moyenne', moyenne_ttfl_ponderee_totale)

    # Créer un DF avec les delta, plutôt que les valeurs
    df_impact_poste_delta = df_impact_poste
    
    # Sélectionnez les colonnes de la 4ème à la 33ème
    columns_to_subtract = df_impact_poste_delta.columns[4:]

    # Soustraire la colonne 'Moyenne' des colonnes sélectionnées
    df_impact_poste_delta[columns_to_subtract] = df_impact_poste_delta[columns_to_subtract].sub(df_impact_poste_delta['Moyenne'], axis=0)

    # Le transposer, puis remettre les colonnes qui sont devenus les index
    df_impact_poste_delta_transposed = df_impact_poste_delta.transpose() # Transposer le DataFrame
    df_impact_poste_delta_transposed.reset_index(drop=False, inplace=True) # Réinitialiser les index et rétablir les intitulés de colonnes
    # print(df_impact_poste_delta_transposed)
    print()
    exporter_vers_Excel_impact_poste(df_impact_poste_delta_transposed)

# Enregistrez le temps de début
temps_debut = time.time()

# Appel de la fonction principale pour obtenir les moyennes pondérées TTFL par poste pour chaque équipe
obtenir_moyennes_ttfl_par_equipe()

# Enregistrez le temps de fin
temps_fin = time.time()
# Calculez la durée d'exécution
duree_execution = temps_fin - temps_debut
minutes = int(duree_execution // 60)
secondes = int(duree_execution % 60)
print(f"Le code a pris {minutes} minutes et {secondes} secondes pour s'exécuter.")