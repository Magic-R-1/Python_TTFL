import matplotlib.pyplot as plt

import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Mon_TI')

from k_Impact_poste import *

# print(obtenir_delta_ttfl_postes())

# Création du DataFrame avec les données fournies
data = {
    "Team": ["MIN", "CLE", "NOP", "NYK", "OKC", "CHI", "LAC", "BOS", "DEN", "PHX", 
             "MEM", "PHI", "ORL", "POR", "HOU", "MIA", "UTA", "TOR", "CHA", "LAL", 
             "WAS", "BKN", "SAC", "DAL", "ATL", "GSW", "MIL", "IND", "DET", "SAS"],
    "Value": [-3.5, -2.4, -1.8, -1.7, -1.4, -1.3, -1.2, -0.9, -0.7, -0.6, -0.6, -0.4,
              -0.1, -0.1, 0.1, 0.2, 0.2, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.1, 1.3, 1.3,
              1.8, 1.9, 1.9, 2.1]
}

# Détermination des limites de l'axe des y
y_min = min(data["Value"]) - 0.5  # Valeur minimale avec une marge de 0.5
y_max = max(data["Value"]) + 0.5  # Valeur maximale avec une marge de 0.5

# Création de la colormap de rouge à vert
colors = plt.cm.RdYlGn(np.linspace(0, 1, len(data["Value"])))

# Création du graphique en nuage de points avec des couleurs graduées
plt.figure(figsize=(10, 6))
for i in range(len(data["Team"])):
    plt.scatter(data["Team"][i], data["Value"][i], color=colors[i])

# Ajout de titres et d'étiquettes
plt.title('Delta pour les Guards')
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
for i in range(len(data["Team"])):
    plt.text(data["Team"][i], data["Value"][i] + 0.1, data["Team"][i], ha='center', va='bottom')

# Tracer une ligne rouge au niveau de Y = 0
plt.axhline(y=0, color='red', linestyle='--')

# Affichage du graphique
plt.tight_layout()
plt.show()