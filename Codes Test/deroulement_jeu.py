import pygame
import sys


pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de tactique tour par tour")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


font = pygame.font.Font(None, 36)

def afficher_texte(text, x, y, couleur=BLACK, centrer=False):
    text_surface = font.render(text, True, couleur)
    text_rect = text_surface.get_rect()
    if centrer:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def choix_mode():
    modes = ["Assassinat", "Traversée de la map", "Capture du drapeau"]
    selection = 0

    while True:
        screen.fill(WHITE)
        afficher_texte("Choisissez un mode de jeu :", SCREEN_WIDTH // 2, 50, BLACK, centrer=True)
        
        # Afficher les modes de jeu
        for i, mode in enumerate(modes):
            couleur = BLUE if i == selection else BLACK
            afficher_texte(mode, SCREEN_WIDTH // 2, 150 + i * 50, couleur, centrer=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    return modes[selection]

def demander_nombre_tours():
    nombre_tours = 10
    while True:
        screen.fill(WHITE)
        afficher_texte(f"Fixez le nombre de tours : {nombre_tours}", SCREEN_WIDTH // 2, 200, BLACK, centrer=True)
        afficher_texte("Utilisez les flèches pour modifier. Appuyez sur Entrée pour valider.", SCREEN_WIDTH // 2, 300, BLACK, centrer=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    nombre_tours += 1
                elif event.key == pygame.K_DOWN and nombre_tours > 1:
                    nombre_tours -= 1
                elif event.key == pygame.K_RETURN:
                    return nombre_tours

def afficher_phase(tour, phase):
    screen.fill(WHITE)
    afficher_texte(f"Tour {tour} - Phase : {phase}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED, centrer=True)
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    mode = choix_mode()
    nombre_tours = demander_nombre_tours()

    print(f"Mode choisi : {mode}")
    print(f"Nombre de tours : {nombre_tours}")

    tour = 1
    phases = ["Mouvement", "Tir/Magie", "Combat"]

    # Boucle de jeu principale
    while tour <= nombre_tours:
        for phase in phases:
            afficher_phase(tour, phase)

            # Logique de la phase ici (vide pour l'instant)
            pygame.time.wait(1000)  # Simule une pause entre phases

        tour += 1

    screen.fill(WHITE)
    afficher_texte("Fin du jeu !", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GREEN, centrer=True)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()

