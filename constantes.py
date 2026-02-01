import pygame
import os

# Configuration Fenêtre
LARGEUR_FENETRE = 1200
HAUTEUR_FENETRE = 800

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 100, 255)
JAUNE = (255, 255, 0)

# Jeu
LARGEUR_COLONNE = LARGEUR_FENETRE // 4
LISTE_FRUITS = ["ananas", "banane", "pomme", "orange", "pasteque", "framboise"]
FPS = 60
TAILLE_OBJET = 80
GRAVITE = 0.18
VITESSE_INITIALE_Y_MIN = -24
VITESSE_INITIALE_Y_MAX = -20

# Musiques
LISTE_MUSIQUES = {
    "1": {"nom": "Queen - Don't Stop Me Now", "fichier": "queen", "offset": 7.85},
    "2": {"nom": "ZZ Top - La Grange", "fichier": "zztop", "offset": 5.80},
}

# Images
DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))
CHEMIN_IMAGES = os.path.join(DOSSIER_PROJET, "image") + os.sep

IMAGES = {
    "ananas": CHEMIN_IMAGES + "ananas.png",
    "banane": CHEMIN_IMAGES + "banane.png",
    "pomme": CHEMIN_IMAGES + "pomme.png",
    "orange": CHEMIN_IMAGES + "orange.png",
    "pasteque": CHEMIN_IMAGES + "pasteque.png",
    "framboise": CHEMIN_IMAGES + "framboise.png",
    "bombe": CHEMIN_IMAGES + "bombe.png",
    "fond": CHEMIN_IMAGES + "paysage.jpg",
    "coeur": CHEMIN_IMAGES + "coeur.png",
    "toasty": CHEMIN_IMAGES + "toasty.png",
    "image_accueil": CHEMIN_IMAGES + "image_accueil.jpg",
    "ananas_coupee": CHEMIN_IMAGES + "ananas_coupee.png",
    "banane_coupee": CHEMIN_IMAGES + "banane_coupee.png",
    "pomme_coupee": CHEMIN_IMAGES + "pomme_coupee.png",
    "orange_coupee": CHEMIN_IMAGES + "orange_coupee.png",
    "pasteque_coupee": CHEMIN_IMAGES + "pasteque_coupee.png",
    "framboise_coupee": CHEMIN_IMAGES + "framboise_coupee.png",
    "bombe_coupee": CHEMIN_IMAGES + "bombe_coupee.png",
    "coeur_coupee": CHEMIN_IMAGES + "coeur_coupee.png"
}
# Si le son est au même endroit que le code
CHEMIN_SONS = DOSSIER_PROJET + os.sep 

SONS = {
    "toasty": os.path.join(CHEMIN_SONS, "toasty.wav")
}