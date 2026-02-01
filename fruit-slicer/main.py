# ============================================
# FRUIT NINJA - RHYTHM GAME
# Fichier principal du jeu
# ============================================

import pygame
from constantes import (
    COULEURS_COLONNES, NOMS_TOUCHES,
    NOMBRE_COLONNES, LARGEUR_COLONNE,
    HAUTEUR_FENETRE, LARGEUR_FENETRE, FPS,
    BLANC, TOUCHES_COLONNES,  # Ajoute TOUCHES_COLONNES
    SCORE_INITIAL, POINTS_PAR_FRUIT, NOMBRE_VIES_INITIAL,
    DIFFICULTES, DUREE_GEL
)
from initialisation import initialiser_pygame, charger_toutes_les_images, charger_sons
from logique import creer_objet_aleatoire
from sauvegarde import charger_scores, sauvegarder_score, est_dans_top_scores

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

    def est_clique(self, pos_souris, sons=None, type_son="clic_play"):
        """
        Vérifie si le bouton est cliqué et joue un son.
        
        Args:
            pos_souris: Position de la souris
            sons: Dictionnaire des sons chargés
            type_son: Nom du son à jouer
        
        Retourne: True si le bouton est cliqué
        """
    
        if self.rect.collidepoint(pos_souris):
                # Jouer le son si disponible
                if sons and type_son in sons and sons[type_son]:
                    sons[type_son].play()
                return True
        return False

def menu_difficulte(ecran, horloge, images, sons):
    """
    Menu pour choisir la difficulté.
    Retourne: "facile", "normal", "difficile", ou "menu" pour retour
    """
    largeur_bouton = 250
    hauteur_bouton = 60
    x_bouton = LARGEUR_FENETRE // 2 - largeur_bouton // 2
    
    bouton_facile = Bouton(
        x_bouton, 300, largeur_bouton, hauteur_bouton,
        "FACILE", (50, 150, 50), (80, 200, 80)
    )
    bouton_normal = Bouton(
        x_bouton, 400, largeur_bouton, hauteur_bouton,
        "NORMAL", (150, 150, 50), (200, 200, 80)
    )
    bouton_difficile = Bouton(
        x_bouton, 500, largeur_bouton, hauteur_bouton,
        "DIFFICILE", (150, 50, 50), (200, 80, 80)
    )
    bouton_retour = Bouton(
        x_bouton, 600, largeur_bouton, hauteur_bouton,
        "RETOUR", (100, 100, 100), (150, 150, 150)
    )
    
    boutons = [bouton_facile, bouton_normal, bouton_difficile, bouton_retour]
    
    while True:
        pos_souris = pygame.mouse.get_pos()
        
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"
            
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_facile.est_clique(pos_souris, sons, "clic_play"):
                    return "facile"
                elif bouton_normal.est_clique(pos_souris, sons, "clic_play"):
                    return "normal"
                elif bouton_difficile.est_clique(pos_souris, sons, "clic_play"):
                    return "difficile"
                elif bouton_retour.est_clique(pos_souris, sons, "clic_play"):
                    return "menu"
            
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu"
        
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
        
        # Affichage
        ecran.blit(images["fond"], (0, 0))
        
        # Titre
        font_titre = pygame.font.Font(None, 80)
        titre = font_titre.render("CHOISIR LA DIFFICULTÉ", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR_FENETRE // 2, 150))
        ecran.blit(titre, titre_rect)
        
        for bouton in boutons:
            bouton.dessiner(ecran)
        
        pygame.display.flip()
        horloge.tick(FPS)

def menu_accueil(ecran, horloge, images, sons):
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
                if bouton_play.est_clique(pos_souris, sons, "clic_play"):
                    return "play"
                elif bouton_score.est_clique(pos_souris, sons, "clic_play"):
                    return "score"
                elif bouton_quitter.est_clique(pos_souris, sons, "clic_bouton"):
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

def ecran_scores(ecran, horloge, images, sons):
    """Affiche l'écran des meilleurs scores."""
    bouton_retour = Bouton(
        LARGEUR_FENETRE // 2 - 125, 650, 250, 60,
        "RETOUR", (100, 100, 100), (150, 150, 150)
    )
    
    # Charger les scores
    scores = charger_scores()
    
    while True:
        pos_souris = pygame.mouse.get_pos()
        
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"
            
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.est_clique(pos_souris, sons, "clic_retour"):
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
        
        # Afficher les scores
        if scores:
            font = pygame.font.Font(None, 50)
            y_position = 200
            for i, score_data in enumerate(scores, 1):
                nom = score_data["nom"]
                score = score_data["score"]
                texte = font.render(f"{i}. {nom}: {score} pts", True, BLANC)
                texte_rect = texte.get_rect(center=(LARGEUR_FENETRE // 2, y_position))
                ecran.blit(texte, texte_rect)
                y_position += 70
        else:
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


def jouer(ecran, horloge, images, difficulte="normal"):
    """
    Lance une partie de jeu.
    
    Args:
        difficulte: "facile", "normal", ou "difficile"
    """
    # Récupérer les paramètres de difficulté
    params = DIFFICULTES[difficulte]
    FRAMES_ENTRE_SPAWN = params["frames_entre_spawn"]
    
    # Variables de jeu
    objets = []
    score = SCORE_INITIAL
    vies = NOMBRE_VIES_INITIAL
    compteur_spawn = 0
    gel_actif = False
    frames_gel_restantes = 0
    
    # Pour détecter les combos (plusieurs touches en même temps)
    touches_appuyees_ce_frame = []
    
    while True:
        # 1. GESTION DES ÉVÉNEMENTS
        touches_appuyees_ce_frame = []  # Réinitialiser chaque frame
        
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter", score
            
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu", score
                
                # Détecter les touches de jeu
                if evenement.key in TOUCHES_COLONNES:
                    colonne = TOUCHES_COLONNES.index(evenement.key)
                    touches_appuyees_ce_frame.append(colonne)
        
        # 2. TRAITER LES TOUCHES APPUYÉES (COMBOS)
        if touches_appuyees_ce_frame:
            objets_tranches = []
            
            for colonne in touches_appuyees_ce_frame:
                # Trouver les objets dans cette colonne qui sont dans la zone de frappe
                for objet in objets:
                    if objet.actif and objet.colonne == colonne:
                        # Zone de frappe : partie haute de l'écran
                        if 100 <= objet.y <= 400:
                            # BOMBE = GAME OVER
                            if objet.type_objet == "bombe":
                                return "game_over", score, "bombe"
                            
                            # GLAÇON = GEL DU TEMPS
                            elif objet.type_objet == "glacon":
                                gel_actif = True
                                frames_gel_restantes = DUREE_GEL
                                objet.actif = False
                            
                            # FRUIT = POINTS
                            elif objet.est_fruit():
                                objet.actif = False
                                objets_tranches.append(objet)
            
            # CALCUL DES POINTS SELON LES NOUVELLES RÈGLES
            nb_fruits_tranches = len(objets_tranches)
            if nb_fruits_tranches > 0:
                # +1 point par fruit
                score += nb_fruits_tranches * POINTS_PAR_FRUIT
                
                # Bonus combo : si 3 fruits ou plus en un coup
                # 3 fruits = +2, 4 fruits = +3, 5 fruits = +4, etc.
                if nb_fruits_tranches >= 3:
                    bonus = nb_fruits_tranches - 1
                    score += bonus
        
        # 3. LOGIQUE DU JEU (si pas gelé)
        if not gel_actif:
            # Spawn de nouveaux objets
            compteur_spawn += 1
            if compteur_spawn >= FRAMES_ENTRE_SPAWN:
                compteur_spawn = 0
                nouvel_objet = creer_objet_aleatoire()
                objets.append(nouvel_objet)
            
            # Mettre à jour les objets
            for objet in objets:
                objet.mettre_a_jour()
            
            # Vérifier les fruits ratés (qui sortent en bas de l'écran)
            for objet in objets[:]:  # Copie de la liste pour pouvoir modifier
                # Un fruit est raté s'il est inactif, descend et sort de l'écran
                if not objet.actif and objet.est_fruit() and objet.descend and objet.y > HAUTEUR_FENETRE:
                    # Fruit raté = perte de vie
                    vies -= 1
                    if vies <= 0:
                        return "game_over", score, "strikes"
            
            # Nettoyer les objets inactifs
            objets = [obj for obj in objets if obj.actif or (obj.y <= HAUTEUR_FENETRE + 100)]
        
        else:
            # Mode gel : décompter
            frames_gel_restantes -= 1
            if frames_gel_restantes <= 0:
                gel_actif = False
        
        # 4. AFFICHAGE
        ecran.blit(images["fond"], (0, 0))
        dessiner_colonnes(ecran)
        
        # Dessiner les objets
        for objet in objets:
            objet.dessiner(ecran, images)
        
        # Afficher le score
        font_score = pygame.font.Font(None, 50)
        score_texte = font_score.render(f"Score: {score}", True, BLANC)
        ecran.blit(score_texte, (20, 20))
        
        # Afficher les vies (cœurs)
        for i in range(vies):
            ecran.blit(images["coeur"], (LARGEUR_FENETRE - 60 - i * 50, 20))
        
        # Afficher l'indicateur de gel
        if gel_actif:
            font_gel = pygame.font.Font(None, 40)
            gel_texte = font_gel.render(" FREEZ ", True, (100, 200, 255))
            ecran.blit(gel_texte, (LARGEUR_FENETRE // 2 - 80, 20))
        
        # 5. MISE À JOUR DE L'ÉCRAN
        pygame.display.flip()
        horloge.tick(FPS)

def ecran_game_over(ecran, horloge, images, sons, score, raison):
    """
    Affiche l'écran de game over avec le score final.
    
    Args:
        score: Score final du joueur
        raison: Raison du game over ("strikes" ou "bombe")
    
    Retourne: "menu", "rejouer", ou "quitter"
    """
    # Vérifier si c'est un top score
    est_top_score = est_dans_top_scores(score)
    
    # États : "affichage" ou "saisie_nom"
    etat_game_over = "saisie_nom" if est_top_score else "affichage"
    nom_joueur = ""
    
    bouton_menu = Bouton(
        LARGEUR_FENETRE // 2 - 280, 600, 220, 60,
        "MENU", (100, 100, 100), (150, 150, 150)
    )
    bouton_rejouer = Bouton(
        LARGEUR_FENETRE // 2 + 60, 600, 220, 60,
        "REJOUER", (50, 150, 50), (80, 200, 80)
    )
    
    # Définir les dimensions de la pop-up (plus grande)
    popup_largeur = 700
    popup_hauteur = 400
    popup_x = LARGEUR_FENETRE // 2 - popup_largeur // 2
    popup_y = HAUTEUR_FENETRE // 2 - popup_hauteur // 2
    
    # Boutons pour la pop-up de saisie (plus petits et centrés dans la pop-up)
    largeur_btn_popup = 150
    hauteur_btn_popup = 45
    espacement = 30
    
    bouton_valider = Bouton(
        popup_x + (popup_largeur // 2) - largeur_btn_popup - espacement // 2,
        popup_y + popup_hauteur - 80,
        largeur_btn_popup,
        hauteur_btn_popup,
        "VALIDER",
        (50, 150, 50),
        (80, 200, 80)
    )
    bouton_skip = Bouton(
        popup_x + (popup_largeur // 2) + espacement // 2,
        popup_y + popup_hauteur - 80,
        largeur_btn_popup,
        hauteur_btn_popup,
        "PASSER",
        (150, 50, 50),
        (200, 80, 80)
    )
    
    while True:
        pos_souris = pygame.mouse.get_pos()
        
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quitter"
            
            if evenement.type == pygame.KEYDOWN:
                if etat_game_over == "saisie_nom":
                    # Saisie du nom
                    if evenement.key == pygame.K_RETURN and len(nom_joueur) > 0:
                        sauvegarder_score(nom_joueur, score)
                        etat_game_over = "affichage"
                    elif evenement.key == pygame.K_ESCAPE:
                        # Permettre de skip la saisie avec ESC
                        etat_game_over = "affichage"
                    elif evenement.key == pygame.K_BACKSPACE:
                        nom_joueur = nom_joueur[:-1]
                    elif evenement.unicode.isalnum() or evenement.unicode == " ":
                        if len(nom_joueur) < 15:
                            nom_joueur += evenement.unicode
                else:
                    # Mode affichage normal
                    if evenement.key == pygame.K_ESCAPE:
                        return "menu"
            
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if etat_game_over == "saisie_nom":
                    # Clics dans la pop-up
                    if bouton_valider.est_clique(pos_souris, sons, "clic_play") and len(nom_joueur) > 0:
                        sauvegarder_score(nom_joueur, score)
                        etat_game_over = "affichage"
                    elif bouton_skip.est_clique(pos_souris, sons, "clic_play"):
                        etat_game_over = "affichage"
                else:
                    # Clics normaux
                    if bouton_menu.est_clique(pos_souris, sons, "clic_bouton"):
                        return "menu"
                    elif bouton_rejouer.est_clique(pos_souris, sons, "clic_play"):
                        return "rejouer"
        
        # Mise à jour des survols
        if etat_game_over == "saisie_nom":
            bouton_valider.verifier_survol(pos_souris)
            bouton_skip.verifier_survol(pos_souris)
        else:
            bouton_menu.verifier_survol(pos_souris)
            bouton_rejouer.verifier_survol(pos_souris)
        
        # ===== AFFICHAGE =====
        ecran.blit(images["fond"], (0, 0))
        
        # Titre Game Over
        font_titre = pygame.font.Font(None, 100)
        titre = font_titre.render("GAME OVER", True, (255, 50, 50))
        titre_rect = titre.get_rect(center=(LARGEUR_FENETRE // 2, 150))
        ecran.blit(titre, titre_rect)
        
        # Raison du game over
        font_raison = pygame.font.Font(None, 40)
        if raison == "bombe":
            texte_raison = "Tu as touché une bombe ! "
        else:
            texte_raison = "3 fruits ratés... "
        raison_surface = font_raison.render(texte_raison, True, BLANC)
        raison_rect = raison_surface.get_rect(center=(LARGEUR_FENETRE // 2, 250))
        ecran.blit(raison_surface, raison_rect)
        
        # Score final
        font_score = pygame.font.Font(None, 60)
        score_texte = font_score.render(f"Score: {score}", True, BLANC)
        score_rect = score_texte.get_rect(center=(LARGEUR_FENETRE // 2, 350))
        ecran.blit(score_texte, score_rect)
        
        # ===== POP-UP DE SAISIE DU NOM =====
        if etat_game_over == "saisie_nom":
            # Assombrir légèrement l'arrière-plan (moins sombre)
            overlay = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE))
            overlay.set_alpha(120)  # Moins opaque (avant 180)
            overlay.fill((0, 0, 0))
            ecran.blit(overlay, (0, 0))
            
            # ===== DESSINER LA POP-UP COLORÉE =====
            # Fond principal avec dégradé violet-bleu
            for i in range(popup_hauteur):
                # Dégradé du violet au bleu
                ratio = i / popup_hauteur
                r = int(120 - ratio * 30)  # 120 -> 90
                g = int(80 + ratio * 100)  # 80 -> 180
                b = int(200 + ratio * 55)  # 200 -> 255
                
                ligne = pygame.Surface((popup_largeur, 1))
                ligne.fill((r, g, b))
                ligne.set_alpha(230)  # Légère transparence
                ecran.blit(ligne, (popup_x, popup_y + i))
            
            # Bordure colorée arc-en-ciel (effet brillant)
            # Bordure extérieure dorée
            pygame.draw.rect(ecran, (255, 215, 0), 
                        (popup_x - 3, popup_y - 3, popup_largeur + 6, popup_hauteur + 6), 
                        5, border_radius=20)
            
            # Bordure intérieure rose/violet
            pygame.draw.rect(ecran, (255, 105, 180), 
                        (popup_x, popup_y, popup_largeur, popup_hauteur), 
                        3, border_radius=18)
            
            # ===== CONTENU DE LA POP-UP =====
            
            # Titre de la pop-up
            font_popup_titre = pygame.font.Font(None, 55)
            titre_popup = font_popup_titre.render(" NOUVEAU RECORD ! ", True, (255, 255, 100))
            titre_popup_rect = titre_popup.get_rect(center=(popup_x + popup_largeur // 2, popup_y + 60))
            ecran.blit(titre_popup, titre_popup_rect)
            
            # Sous-titre avec le score
            font_sous_titre = pygame.font.Font(None, 40)
            sous_titre = font_sous_titre.render(f"Tu as marqué {score} points !", True, (255, 255, 255))
            sous_titre_rect = sous_titre.get_rect(center=(popup_x + popup_largeur // 2, popup_y + 110))
            ecran.blit(sous_titre, sous_titre_rect)
            
            # Instruction
            font_instruction = pygame.font.Font(None, 35)
            instruction = font_instruction.render("Entre ton nom :", True, (255, 255, 255))
            instruction_rect = instruction.get_rect(center=(popup_x + popup_largeur // 2, popup_y + 170))
            ecran.blit(instruction, instruction_rect)
            
            # Champ de saisie stylisé
            champ_largeur = 500
            champ_hauteur = 55
            champ_x = popup_x + (popup_largeur - champ_largeur) // 2
            champ_y = popup_y + 210
            
            # Fond du champ avec effet brillant
            pygame.draw.rect(ecran, (255, 255, 255), 
                        (champ_x, champ_y, champ_largeur, champ_hauteur), 
                        border_radius=12)
            pygame.draw.rect(ecran, (100, 200, 255), 
                        (champ_x, champ_y, champ_largeur, champ_hauteur), 
                        3, border_radius=12)
            
            # Texte saisi avec curseur clignotant
            font_saisie = pygame.font.Font(None, 45)
            
            # Curseur clignotant (toutes les 500ms)
            curseur = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            texte_affiche = nom_joueur + curseur if len(nom_joueur) < 15 else nom_joueur
            
            # Couleur du texte : noir sur fond blanc
            saisie_surface = font_saisie.render(texte_affiche, True, (50, 50, 50))
            saisie_rect = saisie_surface.get_rect(center=(champ_x + champ_largeur // 2, champ_y + champ_hauteur // 2))
            ecran.blit(saisie_surface, saisie_rect)
            
            # Placeholder si vide
            if len(nom_joueur) == 0:
                font_placeholder = pygame.font.Font(None, 35)
                placeholder = font_placeholder.render("Tape ton nom ici...", True, (150, 150, 150))
                placeholder_rect = placeholder.get_rect(center=(champ_x + champ_largeur // 2, champ_y + champ_hauteur // 2))
                ecran.blit(placeholder, placeholder_rect)
            
            # Boutons
            bouton_valider.dessiner(ecran)
            bouton_skip.dessiner(ecran)
            
            # Hint ESC en bas
            font_hint = pygame.font.Font(None, 25)
            hint = font_hint.render("(Appuie sur ESC pour passer)", True, (200, 200, 255))
            hint_rect = hint.get_rect(center=(popup_x + popup_largeur // 2, popup_y + popup_hauteur - 25))
            ecran.blit(hint, hint_rect)
        
        else:
            # Mode affichage normal - montrer les boutons
            bouton_menu.dessiner(ecran)
            bouton_rejouer.dessiner(ecran)
        
        pygame.display.flip()
        horloge.tick(FPS)


# ============================================
# BOUCLE PRINCIPALE
# ============================================

def boucle_principale():
    """Boucle principale qui gère les différents états du jeu."""
    ecran, horloge = initialiser_pygame()
    images = charger_toutes_les_images()
    sons = charger_sons()

    etat = "menu"
    difficulte_choisie = "normal"
    score_final = 0
    raison_game_over = "strikes"
    
    while etat != "quitter":
        if etat == "menu":
            etat = menu_accueil(ecran, horloge, images,sons)
        
        elif etat == "play":
            # Choisir la difficulté
            etat = menu_difficulte(ecran, horloge, images,sons)
            if etat in ["facile", "normal", "difficile"]:
                difficulte_choisie = etat
                resultat = jouer(ecran, horloge, images, difficulte_choisie)
                
                if len(resultat) == 2:
                    etat, score_final = resultat
                else:
                    etat, score_final, raison_game_over = resultat
        
        elif etat == "game_over":
            etat = ecran_game_over(ecran, horloge, images, sons, score_final, raison_game_over)
            if etat == "rejouer":
                resultat = jouer(ecran, horloge, images, difficulte_choisie)
                if len(resultat) == 2:
                    etat, score_final = resultat
                else:
                    etat, score_final, raison_game_over = resultat
        
        elif etat == "score":
            etat = ecran_scores(ecran, horloge, images,sons)
    
    pygame.quit()


# Point d'entrée du programme
if __name__ == "__main__":
    boucle_principale()
