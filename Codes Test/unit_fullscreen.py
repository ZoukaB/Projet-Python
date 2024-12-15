from math import ceil
import pygame
import random

# Initialize Pygame to fetch display info
pygame.init()
screen_info = pygame.display.Info()

# Get the screen dimensions
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Desired cell size (you can adjust this for larger or smaller cells)
CELL_SIZE = 50
# Calculate the number of columns and rows to ensure full coverage
GRID_COLUMNS = 1+(SCREEN_WIDTH + CELL_SIZE ) // CELL_SIZE # Round up to cover full widthD
#Bizarre le + 1, par forcement nécéssaire en fonction de cell_size

GRID_ROWS =(SCREEN_HEIGHT + CELL_SIZE) // CELL_SIZE

# Calculate the exact grid width and height based on the number of columns and rows
WIDTH = GRID_COLUMNS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE

# Colors
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    def __init__(self, x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team):
        self.x = x
        self.y = y
        self.mouvement = mouvement
        self.defense = defense
        self.attaque = attaque
        self.vie = vie
        self.max_vie = max_vie
        self.energie = energie
        self.max_energie = max_energie
        self.team = team  # 'player1' or 'player2'
        self.is_selected = False
        self.empoisonné = False
        self.compteur = 0

    def move(self, dx, dy, all_units):
        target_x = self.x + dx
        target_y = self.y + dy

        # Check if the target position is within the grid bounds
        if not (0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS):
            return False  # Target out of bounds

        # Check if the target cell is occupied by another unit
        for unit in all_units:
            if unit.x == target_x and unit.y == target_y:
                return False  # Target cell is occupied

        # Perform the move if all checks pass
        self.x = target_x
        self.y = target_y
        return True  # Successful move
    
    def poison_actif(self):
        if self.empoisonné:
            self.vie -= 1
            self.compteur -= 1
            if self.compteur <= 0:
                self.empoisonné = False
                
    def draw(self, screen):
        """
        Draws unit on the screen along with health life bar.
        """
         # Draw image according to the player
        image = self.image_player1 if self.team == 'player1' else self.image_player2
        
        # Draw image
        screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        
        # Draw health life bar
        health_bar_width = CELL_SIZE
        health_bar_height = 5
        health_ratio = self.vie / self.max_vie
        filled_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, filled_width, health_bar_height))