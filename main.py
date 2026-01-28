# ============================================
# FRUIT NINJA - RHYTHM GAME
# Fichier principal du jeu
# ============================================

import pygame
from constantes import (
    COULEURS_COLONNES, NOMS_TOUCHES,
    NOMBRE_COLONNES, LARGEUR_COLONNE,
    HAUTEUR_FENETRE, LARGEUR_FENETRE, FPS,
    BLANC
)
from initialisation import initialiser_pygame, charger_toutes_les_images
from logique import creer_objet_aleatoire


# ============================================
# MENU D'ACCUEIL
# ============================================

class Bouton:
    """Classe pour créer des boutons cliquables."""

    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_hover):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_hover = couleur_hover
        self.est_survole = False

    def dessiner(self, ecran):
        """Dessine le bouton sur l'écran."""
        couleur_actuelle = self.couleur_hover if self.est_survole else self.couleur

        # Dessiner le rectangle du bouton
        pygame.draw.rect(ecran, couleur_actuelle, self.rect, border_radius=10)
        pygame.draw.rect(ecran, BLANC, self.rect, 3, border_radius=10)

        # Dessiner le texte
        font = pygame.font.Font(None, 50)
        texte_surface = font.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        ecran.blit(texte_surface, texte_rect)

    def verifier_survol(self, pos_souris):
        """Vérifie si la souris survole le bouton."""
        self.est_survole = self.rect.collidepoint(pos_souris)

    def est_clique(self, pos_souris):
        """Vérifie si le bouton est cliqué."""
        return self.rect.collidepoint(pos_souris)


def menu_accueil(ecran, horloge, images):
    """
    Affiche le menu d'accueil avec les options Play, Score, Quitter.
    Retourne: "play", "score", ou "quitter"
    """
    # Créer les boutons
    largeur_bouton = 250
    hauteur_bouton = 60
    x_bouton = LARGEUR_FENETRE // 2 - largeur_bouton // 2

    bouton_play = Bouton(
        x_bouton, 350, largeur_bouton, hauteur_bouton,
        "PLAY", (50, 150, 50), (80, 200, 80)
    )
    bouton_score = Bouton(
        x_bouton, 450, largeur_bouton, hauteur_bouton,
        "SCORES", (50, 100, 150), (80, 140, 200)
    )
    bouton_quitter = Bouton(
        x_bouton, 550, largeur_bouton, hauteur_bouton,
        "QUITTER", (150, 50, 50), (200, 80, 80)
    )

    boutons = [bouton_play, bouton_score, bouton_quitter]

    while True:
        pos_souris = pygame.mouse.get_pos()

        # Gestion des événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_play.est_clique(pos_souris):
                    return "play"
                elif bouton_score.est_clique(pos_souris):
                    return "score"
                elif bouton_quitter.est_clique(pos_souris):
                    return "quitter"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "quitter"

        # Mettre à jour l'état de survol des boutons
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)

        # Affichage - fond spécifique pour l'accueil
        ecran.blit(images["image_accueil"], (0, 0))

        # Dessiner les boutons
        for bouton in boutons:
            bouton.dessiner(ecran)

        pygame.display.flip()
        horloge.tick(FPS)


# ============================================
# ÉCRAN DES SCORES
# ============================================

def ecran_scores(ecran, horloge, images):
    """Affiche l'écran des scores."""
    bouton_retour = Bouton(
        LARGEUR_FENETRE // 2 - 125, 600, 250, 60,
        "RETOUR", (100, 100, 100), (150, 150, 150)
    )

    while True:
        pos_souris = pygame.mouse.get_pos()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.est_clique(pos_souris):
                    return "menu"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu"

        bouton_retour.verifier_survol(pos_souris)

        # Affichage
        ecran.blit(images["fond"], (0, 0))

        # Titre
        font_titre = pygame.font.Font(None, 80)
        titre = font_titre.render("MEILLEURS SCORES", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR_FENETRE // 2, 100))
        ecran.blit(titre, titre_rect)

        # Message placeholder (à remplacer par les vrais scores plus tard)
        font = pygame.font.Font(None, 40)
        message = font.render("Aucun score enregistré", True, BLANC)
        message_rect = message.get_rect(center=(LARGEUR_FENETRE // 2, 350))
        ecran.blit(message, message_rect)

        bouton_retour.dessiner(ecran)

        pygame.display.flip()
        horloge.tick(FPS)


# ============================================
# JEU PRINCIPAL
# ============================================

def dessiner_colonnes(ecran):
    """Dessine les 4 colonnes très discrètes pour guider les fruits."""
    for i in range(1, NOMBRE_COLONNES):
        x = i * LARGEUR_COLONNE
        ligne = pygame.Surface((1, HAUTEUR_FENETRE))
        ligne.set_alpha(30)
        ligne.fill((255, 255, 255))
        ecran.blit(ligne, (x, 0))

    # Afficher les touches en bas de l'écran
    font = pygame.font.Font(None, 36)
    for i in range(NOMBRE_COLONNES):
        x = i * LARGEUR_COLONNE + LARGEUR_COLONNE // 2
        couleur = COULEURS_COLONNES[i]
        texte = font.render(NOMS_TOUCHES[i], True, couleur)
        texte_rect = texte.get_rect(center=(x, HAUTEUR_FENETRE - 30))
        ecran.blit(texte, texte_rect)


def jouer(ecran, horloge, images):
    """Lance une partie de jeu."""
    objets = []
    compteur_spawn = 0
    FRAMES_ENTRE_SPAWN = 90

    while True:
        # 1. GESTION DES ÉVÉNEMENTS
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu"

        # 2. LOGIQUE DU JEU
        compteur_spawn += 1
        if compteur_spawn >= FRAMES_ENTRE_SPAWN:
            compteur_spawn = 0
            objets.append(creer_objet_aleatoire())

        for objet in objets:
            objet.mettre_a_jour()

        objets = [obj for obj in objets if obj.actif]

        # 3. AFFICHAGE
        ecran.blit(images["fond"], (0, 0))
        dessiner_colonnes(ecran)

        for objet in objets:
            objet.dessiner(ecran, images)

        # 4. MISE À JOUR DE L'ÉCRAN
        pygame.display.flip()
        horloge.tick(FPS)


# ============================================
# BOUCLE PRINCIPALE
# ============================================

def boucle_principale():
    """Boucle principale qui gère les différents états du jeu."""
    ecran, horloge = initialiser_pygame()
    images = charger_toutes_les_images()

    etat = "menu"

    while etat != "quitter":
        if etat == "menu":
            etat = menu_accueil(ecran, horloge, images)
        elif etat == "play":
            etat = jouer(ecran, horloge, images)
        elif etat == "score":
            etat = ecran_scores(ecran, horloge, images)

    pygame.quit()


# Point d'entrée du programme
if __name__ == "__main__":
    boucle_principale()
