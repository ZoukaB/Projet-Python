import sys
import pygame
import random
from unit_fullscreen import *
from Display import *
from unit_fullscreen_attack import Infirmier

# CHARACTER_OPTIONS will include Infirmier stats
CHARACTER_OPTIONS = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10, 10)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 10, 4, 4, 10)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 10, 2, 2, 10)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 10, 10, 10, 10)},
    {"name": "Infirmier", "stats": (0, 0, 3, 3, 2, 5, 3, 10, 6, 6, 10)},
    {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10, 10)},
    {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4, 10)},
    {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2, 10)},
    {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10, 10)},
]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        self.reset_jeu = False  # Flag to indicate reset
        self.display = Display(self.screen, self)

    def pause_menu(self):
        """Displays the pause menu with options to resume or go back to the home screen."""
        font = pygame.font.Font(None, 48)
        button_font = pygame.font.Font(None, 36)

        # Create buttons for "Resume" and "Home Screen"
        button_width = 250
        button_height = 60
        button_spacing = 40
        resume_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height)
        home_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height)

        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with transparency

        paused = True
        while paused:
            self.screen.blit(overlay, (0, 0))
            pause_text = font.render("Game Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))

            pygame.draw.rect(self.screen, WHITE, resume_button)
            resume_text = button_font.render("Resume", True, BLACK)
            self.screen.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2, resume_button.y + (resume_button.height - resume_text.get_height()) // 2))

            pygame.draw.rect(self.screen, WHITE, home_button)
            home_text = button_font.render("Home Screen", True, BLACK)
            self.screen.blit(home_text, (home_button.x + (home_button.width - home_text.get_width()) // 2, home_button.y + (home_button.height - home_text.get_height()) // 2))

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
            pygame.display.flip()

    def reset_game(self):
        """Resets the game state for a fresh start."""
        self.player1_units = []
        self.player2_units = []

    def handle_special_abilities(self, unit):
        """Handles special abilities for Infirmier."""
        if isinstance(unit, Infirmier):
            allies_in_range = [
                ally for ally in self.player1_units if abs(unit.x - ally.x) + abs(unit.y - ally.y) == 1 and ally.vie < ally.max_vie
            ]
            if allies_in_range:
                ally_to_heal = allies_in_range[0]
                ally_to_heal.vie = min(ally_to_heal.vie + 1, ally_to_heal.max_vie)
                self.display.show_message(f"{ally_to_heal.__class__.__name__} soigné par l'Infirmier !")

    def handle_player1_turn(self, unit):
        """Handles movement and attack for a unit during Player 1's turn."""
        hovered_cell = (unit.x, unit.y)
        proposed_x, proposed_y = unit.x, unit.y

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()
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
                        if abs(proposed_x - unit.x) + abs(proposed_y - unit.y) <= unit.mouvement:
                            if unit.move(proposed_x - unit.x, proposed_y - unit.y, self.player1_units + self.player2_units):
                                self.handle_special_abilities(unit)
                                return

                    # Update proposed cell
                    new_x, new_y = proposed_x + dx, proposed_y + dy
                    if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                        proposed_x, proposed_y = new_x, new_y
                        hovered_cell = (proposed_x, proposed_y)

            self.display.flip_display(unit, hovered_cell)

    def check_victory(self):
        """Checks if the game has ended."""
        if not self.player1_units:
            self.display.show_victory_message("Player 2 wins!")
        elif not self.player2_units:
            self.display.show_victory_message("Player 1 wins!")

    def main(self):
        """Main game loop."""
        pygame.init()
        self.display.initialize_main_menu()
        self.display.character_choice_screen()

        while True:
            for unit in self.player1_units:
                self.handle_player1_turn(unit)
            for unit in self.player2_units:
                self.handle_player1_turn(unit)  # Simplified for demo purposes
            self.check_victory()

            if self.reset_jeu:
                self.reset_game()
                self.display.initialize_main_menu()


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie avec Infirmier")
    game = Game(screen)
    game.main()