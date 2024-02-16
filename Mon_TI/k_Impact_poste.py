import pandas as pd
import numpy as np
import sys
import time
from z_Utilitaires import *  # Import des fonctions utilitaires personnalisées
from z_DataFrames_globaux import *  # Import des DataFrames globaux

# Fonction pour obtenir la liste des identifiants des équipes à partir des données globales
def obtenir_liste_equipes_ids():
    return obtenir_liste_equipes_ids_DF_globaux()
    # return [1610612747, 1610612738]

# Fonction pour obtenir la liste des identifiants des matchs d'une équipe
def obtenir_liste_ids_matchs_equipe(equipe_id):
    # Obtenir les derniers matchs de l'équipe à partir des données globales
    equipe_matchs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)
    # Sélectionner uniquement la colonne 'Game_ID'
    df_matchs_equipe = equipe_matchs[['Game_ID']]
    return df_matchs_equipe

# Fonction pour obtenir les logs d'un match spécifique pour une équipe donnée
def obtenir_logs_match_avec_matchID(match_id, equipe_id):
    global cache_match_data  # Accès au cache global des matchs
    global cache_postes_joueurs  # Accès au cache global des postes des joueurs

    # Obtenir les logs du match à partir du cache des matchs
    logs_match = remplir_cache_match_data(match_id)

    # Filtrer les données pour l'équipe spécifiée
    logs_equipe = logs_match.loc[logs_match['TEAM_ID'] != equipe_id]
    logs_equipe = logs_equipe.loc[logs_match['MIN'].notnull()]  # Supprimer les lignes avec MIN nul
    # Ajouter la colonne 'poste' en utilisant les postes abrégés des joueurs
    logs_equipe['poste'] = logs_equipe['PLAYER_ID'].apply(remplir_cache_poste_abrege_data)
    # Calculer le score TTFL pour chaque joueur
    logs_equipe['Score_TTFL'] = logs_equipe.apply(calcul_score_TTFL, axis=1).astype(int)
    # Extraire et convertir la durée de jeu en minutes
    logs_equipe['MIN'] = logs_equipe['MIN'].str.extract(r'(\d+)').astype(int)
    # Calculer le score TTFL total pour chaque joueur dans le temps de jeu
    logs_equipe['Score_TTFL_MIN'] = logs_equipe['MIN'] * logs_equipe['Score_TTFL']
    
    return logs_equipe

# Fonction pour charger les caches des feuilles de matchs et des postes des joueurs
def charger_cache_feuilles_matchs():
    global cache_match_data, cache_postes_joueurs  # Accès aux caches globaux
    cache_match_data = charger_cache_match_data()  # Charger le cache des matchs
    cache_postes_joueurs = charger_cache_postes_joueurs()  # Charger le cache des postes des joueurs

# Fonction pour obtenir les matchs d'une équipe à partir des données globales
def obtenir_matchs_equipe(equipe_id):
    equipe_matchs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)
    return equipe_matchs[['Game_ID']]

# Fonction pour obtenir les statistiques moyennes par poste pour un match et une équipe donnée
def obtenir_df_moyenne_par_poste(match_id, equipe_id):
    logs_equipe = obtenir_logs_match_avec_matchID(match_id, equipe_id)
    # Créer un DataFrame pour les postes
    df_postes = pd.DataFrame(['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'], columns=['Poste'])
    sommes_TTFL = []
    sommes_MIN = []

    # Calculer les sommes TTFL et MIN pour chaque poste
    for poste in df_postes['Poste']:
        lignes_poste = logs_equipe[logs_equipe['poste'] == poste]
        somme_score_ttfl = lignes_poste['Score_TTFL_MIN'].sum()
        somme_minutes = lignes_poste['MIN'].sum()
        sommes_TTFL.append(somme_score_ttfl)
        sommes_MIN.append(somme_minutes)

    # Ajouter les sommes calculées au DataFrame des postes
    df_postes['Somme_TTFL'] = sommes_TTFL
    df_postes['Somme_MIN'] = sommes_MIN

    return df_postes

# Fonction pour calculer la moyenne pondérée TTFL par poste à partir des statistiques
def calculer_moyenne_ponderee_ttfl_par_poste(df_postes):
    somme_ttfl_totale_par_poste = df_postes['Somme_TTFL'].sum()
    somme_min_totale_par_poste = df_postes['Somme_MIN'].sum()
    moyenne_ttfl_ponderee = np.round(somme_ttfl_totale_par_poste / somme_min_totale_par_poste, 1)
    return moyenne_ttfl_ponderee

# Fonction pour transposer mon DF avec la gestion des index
def transposer_mon_DF(df_impact_poste_delta):
    # Transposer
    df_transposed = df_impact_poste_delta.transpose()

    # Réinitialiser l'index du DataFrame transposé
    df_transposed.reset_index(drop=False, inplace=True)

    # Faire prendre aux intitulés de colonnes la ligne d'index 0
    df_transposed.columns = df_transposed.iloc[0]

    # Conserver le DF à partir de la ligne d'index 1 (en plus des intitulés de colonnes), pour ne pas garder celle d'index 0 qui est en doublon avec le code précédent
    df_transposed = df_transposed[1:]

    # Supprimer la colonne 'Poste' des index, elle n'est plus d'index 0
    df_transposed = df_transposed.rename_axis(None, axis=1)

    # Reset à nouveau l'index pour le faire partir de 0 après les intitulés de colonnes
    df_transposed.reset_index(drop=True, inplace=True)

    return df_transposed

# Fonction principale pour obtenir les variations de moyennes pondérées TTFL par poste pour chaque équipe
def obtenir_delta_ttfl_postes():
    charger_cache_feuilles_matchs()  # Charger les caches des feuilles de matchs

    liste_equipes_id = obtenir_liste_equipes_ids()  # Obtenir la liste des identifiants des équipes
    total_equipes = len(liste_equipes_id)  # Calculer le nombre total d'équipes
    
    resultats_par_equipe = {}  # Initialiser le dictionnaire pour stocker les résultats par équipe
    somme_ttfl_totale = np.zeros(7)  # Initialiser les sommes totales des scores TTFL par poste
    somme_min_totale = np.zeros(7)  # Initialiser les sommes totales des minutes par poste

    # Boucle sur chaque équipe
    for equipe_id in liste_equipes_id:
        equipe_ABV = remplir_cache_equipe_abv_data(equipe_id)  # Obtenir l'abréviation de l'équipe
        df_matchs_equipe = obtenir_liste_ids_matchs_equipe(equipe_id)  # Obtenir les matchs de l'équipe
        total_matchs = len(df_matchs_equipe)  # Calculer le nombre total de matchs pour l'équipe
        somme_ttfl_par_poste = []  # Initialiser la liste des sommes TTFL par poste
        somme_min_par_poste = []  # Initialiser la liste des sommes MIN par poste

        # Boucle sur chaque match de l'équipe
        for match_index, match_id in enumerate(df_matchs_equipe['Game_ID'], start=1):

            # Message de progression
            match_progression = (match_index + total_matchs - len(df_matchs_equipe)) / total_matchs * 100
            equipe_index = liste_equipes_id.index(equipe_id) + 1
            equipe_abv = obtenir_equipeABV_avec_equipeID(equipe_id)
            equipe_progression = (equipe_index / total_equipes) * 100

            match_message = f"\r Équipe {equipe_abv} {equipe_index}/{total_equipes} ({equipe_progression:.2f}%) - Match {match_index} sur {total_matchs} ({match_progression:.2f}%)"
            sys.stdout.write(match_message)
            sys.stdout.flush()

            df_statistiques_match = obtenir_df_moyenne_par_poste(match_id, equipe_id)  # Obtenir les statistiques par poste pour le match
            somme_ttfl_par_poste.append(df_statistiques_match['Somme_TTFL'].values)  # Ajouter la somme TTFL par poste à la liste
            somme_min_par_poste.append(df_statistiques_match['Somme_MIN'].values)  # Ajouter la somme MIN par poste à la liste

        somme_ttfl_totale_par_poste = np.sum(somme_ttfl_par_poste, axis=0)  # Somme des scores TTFL par poste pour tous les matchs
        somme_min_totale_par_poste = np.sum(somme_min_par_poste, axis=0)  # Somme des minutes par poste pour tous les matchs
        somme_ttfl_totale += somme_ttfl_totale_par_poste  # Ajouter les sommes TTFL par poste aux sommes totales
        somme_min_totale += somme_min_totale_par_poste  # Ajouter les sommes MIN par poste aux sommes totales

        # Calculer la moyenne pondérée TTFL par poste pour l'équipe et l'ajouter au dictionnaire des résultats
        resultats_par_equipe[equipe_ABV] = np.round(somme_ttfl_totale_par_poste / somme_min_totale_par_poste, 1)

    sauvegarder_cache_match_data(cache_match_data)  # Sauvegarder le cache des matchs
    sauvegarder_cache_postes_joueurs(cache_postes_joueurs)  # Sauvegarder le cache des postes des joueurs

    # Créer un DataFrame à partir du dictionnaire des résultats
    df_impact_poste = pd.DataFrame(resultats_par_equipe)
    somme_ttfl_totale = somme_ttfl_totale.astype(int)  # Convertir les sommes totales TTFL en entiers
    somme_min_totale = somme_min_totale.astype(int)  # Convertir les sommes totales MIN en entiers

    # Insérer les colonnes TTFL et Minutes dans le DataFrame des résultats
    df_impact_poste.insert(0, 'Poste', ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'])
    df_impact_poste.insert(1, 'TTFL', somme_ttfl_totale)
    df_impact_poste.insert(2, 'Minutes', somme_min_totale)
    moyenne_ttfl_ponderee_totale = np.round(somme_ttfl_totale / somme_min_totale, 1) # Calcul de la moyenne pondérée
    df_impact_poste.insert(3, 'Moyenne', moyenne_ttfl_ponderee_totale)

    # Créer une copie du DataFrame des résultats pour calculer les variations
    df_impact_poste_delta = df_impact_poste.copy()
    columns_to_subtract = df_impact_poste_delta.columns[4:]  # Sélectionner les colonnes à soustraire
    df_impact_poste_delta[columns_to_subtract] = df_impact_poste_delta[columns_to_subtract].sub(df_impact_poste_delta['Moyenne'], axis=0)  # Soustraire les valeurs de la colonne 'Moyenne'

    # Calculer la valeur minimum le long de l'axe des colonnes pour chaque ligne
    valeurs_minimum_par_ligne = df_impact_poste_delta.iloc[:,4:].min(axis=1)
    valeurs_maximum_par_ligne = df_impact_poste_delta.iloc[:,4:].max(axis=1)

    df_impact_poste_delta.insert(3, 'Minimum', valeurs_minimum_par_ligne)
    df_impact_poste_delta.insert(4, 'Maximum', valeurs_maximum_par_ligne)

    # Supprime les colonnes de sommes TTFL et Minutes
    df_impact_poste_delta = df_impact_poste_delta.drop(df_impact_poste_delta.columns[[2, 3]], axis=1)

    return df_impact_poste_delta  # Renvoyer le DataFrame des variations

def obtenir_transposer_df_delta():
    # Obtenir le df_delta, le transposer, et l'exporter vers Excel
    df_impact_poste_delta = obtenir_delta_ttfl_postes()  # Appeler la fonction principale
    df_transposed = transposer_mon_DF(df_impact_poste_delta) # Transposer
    return df_transposed

def obtenir_transposer_exporter_df_delta():
    # Obtenir le df_delta, le transposer, et l'exporter vers Excel
    df_impact_poste_delta = obtenir_delta_ttfl_postes()  # Appeler la fonction principale
    df_transposed = transposer_mon_DF(df_impact_poste_delta) # Transposer
    print() # Print vide pour clean la progression
    exporter_vers_Excel_impact_poste(df_transposed) # Exporter vers Excel

# Point d'entrée du programme
if __name__ == "__main__":

    temps_debut = time.time()  # Enregistrer le temps de début d'exécution

    obtenir_transposer_exporter_df_delta()

    temps_fin = time.time()  # Enregistrer le temps de fin d'exécution
    duree_execution = temps_fin - temps_debut  # Calculer la durée d'exécution
    minutes = int(duree_execution // 60)  # Convertir la durée en minutes
    secondes = int(duree_execution % 60)  # Calculer les secondes restantes
    print(f"Le code a pris {minutes} minutes et {secondes} secondes pour s'exécuter.")  # Afficher le temps d'exécution