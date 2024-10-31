import matplotlib.pyplot as plt

import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Python_TTFL/Mon_TI')

from k_Impact_poste import *

def poste_ABV_to_poste_full(poste_ABV):
    mapping = {
        'G': 'Guards',
        'G-F': 'Guard-Forwards',
        'F-G': 'Forward-Guards',
        'F': 'Forwards',
        'F-C': 'Forwards-Centers',
        'C-F': 'Center-Forwards',
        'C': 'Centers'
    }
    return mapping.get(poste_ABV, 'Unknown')

def obtenir_DF_complet():
    # DataFrame initial
    return obtenir_transposer_DF_delta()

def formater_DF_avec_poste_voulu(poste, DF_delta_complet):

    # Sélection des colonnes d'intérêt (Poste et les scores pour chaque équipe)
    DF_delta_poste_unique = DF_delta_complet[["Poste", poste]]

    # Renommer les colonnes pour correspondre au format souhaité
    DF_delta_poste_unique.columns = ["Team", "Delta"]

    # Supprimer les lignes inintéressantes
    # DF_delta_poste_unique = DF_delta_poste_unique.drop(DF_delta_poste_unique.index[[0,1,2]])
    DF_delta_poste_unique = DF_delta_poste_unique.drop(DF_delta_poste_unique.index[[0]])
    # À tester suite nouveau tableau impact poste

    # Réinitialiser l'index
    DF_delta_poste_unique.reset_index(drop=True, inplace=True)

    # Return le DataFrame résultant
    return DF_delta_poste_unique

def creation_et_affichage_du_graphique(poste, DF_delta_poste_unique, liste_equipes_en_gras):

    # Trier le DF
    DF_delta_poste_unique = DF_delta_poste_unique.sort_values(by='Delta', ascending=True)
    DF_delta_poste_unique.reset_index(drop=True, inplace=True)

    # Détermination des limites de l'axe des y
    y_min = min(DF_delta_poste_unique["Delta"]) - 0.5  # Valeur minimale avec une marge de 0.5
    y_max = max(DF_delta_poste_unique["Delta"]) + 0.5  # Valeur maximale avec une marge de 0.5

    # Création de la colormap de rouge à vert
    colors = plt.cm.RdYlGn(np.linspace(0, 1, len(DF_delta_poste_unique["Delta"])))

    # Création du graphique en nuage de points avec des couleurs graduées
    plt.figure(figsize=(10, 6))
    for i in range(len(DF_delta_poste_unique["Team"])):
        plt.scatter(DF_delta_poste_unique["Team"][i], DF_delta_poste_unique["Delta"][i], color=colors[i])

    # Remettre le nom complet du poste
    poste_complet = poste_ABV_to_poste_full(poste)

    # Ajout de titres et d'étiquettes
    plt.title(f'Delta pour les {poste_complet}')
    # plt.xlabel('Équipe')
    plt.ylabel('Delta')

    # Masquer les étiquettes de l'axe des x et l'axe des x lui-même
    plt.xticks([])
    plt.gca().axes.get_xaxis().set_visible(False)

    # Définir l'intervalle des graduations sur l'axe des y à des intervalles de 0.25
    plt.yticks(np.arange(y_min, y_max, 0.25))

    # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
    # plt.xticks(rotation=45, ha='right')

    # Ajout des noms d'équipe au-dessus de chaque point
    # for i in range(len(DF_delta_poste_unique["Team"])):
    #    plt.text(DF_delta_poste_unique["Team"][i], DF_delta_poste_unique["Delta"][i] + 0.1, DF_delta_poste_unique["Team"][i], ha='center', va='bottom')

    # Récupération des données
    teams = DF_delta_poste_unique["Team"]
    deltas = DF_delta_poste_unique["Delta"]

    # Mettre des étiquettes de données au dessus de chaque point
    # Ajout du texte au graphique pour chaque équipe
    for team, delta in zip(teams, deltas):
        # Position horizontale et verticale du texte
        x_position = team
        y_position = delta + 0.1  # Légèrement au-dessus de la valeur de delta

        # Vérifier si l'équipe doit être en gras
        if team in liste_equipes_en_gras:
            # Ajout du texte en gras
            plt.text(x_position, y_position, team, fontweight='bold', ha='center', va='bottom')
        else:
            # Ajout du texte normal
            plt.text(x_position, y_position, team, ha='center', va='bottom')

    # Tracer une ligne rouge au niveau de Y = 0
    plt.axhline(y=0, color='red', linestyle='--')

    # Affichage du graphique
    plt.tight_layout()
    plt.show()

def affichage_du_graphique_avec_boucle_postes():
    
    DF_delta_complet = obtenir_DF_complet()

    # liste_de_postes = ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C']

    liste_de_postes = ['G']

    liste_equipes_en_gras = ['SAS', 'MIN']
        
    for poste in liste_de_postes:
        print(poste)
        DF_delta_poste_unique = formater_DF_avec_poste_voulu(poste, DF_delta_complet)
        creation_et_affichage_du_graphique(poste, DF_delta_poste_unique, liste_equipes_en_gras)

affichage_du_graphique_avec_boucle_postes()