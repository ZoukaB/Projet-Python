import pygame
import random
from unit import *
from Guerrier import *

# Constantes
GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = [
            Unit(0, 0, 4, 4, 4, 4, 5, 4, 10, 'player1'),
            Unit(1, 0, 1, 4, 4, 4, 5, 2, 10, 'player1'),
            # Unit(3, 0, 1, 4, 4, 4, 5, 2, 10, 'player'),
            # Unit(4, 0, 1, 4, 4, 4, 5, 2, 10, 'player')
        ]

        self.player2_units = [
            Unit(6, 6, 1, 4, 4, 4, 5, 1, 10, 'player2'),
            Unit(6, 5, 1, 4, 4, 4, 5, 1, 10, 'player2')
        ]

    def handle_player1_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                    # Select a unit if no unit is currently selected
                    if not selected_unit:
                        for unit in self.player1_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move the selected unit if one is selected
                    elif selected_unit:
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

            if len(moved_units) == len(self.player1_units):
                break  

            self.flip_display(selected_unit, hovered_cell)
    
    def handle_player2_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                    # Select a unit if no unit is currently selected
                    if not selected_unit:
                        for unit in self.player2_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move the selected unit if one is selected
                    elif selected_unit:
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

            if len(moved_units) == len(self.player2_units):
                break  

            self.flip_display(selected_unit, hovered_cell)      
    

    def draw_menu(self, selected_unit):
        """Draws the unit information menu in the lower-left corner."""
        menu_width = WIDTH // 2
        menu_height = HEIGHT // 4  # Increased height to accommodate the character display
        menu_x = 0
        menu_y = HEIGHT - menu_height

        # Draw the menu background
        pygame.draw.rect(self.screen, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))  # Black background
        pygame.draw.rect(self.screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 2)  # White border

        if selected_unit:
            font = pygame.font.Font(None, 16)

            # Column widths for the three sections
            column_width = menu_width // 3

            # === First Column: Character Display and Health Bar ===
            char_center_x = menu_x + column_width // 2  # Center character in the first column
            char_center_y = menu_y + 35  # Position the character near the top
            pygame.draw.circle(self.screen, (0, 0, 255), (char_center_x, char_center_y), 15)  # Blue circle to represent the unit

            # Draw the health bar below the character
            health_bar_width = 80
            health_bar_height = 8
            health_bar_x = char_center_x - health_bar_width // 2  # Center the health bar
            health_bar_y = char_center_y + 30  # Position below the character

            # Calculate the width of the green health bar based on the unit's health
            health_ratio = selected_unit.vie / 10  # Assuming max health is 10
            health_fill_width = int(health_ratio * health_bar_width)

            # Draw the health bar background (gray) and foreground (green)
            pygame.draw.rect(self.screen, (128, 128, 128), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))  # Background
            pygame.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, health_fill_width, health_bar_height))  # Foreground

            # === Second Column: 3 of the 5 stats ===
            second_column_x = menu_x + column_width
            second_column_stats = [
                f"Attaque: {selected_unit.attaque}",
                f"Défense: {selected_unit.defense}",
                f"Tir: {selected_unit.tir}",
            ]

            for i, line in enumerate(second_column_stats):
                text = font.render(line, True, (255, 255, 255))  # White text
                self.screen.blit(text, (second_column_x + 10, menu_y + 20 + i * 20))  # Position with spacing

            # === Third Column: Remaining 2 stats ===
            third_column_x = menu_x + 2 * column_width
            third_column_stats = [
                f"Force: {selected_unit.force}",
                f"Combat: {selected_unit.combat}",
            ]

            for i, line in enumerate(third_column_stats):
                text = font.render(line, True, (255, 255, 255))  # White text
                self.screen.blit(text, (third_column_x + 10, menu_y + 20 + i * 20))  # Position with spacing

            # === Bottom Section: Instructions or Additional Text ===
            bottom_text = "Informations sur les capacités spéciales"
            bottom_font = pygame.font.Font(None, 18)
            text_surface = bottom_font.render(bottom_text, True, (255, 255, 255))  # White text

            # Center the text in the bottom section
            text_x = menu_x + menu_width // 2 - text_surface.get_width() // 2
            text_y = menu_y + menu_height - 45  # Leave some padding from the bottom
            self.screen.blit(text_surface, (text_x, text_y))

    def flip_display(self, selected_unit=None, hovered_cell=None):
        self.screen.fill(BLACK)

        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player1_units + self.player2_units:
            unit.draw(self.screen)

        if selected_unit:
            movement_range = set()

            for dx in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                for dy in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                    if abs(dx) + abs(dy) <= selected_unit.mouvement:
                        target_x, target_y = selected_unit.x + dx, selected_unit.y + dy

                        if (target_x, target_y) == (selected_unit.x, selected_unit.y):
                            continue

                        if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
                            movement_range.add((target_x, target_y))
            
            purple_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            purple_surface.fill((128, 100, 128, 128))
            
            for cell in movement_range:
                rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.screen.blit(purple_surface, rect)

            if hovered_cell in movement_range:
                rect = pygame.Rect(hovered_cell[0] * CELL_SIZE, hovered_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (200, 160, 255), rect)

        # Draw the menu in the lower-left corner
        self.draw_menu(selected_unit)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)

    while True:
        game.handle_player1_turn()
        game.handle_player2_turn()

if __name__ == "__main__":
    main()
