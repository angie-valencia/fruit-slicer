# ============================================
# FRUIT NINJA - MODE MIDI
# Version alternative avec musique MIDI
# ============================================

import pygame
import os
import random
from constantes import *
from initialisation import initialiser_pygame, charger_toutes_les_images
from logique_midi import ObjetMIDI  # Utilise la nouvelle classe
from audio_analysis import AnalyseurMIDI
from sauvegarde import charger_scores, sauvegarder_score  # Garde sauvegarde.py actuel

# --- UTILITAIRES DE POLICE ---
def obtenir_font(taille):
    """
    Utilise la police par défaut (garde ta police actuelle).
    """
    return pygame.font.Font(None, taille)  # Police par défaut pygame

def dessiner_texte_centre(ecran, texte, taille, y, couleur=BLANC):
    font = obtenir_font(taille)
    surf = font.render(texte, True, couleur)
    rect = surf.get_rect(center=(LARGEUR_FENETRE // 2, y))
    ecran.blit(surf, rect)
    return rect

# --- ÉCRAN DES SCORES (VERSION POP-UP) ---
def menu_scores(ecran, horloge, images):
    """
    Menu des scores avec pop-up style et fond semi-transparent.
    """
    # Capturer l'écran actuel pour l'effet de fond
    fond_capture = ecran.copy()
    
    # Créer une surface semi-transparente pour l'overlay
    overlay = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    overlay.set_alpha(180)  # Transparence (0=transparent, 255=opaque)
    overlay.fill((10, 20, 50))  # Bleu foncé
    
    # Dimensions de la pop-up
    popup_largeur = 800
    popup_hauteur = 600
    popup_x = (LARGEUR_FENETRE - popup_largeur) // 2
    popup_y = (HAUTEUR_FENETRE - popup_hauteur) // 2
    
    # Couleurs
    couleur_popup = (30, 60, 120)  # Bleu
    couleur_bordure = (100, 150, 255)  # Bleu clair
    couleur_titre = (255, 255, 100)  # Jaune
    couleur_texte = (255, 255, 255)  # Blanc
    couleur_instructions = (150, 200, 255)  # Bleu clair
    
    # Animation d'entrée
    animation_progress = 0
    
    while True:
        # Dessiner le fond original
        ecran.blit(fond_capture, (0, 0))
        
        # Dessiner l'overlay semi-transparent
        ecran.blit(overlay, (0, 0))
        
        # Animation de la pop-up (zoom in)
        if animation_progress < 1.0:
            animation_progress += 0.05
            scale = animation_progress
        else:
            scale = 1.0
        
        # Calculer les dimensions avec l'animation
        current_width = int(popup_largeur * scale)
        current_height = int(popup_hauteur * scale)
        current_x = popup_x + (popup_largeur - current_width) // 2
        current_y = popup_y + (popup_hauteur - current_height) // 2
        
        # Dessiner la pop-up principale
        popup_rect = pygame.Rect(current_x, current_y, current_width, current_height)
        
        # Ombre portée (effet de profondeur)
        shadow_rect = popup_rect.copy()
        shadow_rect.x += 10
        shadow_rect.y += 10
        shadow_surface = pygame.Surface((current_width, current_height))
        shadow_surface.set_alpha(100)
        shadow_surface.fill((0, 0, 0))
        ecran.blit(shadow_surface, shadow_rect.topleft)
        
        # Fond de la pop-up
        pygame.draw.rect(ecran, couleur_popup, popup_rect, border_radius=20)
        
        # Bordure brillante
        pygame.draw.rect(ecran, couleur_bordure, popup_rect, 5, border_radius=20)
        
        # Double bordure pour l'effet
        inner_rect = popup_rect.inflate(-10, -10)
        pygame.draw.rect(ecran, couleur_bordure, inner_rect, 2, border_radius=15)
        
        # Afficher le contenu seulement si l'animation est terminée
        if animation_progress >= 1.0:
            # TITRE
            font_titre = obtenir_font(70)
            titre_surf = font_titre.render("TOP 5 SCORES", True, couleur_titre)
            titre_rect = titre_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 60))
            ecran.blit(titre_surf, titre_rect)
            
            # Ligne de séparation
            ligne_y = popup_y + 110
            pygame.draw.line(ecran, couleur_bordure, 
                        (popup_x + 50, ligne_y), 
                        (popup_x + popup_largeur - 50, ligne_y), 3)
            
            # SCORES
            scores = charger_scores()
            
            if not scores:
                # Message si aucun score
                font_message = obtenir_font(40)
                message_surf = font_message.render("Aucun score enregistre", True, couleur_texte)
                message_rect = message_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 300))
                ecran.blit(message_surf, message_rect)
            else:
                # Afficher les scores avec style
                for i, score_data in enumerate(scores):
                    nom = score_data.get("nom", "???")
                    score = score_data.get("score", 0)
                    
                    # Position Y pour chaque ligne
                    y_pos = popup_y + 160 + (i * 80)
                    
                    # Fond de la ligne (alternance de couleurs)
                    if i % 2 == 0:
                        ligne_bg = pygame.Rect(popup_x + 40, y_pos - 5, popup_largeur - 80, 70)
                        pygame.draw.rect(ecran, (40, 70, 130), ligne_bg, border_radius=10)
                    
                    # Rang
                    font_rang = obtenir_font(45)
                    rang_surf = font_rang.render(f"#{i+1}", True, couleur_bordure)
                    ecran.blit(rang_surf, (popup_x + 70, y_pos + 15))
                    
                    # Nom du joueur
                    font_nom = obtenir_font(50)
                    nom_surf = font_nom.render(nom, True, couleur_texte)
                    ecran.blit(nom_surf, (popup_x + 180, y_pos + 15))
                    
                    # Points de séparation
                    font_dots = obtenir_font(40)
                    dots_surf = font_dots.render("...", True, couleur_bordure)
                    ecran.blit(dots_surf, (popup_x + 380, y_pos + 20))
                    
                    # Score avec effet brillant
                    font_score = obtenir_font(55)
                    score_surf = font_score.render(str(score), True, (255, 215, 0))  # Or
                    score_rect = score_surf.get_rect(right=popup_x + popup_largeur - 70, centery=y_pos + 35)
                    ecran.blit(score_surf, score_rect)
            
            # INSTRUCTIONS EN BAS
            instructions_y = popup_y + popup_hauteur - 60
            
            # Fond des instructions
            instructions_bg = pygame.Rect(popup_x + 50, instructions_y - 10, popup_largeur - 100, 50)
            pygame.draw.rect(ecran, (20, 40, 80), instructions_bg, border_radius=10)
            pygame.draw.rect(ecran, couleur_bordure, instructions_bg, 2, border_radius=10)
            
            font_instructions = obtenir_font(35)
            instructions_surf = font_instructions.render("Appuyez sur ESPACE ou ECHAP pour continuer", True, couleur_instructions)
            instructions_rect = instructions_surf.get_rect(center=(LARGEUR_FENETRE // 2, instructions_y + 15))
            ecran.blit(instructions_surf, instructions_rect)
        
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            if event.type == pygame.KEYDOWN:
                # Plusieurs touches pour sortir
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
                    return "menu"
        
        horloge.tick(FPS)

# --- MENU ACCUEIL MODE MIDI ---
def menu_accueil_midi(ecran, horloge, images, musique_actuelle):
    """
    Menu avec navigation clavier (garde tes images actuelles).
    """
    options = ["START EASY", "START HARD", "HALL OF FAME", "BACK TO CLASSIC", "EXIT"]
    index_sel = 0
    MARGE_GAUCHE = 100 

    while True:
        # UTILISE TES IMAGES ACTUELLES
        ecran.blit(images.get("image_accueil", images["fond"]), (0, 0))
        
        # TITRE AVEC TA POLICE ACTUELLE
        font_titre = obtenir_font(100)
        titre_surf = font_titre.render("FRUIT SLICER MIDI", True, BLANC)
        ecran.blit(titre_surf, (MARGE_GAUCHE, 80))

        # OPTIONS AVEC SURBRILLANCE ET ALIGNEMENT GAUCHE
        for i, texte in enumerate(options):
            est_sel = (i == index_sel)
            taille = 75 if est_sel else 55
            couleur = JAUNE if est_sel else BLANC
            
            font_option = obtenir_font(taille)
            
            x_pos = MARGE_GAUCHE + (30 if est_sel else 0)
            y_pos = 300 + (i * 70)
            
            txt_final = f"> {texte}" if est_sel else texte
            opt_surf = font_option.render(txt_final, True, couleur)
            ecran.blit(opt_surf, (x_pos, y_pos))

        # INFOS MUSIQUE
        info = LISTE_MUSIQUES[musique_actuelle]
        font_info = obtenir_font(30)
        music_surf = font_info.render(f"TRACK: {info['nom']} (Press M)", True, BLANC)
        ecran.blit(music_surf, (MARGE_GAUCHE, 700))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return "quitter", musique_actuelle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    index_sel = (index_sel - 1) % len(options)
                elif event.key == pygame.K_DOWN: 
                    index_sel = (index_sel + 1) % len(options)
                elif event.key == pygame.K_m: 
                    musique_actuelle = "2" if musique_actuelle == "1" else "1"
                elif event.key == pygame.K_RETURN:
                    choix = options[index_sel]
                    if choix == "START EASY": 
                        return "jouer_facile", musique_actuelle
                    if choix == "START HARD": 
                        return "jouer_difficile", musique_actuelle
                    if choix == "HALL OF FAME": 
                        return "scores", musique_actuelle
                    if choix == "BACK TO CLASSIC":
                        return "classic", musique_actuelle
                    if choix == "EXIT": 
                        return "quitter", musique_actuelle
        horloge.tick(FPS)

# --- ÉCRAN DE FIN DE PARTIE AVEC POP-UP ---
def ecran_fin_partie(ecran, horloge, images, score):
    """
    Écran de fin de partie avec saisie du nom (style pop-up).
    """
    pseudo = ""
    
    # Capturer l'écran actuel
    fond_capture = ecran.copy()
    
    # Overlay semi-transparent
    overlay = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    overlay.set_alpha(180)
    overlay.fill((20, 10, 30))  # Violet/rouge foncé
    
    # Dimensions de la pop-up
    popup_largeur = 700
    popup_hauteur = 500
    popup_x = (LARGEUR_FENETRE - popup_largeur) // 2
    popup_y = (HAUTEUR_FENETRE - popup_hauteur) // 2
    
    # Animation d'entrée
    animation_progress = 0
    
    while True:
        # Fond + overlay
        ecran.blit(fond_capture, (0, 0))
        ecran.blit(overlay, (0, 0))
        
        # Animation
        if animation_progress < 1.0:
            animation_progress += 0.05
            scale = animation_progress
        else:
            scale = 1.0
        
        # Calculer dimensions animées
        current_width = int(popup_largeur * scale)
        current_height = int(popup_hauteur * scale)
        current_x = popup_x + (popup_largeur - current_width) // 2
        current_y = popup_y + (popup_hauteur - current_height) // 2
        
        # Pop-up
        popup_rect = pygame.Rect(current_x, current_y, current_width, current_height)
        
        # Ombre
        shadow_rect = popup_rect.copy()
        shadow_rect.x += 10
        shadow_rect.y += 10
        shadow_surface = pygame.Surface((current_width, current_height))
        shadow_surface.set_alpha(100)
        shadow_surface.fill((0, 0, 0))
        ecran.blit(shadow_surface, shadow_rect.topleft)
        
        # Fond de la pop-up
        pygame.draw.rect(ecran, (60, 30, 80), popup_rect, border_radius=20)
        
        # Bordures
        pygame.draw.rect(ecran, (150, 100, 200), popup_rect, 5, border_radius=20)
        inner_rect = popup_rect.inflate(-10, -10)
        pygame.draw.rect(ecran, (150, 100, 200), inner_rect, 2, border_radius=15)
        
        # Contenu (seulement si animation terminée)
        if animation_progress >= 1.0:
            # TITRE
            font_titre = obtenir_font(70)
            titre_surf = font_titre.render("PARTIE TERMINEE !", True, ROUGE)
            titre_rect = titre_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 60))
            ecran.blit(titre_surf, titre_rect)
            
            # Ligne de séparation
            ligne_y = popup_y + 110
            pygame.draw.line(ecran, (150, 100, 200), 
                        (popup_x + 50, ligne_y), 
                        (popup_x + popup_largeur - 50, ligne_y), 3)
            
            # SCORE
            font_score_label = obtenir_font(40)
            label_surf = font_score_label.render("VOTRE SCORE :", True, BLANC)
            label_rect = label_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 160))
            ecran.blit(label_surf, label_rect)
            
            # Score en gros (avec effet or)
            font_score = obtenir_font(80)
            score_surf = font_score.render(str(score), True, (255, 215, 0))  # Or
            score_rect = score_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 220))
            ecran.blit(score_surf, score_rect)
            
            # SAISIE DU NOM
            font_nom_label = obtenir_font(35)
            nom_label_surf = font_nom_label.render("ENTREZ VOTRE NOM (3 LETTRES) :", True, JAUNE)
            nom_label_rect = nom_label_surf.get_rect(center=(LARGEUR_FENETRE // 2, popup_y + 290))
            ecran.blit(nom_label_surf, nom_label_rect)
            
            # Champ de saisie
            champ_largeur = 300
            champ_hauteur = 70
            champ_x = (LARGEUR_FENETRE - champ_largeur) // 2
            champ_y = popup_y + 340
            champ_rect = pygame.Rect(champ_x, champ_y, champ_largeur, champ_hauteur)
            
            # Fond du champ
            pygame.draw.rect(ecran, (40, 20, 60), champ_rect, border_radius=10)
            pygame.draw.rect(ecran, (200, 150, 255), champ_rect, 3, border_radius=10)
            
            # Texte saisi avec underscores
            font_input = obtenir_font(60)
            texte_affiche = pseudo + "_" * (3 - len(pseudo))
            input_surf = font_input.render(texte_affiche, True, VERT)
            input_rect = input_surf.get_rect(center=champ_rect.center)
            ecran.blit(input_surf, input_rect)
            
            # Instructions
            instructions_y = popup_y + popup_hauteur - 50
            font_instructions = obtenir_font(30)
            
            if len(pseudo) > 0:
                instructions_text = "Appuyez sur ENTREE pour valider"
                instructions_color = (100, 255, 100)  # Vert
            else:
                instructions_text = "Tapez votre nom avec le clavier"
                instructions_color = (150, 200, 255)  # Bleu clair
            
            instructions_surf = font_instructions.render(instructions_text, True, instructions_color)
            instructions_rect = instructions_surf.get_rect(center=(LARGEUR_FENETRE // 2, instructions_y))
            ecran.blit(instructions_surf, instructions_rect)
        
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(pseudo) > 0:
                    # Sauvegarder le score
                    sauvegarder_score(pseudo, score)
                    return "menu"
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Sortir sans sauvegarder
                    return "menu"
                elif len(pseudo) < 3 and event.unicode.isalpha():
                    pseudo += event.unicode.upper()
        
        horloge.tick(FPS)

# --- BOUCLE DE JEU MODE MIDI ---
def jouer_midi(ecran, horloge, images, mode, musique_id):
    """
    Boucle de jeu avec système MIDI.
    """
    # Chargement du son Toasty (optionnel, peut ne pas exister)
    son_toasty = None
    if os.path.exists("toasty.wav"):
        try:
            son_toasty = pygame.mixer.Sound("toasty.wav")
        except:
            print("Fichier toasty.wav non chargé.")

    objets = []
    effets_coupes = [] 
    vies = 3
    score = 0
    combo = 0
    compteur_objets = 0 
    timer_toasty = 0
    font_ui = obtenir_font(50)
    font_lettre = obtenir_font(45)   
    
    m_info = LISTE_MUSIQUES[musique_id]
    
    try:
        analyseur = AnalyseurMIDI(f"{m_info['fichier']}.mid")
        pygame.mixer.music.load(f"{m_info['fichier']}.wav")
        pygame.mixer.music.play()
        temps_debut = pygame.time.get_ticks()
    except Exception as e:
        print(f"Erreur chargement MIDI : {e}")
        return "menu"

    fruits_a_spawner = analyseur.get_fruits_precalcules(anticipation=1.8)
    prochain_idx = 0

    while vies > 0:
        temps_ecoule = (pygame.time.get_ticks() - temps_debut) / 1000.0 - m_info["offset"]
        
        # UTILISE TON FOND ACTUEL
        ecran.blit(images["fond"], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "menu"
                
                # Détection des touches
                touche_trouvee = False
                for obj in sorted(objets, key=lambda o: o.y, reverse=True):
                    if event.key == obj.touche_code and obj.actif:
                        obj.actif = False
                        touche_trouvee = True
                        
                        # Effets visuels avec TES IMAGES
                        cle_image = f"{obj.type_objet}_coupee" if f"{obj.type_objet}_coupee" in images else obj.type_objet
                        effets_coupes.append({"cle": cle_image, "pos": [obj.x, obj.y], "timer": 40})
                        
                        if obj.type_objet == "bombe":
                            vies -= 1
                            combo = 0
                        elif obj.type_objet == "coeur":
                            vies = min(vies + 1, 5)
                        else:
                            combo += 1
                            score += (3 if combo >= 10 else 1)
                            # Déclenchement Toasty
                            if combo == 10:
                                timer_toasty = 60
                                if son_toasty: 
                                    son_toasty.play()
                        break
                        
                if not touche_trouvee: 
                    combo = 0

        # SPAWN LOGIC : 1 bonus/malus tous les 5 objets
        while prochain_idx < len(fruits_a_spawner) and fruits_a_spawner[prochain_idx]['temps_spawn'] <= temps_ecoule:
            compteur_objets += 1
            if compteur_objets % 5 == 0:
                type_obj = random.choice(["bombe", "coeur"])
            else:
                type_obj = random.choice(LISTE_FRUITS)
            
            # Utilise ObjetMIDI avec le mode
            objets.append(ObjetMIDI(fruits_a_spawner[prochain_idx]['colonne'], type_obj, mode))
            prochain_idx += 1

        # Mises à jour
        nouveaux_objets = []
        for obj in objets:
            obj.mettre_a_jour()
            if obj.actif and obj.y <= HAUTEUR_FENETRE:
                obj.dessiner(ecran, images, font_lettre)
                nouveaux_objets.append(obj)
            elif obj.actif: 
                if obj.type_objet not in ["bombe", "coeur"]:
                    vies -= 1
                    combo = 0
        objets = nouveaux_objets

        # Effets de coupe
        for effet in effets_coupes[:]:
            effet["pos"][1] += 2 
            ecran.blit(images[effet["cle"]], effet["pos"])
            effet["timer"] -= 1
            if effet["timer"] <= 0: 
                effets_coupes.remove(effet)

        # Affichage Toasty (si image existe)
        if timer_toasty > 0 and "toasty" in images:
            ecran.blit(images["toasty"], (LARGEUR_FENETRE - 250, HAUTEUR_FENETRE - 250))
            timer_toasty -= 1

        # UI
        ecran.blit(font_ui.render(f"SCORE: {score}", True, BLANC), (20, 20))
        ecran.blit(font_ui.render(f"VIES: {vies}", True, ROUGE), (20, 70))
        if combo >= 3:
            ecran.blit(font_ui.render(f"COMBO: {combo}", True, JAUNE), (20, 120))

        # Fin de la musique
        if prochain_idx >= len(fruits_a_spawner) and len(objets) == 0:
            break

        pygame.display.flip()
        horloge.tick(FPS)

    pygame.mixer.music.stop()
    return ecran_fin_partie(ecran, horloge, images, score)

# --- BOUCLE PRINCIPALE ---
def boucle_principale_midi():
    """
    Boucle principale du mode MIDI.
    """
    pygame.init() 
    pygame.mixer.init()
    ecran, horloge = initialiser_pygame()
    images = charger_toutes_les_images()
    etat = "menu"
    musique_id = "1"
    
    while etat != "quitter":
        if etat == "menu":
            etat, musique_id = menu_accueil_midi(ecran, horloge, images, musique_id)
        elif etat == "scores":
            etat = menu_scores(ecran, horloge, images)
        elif etat == "classic":
            # Retourner au main.py classique
            print("Lancer main.py pour le mode classique")
            etat = "quitter"
        elif "jouer" in etat:
            mode_jeu = "facile" if "facile" in etat else "difficile"
            etat = jouer_midi(ecran, horloge, images, mode_jeu, musique_id)
    
    pygame.quit()

if __name__ == "__main__":
    boucle_principale_midi()