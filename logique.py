import random
import string
import pygame
from constantes import (
    LARGEUR_COLONNE, TAILLE_OBJET, 
    HAUTEUR_FENETRE, GRAVITE,
    VITESSE_INITIALE_Y_MIN, VITESSE_INITIALE_Y_MAX
)

class Objet:
    def __init__(self, colonne, type_objet, mode="difficile"):
        self.colonne = colonne
        self.type_objet = type_objet
        self.mode = mode
        
        centre_colonne = colonne * LARGEUR_COLONNE + LARGEUR_COLONNE // 2
        self.x = centre_colonne - TAILLE_OBJET // 2
        self.y = HAUTEUR_FENETRE
        self.vitesse_y = random.uniform(VITESSE_INITIALE_Y_MIN, VITESSE_INITIALE_Y_MAX)
        self.actif = True

        # --- GESTION DES TOUCHES SELON LE MODE ---
        if self.mode == "facile":
            # Mode facile : Touches fixes C, V, B, N selon la colonne
            touches_fixes = ["C", "V", "B", "N"]
            self.lettre = touches_fixes[colonne]
            codes_fixes = [pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n]
            self.touche_code = codes_fixes[colonne]
        else:
            # Mode difficile : Lettre aléatoire
            self.lettre = random.choice(string.ascii_uppercase)
            self.touche_code = getattr(pygame, f"K_{self.lettre.lower()}")

    def mettre_a_jour(self):
        # Applique la vitesse
        self.y += self.vitesse_y
        
        # Applique la gravité
        self.vitesse_y += GRAVITE
        
        # Optionnel : Ajoute une légère friction (amorti)
        self.vitesse_y *= 0.99 
        
        if self.y > HAUTEUR_FENETRE + 100:
            self.actif = False

    def dessiner(self, ecran, images, font):
        if self.actif and self.type_objet in images:
            # Dessin du fruit/bombe/coeur
            ecran.blit(images[self.type_objet], (int(self.x), int(self.y)))
            
            # Dessin de la lettre en dessous
            # Petit fond noir pour la lisibilité
            surface_lettre = font.render(self.lettre, True, (255, 255, 255))
            pos_lettre = (self.x + 20, self.y + TAILLE_OBJET + 5)
            pygame.draw.circle(ecran, (0,0,0), (int(self.x + 32), int(self.y + TAILLE_OBJET + 20)), 18)
            ecran.blit(surface_lettre, pos_lettre)