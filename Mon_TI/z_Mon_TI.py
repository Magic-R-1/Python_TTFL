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
    progression = int(round(index/nombre_DF * 100, 0))
    bar_length = 50
    bar_fill = '#' * int(bar_length * progression / 100)
    bar_empty = ' ' * (bar_length - len(bar_fill))
    message = f'\rTableau {index}/{nombre_DF} en cours [{bar_fill}{bar_empty}] {progression}%'

    sys.stdout.write(message)  # Effacer la ligne précédente
    sys.stdout.flush()

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

    # Liste contenant tous les DataFrames que vous voulez concaténer
    list_DF = [
        DF_equipes_noms,
        DF_joueurs_status,
        DF_postes,
        DF_back_to_back,
        DF_moyennes,
        DF_matchs_joues_X_derniers_jours,
        DF_intervalles,
        DF_X_derniers_matchs_avec_NaN,
        DF_adversaire_du_soir,
        DF_historiques_vs_adversaires,
        DF_X_prochains_matchs,
        DF_impact_domicile_ou_exterieurs,
        DF_impact_B2B
    ]

    # Concaténation des DataFrames
    mon_TI = pd.concat(list_DF, axis=1)

    # Tri du tableau par ordre décroissant de la colonne 15 matchs
    mon_TI = mon_TI.sort_values(by='15M', ascending=False)

    # Diviser le DataFrame en deux parties: une avec le statut "Out" et une avec les autres statuts
    mon_TI_not_out = mon_TI[mon_TI['Statut'] != 'Out']
    mon_TI_out = mon_TI[mon_TI['Statut'] == 'Out']

    # Réassembler les deux parties
    mon_TI = pd.concat([mon_TI_not_out, mon_TI_out])

    return mon_TI

# ------------------------------
# Point d'entrée du programme
if __name__ == "__main__":

    temps_debut = time.time()   # Enregistrer le temps de début d'exécution
    charger_cache()             # Charger le cache

    # Variables
    ids_joueurs = [203952, 1627742, 1641706, 1629636, 1629028, 1627749, 1630166, 1628378, 1630596, 1627750, 1628386, 203924, 203954, 1628381, 1630228, 202695, 1628398, 1628374, 1629008, 1628970, 202696, 201566, 201939, 1630178, 203897, 1629627]
    date_du_jour = '30/12/2024'

    mon_TI = obtenir_mon_TI(ids_joueurs, date_du_jour)              # Obtenir le TI
    prefixe = ""
    exporter_vers_Excel_mon_TI(mon_TI, date_du_jour, prefixe)       # Exporter le TI vers Excel
    sauvegarder_cache()                                             # Sauvegarder le cache
    print_message_de_confirmation(temps_debut)                      # Afficher le message de confirmation