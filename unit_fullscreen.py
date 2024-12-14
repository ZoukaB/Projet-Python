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
    def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team):
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
        self.capacite_active = False

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
    
    def is_in_range(self, target):
        """
        Verify if the target is between the attack range.
        Use self.range_ for the attack range.
        """
        return max(abs(self.x - target.x), abs(self.y - target.y)) <= self.range_
    
    def draw(self, screen):
        color = BLUE if self.team == 'player1' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        # Draws health life bar
        health_bar_width = CELL_SIZE
        health_bar_height = 5
        health_ratio = self.vie / self.max_vie
        filled_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, filled_width, health_bar_height))
        
class Guerrier:

    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,energie,team):

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
        self.energie = energie
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.capacités = ['Boisson du guerrier','Téméraire']
        self.boisson_du_guerrier = 3
        self.attack_range = 1
        self.temeraire_active = False

        self.image_player1 = pygame.image.load("PersosBoard/warrior1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/warrior2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
    def attack(self, target): #10% de chance de doubler ses dégats
        """Attaque une unité cible."""
        pourcentage = random.randint(1,11)
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            if pourcentage <= 2:
                target.vie -= 2*self.attaque
            else:
                target.vie -= self.attaque
        else:
            print("Impossible d'attaquer")
        
    def boisson_guerrier(self):
        if self.boisson_du_guerrier != 0:
            self.boisson_du_guerrier -= 1
            self.vie += 3 #Adapter chiffre
        else: 
            print("Vous n'avez plus de boisson du guerrier")
    
    def temeraire(self): #Assure des dégats doublé mais utilise de l'énergie
        if self.energie >= 5:
            self.temeraire_active = True
            self.energie -= 5
            self.attaque = 2*self.attaque
        else:
            print("Plus assez d'énergie")    

    def desactive_temeraire(self):
        self.attaque = self.attaque // 2
        self.temeraire = False

    def move(self, dx, dy, all_units):
        """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
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

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Choose the image based on the player
        image = self.image_player1 if self.team == 'player1' else self.image_player2
        # Draw the selected image
        if image:
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
    
        
class Archer:
    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,energie,team):
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
        self.team = team
        self.capacités = ['Fleche de soin','Headshot']
        self.attack_range = 5
        self.is_selected = False
        self.fleche_soigneuse = 3
        self.energie = energie
        self.headshot_actif = False

        self.image_player1 = pygame.image.load("PersosBoard/archer1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/archer2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy, all_units):
        """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
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

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= self.attack_range or abs(self.y - target.y) <= self.attack_range:
            target.vie -= self.attaque

    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Choose the image based on the player
        image = self.image_player1 if self.team == 'player1' else self.image_player2
        # Draw the selected image
        if image:
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def fleche_de_guerison(self,target):
        #Tire un fleche qui soigne ses aliés 
        if self.fleche_soigneuse != 0:
            self.fleche_soigneuse -= 1
            if target.vie <= target.max_vie-5:
                target.vie += 5
            else:
                target.vie = target.max_vie
        else:
            print("Vous n'avez plus de flèches de guérison")
    
    def headshot(self):
        if self.energie >= 10:
            self.energie -= 6
            self.attaque = 3*self.attaque
            self.headshot_actif = True
        else:
            print("Vous n'avez pas assez d'énergie pour cette attaque")
    
    def annul_headshot(self):
        self.attaque = self.attaque//3
        self.headshot_actif = False

        

class Magicien:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    vie : int
        La santé de l'unité.
    attaque : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,energie,team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        vie : int
            La santé de l'unité.
        attaque : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
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
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.energie = energie

        self.image_player1 = pygame.image.load("PersosBoard/wizard1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/wizard2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy, all_units):
        """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
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

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.vie -= self.attaque

    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Choose the image based on the player
        image = self.image_player1 if self.team == 'player1' else self.image_player2
        # Draw the selected image
        if image:
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

class Assassin:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    vie : int
        La santé de l'unité.
    attaque : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,energie,team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        vie : int
            La santé de l'unité.
        attaque : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
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
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.energie = energie

        self.image_player1 = pygame.image.load("PersosBoard/assasin1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/assasin2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy, all_units):
        """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
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

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.vie -= self.attaque

    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Choose the image based on the player
        image = self.image_player1 if self.team == 'player1' else self.image_player2
        # Draw the selected image
        if image:
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        
