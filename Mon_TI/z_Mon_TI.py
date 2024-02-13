import pandas as pd
from datetime import datetime
import time
import sys

from a_Equipes_Noms import generer_df_quipe_nom
from b_Postes import generer_df_postes
# from c_Blessures import rien
from d_Back_to_back import est_en_back_to_back
from e_Moyennes import generer_df_moyennes
from f_Nombre_matchs_joues_X_derniers_jours import get_games_played_last_X_days
from g_Intervalles_X_derniers_jours import generer_intervalles_last_X_days
from h1_Scores_X_derniers_matchs_NaN import construire_tableau_X_derniers_matchs_with_NaN
from j_X_historique_vs_adversaire import obtenir_X_historique_vs_adversaire
from l_Impact_Domicile_Exterieur import obtenir_delta_globale_domicile_ou_exterieur
from m_Impact_back_to_back import obtenir_resultats_impact_B2B
from n_Adversaires_X_prochains_matchs import obtenir_prochains_matchs_joueurs
from z_Utilitaires import exporter_vers_Excel_mon_TI

# Enregistrez le temps de début
temps_debut = time.time()

# Liste d'identifiants de joueurs
ids_joueurs = [203507, 1630162, 203081, 1628368, 1627759, 1626157, 1631094, 203078, 1630595, 1630532, 1631105, 203114, 1630559, 1626156, 203924, 1629639]
date_du_jour = '13/02/2024'

# Conversion de la date du jour
date_du_jour = datetime.strptime(date_du_jour, '%d/%m/%Y') # Convertir la chaîne en objet datetime
date_du_jour = date_du_jour.strftime("%b %d, %Y") # Formater la date

# Nombre de joueurs dans ma liste
total_joueurs = len(ids_joueurs)

# Variables générales
nb_derniers_matchs = 5 # Nombre de matchs joués en derniers (score)
number_of_days_matchs_joues = 30 # Nombre de matchs joués et Intervalles
nombre_de_matchs_vs_adversaire = 3 # Nombre de matchs joués contre l'adversaire du jour (score)

# Intervalles
limite_1 = 20
limite_2 = 30
limite_3 = 40

# Création des DataFrames
df_equipes_noms = pd.DataFrame(columns=['Equipe', 'Joueur']) # Équipe, joueur
df_postes = pd.DataFrame(columns=['Joueur', 'Poste']) # Postes
df_back_to_back = pd.DataFrame(columns=['Joueur', 'B2B']) # B2B
df_moyennes = pd.DataFrame(columns=['Joueur', '5M', '15M', 'Saison']) # Moyennes
df_matchs_joues_X_derniers_jours = pd.DataFrame(columns=['Joueur', 'GP']) # Nombre de matchs joués
df_intervalles = pd.DataFrame(columns=['Joueur', f'<{limite_1}', f'{limite_1}-{limite_2-1}', f'{limite_2}-{limite_3-1}', f'{limite_3}+']) # Intervalles
df_X_derniers_matchs = pd.DataFrame() # Derniers matchs
df_adversaire_du_soir = pd.DataFrame() # Adversaire du soir
df_historique_vs_adversaire = pd.DataFrame() # Historique contre adversaire du soir
df_X_prochains_matchs = pd.DataFrame() # Prochains matchs
df_impact_domicile_ou_exterieurs = pd.DataFrame(columns=['Joueur', 'vs or @','Delta']) # Impact domicile ou exterieur
df_impact_B2B = pd.DataFrame(columns=['Joueur', 'delta_B2B', 'nombre_de_B2B']) # Impact B2B

# Début de la boucle
for joueur_index, joueur_id in enumerate(ids_joueurs, start=1):

    # Affichage de la progression dans la console
    joueur_progression = int(round((joueur_index/total_joueurs)*100,0))
    message = f'\rJoueur {joueur_index}/{total_joueurs}, {joueur_progression}%'
    # sys.stdout.write(message + ' ' * (len(message) - 1))  # Effacer la ligne précédente
    sys.stdout.write(message)  # Effacer la ligne précédente
    sys.stdout.flush()

    # ---------------------------------------------------------------------------------------
    # Équipes, Noms
    resultats = generer_df_quipe_nom(joueur_id)
    df_equipes_noms.loc[len(df_equipes_noms)] = resultats
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Postes
    resultats = generer_df_postes(joueur_id)
    df_postes.loc[len(df_postes)] = resultats
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # B2B
    df_back_to_back.loc[len(df_back_to_back)] = est_en_back_to_back(joueur_id, date_du_jour)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Moyennes
    df_moyennes.loc[len(df_moyennes)] = generer_df_moyennes(joueur_id)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Nombre de matchs joués
    df_matchs_joues_X_derniers_jours.loc[len(df_matchs_joues_X_derniers_jours)] = get_games_played_last_X_days(joueur_id,number_of_days_matchs_joues)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Intervalles
    df_intervalles.loc[len(df_intervalles)] = generer_intervalles_last_X_days(joueur_id,limite_1,limite_2,limite_3,number_of_days_matchs_joues)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Derniers matchs
    tableau_X_derniers_matchs = construire_tableau_X_derniers_matchs_with_NaN(joueur_id, nb_derniers_matchs)
    df_X_derniers_matchs = pd.concat([df_X_derniers_matchs, tableau_X_derniers_matchs], ignore_index=True)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Adversaire du soir
    nb_matchs_a_sauter = 0 # variables pour afficher les prochains adversaire, moins le prochain (qui sera affiché ailleurs) dans le cas de variable = 1
    nb_prochains_matchs = 1
    df_adversaire_du_soir = pd.concat([df_adversaire_du_soir, obtenir_prochains_matchs_joueurs(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)], ignore_index=True)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Historique contre adversaire du soir
    df_historique_vs_adversaire = pd.concat([df_historique_vs_adversaire, obtenir_X_historique_vs_adversaire(joueur_id, nombre_de_matchs_vs_adversaire)], ignore_index=True)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Prochains matchs
    nb_matchs_a_sauter = 1 # variables pour afficher les prochains adversaire, moins le prochain (qui sera affiché ailleurs) dans le cas de variable = 1
    nb_prochains_matchs = 4
    df_X_prochains_matchs = pd.concat([df_X_prochains_matchs, obtenir_prochains_matchs_joueurs(joueur_id, nb_prochains_matchs, nb_matchs_a_sauter, date_du_jour)], ignore_index=True)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Impact domicile ou exterieur
    df_impact_domicile_ou_exterieurs.loc[len(df_impact_domicile_ou_exterieurs)] = obtenir_delta_globale_domicile_ou_exterieur(joueur_id)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Impact B2B
    df_impact_B2B.loc[len(df_impact_B2B)] = obtenir_resultats_impact_B2B(joueur_id, date_du_jour)
    # ---------------------------------------------------------------------------------------

# Enlever les joueurs
df_postes = df_postes.drop(columns=['Joueur']) # Postes
df_back_to_back = df_back_to_back.drop(columns=['Joueur']) # B2B
df_moyennes = df_moyennes.drop(columns=['Joueur']) # Moyennes
df_matchs_joues_X_derniers_jours = df_matchs_joues_X_derniers_jours.drop(columns=['Joueur']) # Nombre de matchs joués
df_intervalles = df_intervalles.drop(columns=['Joueur']) # Intervalles
df_X_derniers_matchs = df_X_derniers_matchs.drop(columns=['Joueur']) # Derniers matchs
df_adversaire_du_soir = df_adversaire_du_soir.drop(columns=['Joueur']) # Adversaire du soir
df_historique_vs_adversaire = df_historique_vs_adversaire.drop(columns=['Joueur']) # Historique contre adversaire du soir
df_X_prochains_matchs = df_X_prochains_matchs.drop(columns=['Joueur']) # Prochains matchs
df_impact_domicile_ou_exterieurs = df_impact_domicile_ou_exterieurs.drop(columns=['Joueur']) # Impact domicile ou exterieur
df_impact_B2B = df_impact_B2B.drop(columns=['Joueur']) # Impact B2B

# Gestion des 0
# Derniers matchs
df_X_derniers_matchs = df_X_derniers_matchs.fillna(0) # Trasnformer les NaN en 0
df_X_derniers_matchs = df_X_derniers_matchs.round(0).astype(int) # Convertir les valeurs en integer pour ne plus avoir de décimales
df_X_derniers_matchs = df_X_derniers_matchs.replace(0,"-") # Remplacer les 0 par des tirets pour la lisibilité

# Concaténation des tableaux
mon_TI = pd.DataFrame()
mon_TI = pd.concat([mon_TI, df_equipes_noms], axis=1)
mon_TI = pd.concat([mon_TI, df_postes], axis=1)
mon_TI = pd.concat([mon_TI, df_back_to_back], axis=1)
mon_TI = pd.concat([mon_TI, df_moyennes], axis=1)
mon_TI = pd.concat([mon_TI, df_matchs_joues_X_derniers_jours], axis=1)
mon_TI = pd.concat([mon_TI, df_intervalles], axis=1)
mon_TI = pd.concat([mon_TI, df_X_derniers_matchs], axis=1)
mon_TI = pd.concat([mon_TI, df_adversaire_du_soir], axis=1)
mon_TI = pd.concat([mon_TI, df_historique_vs_adversaire], axis=1)
mon_TI = pd.concat([mon_TI, df_X_prochains_matchs], axis=1)
mon_TI = pd.concat([mon_TI, df_impact_domicile_ou_exterieurs], axis=1)
mon_TI = pd.concat([mon_TI, df_impact_B2B], axis=1)

# Tri du tableau par ordre décroissant de la colonne 5 matchs
mon_TI = mon_TI.sort_values(by='5M', ascending=False)

# Exporter le TI vers Excel
print()
exporter_vers_Excel_mon_TI(mon_TI, date_du_jour)

# Enregistrez le temps de fin
temps_fin = time.time()
# Calculez la durée d'exécution
duree_execution = temps_fin - temps_debut
duree_execution = int(round(duree_execution,0))
print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")