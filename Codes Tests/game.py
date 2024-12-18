import pygame
import random
from unit import *
from Guerrier import *
from combat import combat_round


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
        self.player_units = [Guerrier(0, 0, 4, 4, 4 , 4 , 5 , 4 , 10 , 'player'),
                             Unit(1, 0, 1, 4, 4 , 4 , 5, 2 , 10 ,'player')]

        self.enemy_units = [Unit(6, 6, 1, 4, 4 , 4 , 5 , 2 , 10 , 'enemy'),
                            Unit(6, 5, 1, 4, 4 , 4 , 5 , 2 , 10 , 'enemy')]

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            i = 0 
            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                            i += 1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                            i += 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                            i += 1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                            i += 1
                        
                        selected_unit.move(dx, dy)
                        self.flip_display()
                        if (i > selected_unit.mouvement-1):
                            has_acted = True
                            selected_unit.is_selected = False

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    combat_round(self.screen, selected_unit, enemy)
                                    if enemy.vie <= 0:
                                        self.enemy_units.remove(enemy)
                                    has_acted = True
                                    selected_unit.is_selected = False
                        #Capacité spéciale 
                        if event.key == pygame.K_TAB:
                            for enemy in self.enemy_units:
                                selected_unit.battle_cry(enemy)
                                print('ok man')
                                if enemy.vie <= 0:
                                    self.enemy_units.remove(enemy)
                                has_acted = True
                                selected_unit.is_selected = False

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
