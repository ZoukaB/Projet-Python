import pygame
import random

# Constantes
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.
    """

    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,team):
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

    def move(self, dx, dy, all_units):
        """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
        target_x = self.x + dx
        target_y = self.y + dy

        # Check if the target position is within the grid bounds
        if not (0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE):
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
        damage = max(1, 5 - 2) # result: 3
        target.vie -= damage # reduce health 
        target.vie = max(0, target.vie) # avoid having negative health
        return damage
    
    def is_in_range(self, target, range_distance=3):
        # verify is target is bewteen range attack
        return abs(self.x - target.x) + abs(self.y - target.y) <= range_distance

    def draw(self, screen):
        """Affiche l'unité sur l'écran avec health points."""
        color = BLUE if self.team == 'player1' else RED
        pygame.draw.circle(screen, color,
                          (self.x * CELL_SIZE + CELL_SIZE //2,
                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Draw health points
        health_bar_width = CELL_SIZE
        health_bar_height = 5
        health_ratio = self.vie / self.max_vie
        filled_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, filled_width, health_bar_height))


#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# class Guerrier:
#     """
#     Classe pour représenter une unité.

#     ...
#     Attributs
#     ---------
#     x : int
#         La position x de l'unité sur la grille.
#     y : int
#         La position y de l'unité sur la grille.
#     vie : int
#         La santé de l'unité.
#     attaque : int
#         La puissance d'attaque de l'unité.
#     team : str
#         L'équipe de l'unité ('player' ou 'enemy').
#     is_selected : bool
#         Si l'unité est sélectionnée ou non.

#     Méthodes
#     --------
#     move(dx, dy)
#         Déplace l'unité de dx, dy.
#     attack(target)
#         Attaque une unité cible.
#     draw(screen)
#         Dessine l'unité sur la grille.
#     """

#     def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,team):
#         """
#         Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

#         Paramètres
#         ----------
#         x : int
#             La position x de l'unité sur la grille.
#         y : int
#             La position y de l'unité sur la grille.
#         vie : int
#             La santé de l'unité.
#         attaque : int
#             La puissance d'attaque de l'unité.
#         team : str
#             L'équipe de l'unité ('player' ou 'enemy').
#         """
#         self.x = x
#         self.y = y
#         self.mouvement = mouvement
#         self.combat = combat
#         self.tir = tir
#         self.force = force
#         self.defense = defense
#         self.attaque = attaque
#         self.vie = vie
#         self.max_vie = max_vie
#         self.team = team  # 'player' ou 'enemy'
#         self.is_selected = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE):
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
#         if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
# class Archer:
#     """
#     Classe pour représenter une unité.

#     ...
#     Attributs
#     ---------
#     x : int
#         La position x de l'unité sur la grille.
#     y : int
#         La position y de l'unité sur la grille.
#     vie : int
#         La santé de l'unité.
#     attaque : int
#         La puissance d'attaque de l'unité.
#     team : str
#         L'équipe de l'unité ('player' ou 'enemy').
#     is_selected : bool
#         Si l'unité est sélectionnée ou non.

#     Méthodes
#     --------
#     move(dx, dy)
#         Déplace l'unité de dx, dy.
#     attack(target)
#         Attaque une unité cible.
#     draw(screen)
#         Dessine l'unité sur la grille.
#     """

#     def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,team):
#         """
#         Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

#         Paramètres
#         ----------
#         x : int
#             La position x de l'unité sur la grille.
#         y : int
#             La position y de l'unité sur la grille.
#         vie : int
#             La santé de l'unité.
#         attaque : int
#             La puissance d'attaque de l'unité.
#         team : str
#             L'équipe de l'unité ('player' ou 'enemy').
#         """
#         self.x = x
#         self.y = y
#         self.mouvement = mouvement
#         self.combat = combat
#         self.tir = tir
#         self.force = force
#         self.defense = defense
#         self.attaque = attaque
#         self.vie = vie
#         self.max_vie = max_vie
#         self.team = team  # 'player' ou 'enemy'
#         self.is_selected = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE):
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
#         if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# class Magicien:
#     """
#     Classe pour représenter une unité.

#     ...
#     Attributs
#     ---------
#     x : int
#         La position x de l'unité sur la grille.
#     y : int
#         La position y de l'unité sur la grille.
#     vie : int
#         La santé de l'unité.
#     attaque : int
#         La puissance d'attaque de l'unité.
#     team : str
#         L'équipe de l'unité ('player' ou 'enemy').
#     is_selected : bool
#         Si l'unité est sélectionnée ou non.

#     Méthodes
#     --------
#     move(dx, dy)
#         Déplace l'unité de dx, dy.
#     attack(target)
#         Attaque une unité cible.
#     draw(screen)
#         Dessine l'unité sur la grille.
#     """

#     def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,team):
#         """
#         Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

#         Paramètres
#         ----------
#         x : int
#             La position x de l'unité sur la grille.
#         y : int
#             La position y de l'unité sur la grille.
#         vie : int
#             La santé de l'unité.
#         attaque : int
#             La puissance d'attaque de l'unité.
#         team : str
#             L'équipe de l'unité ('player' ou 'enemy').
#         """
#         self.x = x
#         self.y = y
#         self.mouvement = mouvement
#         self.combat = combat
#         self.tir = tir
#         self.force = force
#         self.defense = defense
#         self.attaque = attaque
#         self.vie = vie
#         self.max_vie = max_vie
#         self.team = team  # 'player' ou 'enemy'
#         self.is_selected = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE):
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
#         if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# class Assassin:
#     """
#     Classe pour représenter une unité.

#     ...
#     Attributs
#     ---------
#     x : int
#         La position x de l'unité sur la grille.
#     y : int
#         La position y de l'unité sur la grille.
#     vie : int
#         La santé de l'unité.
#     attaque : int
#         La puissance d'attaque de l'unité.
#     team : str
#         L'équipe de l'unité ('player' ou 'enemy').
#     is_selected : bool
#         Si l'unité est sélectionnée ou non.

#     Méthodes
#     --------
#     move(dx, dy)
#         Déplace l'unité de dx, dy.
#     attack(target)
#         Attaque une unité cible.
#     draw(screen)
#         Dessine l'unité sur la grille.
#     """

#     def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,vie,max_vie,team):
#         """
#         Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

#         Paramètres
#         ----------
#         x : int
#             La position x de l'unité sur la grille.
#         y : int
#             La position y de l'unité sur la grille.
#         vie : int
#             La santé de l'unité.
#         attaque : int
#             La puissance d'attaque de l'unité.
#         team : str
#             L'équipe de l'unité ('player' ou 'enemy').
#         """
#         self.x = x
#         self.y = y
#         self.mouvement = mouvement
#         self.combat = combat
#         self.tir = tir
#         self.force = force
#         self.defense = defense
#         self.attaque = attaque
#         self.vie = vie
#         self.max_vie = max_vie
#         self.team = team  # 'player' ou 'enemy'
#         self.is_selected = False

#     def move(self, dx, dy, all_units):
#         """Move the unit by dx, dy if within grid bounds and target cell is unoccupied."""
#         target_x = self.x + dx
#         target_y = self.y + dy

#         # Check if the target position is within the grid bounds
#         if not (0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE):
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
#         if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
#             target.vie -= self.attaque

#     def draw(self, screen):
#         """Affiche l'unité sur l'écran."""
#         color = BLUE if self.team == 'player1' else RED
#         if self.is_selected:
#             pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
#                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#         pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
#                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
