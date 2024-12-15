import sys
import pygame
from unit_fullscreen import *
from Display import *
from duel import Character
from test_combat import test_combat

CHARACTER_OPTIONS = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
    {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        self.display = Display(self.screen, self)

    def pause_menu(self):
        font = pygame.font.Font(None, 48)
        button_font = pygame.font.Font(None, 36)
        button_width, button_height = 250, 60
        resume_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - 20, button_width, button_height)
        home_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        paused = True

        while paused:
            self.screen.blit(overlay, (0, 0))
            pause_text = font.render("Game Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))
            pygame.draw.rect(self.screen, WHITE, resume_button)
            resume_text = button_font.render("Resume", True, BLACK)
            self.screen.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
                                           resume_button.y + (resume_button.height - resume_text.get_height()) // 2))
            pygame.draw.rect(self.screen, WHITE, home_button)
            home_text = button_font.render("Home Screen", True, BLACK)
            self.screen.blit(home_text, (home_button.x + (home_button.width - home_text.get_width()) // 2,
                                         home_button.y + (home_button.height - home_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.collidepoint(event.pos):
                        paused = False
                    elif home_button.collidepoint(event.pos):
                        self.reset_game()
                        paused = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False

            pygame.display.flip()

    def reset_game(self):
        self.player1_units = []
        self.player2_units = []

    def check_combat(self):
        for unit1 in self.player1_units:
            for unit2 in self.player2_units:
                if abs(unit1.x - unit2.x) + abs(unit1.y - unit2.y) == 1:
                    char1 = Character(name=unit1.__class__.__name__, attaque=unit1.attaque, combat=unit1.combat, force=unit1.force, defense=unit1.defense, vie=unit1.vie)
                    char2 = Character(name=unit2.__class__.__name__, attaque=unit2.attaque, combat=unit2.combat, force=unit2.force, defense=unit2.defense, vie=unit2.vie)
                    print(f"Combat détecté entre {char1.name} et {char2.name}.")
                    test_combat(self.screen, char1, char2)
                    unit1.vie, unit2.vie = char1.vie, char2.vie
                    if char1.vie <= 0:
                        self.player1_units.remove(unit1)
                    if char2.vie <= 0:
                        self.player2_units.remove(unit2)
                    return True
        return False

    def handle_turn(self, player_units, enemy_units):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        def select_next_unit():
            for unit in player_units:
                if unit not in moved_units:
                    unit.is_selected = True
                    return unit
            return None

        selected_unit = select_next_unit()
        proposed_x, proposed_y = None, None
        while selected_unit:
            proposed_x, proposed_y = selected_unit.x, selected_unit.y
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.pause_menu()
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                            dx, dy = 0, 0
                            if event.key == pygame.K_UP:
                                dy = -1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
                            elif event.key == pygame.K_LEFT:
                                dx = -1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1

                            # Update hovered cell within range
                            if abs(proposed_x + dx - selected_unit.x) + abs(proposed_y + dy - selected_unit.y) <= selected_unit.mouvement:
                                if 0 <= proposed_x + dx < GRID_COLUMNS and 0 <= proposed_y + dy < GRID_ROWS:
                                    proposed_x += dx
                                    proposed_y += dy
                        elif event.key == pygame.K_SPACE:
                            # Move to the selected cell
                            if abs(proposed_x - selected_unit.x) + abs(proposed_y - selected_unit.y) <= selected_unit.mouvement:
                                selected_unit.move(proposed_x - selected_unit.x, proposed_y - selected_unit.y, player_units + enemy_units)
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = select_next_unit()
                                break

                if len(moved_units) == len(player_units):
                    return  # End the turn

                hovered_cell = (proposed_x, proposed_y)
                self.display.flip_display(selected_unit, hovered_cell)

    def main(self):
        pygame.init()
        self.display.initialize_main_menu()
        self.display.character_choice_screen()

        while True:
            print("Phase de déplacement du Joueur A")
            self.handle_turn(self.player1_units, self.player2_units)
            print("Phase de déplacement du Joueur B")
            self.handle_turn(self.player2_units, self.player1_units)
            combat_occurred = self.check_combat()
            if not combat_occurred:
                print("Aucun combat détecté. Passage à la phase suivante.")

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie avec Combats")
    game = Game(screen)
    game.main()
