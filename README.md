# Fruit Ninja - Rhythm Game

Jeu de typing inspiré de Fruit Ninja - Projet Python/Pygame (1ère année IA/Data)

## Description

Un jeu de rythme où des fruits sont propulsés en l'air avec un système de gravité réaliste. Le joueur doit appuyer sur les bonnes touches (D, F, J, K) pour trancher les fruits au bon moment.

## Fonctionnalités implémentées

### Menu d'accueil
- Image de fond personnalisée
- 3 boutons interactifs avec effet de survol :
  - **PLAY** : Lance une partie
  - **SCORES** : Affiche les meilleurs scores (en cours)
  - **QUITTER** : Ferme le jeu

### Système de jeu
- **4 colonnes** correspondant aux touches D, F, J, K
- **Physique de gravité** : les fruits sont lancés depuis le bas et suivent une trajectoire parabolique
- **Spawn aléatoire** des fruits dans les différentes colonnes
- Colonnes discrètes pour guider visuellement le joueur

### Assets graphiques
- 6 fruits : ananas, banane, pomme, orange, pastèque, framboise
- Objets spéciaux : bombe, glaçon
- Effets visuels : explosion (boom), coeurs
- Fonds d'écran : accueil et jeu

## Structure du projet

```
fruit-slicer/
├── main.py           # Boucle principale, menu et logique de jeu
├── constantes.py     # Configuration (dimensions, couleurs, physique)
├── initialisation.py # Initialisation Pygame et chargement des images
├── logique.py        # Classe Objet et gestion des fruits
└── README.md
```

## Contrôles

| Touche | Action |
|--------|--------|
| D | Colonne 1 (rouge) |
| F | Colonne 2 (vert) |
| J | Colonne 3 (bleu) |
| K | Colonne 4 (jaune) |
| ESC | Retour au menu / Quitter |

## Configuration

Les paramètres du jeu sont modifiables dans `constantes.py` :
- Dimensions de la fenêtre (1200x800)
- Gravité et vitesse de lancement des fruits
- Taille des objets
- FPS (60)

## Lancement

```bash
cd fruit-slicer
python3 main.py
```

## Prérequis

- Python 3.x
- Pygame (`pip install pygame`)

## À implémenter

- [ ] Détection des touches pour trancher les fruits
- [ ] Système de score
- [ ] Système de strikes (3 fruits ratés = game over)
- [ ] Bombes (game over instantané)
- [ ] Glaçons (gel du temps)
- [ ] Combos (plusieurs fruits tranchés d'un coup)
- [ ] Sauvegarde des scores
- [ ] Niveaux de difficulté
