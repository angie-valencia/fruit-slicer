# ============================================
# INITIALISATION DE PYGAME ET CHARGEMENT
# ============================================

import pygame
from constantes import (
    LARGEUR_FENETRE, HAUTEUR_FENETRE,
    IMAGES, TAILLE_OBJET
)


def initialiser_pygame():
    """
    Initialise Pygame et crée la fenêtre du jeu.
    Retourne: la surface de la fenêtre (écran)
    """
    pygame.init()

    # Création de la fenêtre
    ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption("Fruit Ninja - Rhythm Game")

    # Horloge pour contrôler les FPS
    horloge = pygame.time.Clock()

    return ecran, horloge


def charger_image(chemin, taille=None):
    """
    Charge une image et la redimensionne si nécessaire.

    Args:
        chemin: Le chemin vers l'image
        taille: Tuple (largeur, hauteur) ou None pour garder la taille originale

    Retourne: La surface de l'image chargée
    """
    try:
        image = pygame.image.load(chemin).convert_alpha()
        if taille:
            image = pygame.transform.scale(image, taille)
        return image
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image {chemin}: {e}")
        # Retourne une surface rouge en cas d'erreur (pour debug)
        surface = pygame.Surface((TAILLE_OBJET, TAILLE_OBJET))
        surface.fill((255, 0, 0))
        return surface


def charger_toutes_les_images():
    """
    Charge toutes les images du jeu.
    Retourne: Un dictionnaire avec toutes les images chargées
    """
    images_chargees = {}

    for nom, chemin in IMAGES.items():
        if nom == "fond" or nom == "image_accueil":
            # Les fonds prennent toute la fenêtre
            images_chargees[nom] = charger_image(chemin, (LARGEUR_FENETRE, HAUTEUR_FENETRE))
        elif nom == "coeur":
            # Les coeurs sont plus petits
            images_chargees[nom] = charger_image(chemin, (40, 40))
        else:
            # Les fruits et objets ont une taille standard
            images_chargees[nom] = charger_image(chemin, (TAILLE_OBJET, TAILLE_OBJET))

    return images_chargees
