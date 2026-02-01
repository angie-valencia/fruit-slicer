# ============================================
# LAUNCHER - CHOIX DE LA VERSION
# ============================================

import pygame
import sys

def menu_launcher():
    """
    Menu pour choisir entre mode classique et mode MIDI.
    """
    pygame.init()
    ecran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Fruit Slicer - Launcher")
    horloge = pygame.time.Clock()
    
    font_titre = pygame.font.Font(None, 80)
    font_option = pygame.font.Font(None, 50)
    
    options = ["MODE CLASSIQUE", "MODE MIDI", "QUITTER"]
    selection = 0
    
    while True:
        ecran.fill((20, 20, 40))
        
        # Titre
        titre = font_titre.render("FRUIT SLICER", True, (255, 255, 255))
        ecran.blit(titre, (800//2 - titre.get_width()//2, 100))
        
        # Options
        for i, option in enumerate(options):
            couleur = (255, 255, 0) if i == selection else (255, 255, 255)
            texte = font_option.render(f"{'> ' if i == selection else ''}{option}", True, couleur)
            ecran.blit(texte, (800//2 - texte.get_width()//2, 250 + i * 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selection == 0:  # Mode classique
                        pygame.quit()
                        import main
                        main.boucle_principale()
                        return
                    elif selection == 1:  # Mode MIDI
                        pygame.quit()
                        import main_midi
                        main_midi.boucle_principale_midi()
                        return
                    elif selection == 2:  # Quitter
                        pygame.quit()
                        sys.exit()
        
        horloge.tick(60)

if __name__ == "__main__":
    menu_launcher()