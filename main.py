import pygame
import os
import random
from constantes import *
from initialisation import initialiser_pygame, charger_toutes_les_images
from logique import Objet 
from audio_analysis import AnalyseurMIDI
from scores import charger_scores, sauver_score

# --- UTILITAIRES DE POLICE ---
def obtenir_font(taille):
    """Charge la police rock.ttf ou utilise la police par défaut en cas d'erreur."""
    try:
        # Assure-toi que le fichier s'appelle exactement rock.ttf à la racine
        return pygame.font.Font("rock.ttf", taille)
    except:
        return pygame.font.Font(None, taille)

def dessiner_texte_centre(ecran, texte, taille, y, couleur=BLANC):
    font = obtenir_font(taille)
    surf = font.render(texte, True, couleur)
    rect = surf.get_rect(center=(LARGEUR_FENETRE // 2, y))
    ecran.blit(surf, rect)
    return rect

# --- ÉCRANS ANNEXES ---
def menu_scores(ecran, horloge, images):
    while True:
        ecran.blit(images["fond"], (0, 0))
        dessiner_texte_centre(ecran, "TOP 5 SCORES", 80, 100, JAUNE)
        scores = charger_scores()
        if not scores:
            dessiner_texte_centre(ecran, "AUCUN SCORE ENCORE", 40, 300, BLANC)
        else:
            for i, (pseudo, score) in enumerate(scores):
                texte = f"{i+1}. {pseudo} : {score}"
                dessiner_texte_centre(ecran, texte, 50, 200 + (i * 60), BLANC)
        dessiner_texte_centre(ecran, "ECHAP POUR RETOURNER AU MENU", 30, 700, BLEU)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "menu"
        horloge.tick(FPS)

def ecran_fin_partie(ecran, horloge, images, score):
    pseudo = ""
    while True:
        ecran.blit(images["fond"], (0, 0))
        dessiner_texte_centre(ecran, "PARTIE TERMINEE !", 80, 150, ROUGE)
        dessiner_texte_centre(ecran, f"SCORE : {score}", 60, 250, BLANC)
        dessiner_texte_centre(ecran, "ENTREZ VOTRE NOM (3 LETTRES) :", 40, 350, JAUNE)
        dessiner_texte_centre(ecran, pseudo + "_" * (3 - len(pseudo)), 100, 450, VERT)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(pseudo) > 0:
                    sauver_score(pseudo, score)
                    return "menu"
                elif event.key == pygame.K_BACKSPACE: pseudo = pseudo[:-1]
                elif len(pseudo) < 3 and event.unicode.isalpha(): pseudo += event.unicode.upper()
        horloge.tick(FPS)

# --- MENU ACCUEIL (ROCK STYLE) ---
def menu_accueil(ecran, horloge, images, musique_actuelle):
    options = ["START EASY", "START HARD", "HALL OF FAME", "EXIT"]
    index_sel = 0
    MARGE_GAUCHE = 100 

    while True:
        ecran.blit(images.get("image_accueil", images["fond"]), (0, 0))
        
        # TITRE AVEC POLICE ROCK
        font_titre = obtenir_font(100)
        titre_surf = font_titre.render("FRUIT SLICER", True, BLANC)
        ecran.blit(titre_surf, (MARGE_GAUCHE, 80))

        # OPTIONS AVEC SURBRILLANCE ET ALIGNEMENT GAUCHE
        for i, texte in enumerate(options):
            est_sel = (i == index_sel)
            taille = 75 if est_sel else 55
            couleur = JAUNE if est_sel else BLANC
            
            font_option = obtenir_font(taille)
            
            x_pos = MARGE_GAUCHE + (30 if est_sel else 0)
            y_pos = 300 + (i * 90)
            
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
            if event.type == pygame.QUIT: return "quitter", musique_actuelle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: index_sel = (index_sel - 1) % len(options)
                elif event.key == pygame.K_DOWN: index_sel = (index_sel + 1) % len(options)
                elif event.key == pygame.K_m: musique_actuelle = "2" if musique_actuelle == "1" else "1"
                elif event.key == pygame.K_RETURN:
                    choix = options[index_sel]
                    if choix == "START EASY": return "jouer_facile", musique_actuelle
                    if choix == "START HARD": return "jouer_difficile", musique_actuelle
                    if choix == "HALL OF FAME": return "scores", musique_actuelle
                    if choix == "EXIT": return "quitter", musique_actuelle
        horloge.tick(FPS)

# --- BOUCLE DE JEU ---
def jouer(ecran, horloge, images, mode, musique_id):
    # Chargement du son Toasty (à la racine)
    son_toasty = None
    try:
        son_toasty = pygame.mixer.Sound("toasty.wav")
    except:
        print("Fichier toasty.wav introuvable à la racine.")

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
        print(f"Erreur : {e}")
        return "menu"

    fruits_a_spawner = analyseur.get_fruits_precalcules(anticipation=1.8)
    prochain_idx = 0

    while vies > 0:
        temps_ecoule = (pygame.time.get_ticks() - temps_debut) / 1000.0 - m_info["offset"]
        ecran.blit(images["fond"], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "menu"
                
                touche_trouvee = False
                for obj in sorted(objets, key=lambda o: o.y, reverse=True):
                    if event.key == obj.touche_code and obj.actif:
                        obj.actif = False
                        touche_trouvee = True
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
                                if son_toasty: son_toasty.play()
                        break
                if not touche_trouvee: combo = 0

        # SPAWN LOGIC : 1 bonus/malus tous les 5 objets
        while prochain_idx < len(fruits_a_spawner) and fruits_a_spawner[prochain_idx]['temps_spawn'] <= temps_ecoule:
            compteur_objets += 1
            if compteur_objets % 5 == 0:
                type_obj = random.choice(["bombe", "coeur"])
            else:
                type_obj = random.choice(LISTE_FRUITS)
            objets.append(Objet(fruits_a_spawner[prochain_idx]['colonne'], type_obj, mode))
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

        for effet in effets_coupes[:]:
            effet["pos"][1] += 2 
            ecran.blit(images[effet["cle"]], effet["pos"])
            effet["timer"] -= 1
            if effet["timer"] <= 0: effets_coupes.remove(effet)

        # Affichage Toasty
        if timer_toasty > 0:
            ecran.blit(images["toasty"], (LARGEUR_FENETRE - 250, HAUTEUR_FENETRE - 250))
            timer_toasty -= 1

        # UI
        ecran.blit(font_ui.render(f"SCORE: {score}", True, BLANC), (20, 20))
        ecran.blit(font_ui.render(f"VIES: {vies}", True, ROUGE), (20, 70))
        if combo >= 3:
            ecran.blit(font_ui.render(f"COMBO: {combo}", True, JAUNE), (20, 120))

        if prochain_idx >= len(fruits_a_spawner) and len(objets) == 0:
            break

        pygame.display.flip()
        horloge.tick(FPS)

    pygame.mixer.music.stop()
    return ecran_fin_partie(ecran, horloge, images, score)

def boucle_principale():
    pygame.init() 
    pygame.mixer.init()
    ecran, horloge = initialiser_pygame()
    images = charger_toutes_les_images()
    etat = "menu"
    musique_id = "1"
    
    while etat != "quitter":
        if etat == "menu":
            etat, musique_id = menu_accueil(ecran, horloge, images, musique_id)
        elif etat == "scores":
            etat = menu_scores(ecran, horloge, images)
        elif "jouer" in etat:
            mode_jeu = "facile" if "facile" in etat else "difficile"
            etat = jouer(ecran, horloge, images, mode_jeu, musique_id)
    pygame.quit()

if __name__ == "__main__":
    boucle_principale()