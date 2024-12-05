import pygame
import random

# Constantes
GRID_SIZE = 40
CELL_SIZE = 20
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit_new:
    """
    Classe pour représenter le guerrier.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    mouvement : int
        Nombre de case pouvant parcourir en 1 tour
    combat: int
        Nombre entre 1 et 6 correspondant la capacité de combat d'un personnage
    tir: int 
        Valeur de dés nécéssaire pour infliger des dégats
    force: int
        Capacité à blesser une fois un combat gagné
    defense: int
        Capacité de résister 
    attaque : int
        Nombre de dés utilisés dans un combat 
    vie : int
        Point de vie de l'unité. 
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
    pouvoir(self,index_capacite,target)
        Utilise une des 3 capacités spéciales du personnage
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y,mouvement,combat,tir,force,defense,attaque,energie,energie_max,vie,team):
        """
        Construit une unité avec une position, mouvement, combat, tir, force, defense, attaque, vie et équipe.
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
        self.team = team  # 'player' ou 'enemy'
        self.energie = energie
        self.energie_max = energie_max
        self.is_selected = False


    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
    
    def recupération(self,energie):
        if self.energie < self.energie_max:
            self.energie += 1

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = WHITE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
