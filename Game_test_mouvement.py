import pygame
import random
from unit import *
from Guerrier import *


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
        self.player_units = [Unit(0, 0, 4, 4, 4 , 4 , 5 , 4 , 10 , 'player'),
                             Unit(1, 0, 1, 4, 4 , 4 , 5, 2 , 10 ,'player')]

        self.enemy_units = [Unit(6, 6, 1, 4, 4 , 4 , 5 , 0 , 10 , 'enemy'),
                            Unit(6, 5, 1, 4, 4 , 4 , 5 , 0 , 10 , 'enemy')]
    def handle_player_turn(self):
        has_acted = False
        selected_unit = None

        while True:
            hovered_cell = None
            # Gestion des événements Pygame
            for event in pygame.event.get():
                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                # Sélection d'une unité avec un clic gauche
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                    
                    if not selected_unit:  # First click: Select the unit
                        for unit in self.player_units:
                            if unit.x == grid_x and unit.y == grid_y:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    elif selected_unit:  # Second click: Attempt to move the unit
                        # Check if the clicked cell is within the movement range
                        if abs(grid_x - selected_unit.x) + abs(grid_y - selected_unit.y) <= selected_unit.mouvement:
                            selected_unit.move(grid_x - selected_unit.x, grid_y - selected_unit.y)
                            selected_unit.is_selected = False
                            return  # End the player's turn
            # Update the display
            self.flip_display()

            if selected_unit:
                # Highlight all possible movement cells in light purple
                for dx in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                    for dy in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            target_x, target_y = selected_unit.x + dx, selected_unit.y + dy
                            if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
                                rect = pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                pygame.draw.rect(self.screen, (128, 100, 128), rect)  # Peut être retiré
                                # Now handle hover effect
                                if event.type == pygame.MOUSEMOTION:
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)
                                    # If hovered cell, color it light purple
                                    if (target_x, target_y) == hovered_cell:
                                        pygame.draw.rect(self.screen, (200, 160, 255), rect)
                                    
            # Refresh the display on every loop iteration
            pygame.display.update() 
              
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


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
