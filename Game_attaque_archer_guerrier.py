import sys
import pygame
import random
from unit_fullscreen import *
from Display import *

# Character names and image file paths (replace with actual image paths)
# Character options with their stats
# CHARACTER_OPTIONS = [
#     {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10, 10)},
#     {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 10, 4, 4, 10,10)},
#     {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 10, 2, 2, 10)},
#     {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 10, 10, 10, 10)},
#     {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10,10, 10)},
#     {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4, 10)},
#     {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2, 10)},
#     {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)}
# ]
# A terme, remplacer par vraies statistiques des personnages dans la fonction remplacer Unit par nos classes Personnages

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        self.reset_jeu = False  # Flag to indicate a reset
        self.display = Display(self.screen,self)

    def pause_menu(self):
        """Displays the pause menu with options to resume or go back to the home screen."""
        font = pygame.font.Font(None, 48)
        button_font = pygame.font.Font(None, 36)

        # Create buttons for "Resume" and "Home Screen"
        button_width = 250
        button_height = 60
        button_spacing = 40

        # Calculate button positions
        resume_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height)
        home_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height)

        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with 150 alpha for transparency

        paused = True
        while paused:
            # Draw the current game screen with the overlay
            self.screen.blit(overlay, (0, 0))

            # Draw the "Pause" title
            pause_text = font.render("Game Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))

            # Draw the "Resume" button
            pygame.draw.rect(self.screen, WHITE, resume_button)
            resume_text = button_font.render("Resume", True, BLACK)
            self.screen.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
                                           resume_button.y + (resume_button.height - resume_text.get_height()) // 2))

            # Draw the "Home Screen" button
            pygame.draw.rect(self.screen, WHITE, home_button)
            home_text = button_font.render("Home Screen", True, BLACK)
            self.screen.blit(home_text, (home_button.x + (home_button.width - home_text.get_width()) // 2,
                                         home_button.y + (home_button.height - home_text.get_height()) // 2))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if "Resume" button was clicked
                    if resume_button.collidepoint(mouse_pos):
                        paused = False  # Resume the game

                    # Check if "Home Screen" button was clicked
                    if home_button.collidepoint(mouse_pos):
                        self.reset_game()  
                        self.reset_jeu = True  # Set the reset flag to restart the main loop
                        paused = False

                if event.type == pygame.KEYDOWN:
                    # Press "Esc" to resume the game
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            pygame.display.flip()

    def reset_game(self):
        """Resets the game state for a fresh start."""
        self.player1_units = []
        self.player2_units = [] 

    def handle_player1_turn(self, selected_unit):
        hovered_cell = (selected_unit.x, selected_unit.y)
        proposed_x, proposed_y = selected_unit.x, selected_unit.y

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                    # Handle movement keys
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
                        # Confirm the move if it's within range and valid
                        final_dx = proposed_x - selected_unit.x
                        final_dy = proposed_y - selected_unit.y
                        if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                            if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                #selected_unit.is_selected = False
                                return  # Exit the function after moving the unit

                    # Update proposed cell position with arrow keys
                    if dx != 0 or dy != 0:
                        new_x = proposed_x + dx
                        new_y = proposed_y + dy
                        # Check if within movement range and grid boundaries
                        if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                            if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                proposed_x, proposed_y = new_x, new_y
                                hovered_cell = (proposed_x, proposed_y)

            # Update the display
            self.display.flip_display(selected_unit, hovered_cell)
            pygame.display.flip()

    def handle_player2_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []
        proposed_x = None
        proposed_y = None

        # Function to select the next unmoved unit automatically
        def select_next_unit():
            for unit in self.player2_units:
                if unit not in moved_units:
                    unit.is_selected = True
                    return unit
            return None  # No unmoved units remain

        # Initially select the first unmoved unit automatically
        selected_unit = select_next_unit()
        if selected_unit:
            proposed_x, proposed_y = selected_unit.x, selected_unit.y
            hovered_cell = (proposed_x, proposed_y)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                    # Only handle movement keys if we have a selected unit
                    if selected_unit:
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
                            # Confirm the move if it's within range and valid
                            final_dx = proposed_x - selected_unit.x
                            final_dy = proposed_y - selected_unit.y
                            if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                                if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                    selected_unit.is_selected = False
                                    moved_units.append(selected_unit)
                                    # Select next unit automatically
                                    selected_unit = select_next_unit()
                                    if selected_unit:
                                        proposed_x, proposed_y = selected_unit.x, selected_unit.y
                                        hovered_cell = (proposed_x, proposed_y)
                                    else:
                                        # No more units to move
                                        break

                        # If the player pressed an arrow key, update the proposed cell position
                        if dx != 0 or dy != 0 and selected_unit is not None:
                            new_x = proposed_x + dx
                            new_y = proposed_y + dy
                            # Check if within movement range
                            if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                                # Also check if within grid boundaries
                                if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                    proposed_x, proposed_y = new_x, new_y
                                    hovered_cell = (proposed_x, proposed_y)

                if event.type == pygame.MOUSEMOTION:
                    # If no unit selected, just update hovered cell for UI feedback
                    if not selected_unit:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

            # If all units have moved, end the turn
            if len(moved_units) == len(self.player2_units):
                break

            self.display.flip_display(selected_unit, hovered_cell)
     
    def handle_player1_attack(self, selected_unit):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                    if event.key == pygame.K_TAB:
                        self.display.capacity_choice(selected_unit)
                        self.display.draw_menu(selected_unit)
                    
                    if event.key == pygame.K_RETURN:
                        # Attack logic when Enter is pressed
                        attacked = False
                        for enemy in self.player2_units:
                            if selected_unit.__class__.__name__ == 'Archer' or selected_unit.__class__.__name__ == 'Magicien':
                                if (abs(selected_unit.x - enemy.x) <= selected_unit.attack_range and abs(selected_unit.y - enemy.y) == 0) or (abs(selected_unit.y - enemy.y) <= selected_unit.attack_range and abs(selected_unit.x - enemy.x) ==0):
                                    selected_unit.attack(enemy)
                                    print("archer attaque")
                                    attacked = True
                            else:
                                if abs(selected_unit.x - enemy.x) <= selected_unit.attack_range and abs(selected_unit.y - enemy.y) <= selected_unit.attack_range:
                                    selected_unit.attack(enemy)
                                    attacked = True

                            # Remove the enemy if their health is 0 or less
                            if enemy.vie <= 0:
                                self.player2_units.remove(enemy)
                            break  # Only one attack per turn

                        if not attacked:
                            print("No enemy to attack!")

                        # Mark the unit's turn as complete
                        #selected_unit.is_selected = False
                        if selected_unit.__class__.__name__ == 'Guerrier' and selected_unit.temeraire_active == True:
                            selected_unit.desactive_temeraire()
                        
                        if selected_unit.__class__.__name__ == 'Archer' and selected_unit.headshot_actif == True:
                            selected_unit.annul_headshot()
                        
                        return  # Exit the function after the attack
                    
            # Update the display
            self.display.flip_display_basic(selected_unit)
            
            # Outline possible enemies to attack in red
            for enemy in self.player2_units:
                if selected_unit.__class__.__name__ == 'Archer' or selected_unit.__class__.__name__ == 'Magicien':
                    if (abs(selected_unit.x - enemy.x) <= selected_unit.attack_range and abs(selected_unit.y - enemy.y) == 0) or (abs(selected_unit.y - enemy.y) <= selected_unit.attack_range and abs(selected_unit.x - enemy.x) ==0):
                        enemy_rect = pygame.Rect(enemy.x * CELL_SIZE, enemy.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (255, 0, 0), enemy_rect, 3)  # Red outline with 3-pixel thickness
                else:
                    if abs(selected_unit.x - enemy.x) <= selected_unit.attack_range and abs(selected_unit.y - enemy.y) <= selected_unit.attack_range:
                        enemy_rect = pygame.Rect(enemy.x * CELL_SIZE, enemy.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (255, 0, 0), enemy_rect, 3)  # Red outline with 3-pixel thickness
            
            pygame.display.flip()
         
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie")
    game = Game(screen)
    display = Display(screen,game)
    while True:
        # Display the character selection screen
        display.character_choice_screen()

        # After character selection, start the game loop
        running = True
        while running:
            # Handle player 1's turn by moving all units one by one
            for unit in game.player1_units:
                unit.is_selected = True
                game.handle_player1_turn(unit)
                game.handle_player1_attack(unit)
                unit.is_selected = False  # Deselect the unit after moving

            # Handle player 2's turn
            game.handle_player2_turn()

            # Check if the game has been reset (e.g., when returning to the main menu)
            if game.reset_jeu:
                running = False
                pygame.display.flip()
                # Exit the game loop to restart the main loop


if __name__ == "__main__":
    main()