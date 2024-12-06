import pygame
import random
from unit import *
from Classes_personnages import *
from Guerrier import *
from unit_new import *


GRAY = [200,200,200]

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        #x, y,mouvement,combat,tir,force,defense,attaque,vie,team
        self.screen = screen
        self.player_units = []

        self.enemy_units = [Unit(6, 6, 1, 4, 4 , 4 , 5 , 2 , 10 , 'enemy'),
                            Unit(6, 5, 1, 4, 4 , 4 , 5 , 2 , 10 , 'enemy')]

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            print(type(selected_unit))
            i = 0 
            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                            i += 1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                            i += 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                            i += 1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                            i += 1
                        
                        selected_unit.move(dx, dy)
                        self.flip_display()
                        if (i > selected_unit.mouvement-1):
                            has_acted = True
                            selected_unit.is_selected = False

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                selected_unit.attack(enemy)
                                if enemy.vie <= 0:
                                    self.enemy_units.remove(enemy)
                                has_acted = True
                                selected_unit.is_selected = False
                        #Capacité spéciale 
                        if event.key == pygame.K_TAB:
                            for enemy in self.enemy_units:
                                selected_unit.battle_cry(enemy)
                                print('ok man')
                                if enemy.vie <= 0:
                                    self.enemy_units.remove(enemy)
                                has_acted = True
                                selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.vie <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()
        
def show_start_screen(screen):
    """Affiche l'écran d'accueil avec choix des personnages et un bouton Start."""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    running = True

    # Options de personnages (à personnaliser)
    character_options = ["Warrior", "Magicien", "Archer","Mineur","Bourrin","Infirmier"]
    selected_character = 0

    while running:
        screen.fill(BLACK)

        # Titre
        title_text = font.render("Bienvenue dans le jeu de stratégie !", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Affichage des options de personnages
        for i, character in enumerate(character_options):
            color = WHITE if i == selected_character else GRAY
            option_text = font.render(character, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 150 + i * 50))

        # Bouton Start
        start_text = font.render("START", True, WHITE)
        start_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
        pygame.draw.rect(screen, GREEN, start_rect)
        screen.blit(start_text, (start_rect.x + start_rect.width // 2 - start_text.get_width() // 2,
                                 start_rect.y + start_rect.height // 2 - start_text.get_height() // 2))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_character = (selected_character - 1) % len(character_options)
                elif event.key == pygame.K_DOWN:
                    selected_character = (selected_character + 1) % len(character_options)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    running = False

        clock.tick(30)

    # Retourne le personnage sélectionné
    return character_options[selected_character]


def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Affiche l'écran d'accueil et récupère le personnage choisi
    selected_character = show_start_screen(screen)
    print(f"Personnage sélectionné : {selected_character}")

    # Créez les unités basées sur le personnage choisi
    if selected_character == "Warrior":
        player_units = [Warrior()]
    elif selected_character == "Magicien":
        player_units = [Magicien()]
    elif selected_character == "Archer":
        player_units = [Archer()]
    elif selected_character == "Mineur":
        player_units = [Mineur()]
    elif selected_character == "Bourrin":
        player_units = [Bourrin()]
    elif selected_character == "Infirmier":
        player_units = [Infirmier()]
    else:
        player_units = []

    # Instanciation du jeu
    game = Game(screen)
    game.player_units = player_units

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()



if __name__ == "__main__":
    main()
