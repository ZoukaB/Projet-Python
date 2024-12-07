import pygame
import random
from unitcopy import *
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
                             Unit(1, 0, 1, 4, 4 , 4 , 5, 2 , 10 ,'player'),
                             Unit(3, 0, 1, 4, 4 , 4 , 5, 2 , 10 ,'player'),
                             Unit(4, 0, 1, 4, 4 , 4 , 5, 2 , 10 ,'player')]

        self.enemy_units = [Unit(6, 6, 1, 4, 4 , 4 , 5 , 0 , 10 , 'enemy'),
                            Unit(6, 5, 1, 4, 4 , 4 , 5 , 0 , 10 , 'enemy')]
        
    def handle_player_turn(self):
        selected_unit = None
        hovered_cell = None  # Persistent hovered cell state
        moved_units = []  # Track units that have moved

        while True:
            # Handle Pygame events
            for event in pygame.event.get():
                # Handle quitting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                # Handle selecting a unit with a left mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                    
                    if not selected_unit:  # First click: Select the unit
                        for unit in self.player_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    elif selected_unit:  # Second click: Attempt to move the unit
                        # Check if the clicked cell is within the movement range
                        if abs(grid_x - selected_unit.x) + abs(grid_y - selected_unit.y) <= selected_unit.mouvement:
                            selected_unit.move(grid_x - selected_unit.x, grid_y - selected_unit.y)
                            selected_unit.is_selected = False
                            moved_units.append(selected_unit)  # Mark the unit as moved
                            selected_unit = None
                
                # Update the hovered cell position
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)
                    
            # Check if all units have moved, end turn if so
            if len(moved_units) == len(self.player_units):
                break  # All units have moved, end the player's turn  

            # Refresh the display, passing in highlights to avoid flickering
            self.flip_display(selected_unit, hovered_cell)
            
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

    def flip_display(self, selected_unit=None, hovered_cell=None):
        """Renders the game grid, units, and optional highlights."""
        
        # Clear the screen with a black background
        self.screen.fill(BLACK)

        # Draw the grid (white lines)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)  # Grid lines

        # Draw all units
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Highlight movement range in purple if a unit is selected
        if selected_unit:
            movement_range = set()  # To track all valid movement cells

            # Calculate valid movement range
            for dx in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                for dy in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                    if abs(dx) + abs(dy) <= selected_unit.mouvement:
                        target_x, target_y = selected_unit.x + dx, selected_unit.y + dy

                        # Skip the current unit's position
                        if (target_x, target_y) == (selected_unit.x, selected_unit.y):
                            continue

                        # Ensure the target cell is within the grid bounds
                        if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
                            movement_range.add((target_x, target_y))
            
            # Draw the movement range in semi-transparent purple
            purple_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Create a transparent surface
            purple_surface.fill((128, 100, 128, 128))  # RGBA for transparent purple (50% opacity)
            
            # Draw the movement range in purple
            for cell in movement_range:
                rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.screen.blit(purple_surface,rect)

            # Highlight hovered cell in light purple
            if hovered_cell in movement_range:
                rect = pygame.Rect(hovered_cell[0] * CELL_SIZE, hovered_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (200, 160, 255), rect)  # Light purple

        # Update the display
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
