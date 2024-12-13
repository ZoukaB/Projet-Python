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
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=1):
        self.x = x
        self.y = y
        self.mouvement = mouvement
        self.combat = combat
        self.tir = tir
        self.force = force
        self.defense = defense
        self.attaque = attaque
        self.vie = vie
        self.max_vie = max_vie
        self.team = team  # 'player1' or 'player2'
        self.is_selected = False
        self.range_ = range_  # Attack range (according to unit)

    def move(self, dx, dy, all_units):
        target_x = self.x + dx
        target_y = self.y + dy

        # Verify if the selected position is between the limits
        if not (0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS):
            return False  # Out of range

        # Verify if the cell is occupied by another unit
        for unit in all_units:
            if unit.x == target_x and unit.y == target_y:
                return False  # Cell ocuppied

        # Perform movement if the verifications are successful
        self.x = target_x
        self.y = target_y
        return True  # Successful movement

    def attack(self, target):
        """
        Attacks target unit. 
        Minimize health life based on attack and defense.
        """
        # Calculates the damage as the difference between attack and defense.
        damage = max(3, self.attaque - target.defense)
        target.vie -= damage  # Reduce health life of the target unit
        target.vie = max(0, target.vie)  # Avoids having negative health life
        return damage  # Returns the damage inflicted

    def is_in_range(self, target):
        """
        Verify if the target is between the attack range.
        Use self.range_ for the attack range.
        """
        return max(abs(self.x - target.x), abs(self.y - target.y)) <= self.range_

    def draw(self, screen):
        """
        Draws unit on the screen along with health life bar.
        """
        color = BLUE if self.team == 'player1' else RED
        pygame.draw.circle(screen, color, 
                           (self.x * CELL_SIZE + CELL_SIZE // 2, 
                            self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Draws health life bar
        health_bar_width = CELL_SIZE
        health_bar_height = 5
        health_ratio = self.vie / self.max_vie
        filled_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, filled_width, health_bar_height))

        
class Guerrier(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=1)  # Guerrier range 1

class Archer(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=3)  # Archer range 3

class Magicien(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=2)  # Magicien range 2

class Assassin(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=1)  # Assassin range 1



  
        
