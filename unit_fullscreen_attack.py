from math import ceil
import pygame
import random
import math

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
        self.range_ = range_  # Attack range (depending on the unit)
        self.abilities = []
    
    

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
        # Calculate the damage as the difference between attack and defense
        damage = max(1, self.attaque - target.defense)
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

        
class Guerrier(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=1)
        
        # Images of sword and warrior
        self.arrow_image = pygame.image.load("Espada.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))
        
        self.image_player1 = pygame.image.load("PersosBoard/warrior1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/warrior2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

        self.abilities = ["Powerful Blow", "Escudo Defensivo"]
    
    def attack_with_animation(self, target, game, screen):
        """
        Attack animation with sword
        """
        start_x = self.x * CELL_SIZE + CELL_SIZE // 2
        start_y = self.y * CELL_SIZE + CELL_SIZE // 2
        end_x = target.x * CELL_SIZE + CELL_SIZE // 2
        end_y = target.y * CELL_SIZE + CELL_SIZE // 2

        angle = self.calculate_angle(start_x, start_y, end_x, end_y)
        steps = 30
        
        for step in range(steps):
            t = step / steps
            current_x = int(start_x + t * (end_x - start_x))
            current_y = int(start_y + t * (end_y - start_y))
            
            game.display.flip_display()  
            rotated_sword = pygame.transform.rotate(self.arrow_image, angle)
            sword_rect = rotated_sword.get_rect(center=(current_x, current_y))
            screen.blit(rotated_sword, sword_rect)

            pygame.display.flip()
            pygame.time.delay(30)

        # Calculate damage and apply to target
        damage = max(1, self.attaque - target.defense)
        target.vie -= damage
        return damage
    
    def calculate_angle(self, start_x, start_y, end_x, end_y):
        """
        Calculate degree of rotation of the sword in degrees.
        """
        dx = end_x - start_x
        dy = end_y - start_y
        return -math.degrees(math.atan2(dy, dx))
        
    def powerful_strike(self, target, game, screen):
        """
        Powerful blow/Golpe Poderoso: inflicts damage of 8 to the target.
        """
        # Attack animation
        self.attack_with_animation(target, game, screen)

        # Inflict damage of 8 (ignore defense)
        damage = 8
        target.vie -= damage

        # Message of inflicted damage
        game.display.show_message(
            f"{self.__class__.__name__} used Powerful Blow and inflicted {damage} of damage to {target.__class__.__name__}!"
        )
        return damage

        



class Archer(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=4)
        # Image of the arrow
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # scale image
        
        self.image_player1 = pygame.image.load("PersosBoard/archer1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/archer2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
        self.abilities = ["Healing Arrow"]  # Archer's ability

    def attack_with_animation(self, target, game, screen):
        """
        Simulate the normal attack of the archer with animated arrow.
        """
        # Initial and final coordinates of the arrow
        start_x = self.x * CELL_SIZE + CELL_SIZE // 2
        start_y = self.y * CELL_SIZE + CELL_SIZE // 2
        end_x = target.x * CELL_SIZE + CELL_SIZE // 2
        end_y = target.y * CELL_SIZE + CELL_SIZE // 2

        # Duration of the animation
        steps = 30
        for step in range(steps):
            t = step / steps
            current_x = int(start_x + t * (end_x - start_x))
            current_y = int(start_y + t * (end_y - start_y))

            # Draw arrow in movement
            game.display.flip_display()  # Redraw board
            arrow_rotated = pygame.transform.rotate(self.arrow_image, self.calculate_angle(start_x, start_y, end_x, end_y))
            arrow_rect = arrow_rotated.get_rect(center=(current_x, current_y))
            screen.blit(arrow_rotated, arrow_rect)

            pygame.display.flip()
            pygame.time.delay(30)

        # Attack or healing
        damage = max(1, self.attaque - target.defense)
        target.vie -= damage
        return damage

    def heal_with_arrow(self, ally):
        """
        Throw healing arrow to an ally.
        """
        heal_amount = 10  # amount of healing
        ally.vie += heal_amount
        return heal_amount

    def calculate_angle(self, start_x, start_y, end_x, end_y):
        """
        Calculates degree of rotation of the arrow in degrees.
        """
        dx = end_x - start_x
        dy = end_y - start_y
        return -math.degrees(math.atan2(dy, dx))  


class Magicien(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=6)  # Magicien has a range of 2
        
        self.abilities = ["Healing Potion", "Ataque de Área"]
        # Image of the fireball
        self.arrow_image = pygame.image.load("fireball.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # Scale image
        
        self.image_player1 = pygame.image.load("PersosBoard/wizard1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/wizard2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
    def attack_with_animation(self, target, game, screen):
        """
        Simulates attack of the fireball.
        """
        # Initial and final coordinates of fireball
        start_x = self.x * CELL_SIZE + CELL_SIZE // 2
        start_y = self.y * CELL_SIZE + CELL_SIZE // 2
        end_x = target.x * CELL_SIZE + CELL_SIZE // 2
        end_y = target.y * CELL_SIZE + CELL_SIZE // 2

        # Duration of the animation
        steps = 30
        for step in range(steps):
            t = step / steps
            current_x = int(start_x + t * (end_x - start_x))
            current_y = int(start_y + t * (end_y - start_y))

            # Draw fireball with movement
            game.display.flip_display()  # Redraw board
            arrow_rotated = pygame.transform.rotate(self.arrow_image, self.calculate_angle(start_x, start_y, end_x, end_y))
            arrow_rect = arrow_rotated.get_rect(center=(current_x, current_y))
            screen.blit(arrow_rotated, arrow_rect)

            pygame.display.flip()
            pygame.time.delay(30)

        # Attack and calculate the damage
        damage = max(1, self.attaque - target.defense)
        target.vie -= damage
        return damage
    
    def calculate_angle(self, start_x, start_y, end_x, end_y):
        """
        Calculate the angle of rotation of the fireball.
        """
        dx = end_x - start_x
        dy = end_y - start_y
        return -math.degrees(math.atan2(dy, dx))    
    
    def heal(self):
        """Restores a life percentage of life to the wizard."""
        heal_amount = self.max_vie * 0.25  # Heals 25% of max life
        self.vie = min(self.max_vie, self.vie + heal_amount)  # So it does't exceed max life
        return heal_amount

class Assassin(Unit):
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
        super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team, range_=1)
        
        # Image to attack and character
        self.arrow_image = pygame.image.load("ninja.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))
        
        self.image_player1 = pygame.image.load("PersosBoard/assasin1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/assasin2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
        self.abilities = ["Movimiento Adicional", "Critical Fang"]
        
        # Skill status
        self.colmillo_critico_target = None  # Selected target to attack
        self.colmillo_critico_turns = 0  # Shift counter
        self.colmillo_critico_effect = False  # Active effect
        self.colmillo_critico_initial_vie = 0  # Initial enemy health to restore correctly

    def attack_with_animation(self, target, game, screen):
        """
        Simulate the attack of the assassin.
        """
        # Initial and final coordinates of the attack
        start_x = self.x * CELL_SIZE + CELL_SIZE // 2
        start_y = self.y * CELL_SIZE + CELL_SIZE // 2
        end_x = target.x * CELL_SIZE + CELL_SIZE // 2
        end_y = target.y * CELL_SIZE + CELL_SIZE // 2

        # Duration of animation
        steps = 30
        for step in range(steps):
            t = step / steps
            current_x = int(start_x + t * (end_x - start_x))
            current_y = int(start_y + t * (end_y - start_y))

            # Draw attack movement
            game.display.flip_display()  # Redraw board
            arrow_rotated = pygame.transform.rotate(self.arrow_image, self.calculate_angle(start_x, start_y, end_x, end_y))
            arrow_rect = arrow_rotated.get_rect(center=(current_x, current_y))
            screen.blit(arrow_rotated, arrow_rect)

            pygame.display.flip()
            pygame.time.delay(30)

        # Attack and calculate damage
        damage = max(1, self.attaque - target.defense)
        target.vie -= damage
        return damage
    
    def calculate_angle(self, start_x, start_y, end_x, end_y):
        """
        Calculate the angle of rotation of the attack in degrees.
        """
        dx = end_x - start_x
        dy = end_y - start_y
        return -math.degrees(math.atan2(dy, dx)) 

    def activate_colmillo_critico(self, target):
        """Activates the skill Critical Fang on the selected target"""
        self.colmillo_critico_target = target
        self.colmillo_critico_effect = True
        self.colmillo_critico_turns = 3  # Duration of 3 turns
        self.colmillo_critico_initial_vie = target.vie  # Store initial life of the target
        target.vie = max(target.vie // 2, 1)  # Reduces life by half but not to 0

    def update(self):
        """Update skill status and shift counter"""
        if self.colmillo_critico_effect:
            self.colmillo_critico_turns -= 1
            if self.colmillo_critico_turns <= 0:
                # Restore life to original value after 3 turns
                if self.colmillo_critico_target:
                    self.colmillo_critico_target.vie = self.colmillo_critico_initial_vie
                self.colmillo_critico_effect = False
                self.colmillo_critico_target = None 
