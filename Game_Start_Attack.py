import sys
import pygame
import random
from unit_fullscreen_attack import *
from Display_Attack import *

# Character names and image file paths (replace with actual image paths)
# Character options with their stats

# A terme, remplacer par vraies statistiques des personnages dans la fonction remplacer Unit par nos classes Personnages
class GameObject:
    def __init__(self, x, y, obj_type):
        self.x = x
        self.y = y
        self.obj_type = obj_type

        # Image according to object type
        if obj_type == "piedra":
            self.image = pygame.image.load("rock.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        else:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.image.fill((255, 0, 0))  # Red for unknown objects

    def draw(self, screen):
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        self.reset_jeu = False  # Flag to reset
        self.display = Display(self.screen, self)

        # Generate objects at the start of the game
        self.generate_objects()

    def generate_objects(self):
        """Generate rocks and other objects on the map."""
        for _ in range(10):  # Number of objects
            x, y = random.randint(0, GRID_COLUMNS - 1), random.randint(0, GRID_ROWS - 1)
            self.display.objects.append(GameObject(x, y, "piedra"))
    
    def is_cell_occupied(self, x, y):
        """Verify is cell is occupied by an object (like a rock)."""
        for obj in self.display.objects:  # Iterate over the map objects
            if obj.x == x and obj.y == y:
                return True  # If there is an object on the cell, returns True
        return False  # If there is not object, returns False        
    
    def check_victory(self):
        """Verify if there's a winner."""
        if not self.player1_units:
            self.display.show_victory_message("Player 2 wins!", confetti_color=(255, 0, 0))  # Red for player 2
        elif not self.player2_units:
            self.display.show_victory_message("Player 1 wins!", confetti_color=(0, 0, 255))  # Blue for player 1


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
        
    def create_units(self):
        """Crée les unités pour les deux joueurs avec les statistiques appropriées."""
        # Exemple de création d'unités pour chaque joueur
        player1_units = []
        player2_units = []

        for i, character in enumerate(CHARACTER_OPTIONS[:4]):  # Les 4 premières options pour player1
            character_stats = character["stats"]
            unit = Unit(x=i, y=i, character_stats=character_stats, team='player1')
            player1_units.append(unit)

        for i, character in enumerate(CHARACTER_OPTIONS[4:]):  # Les 4 suivantes pour player2
            character_stats = character["stats"]
            unit = Unit(x=i, y=i, character_stats=character_stats, team='player2')
            player2_units.append(unit)

        return player1_units, player2_units
        
    def handle_player1_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []
        proposed_x = None
        proposed_y = None

        # Initially do not select any unit automatically
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                    if event.key == pygame.K_TAB:
                        # Change manually between units not moved
                        unmoved_units = [unit for unit in self.player1_units if unit not in moved_units]
                        if unmoved_units:
                            current_index = unmoved_units.index(selected_unit) if selected_unit in unmoved_units else -1
                            next_index = (current_index + 1) % len(unmoved_units)
                            selected_unit = unmoved_units[next_index]
                            proposed_x, proposed_y = selected_unit.x, selected_unit.y
                            hovered_cell = (proposed_x, proposed_y)

                    # Handle movement and selection if there's a unit selected
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
                    
                        # Refresh position selected with arrow keys
                        if dx != 0 or dy != 0:
                            new_x = proposed_x + dx
                            new_y = proposed_y + dy
                            # Verify movement range and limits of the grid
                            if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                                if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                    proposed_x, proposed_y = new_x, new_y
                                    hovered_cell = (proposed_x, proposed_y)

                        # Space bar to confirm movement or prepare attack
                        if event.key == pygame.K_SPACE:
                            # Verify if it's a valid movement
                            final_dx = proposed_x - selected_unit.x
                            final_dy = proposed_y - selected_unit.y
                            if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                                if not self.is_cell_occupied(proposed_x, proposed_y):
                                    # Move unit
                                    if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                        moved_units.append(selected_unit)
                                    
                                        # Verify if enemy units are in range to attack
                                        enemies_in_range = [
                                            enemy for enemy in self.player2_units 
                                            if max(abs(enemy.x - selected_unit.x), abs(enemy.y - selected_unit.y)) <= selected_unit.range_
                                        ]
                                    
                                        if enemies_in_range:
                                            # Show message of the units that are in range
                                            self.display.show_message("Enemy units in range. Press A to select target for the attack.")
                                        
                                            # Wait for the selection of the target to attack
                                            waiting_for_attack = True
                                            selected_enemy_index = 0
                                            while waiting_for_attack:
                                                for attack_event in pygame.event.get():
                                                    if attack_event.type == pygame.KEYDOWN:
                                                        if attack_event.key == pygame.K_a:
                                                            # Select next enemy in range
                                                            selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                            self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")
                                                    
                                                        elif attack_event.key == pygame.K_SPACE:
                                                            # Confirm attack
                                                            enemy = enemies_in_range[selected_enemy_index]
                                                            damage = selected_unit.attack(enemy)
                                                            if isinstance(selected_unit, Archer):
                                                                damage = selected_unit.attack_with_animation(enemy, self, self.screen)
                                                                
                                                            if isinstance(selected_unit, Magicien):
                                                                damage = selected_unit.attack_with_animation(enemy, self, self.screen)    
                                                            else:
                                                                damage = selected_unit.attack(enemy) 
                                                            self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__}!")
                                                        
                                                            if enemy.vie <= 0:
                                                                self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                                self.player2_units.remove(enemy)
                                                                
                                                                # Verify victory after defeating a unit
                                                                self.check_victory()
                                                        
                                                            waiting_for_attack = False
                                                    
                                                        elif attack_event.key == pygame.K_ESCAPE:
                                                            waiting_for_attack = False
                                            
                                                self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("You can't move, the cell is occupied!")
                                else:
                                    self.display.show_message("You can't move, the cell is occupied by an obstacle!")        

                    # If all the units moved, finish turn
                    if len(moved_units) == len(self.player1_units):
                        return

                    self.display.flip_display(selected_unit, hovered_cell)
    
    def handle_player2_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []
        proposed_x = None
        proposed_y = None

        # Initially do not select any unit automatically
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                    if event.key == pygame.K_TAB:
                        # Change manually between units not moved
                        unmoved_units = [unit for unit in self.player2_units if unit not in moved_units]
                        if unmoved_units:
                            current_index = unmoved_units.index(selected_unit) if selected_unit in unmoved_units else -1
                            next_index = (current_index + 1) % len(unmoved_units)
                            selected_unit = unmoved_units[next_index]
                            proposed_x, proposed_y = selected_unit.x, selected_unit.y
                            hovered_cell = (proposed_x, proposed_y)

                    # Handle movement and selection if there's a unit selected
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
                    
                        # Refresh position selected with arrow keys
                        if dx != 0 or dy != 0:
                            new_x = proposed_x + dx
                            new_y = proposed_y + dy
                            # Verify if enemy units are in range to attack
                            if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                                if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                    proposed_x, proposed_y = new_x, new_y
                                    hovered_cell = (proposed_x, proposed_y)

                        # Space bar to confirm movement or prepare attack
                        if event.key == pygame.K_SPACE:
                            # Verify if it's a valid movement
                            final_dx = proposed_x - selected_unit.x
                            final_dy = proposed_y - selected_unit.y
                            if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                                if not self.is_cell_occupied(proposed_x, proposed_y):
                                    # Move unit
                                    if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                        moved_units.append(selected_unit)
                                    
                                        # Verify if enemy units are in range to attack
                                        enemies_in_range = [
                                            enemy for enemy in self.player1_units 
                                            if max(abs(enemy.x - selected_unit.x), abs(enemy.y - selected_unit.y)) <= selected_unit.range_
                                        ]
                                    
                                        if enemies_in_range:
                                            # Show message of the units that are in range
                                            self.display.show_message("Enemy units in range. Press A to select target for the attack.")
                                        
                                            # Wait for the selection of the target to attack
                                            waiting_for_attack = True
                                            selected_enemy_index = 0
                                            while waiting_for_attack:
                                                for attack_event in pygame.event.get():
                                                    if attack_event.type == pygame.KEYDOWN:
                                                        if attack_event.key == pygame.K_a:
                                                            # Select next enemy in range
                                                            selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                            self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")
                                                    
                                                        elif attack_event.key == pygame.K_SPACE:
                                                            # Confirm attack
                                                            enemy = enemies_in_range[selected_enemy_index]
                                                            damage = selected_unit.attack(enemy)
                                                            self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__}!")
                                                        
                                                            if enemy.vie <= 0:
                                                                self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                                self.player1_units.remove(enemy)
                                                                # Verify victory after defeating a unit
                                                                self.check_victory()
                                                        
                                                            waiting_for_attack = False
                                                    
                                                        elif attack_event.key == pygame.K_ESCAPE:
                                                            waiting_for_attack = False
                                            
                                                self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("You can't move, the cell is occupied!")
                                else:
                                    self.display.show_message("You can't move, the cell is occupied by an obstacle!")        

                    # If all the units moved, finish turn
                    if len(moved_units) == len(self.player2_units):
                        return

                    self.display.flip_display(selected_unit, hovered_cell)
     
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie")
    game = Game(screen)
    display = Display(screen,game)
    
    while True:
        display.initialize_main_menu()  # Start at the main menu and character selection
        display.character_choice_screen()
        # After character selection, start the game loop
        running = True
        while running:
            game.handle_player1_turn()
            game.handle_player2_turn()
            
            # Verify if there's a winner
            game.check_victory()

            # Check if the game has been reset (e.g., when returning to the main menu)
            if game.reset_jeu:
                running = False
                pygame.display.flip()
                # Exit the game loop to restart the main loop

if __name__ == "__main__":
    main()
