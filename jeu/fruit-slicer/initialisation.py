# ============================================
# INITIALISATION DE PYGAME ET CHARGEMENT
# ============================================

import pygame
from constantes import (
    LARGEUR_FENETRE, HAUTEUR_FENETRE,
    IMAGES, TAILLE_OBJET, SONS
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
    except (pygame.error, FileNotFoundError) as e:
        print(f"Erreur lors du chargement de l'image {chemin}: {e}")
        # Retourne une surface colorée en cas d'erreur (pour debug)
        largeur = taille[0] if taille else TAILLE_OBJET
        hauteur = taille[1] if taille else TAILLE_OBJET
        surface = pygame.Surface((largeur, hauteur))
        surface.fill((255, 0, 255))  # Magenta pour repérer facilement
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

def charger_sons():
    """
    Charge tous les sons du jeu.
    Retourne: Un dictionnaire avec tous les sons chargés
    """
    sons_charges = {}
    
    for nom, chemin in SONS.items():
        try:
            son = pygame.mixer.Sound(chemin)
            son.set_volume(0.7)  # Volume à 50% (0.0 à 1.0)
            sons_charges[nom] = son
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erreur lors du chargement du son {chemin}: {e}")
            # Créer un son vide en cas d'erreur (pour ne pas planter le jeu)
            sons_charges[nom] = None
    
    return sons_charges
