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
        
# class Guerrier(Unit):
#     def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, energie, team):
#         super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team)
#         self.energie = energie
#         self.capacités = ['Boisson du guerrier', 'Téméraire']
#         self.boisson_du_guerrier = 3
#         self.attack_range = 1
#         self.temeraire_actif = False
  
#     def attack(self, target): #10% de chance de doubler ses dégats
#         """Attaque une unité cible."""
#         pourcentage = random.randint(1,11)
#         if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
#             if pourcentage <= 2:
#                 target.vie -= 2*self.attaque
#             else:
#                 target.vie -= self.attaque
#         else:
#             print("Impossible d'attaquer")
        
#     def boisson_guerrier(self):
#         if self.boisson_du_guerrier != 0:
#             self.boisson_du_guerrier -= 1
#             self.vie += 3 #Adapter chiffre
#         else: 
#             print("Vous n'avez plus de boisson du guerrier")
    
#     def temeraire(self): #Assure des dégats doublé mais utilise de l'énergie
#         if self.energie >= 5:
#             self.temeraire_actif = True
#             self.energie -= 5
#             self.attaque = 2*self.attaque
#         else:
#             print("Plus assez d'énergie")    

#     def desactive_temeraire(self):
#         self.attaque = self.attaque // 2
#         self.temeraire_actif = False

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    
        
# class Archer(Unit):
#     def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, energie, team):
#         super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team)
#         self.capacités = ['Fleche de soin', 'Headshot']
#         self.attack_range = 5
#         self.fleche_soigneuse = 3
#         self.energie = energie
#         self.headshot_actif = False
#         self.empoisonné = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS):
#             return False  # Target out of bounds

#         # Check if the target cell is occupied by another unit
#         for unit in all_units:
#             if unit.x == target_x and unit.y == target_y:
#                 return False  # Target cell is occupied

#         # Perform the move if all checks pass
#         self.x = target_x
#         self.y = target_y
#         return True  # Successful move

#     def attack(self, target):
#         """Attaque une unité cible."""
#         if (abs(self.x - target.x) <= self.attack_range and abs(self.y-target.y == 0)) or (abs(self.y - target.y) <= self.attack_range and abs(self.x-target.x == 0)):
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

#     def fleche_de_guerison(self,target):
#         #Tire un fleche qui soigne ses aliés 
#         if self.fleche_soigneuse != 0:
#             self.fleche_soigneuse -= 1
#             if target.vie <= target.max_vie-5:
#                 target.vie += 5
#             else:
#                 target.vie = target.max_vie
#         else:
#             print("Vous n'avez plus de flèches de guérison")
    
#     def headshot(self):
#         if self.energie >= 10:
#             self.energie -= 6
#             self.attaque = 3*self.attaque
#             self.headshot_actif = True
#         else:
#             print("Vous n'avez pas assez d'énergie pour cette attaque")
    
#     def annul_headshot(self):
#         self.attaque = self.attaque//3
#         self.headshot_actif = False

# class Magicien(Unit):
#     def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, energie, team):
#         super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team)
#         self.capacités = ["Sort de poison", "Boule de feu"]
#         self.attack_range = 5
#         self.energie = energie
#         self.stock_boule_de_feu = 3
#         self.poison = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS):
#             return False  # Target out of bounds

#         # Check if the target cell is occupied by another unit
#         for unit in all_units:
#             if unit.x == target_x and unit.y == target_y:
#                 return False  # Target cell is occupied

#         # Perform the move if all checks pass
#         self.x = target_x
#         self.y = target_y
#         return True  # Successful move

#     def attack(self, target):
#         """Attaque une unité cible."""
#         if (abs(self.x - target.x) <= self.attack_range and abs(self.y-target.y == 0)) or (abs(self.y - target.y) <= self.attack_range and abs(self.x-target.x == 0)):
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

#     def sort_de_poison(self,target):
#         if self.energie >= 4:
#             self.energie -=4
#             target.empoisonné = True
#             target.compteur = 3
#         else:
#             print("Pas assez d'énergie pour utiliser ce sort")

#     def boule_de_feu(self, target_x, target_y, enemies):
#         if self.stock_boule_de_feu != 0:
#             for enemy in enemies:
#                 if abs(enemy.x - target_x) <= 1 and abs(enemy.y - target_y) <= 1:
#                     enemy.vie -= 3
#                     # Check if the enemy has been defeated
#                     if enemy.vie <= 0:
#                         enemies.remove(enemy)
#                         print(f"{enemy.name} a été éliminé!")
#         else:
#             print("Plus de boules de feu")
          
# class Assassin(Unit):
#     def __init__(self, x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, energie, team):
#         super().__init__(x, y, mouvement, combat, tir, force, defense, attaque, vie, max_vie, team)
#         self.energie = energie
#         self.fatality = 1
#         self.attack_range = 2
#         self.capacités = ["Coup fatal", "Fuite"]
#         self.coup_fatal_actif = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS):
#             return False  # Target out of bounds

#         # Check if the target cell is occupied by another unit
#         for unit in all_units:
#             if unit.x == target_x and unit.y == target_y:
#                 return False  # Target cell is occupied

#         # Perform the move if all checks pass
#         self.x = target_x
#         self.y = target_y
#         return True  # Successful move

#     def attack(self, target):
#         """Attaque une unité cible."""
#         if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
#     def coup_fatal(self):
#         if self.fatality != 0 and self.energie == 10:
#             self.coup_fatal_actif = True
#             self.fatality = 0 
#             self.attaque = self.attaque * 100
#             self.vie = 2
#             self.energie = 0
#         else:
#             print("Vous n'êtes pas en mesure d'utiliser cette capacité")
    
#     def desactive_coup_fatal(self):
#         self.coup_fatal_actif = False
#         self.attaque = self.attaque //100
        
#     def fuite(self,target_x,target_y):
#         if self.vie <= 10 and self.energie >= 5: 
#             self.x = target_x
#             self.y = target_y
#         else:
#             print("Vous ne pouvez pas prendre la fuite")
            
            