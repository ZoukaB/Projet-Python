import sys
import pygame
from unit_fullscreen import *
from duel import duel_phase
from tir import phase_tir
from Display import Display

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
        self.display = Display(screen, self)
        self.player1_units = []
        self.player2_units = []
        self.reset_game_flag = False

    def pause_menu(self):
        font = pygame.font.Font(None, 48)
        button_font = pygame.font.Font(None, 36)
        resume_button = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 80, 250, 60)
        home_button = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 20, 250, 60)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        paused = True

        while paused:
            self.screen.blit(overlay, (0, 0))
            pause_text = font.render("Game Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))
            pygame.draw.rect(self.screen, WHITE, resume_button)
            pygame.draw.rect(self.screen, WHITE, home_button)
            resume_text = button_font.render("Resume", True, BLACK)
            home_text = button_font.render("Home Screen", True, BLACK)
            self.screen.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2, resume_button.y + 10))
            self.screen.blit(home_text, (home_button.x + (home_button.width - home_text.get_width()) // 2, home_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_button.collidepoint(mouse_pos):
                        paused = False
                    if home_button.collidepoint(mouse_pos):
                        self.reset_game()
                        self.reset_game_flag = True
                        paused = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            pygame.display.flip()

    def reset_game(self):
        self.player1_units = []
        self.player2_units = []

    def handle_turn(self, player_units, opponent_units):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                if selected_unit and event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    elif event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_SPACE:
                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if selected_unit.move(dx, dy, player_units + opponent_units):
                                moved_units.append(selected_unit)
                                selected_unit.is_selected = False
                                selected_unit = None

                    elif event.key == pygame.K_RETURN and selected_unit:
                        if isinstance(selected_unit, Archer):
                            phase_tir(self.display, selected_unit, opponent_units)
                        else:
                            for unit in opponent_units:
                                if abs(unit.x - selected_unit.x) + abs(unit.y - selected_unit.y) == 1:
                                    duel_phase(self.display, selected_unit, unit)
                                    break

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

                if len(moved_units) == len(player_units):
                    return

            self.display.flip_display(selected_unit, hovered_cell)

    def main(self):
        pygame.init()
        while True:
            self.display.initialize_main_menu()
            self.display.character_choice_screen()
            running = True
            while running:
                self.handle_turn(self.player1_units, self.player2_units)
                self.handle_turn(self.player2_units, self.player1_units)
                if self.reset_game_flag:
                    running = False

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Jeu de stratégie")
    game = Game(screen)
    game.main()
