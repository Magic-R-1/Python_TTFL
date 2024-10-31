# Axe X en float avec image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

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

    """ DF_data = pd.DataFrame({
        'Poste': ["MIN", "CLE", "NOP", "NYK", "OKC", "CHI", "LAC", "BOS", "DEN", "PHX", 
        "MEM", "PHI", "ORL", "POR", "HOU", "MIA", "UTA", "TOR", "CHA", "LAL", 
        "WAS", "BKN", "SAC", "DAL", "ATL", "GSW", "MIL", "IND", "DET", "SAS"],
        'G': [-3.5, -2.4, -1.8, -1.7, -1.4, -1.3, -1.2, -0.9, -0.7, -0.6, -0.6, -0.4,
        -0.1, -0.1, 0.1, 0.2, 0.2, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.1, 1.3, 1.3,
        1.8, 1.9, 1.9, 2.1]},
        columns = ['Poste', 'G'])

    return DF_data """

def formater_DF_avec_poste_voulu(poste, DF_delta_complet):

    # Sélection des colonnes d'intérêt (Poste et les scores pour chaque équipe)
    DF_delta_poste_unique = DF_delta_complet[["Poste", poste]]

    # Renommer les colonnes pour correspondre au format souhaité
    DF_delta_poste_unique.columns = ["Team", "Delta"]

    # Supprimer les lignes inintéressantes
    DF_delta_poste_unique = DF_delta_poste_unique.drop(DF_delta_poste_unique.index[[0,1,2]])

    # Réinitialiser l'index
    DF_delta_poste_unique.reset_index(drop=True, inplace=True)

    # Return le DataFrame résultant
    return DF_delta_poste_unique

def creation_et_affichage_du_graphique(poste, DF_delta_poste_unique):

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
    for i in range(len(DF_delta_poste_unique.index)):
        plt.scatter(DF_delta_poste_unique.index[i], DF_delta_poste_unique["Delta"][i], color=colors[i])

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

    # Récupération des données
    teams = DF_delta_poste_unique.index  # Utilisation de l'index des équipes
    deltas = DF_delta_poste_unique["Delta"]

    # Mettre des étiquettes de données au dessus de chaque point
    for i, delta in zip(teams, deltas):
        # Position horizontale et verticale du texte
        x_position = i
        y_position = round(delta + 0.1,2)  # Légèrement au-dessus de la valeur de delta

        team = DF_delta_poste_unique["Team"][i]

        # Ajout du texte
        # plt.text(x_position, y_position, team, ha='center', va='bottom')

        # Ajout de l'image
        ajout_image(y_min, y_max, team, x_position, y_position)

    # Définir les limites de l'axe x et y manuellement
    plt.xlim(-1, len(DF_delta_poste_unique))  # Ajuster les limites de l'axe x selon le nombre d'équipes
    plt.ylim(y_min, y_max)  # Utiliser les limites précédemment déterminées pour l'axe y

    # Tracer une ligne rouge au niveau de Y = 0
    plt.axhline(y=0, color='red', linestyle='--')

    # Affichage du graphique
    # plt.tight_layout()
    plt.show()

def ajout_image(y_min, y_max, team, x_position, y_position):
    
    chemin = f"C:/Users/egretillat/Documents/Personnel/Python_TTFL/Charts/Logos/{team}.png"

    # Charger et afficher l'image
    img = mpimg.imread(chemin)  # Remplacez "chemin_vers_votre_image/image.jpg" par le chemin de votre image

    # Largeur et hauteur de l'image
    taille_y = 0.25
    total_range_y = y_max - y_min
    ratio_y = taille_y/total_range_y

    total_range_x = 31
    taille_x = round(ratio_y * total_range_x,2)

    # Affichage de l'image
    plt.imshow(img, extent=[x_position, x_position+taille_x, y_position, y_position+taille_y], aspect='auto')

def affichage_du_graphique_avec_boucle_postes():
    
    DF_delta_complet = obtenir_DF_complet()

    # liste_de_postes = ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C']

    liste_de_postes = ['G']

    for poste in liste_de_postes:
        DF_delta_poste_unique = formater_DF_avec_poste_voulu(poste, DF_delta_complet)
        creation_et_affichage_du_graphique(poste, DF_delta_poste_unique)

affichage_du_graphique_avec_boucle_postes()

# gestion_taille_image()