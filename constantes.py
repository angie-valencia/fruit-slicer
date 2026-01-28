# ============================================
# CONSTANTES DU JEU FRUIT NINJA - RHYTHM GAME
# ============================================

import pygame

# ----- DIMENSIONS DE LA FENÊTRE -----
LARGEUR_FENETRE = 1200
HAUTEUR_FENETRE = 800

# ----- COULEURS (format RGB) -----
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 100, 255)
JAUNE = (255, 255, 0)

# Couleurs des colonnes (une par colonne)
COULEURS_COLONNES = [
    (255, 100, 100),  # Rouge clair - Colonne D
    (100, 255, 100),  # Vert clair - Colonne F
    (100, 100, 255),  # Bleu clair - Colonne J
    (255, 255, 100),  # Jaune clair - Colonne K
]

# ----- CONFIGURATION DES COLONNES -----
# Les touches que le joueur doit utiliser
TOUCHES_COLONNES = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
NOMS_TOUCHES = ["D", "F", "J", "K"]
NOMBRE_COLONNES = 4

# Calcul automatique de la largeur des colonnes
LARGEUR_COLONNE = LARGEUR_FENETRE // NOMBRE_COLONNES

# ----- ZONE DE FRAPPE -----
# Zone où les fruits atteignent leur apogée (en haut de l'écran)
# C'est là que le joueur doit appuyer pour trancher
HAUTEUR_ZONE_FRAPPE = 120
POSITION_Y_ZONE_FRAPPE = 80  # Position en haut de l'écran

# ----- OBJETS (FRUITS/BOMBES) -----
TAILLE_OBJET = 98  # Taille des sprites redimensionnés

# ----- PHYSIQUE (GRAVITÉ) -----
GRAVITE = 0.35  # Accélération vers le bas (pixels/frame²)
VITESSE_INITIALE_Y_MIN = -27  # Vitesse verticale de lancement (négative = vers le haut)
VITESSE_INITIALE_Y_MAX = -23  # Variation pour plus de diversité
VITESSE_INITIALE_X_MIN = 0  # Pas de déviation horizontale (fruits restent dans leur colonne)
VITESSE_INITIALE_X_MAX = 0

# ----- TIMING ET FPS -----
FPS = 60  # Images par seconde

# ----- CHEMINS DES IMAGES -----
# Chemin absolu basé sur l'emplacement de ce fichier
import os
DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))
CHEMIN_IMAGES = os.path.join(DOSSIER_PROJET, "image") + os.sep

# Dictionnaire des images disponibles
IMAGES = {
    "ananas": CHEMIN_IMAGES + "ananas.png",
    "banane": CHEMIN_IMAGES + "banane.png",
    "pomme": CHEMIN_IMAGES + "pomme.png",
    "orange": CHEMIN_IMAGES + "orange.png",
    "pasteque": CHEMIN_IMAGES + "pasteque.png",
    "framboise": CHEMIN_IMAGES + "framboise.png",
    "bombe": CHEMIN_IMAGES + "bombe.png",
    "glacon": CHEMIN_IMAGES + "ice-cube.png",
    "fond": CHEMIN_IMAGES + "paysage.png",
    "coeur": CHEMIN_IMAGES + "coeur.webp",
    "boom": CHEMIN_IMAGES + "boom.png",
    "image_accueil": CHEMIN_IMAGES + "image_accueil.png",
}

# Liste des fruits (pour le spawn aléatoire)
LISTE_FRUITS = ["ananas", "banane", "pomme", "orange", "pasteque", "framboise"]

# ----- RÈGLES DU JEU -----
NOMBRE_STRIKES_MAX = 3  # Game over après 3 strikes
DUREE_GEL_GLACON = 3  # Secondes de gel quand on touche un glaçon
