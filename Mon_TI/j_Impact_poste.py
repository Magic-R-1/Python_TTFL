import pandas as pd
import numpy as np
import sys
import time

from x_Utilitaires import *
from x_DataFrames_globaux import *

# ------------------------------
# Fonction pour obtenir la liste des identifiants des équipes à partir des données globales
def obtenir_liste_equipes_IDs():
    return obtenir_liste_equipes_IDs_DF_globaux()
    # return [1610612747, 1610612738]

# ------------------------------
# Fonction pour obtenir la liste des identifiants des matchs d'une équipe
def obtenir_liste_matchs_IDs_avec_equipeID(equipe_id):
    liste_matchs_IDs = obtenir_equipe_derniers_matchs_DF_globaux(equipe_id)    # Obtenir les derniers matchs de l'équipe à partir des données globales
    return liste_matchs_IDs[['Game_ID']]                                       # Sélectionner uniquement la colonne 'Game_ID'

# ------------------------------
# Fonction pour retourner un DF avec le score TTFL, les minutes, le score TTFL pondéré de chaque joueur, à partir du BoxScore initial
def obtenir_DF_BoxScore_TTFL_avec_matchID(match_id, equipe_id):

    # Obtenir les logs du match à partir du cache des matchs
    DF_BoxScore_initial = obtenir_BoxScoreTraditionalV2_DF_globaux(match_id)

    # Filtrer les données pour l'équipe spécifiée
    DF_BoxScore_TTFL = DF_BoxScore_initial.loc[DF_BoxScore_initial['TEAM_ID'] != equipe_id]
    DF_BoxScore_TTFL = DF_BoxScore_TTFL.loc[DF_BoxScore_initial['MIN'].notnull()]   # Supprimer les lignes avec MIN nul
    
    # Ajouter la colonne 'poste' en utilisant les postes abrégés des joueurs
    DF_BoxScore_TTFL['Poste'] = DF_BoxScore_TTFL['PLAYER_ID'].apply(obtenir_joueurPosteAbregee_avec_joueurID)
    # Calculer le score TTFL pour chaque joueur
    DF_BoxScore_TTFL['Score_TTFL'] = DF_BoxScore_TTFL.apply(calcul_score_TTFL, axis=1).astype(int)
    # Extraire et convertir la durée de jeu en minutes
    DF_BoxScore_TTFL['Minutes'] = DF_BoxScore_TTFL['MIN'].str.extract(r'(\d+)').astype(int)
    # Calculer le score TTFL total pour chaque joueur dans le temps de jeu
    DF_BoxScore_TTFL['Score_TTFL_pondere'] = DF_BoxScore_TTFL['Score_TTFL'] * DF_BoxScore_TTFL['Minutes']

    # Ne garder que les colonnes d'intérêt
    DF_BoxScore_TTFL = DF_BoxScore_TTFL[['Poste', 'Score_TTFL', 'Minutes', 'Score_TTFL_pondere']]

    return DF_BoxScore_TTFL

# ------------------------------
# Fonction pour obtenir les statistiques moyennes par poste pour un match et une équipe donnée
def obtenir_DF_BoxScore_scoreTTFLpondere_minutes(match_id, equipe_id):
    DF_BoxScore_TTFL = obtenir_DF_BoxScore_TTFL_avec_matchID(match_id, equipe_id)
    
    # Création du DF final, récapitulant la somme des scores TTFL pondérés et la somme des minutes par porte pour un match
    # DF_BoxScore_scoreTTFLpondere_minutes = pd.DataFrame(['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C'], columns=['Poste'])
    DF_BoxScore_scoreTTFLpondere_minutes = pd.DataFrame(['G', 'F', 'C'], columns=['Poste'])
    
    # Définir les variables faisant les sommes par poste pour un match
    liste_sommes_scores_TTFL_ponderes = []
    liste_sommes_minutes = []

    # Calculer les sommes TTFL et Minutes pour chaque poste
    for poste in DF_BoxScore_scoreTTFLpondere_minutes['Poste']:

        # Trier le DF pour n'avoir que le poste itéré (celui en cours sur la boucle)
        DF_poste_itere = DF_BoxScore_TTFL[DF_BoxScore_TTFL['Poste'] == poste]

        # Calcul des sommes pour le poste itéré
        somme_score_TTFL_pondere_poste_itere = DF_poste_itere['Score_TTFL_pondere'].sum()   # Somme du score TTFL pour le poste itéré
        Somme_minutes_poste_itere = DF_poste_itere['Minutes'].sum()                         # Somme des minutes pour le poste itéré

        # Ajout de ces sommes au DF final
        liste_sommes_scores_TTFL_ponderes.append(somme_score_TTFL_pondere_poste_itere)
        liste_sommes_minutes.append(Somme_minutes_poste_itere)

    # Ajout des 2 listes de sommes au DF final
    DF_BoxScore_scoreTTFLpondere_minutes['Somme_score_TTFL_pondere'] = liste_sommes_scores_TTFL_ponderes
    DF_BoxScore_scoreTTFLpondere_minutes['Somme_minutes'] = liste_sommes_minutes

    return DF_BoxScore_scoreTTFLpondere_minutes

# ------------------------------
# Fonction pour afficher le message de progression
def afficher_message_de_progression(match_index, liste_matchs_IDs, liste_equipes_IDs, equipe_id, equipe_ABV):
    
    total_equipes = len(liste_equipes_IDs)  # Calculer le nombre total d'équipes
    total_matchs = len(liste_matchs_IDs)    # Calculer le nombre total de matchs pour l'équipe

    match_progression = int(round(match_index / total_matchs * 100, 0))  # Pourcentage de progression du match
    equipe_index = liste_equipes_IDs.index(equipe_id) + 1
    equipe_progression = int(round((equipe_index / total_equipes) * 100, 0)) # Pourcentage de progression de l'équipe

    # Barre de progression pour les matchs
    bar_length_match = 30
    bar_fill_match = '#' * int(bar_length_match * match_index / total_matchs)
    bar_empty_match = ' ' * (bar_length_match - len(bar_fill_match))

    # Barre de progression pour les équipes
    bar_length_equipe = 20
    bar_fill_equipe = '#' * int(bar_length_equipe * equipe_index / total_equipes)
    bar_empty_equipe = ' ' * (bar_length_equipe - len(bar_fill_equipe))

    match_message = f"\rÉquipe {equipe_ABV} [{bar_fill_equipe}{bar_empty_equipe}] {equipe_index}/{total_equipes} ({equipe_progression}%) - Match {match_index}/{total_matchs} [{bar_fill_match}{bar_empty_match}] ({match_progression}%)"
    
    sys.stdout.write(match_message)
    sys.stdout.flush()

# ------------------------------
# Fonction pour transposer mon DF avec la gestion des index
def obtenir_DF_delta_par_poste_transposed():
    
    # Obtenir le DF
    DF_delta_par_poste = obtenir_rajouter_Min_Max_PosteGlobal_DF_delta_par_poste()

    # Transposer
    DF_delta_par_poste_transposed = DF_delta_par_poste.transpose()

    # Réinitialiser l'index du DataFrame transposé
    DF_delta_par_poste_transposed.reset_index(drop=False, inplace=True)

    # Faire prendre aux intitulés de colonnes la ligne d'index 0
    DF_delta_par_poste_transposed.columns = DF_delta_par_poste_transposed.iloc[0]

    # Conserver le DF à partir de la ligne d'index 1 (en plus des intitulés de colonnes), pour ne pas garder celle d'index 0 qui est en doublon avec le code précédent
    DF_delta_par_poste_transposed = DF_delta_par_poste_transposed[1:]

    # Supprimer la ligne 'Poste' des index, elle n'est plus d'index 0
    DF_delta_par_poste_transposed = DF_delta_par_poste_transposed.rename_axis(None, axis=1)

    # Reset de l'index après manipulations
    DF_delta_par_poste_transposed.reset_index(drop=True, inplace=True)

    # Trier les colonnes par ordre alphabétique de la colonne 1 à partir de la ligne d'index 2
    DF_not_sorted = DF_delta_par_poste_transposed.iloc[:2]
    DF_sorted  = DF_delta_par_poste_transposed.iloc[2:].sort_values(by=DF_delta_par_poste_transposed.columns[0])
    DF_delta_par_poste_transposed = pd.concat([DF_not_sorted, DF_sorted])

    # Reset de l'index après manipulations
    DF_delta_par_poste_transposed.reset_index(drop=True, inplace=True)

    return DF_delta_par_poste_transposed

# ------------------------------
# Fonction principale pour obtenir les moyennes pondérées TTFL par poste pour chaque équipe, plus le global
def obtenir_DF_moyenne_par_poste():

    liste_equipes_IDs = obtenir_liste_equipes_IDs() # Obtenir la liste des identifiants des équipes
    
    Dictionnaire_moyenne_par_poste = {} # Initialiser le dictionnaire pour stocker les résultats par équipe
    liste_somme_TTFL_par_poste_globale = np.zeros(4)    # Initialiser les sommes totales des scores TTFL par poste. 8 correspond aux 7 postes plus le global
    liste_somme_minutes_par_poste_globale = np.zeros(4) # Initialiser les sommes totales des minutes par poste. 8 correspond aux 7 postes plus le global

    # Boucle sur chaque équipe
    for equipe_id in liste_equipes_IDs:
        
        liste_matchs_IDs = obtenir_liste_matchs_IDs_avec_equipeID(equipe_id)    # Obtenir les matchs de l'équipe
        equipe_ABV = obtenir_equipeABV_avec_equipeID(equipe_id)                 # Obtenir l'abréviation de l'équipe

        liste_somme_TTFL_par_poste = []     # Initialisation. Ce sera une liste, contenant elle-même des listes des scores TTFL pondérés par poste pour un match. Chaque match sera une liste dans cette liste
        liste_somme_minutes_par_poste = []  # Initialisation. Ce sera une liste, contenant elle-même des listes des minutes par poste pour un match. Chaque match sera une liste dans cette liste

        # Boucle sur chaque match de l'équipe
        for match_index, match_id in enumerate(liste_matchs_IDs['Game_ID'], start=1):

            # Afficher le message de progression
            afficher_message_de_progression(match_index, liste_matchs_IDs, liste_equipes_IDs, equipe_id, equipe_ABV)

            DF_BoxScore_scoreTTFLpondere_minutes = obtenir_DF_BoxScore_scoreTTFLpondere_minutes(match_id, equipe_id)    # Obtenir les statistiques par poste pour le match itéré

            liste_somme_TTFL_par_poste.append(DF_BoxScore_scoreTTFLpondere_minutes['Somme_score_TTFL_pondere'].values)  # Ajouter la somme TTFL par poste à la liste. Les postes disparaissent
            liste_somme_minutes_par_poste.append(DF_BoxScore_scoreTTFLpondere_minutes['Somme_minutes'].values)          # Ajouter la somme Minutes par poste à la liste. Les postes disparaissent

        # Somme des scores TTFL par poste pour tous les matchs. Somme des listes contenues dans liste_somme_TTFL_par_poste, avec axis 0, donc par colonne (donc par poste).
        liste_somme_TTFL_par_poste_une_equipe = np.sum(liste_somme_TTFL_par_poste, axis=0)
        # Somme TTFL de l'équipe pour tous les postes (pour la moyenne globale plus tard)
        somme_TTFL_equipe_tous_les_postes = np.array(np.sum(liste_somme_TTFL_par_poste))
        # Ajout de cette somme à la liste
        liste_somme_TTFL_par_poste_une_equipe = np.append(liste_somme_TTFL_par_poste_une_equipe, somme_TTFL_equipe_tous_les_postes)

        # Somme des minutes par poste pour tous les matchs. Somme des listes contenues dans liste_somme_minutes_par_poste, avec axis 0, donc par colonne (donc par poste).
        liste_somme_minutes_par_poste_une_equipe = np.sum(liste_somme_minutes_par_poste, axis=0)
        # Somme des minutes de l'équipe pour tous les postes (pour la moyenne globale plus tard)
        somme_minutes_equipe_tous_les_postes = np.array(np.sum(liste_somme_minutes_par_poste))
        # Ajout de cette somme à la liste
        liste_somme_minutes_par_poste_une_equipe = np.append(liste_somme_minutes_par_poste_une_equipe, somme_minutes_equipe_tous_les_postes)

        liste_somme_TTFL_par_poste_globale += liste_somme_TTFL_par_poste_une_equipe         # Ajouter les sommes TTFL par poste par équipe aux sommes totales
        liste_somme_minutes_par_poste_globale += liste_somme_minutes_par_poste_une_equipe   # Ajouter les sommes des minutes par poste par équipe aux sommes totales
        
        # Calculer la moyenne pondérée TTFL par poste pour l'équipe et l'ajouter au dictionnaire
        Dictionnaire_moyenne_par_poste[equipe_ABV] = np.round(liste_somme_TTFL_par_poste_une_equipe / liste_somme_minutes_par_poste_une_equipe, 1)

    liste_somme_TTFL_par_poste_globale = liste_somme_TTFL_par_poste_globale.astype(int)         # Convertir les sommes totales TTFL en entiers
    liste_somme_minutes_par_poste_globale = liste_somme_minutes_par_poste_globale.astype(int)   # Convertir les sommes totales MIN en entiers

    # Créer un DataFrame à partir du dictionnaire des résultats
    DF_moyenne_par_poste = pd.DataFrame(Dictionnaire_moyenne_par_poste)
    # DF_moyenne_par_poste.insert(0, 'Poste', ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C', 'Global'])    # Insérer les postes
    DF_moyenne_par_poste.insert(0, 'Poste', ['G', 'F', 'C', 'Global'])    # Insérer les postes

    # Appel de la fonction obtenir_DF_moyenne_par_poste qui retourne liste_somme_TTFL_par_poste_globale uniquement
    # _, liste_somme_TTFL_par_poste_globale, _ = obtenir_DF_moyenne_par_poste()
    return DF_moyenne_par_poste, liste_somme_TTFL_par_poste_globale, liste_somme_minutes_par_poste_globale

# ------------------------------
# Fonction principale pour obtenir les deltas TTFL par poste pour chaque équipe
def obtenir_DF_delta_par_poste():

    # Appel de la fonction obtenir_DF_moyenne_par_poste qui retourne DF_moyenne_par_poste, liste_somme_TTFL_par_poste_globale, et liste_somme_minutes_par_poste_globale
    DF_moyenne_par_poste, liste_somme_TTFL_par_poste_globale, liste_somme_minutes_par_poste_globale = obtenir_DF_moyenne_par_poste()

    # Calcul de la moyenne pondérée globale
    liste_moyenne_TTFL_ponderee_globale = np.round(liste_somme_TTFL_par_poste_globale / liste_somme_minutes_par_poste_globale, 1)

    # Créer une copie du DataFrame des résultats pour calculer les variations
    DF_delta_par_poste = DF_moyenne_par_poste.copy()
    # Sélectionner les colonnes à soustraire
    columns_to_subtract = DF_delta_par_poste.columns[1:]
    # Soustraire les valeurs de la liste contenant les  moyennes
    DF_delta_par_poste[columns_to_subtract] = DF_delta_par_poste[columns_to_subtract].sub(liste_moyenne_TTFL_ponderee_globale, axis=0)

    return DF_delta_par_poste

# ------------------------------
def obtenir_rajouter_Min_Max_PosteGlobal_DF_delta_par_poste():

    DF_delta_par_poste = obtenir_DF_delta_par_poste()

    # Calculer la valeur minimum le long de l'axe des colonnes pour chaque ligne, à partir de la 2ème colonne
    liste_valeurs_minimum_par_poste = DF_delta_par_poste.iloc[:,1:].min(axis=1)
    liste_valeurs_maximum_par_poste = DF_delta_par_poste.iloc[:,1:].max(axis=1)

    # Insérer les listes de valeurs minimums et maximums
    DF_delta_par_poste.insert(1, 'Minimum', liste_valeurs_minimum_par_poste)
    DF_delta_par_poste.insert(2, 'Maximum', liste_valeurs_maximum_par_poste)

    return DF_delta_par_poste

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":

    temps_debut = time.time()                                               # Enregistrer le temps de début d'exécution
    charger_cache()                                                         # Charger le cache
    DF_delta_par_poste_transposed = obtenir_DF_delta_par_poste_transposed() # Obtenir le DF transposé contenant les delta
    exporter_vers_Excel_impact_poste(DF_delta_par_poste_transposed)         # Exporter vers Excel
    sauvegarder_cache()                                                     # Sauvegarder le cache
    print_message_de_confirmation(temps_debut)                              # Afficher le message de confirmation