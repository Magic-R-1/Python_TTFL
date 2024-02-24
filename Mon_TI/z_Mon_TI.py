import pandas as pd
import time
import sys

from a_Equipes_Noms import obtenir_DF_equipes_noms
from c_Postes import obtenir_DF_postes
from b_Blessures import obtenir_DF_joueurs_status
from d_Back_to_back import obtenir_DF_back_to_back
from e_Moyennes import obtenir_DF_moyennes
from f_Nombre_matchs_joues_X_derniers_jours import obtenir_DF_nb_matchs_joues_derniers_X_jours
from g_Intervalles_X_derniers_jours import obtenir_DF_intervalles_derniers_X_jours
from h1_Scores_X_derniers_matchs_NaN import obtenir_DF_X_derniers_matchs_avec_NaN
from k_historique_vs_adversaire import obtenir_DF_historiques_vs_adversaires
from l_Impact_Domicile_Exterieur import obtenir_DF_impact_domicile_ou_exterieurs
from m_Impact_back_to_back import obtenir_DF_impact_B2B
from i_Adversaires_X_prochains_matchs import obtenir_DF_X_prochains_matchs
from x_Utilitaires import *

# ------------------------------
# Fonction pour afficher la progression dans la construction des tableaux
def afficher_progression(index):
    nombre_DF = 13
    progression = int(round(index/nombre_DF * 100,0))
    message = f'\rTableau {index}/{nombre_DF} en cours ({progression}%)'

    sys.stdout.write(message)  # Effacer la ligne précédente
    sys.stdout.flush()

    if index==nombre_DF: print()

# ------------------------------
# Fonction principale, pour construire les tableaux et les assembler en un TI
def obtenir_mon_TI(ids_joueurs, date_du_jour):

    # Variables générales
    nb_derniers_matchs = 5 # Nombre de matchs joués en derniers (score)
    nb_jours_matchs_joues = 30 # Nombre de matchs joués et Intervalles
    nombre_de_matchs_vs_adversaire = 3 # Nombre de matchs joués contre l'adversaire du jour (score)

    # Intervalles
    limite_1 = 20
    limite_2 = 30
    limite_3 = 40

    # Progression
    index = 1

    # ---------------------------------------------------------------------------------------
    # Équipes, Noms
    afficher_progression(index)
    index += 1
    DF_equipes_noms = obtenir_DF_equipes_noms(ids_joueurs)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Blessure
    afficher_progression(index)
    index += 1
    DF_joueurs_status = obtenir_DF_joueurs_status(ids_joueurs)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Postes
    afficher_progression(index)
    index += 1
    DF_postes = obtenir_DF_postes(ids_joueurs)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # B2B
    afficher_progression(index)
    index += 1
    DF_back_to_back = obtenir_DF_back_to_back(ids_joueurs, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Moyennes
    afficher_progression(index)
    index += 1
    DF_moyennes = obtenir_DF_moyennes(ids_joueurs)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Nombre de matchs joués
    afficher_progression(index)
    index += 1
    DF_matchs_joues_X_derniers_jours = obtenir_DF_nb_matchs_joues_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Intervalles
    afficher_progression(index)
    index += 1
    DF_intervalles = obtenir_DF_intervalles_derniers_X_jours(ids_joueurs, nb_jours_matchs_joues, limite_1, limite_2, limite_3)
    # ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
    # Derniers matchs_avec_NaN
    afficher_progression(index)
    index += 1
    DF_X_derniers_matchs_avec_NaN = obtenir_DF_X_derniers_matchs_avec_NaN(ids_joueurs, nb_derniers_matchs)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Adversaire du soir
    afficher_progression(index)
    index += 1
    nb_matchs_a_sauter = 0 # variables pour afficher les prochains adversaire, moins le prochain (qui sera affiché ailleurs) dans le cas de variable = 1
    nb_prochains_matchs = 1
    DF_adversaire_du_soir = obtenir_DF_X_prochains_matchs(ids_joueurs, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Historique contre adversaire du soir
    afficher_progression(index)
    index += 1
    DF_historiques_vs_adversaires = obtenir_DF_historiques_vs_adversaires(ids_joueurs, nombre_de_matchs_vs_adversaire, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Prochains matchs
    afficher_progression(index)
    index += 1
    nb_matchs_a_sauter = 1 # variables pour afficher les prochains adversaire, moins le prochain (qui sera affiché ailleurs) dans le cas de variable = 1
    nb_prochains_matchs = 4
    DF_X_prochains_matchs = obtenir_DF_X_prochains_matchs(ids_joueurs, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Impact domicile ou exterieur
    afficher_progression(index)
    index += 1
    DF_impact_domicile_ou_exterieurs = obtenir_DF_impact_domicile_ou_exterieurs(ids_joueurs, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Impact B2B
    afficher_progression(index)
    index += 1
    DF_impact_B2B = obtenir_DF_impact_B2B(ids_joueurs, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # Concaténation des tableaux
    mon_TI = pd.DataFrame()
    mon_TI = pd.concat([mon_TI, DF_equipes_noms], axis=1)
    mon_TI = pd.concat([mon_TI, DF_joueurs_status], axis=1)
    mon_TI = pd.concat([mon_TI, DF_postes], axis=1)
    mon_TI = pd.concat([mon_TI, DF_back_to_back], axis=1)
    mon_TI = pd.concat([mon_TI, DF_moyennes], axis=1)
    mon_TI = pd.concat([mon_TI, DF_matchs_joues_X_derniers_jours], axis=1)
    mon_TI = pd.concat([mon_TI, DF_intervalles], axis=1)
    mon_TI = pd.concat([mon_TI, DF_X_derniers_matchs_avec_NaN], axis=1)
    mon_TI = pd.concat([mon_TI, DF_adversaire_du_soir], axis=1)
    mon_TI = pd.concat([mon_TI, DF_historiques_vs_adversaires], axis=1)
    mon_TI = pd.concat([mon_TI, DF_X_prochains_matchs], axis=1)
    mon_TI = pd.concat([mon_TI, DF_impact_domicile_ou_exterieurs], axis=1)
    mon_TI = pd.concat([mon_TI, DF_impact_B2B], axis=1)

    # Tri du tableau par ordre décroissant de la colonne 15 matchs
    mon_TI = mon_TI.sort_values(by='15M', ascending=False)

    return mon_TI

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":

    # Variables
    ids_joueurs = [1627759, 203944, 1631094, 203497, 1630595, 1628978, 1630532, 1631105]
    date_du_jour = '24/02/2024'

    temps_debut = time.time()  # Enregistrer le temps de début d'exécution

    mon_TI = obtenir_mon_TI(ids_joueurs, date_du_jour)

    exporter_vers_Excel_mon_TI(mon_TI, date_du_jour)    # Exporter le TI vers Excel

    print_message_de_confirmation(temps_debut)