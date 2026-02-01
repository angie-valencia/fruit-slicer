# ============================================
# LOGIQUE DU JEU - OBJETS ET GAMEPLAY
# ============================================

import random
from constantes import (
    LARGEUR_COLONNE, NOMBRE_COLONNES,
    TAILLE_OBJET, LISTE_FRUITS,
    HAUTEUR_FENETRE, LARGEUR_FENETRE,
    GRAVITE,
    VITESSE_INITIALE_Y_MIN, VITESSE_INITIALE_Y_MAX,
    VITESSE_INITIALE_X_MIN, VITESSE_INITIALE_X_MAX,
    PROBABILITE_BOMBE, PROBABILITE_GLACON 
)


class Objet:
    """
    Classe représentant un objet lancé en l'air (fruit, bombe, glaçon).
    Utilise une physique de gravité pour une trajectoire parabolique.
    """

    def __init__(self, colonne, type_objet):
        """
        Crée un nouvel objet lancé depuis le bas de l'écran.

        Args:
            colonne: Numéro de la colonne (0 à 3)
            type_objet: Type d'objet ("banane", "bombe", "glacon", etc.)
        """
        self.colonne = colonne
        self.type_objet = type_objet

        # Position X : centré dans la colonne avec légère variation
        centre_colonne = colonne * LARGEUR_COLONNE + LARGEUR_COLONNE // 2
        self.x = centre_colonne - TAILLE_OBJET // 2

        # Position Y : commence en bas de l'écran (juste en dessous)
        self.y = HAUTEUR_FENETRE + TAILLE_OBJET

        # Vitesse initiale (lancé vers le haut)
        self.vitesse_y = random.uniform(VITESSE_INITIALE_Y_MIN, VITESSE_INITIALE_Y_MAX)
        self.vitesse_x = random.uniform(VITESSE_INITIALE_X_MIN, VITESSE_INITIALE_X_MAX)

        # L'objet est-il encore actif ?
        self.actif = True

        # L'objet a-t-il atteint son point le plus haut ? (pour savoir quand il redescend)
        self.descend = False

    def mettre_a_jour(self):
        """
        Met à jour la position de l'objet avec la gravité.
        Trajectoire parabolique : monte puis redescend.
        """
        # Appliquer la gravité à la vitesse verticale
        self.vitesse_y += GRAVITE

        # Mettre à jour la position
        self.y += self.vitesse_y
        self.x += self.vitesse_x

        # Détecter si l'objet redescend
        if self.vitesse_y > 0:
            self.descend = True

        # Désactiver si l'objet sort de l'écran par le bas (après être redescendu)
        if self.y > HAUTEUR_FENETRE + TAILLE_OBJET and self.descend:
            self.actif = False

        # Garder l'objet dans les limites horizontales de l'écran
        if self.x < 0:
            self.x = 0
            self.vitesse_x = -self.vitesse_x * 0.5  # Rebond léger
        elif self.x > LARGEUR_FENETRE - TAILLE_OBJET:
            self.x = LARGEUR_FENETRE - TAILLE_OBJET
            self.vitesse_x = -self.vitesse_x * 0.5

    def dessiner(self, ecran, images):
        """
        Dessine l'objet sur l'écran.

        Args:
            ecran: Surface Pygame où dessiner
            images: Dictionnaire des images chargées
        """
        if self.actif and self.type_objet in images:
            ecran.blit(images[self.type_objet], (int(self.x), int(self.y)))

    def est_dans_zone_frappe(self, zone_y_min, zone_y_max):
        """
        Vérifie si l'objet est dans la zone de frappe.

        Args:
            zone_y_min: Position Y minimale de la zone
            zone_y_max: Position Y maximale de la zone

        Retourne: True si l'objet est dans la zone
        """
        centre_y = self.y + TAILLE_OBJET // 2
        return zone_y_min <= centre_y <= zone_y_max

class Objet:
    """
    Classe représentant un objet lancé en l'air (fruit, bombe, glaçon).
    Utilise une physique de gravité pour une trajectoire parabolique.
    """

    def __init__(self, colonne, type_objet):
        """
        Crée un nouvel objet lancé depuis le bas de l'écran.

        Args:
            colonne: Numéro de la colonne (0 à 3)
            type_objet: Type d'objet ("banane", "bombe", "glacon", etc.)
        """
        self.colonne = colonne
        self.type_objet = type_objet

        # Position X : centré dans la colonne avec légère variation
        centre_colonne = colonne * LARGEUR_COLONNE + LARGEUR_COLONNE // 2
        self.x = centre_colonne - TAILLE_OBJET // 2

        # Position Y : commence en bas de l'écran (juste en dessous)
        self.y = HAUTEUR_FENETRE + TAILLE_OBJET

        # Vitesse initiale (lancé vers le haut)
        self.vitesse_y = random.uniform(VITESSE_INITIALE_Y_MIN, VITESSE_INITIALE_Y_MAX)
        self.vitesse_x = random.uniform(VITESSE_INITIALE_X_MIN, VITESSE_INITIALE_X_MAX)

        # L'objet est-il encore actif ?
        self.actif = True

        # L'objet a-t-il atteint son point le plus haut ? (pour savoir quand il redescend)
        self.descend = False

    def mettre_a_jour(self):
        """
        Met à jour la position de l'objet avec la gravité.
        Trajectoire parabolique : monte puis redescend.
        """
        # Appliquer la gravité à la vitesse verticale
        self.vitesse_y += GRAVITE

        # Mettre à jour la position
        self.y += self.vitesse_y
        self.x += self.vitesse_x

        # Détecter si l'objet redescend
        if self.vitesse_y > 0:
            self.descend = True

        # Désactiver si l'objet sort de l'écran par le bas (après être redescendu)
        if self.y > HAUTEUR_FENETRE + TAILLE_OBJET and self.descend:
            self.actif = False

        # Garder l'objet dans les limites horizontales de l'écran
        if self.x < 0:
            self.x = 0
            self.vitesse_x = -self.vitesse_x * 0.5  # Rebond léger
        elif self.x > LARGEUR_FENETRE - TAILLE_OBJET:
            self.x = LARGEUR_FENETRE - TAILLE_OBJET
            self.vitesse_x = -self.vitesse_x * 0.5

    def dessiner(self, ecran, images):
        """
        Dessine l'objet sur l'écran.

        Args:
            ecran: Surface Pygame où dessiner
            images: Dictionnaire des images chargées
        """
        if self.actif and self.type_objet in images:
            ecran.blit(images[self.type_objet], (int(self.x), int(self.y)))

    def est_dans_zone_frappe(self, zone_y_min, zone_y_max):
        """
        Vérifie si l'objet est dans la zone de frappe.

        Args:
            zone_y_min: Position Y minimale de la zone
            zone_y_max: Position Y maximale de la zone

        Retourne: True si l'objet est dans la zone
        """
        centre_y = self.y + TAILLE_OBJET // 2
        return zone_y_min <= centre_y <= zone_y_max

    def est_fruit(self):
        """
        Vérifie si l'objet est un fruit (pas une bombe ou un glaçon).
        
        Retourne: True si c'est un fruit, False sinon
        """
        return self.type_objet in LISTE_FRUITS

def creer_objet_aleatoire():
    """
    Crée un objet aléatoire dans une colonne aléatoire.
    L'objet est lancé depuis le bas avec une trajectoire parabolique.

    Retourne: Un nouvel objet Objet
    """
    colonne = random.randint(0, NOMBRE_COLONNES - 1)

    # Déterminer le type d'objet avec des probabilités
    rand = random.random()  # Nombre entre 0 et 1

    if rand < PROBABILITE_BOMBE:
        type_objet = "bombe"
    elif rand < PROBABILITE_BOMBE + PROBABILITE_GLACON:
        type_objet = "glacon"
    else:
        type_objet = random.choice(LISTE_FRUITS)

    return Objet(colonne, type_objet)

    def est_fruit(self):
        """Retourne True si l'objet est un fruit (pas bombe/glaçon)."""
        return self.type_objet in LISTE_FRUITS