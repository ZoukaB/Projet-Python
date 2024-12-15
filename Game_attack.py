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

        # Image object type
        if obj_type == "piedra":
            self.image = pygame.image.load("rock.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        else:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.image.fill((255, 0, 0))  # unknown objects in red color

    def draw(self, screen):
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        self.reset_jeu = False  # Flag pto reset
        self.display = Display(self.screen, self)

        # Generate objects at the beginning of the game
        self.generate_objects()

    def generate_objects(self):
        """Generate rocks and other objects on the map."""
        for _ in range(10):  # Number of objects
            x, y = random.randint(0, GRID_COLUMNS - 1), random.randint(0, GRID_ROWS - 1)
            self.display.objects.append(GameObject(x, y, "piedra"))
    
    def is_cell_occupied(self, x, y):
        """Verify if cell is occupied by an object (like a rock)."""
        for obj in self.display.objects:  # Itera on the objects on the map
            if obj.x == x and obj.y == y:
                return True  # If there is an object, return True
        return False  # If there is not, return False        
    
    def execute_critical_bite(self, assassin, enemy):
        """Execute the ability ‘Critical Fang’."""
        if assassin and enemy:
            # BLower half of the enemy's life for 3 turns.
            initial_hp = enemy.vie
            damage = initial_hp // 2
            enemy.vie -= damage  # Apply initial damage

            # Show message about critical damage
            self.display.show_message(f"{assassin.__class__.__name__} used Critical Fang in {enemy.__class__.__name__}! {damage} reduced life points.")
            
            # We can add a way to storage duration time in which the enemy will be under this weakness
            enemy.critical_bite_turns = 3  # The enemy will be debuffed for 3 turns.
            enemy.initial_hp = initial_hp  # Save initial life for later restoration

    def handle_turn(self):
        # Logic to manage turns
        selected_unit = self.player1_units[0]  # Select unit 
        selected_enemy = self.player2_units[0]  # Select enemy

        # If the player uses Critical fang
        if isinstance(selected_unit, Assassin):
            self.execute_critical_bite(selected_unit, selected_enemy)
    
            
                
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

        for i, character in enumerate(CHARACTER_OPTIONS_p1[:4]):  # Les 4 premières options pour player1
            character_stats = character["stats"]
            unit = Unit(x=i, y=i, character_stats=character_stats, team='player1')
            player1_units.append(unit)

        for i, character in enumerate(CHARACTER_OPTIONS_p2[4:]):  # Les 4 suivantes pour player2
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

        def select_next_unit():
            unmoved_units = [unit for unit in self.player1_units if unit not in moved_units]
            if unmoved_units:
                return unmoved_units[0]
            return None

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

                    if event.key == pygame.K_TAB:
                        unmoved_units = [unit for unit in self.player1_units if unit not in moved_units]
                        if unmoved_units:
                            current_index = unmoved_units.index(selected_unit) if selected_unit in unmoved_units else -1
                            next_index = (current_index + 1) % len(unmoved_units)
                            selected_unit = unmoved_units[next_index]
                            proposed_x, proposed_y = selected_unit.x, selected_unit.y
                            hovered_cell = (proposed_x, proposed_y)
                            
                    if selected_unit:
                        # Show action options when unit is selected
                        self.display.show_message("What do you want to do? Move (M), Attack (A), Ability (H)")
                        if event.key == pygame.K_m:
                            self.display.show_message(f"You selected move with {selected_unit.__class__.__name__}. Use arrow keys to select destination.")
                            while True:
                                for move_event in pygame.event.get():
                                    if move_event.type == pygame.KEYDOWN:
                                        dx, dy = 0, 0
                                        if move_event.key == pygame.K_UP:
                                            dy = -1
                                        elif move_event.key == pygame.K_DOWN:
                                            dy = 1
                                        elif move_event.key == pygame.K_LEFT:
                                            dx = -1
                                        elif move_event.key == pygame.K_RIGHT:
                                            dx = 1

                                        if dx != 0 or dy != 0:
                                            new_x = proposed_x + dx
                                            new_y = proposed_y + dy
                                            if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                                                if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                                    proposed_x, proposed_y = new_x, new_y
                                                    hovered_cell = (proposed_x, proposed_y)

                                        elif move_event.key == pygame.K_SPACE:
                                            final_dx = proposed_x - selected_unit.x
                                            final_dy = proposed_y - selected_unit.y
                                            if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                                                if not self.is_cell_occupied(proposed_x, proposed_y):
                                                    if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                                        moved_units.append(selected_unit)
                                                        selected_unit = select_next_unit()
                                                        return
                                                    else:
                                                        self.display.show_message("You can't move, cell is occupied!")
                                                else:
                                                    self.display.show_message("You can't move, cell is occupied by an obstacle!")
                                                break

                                    self.display.flip_display(selected_unit, hovered_cell)

                        elif event.key == pygame.K_a:
                            enemies_in_range = [
                                enemy for enemy in self.player2_units
                                if max(abs(enemy.x - selected_unit.x), abs(enemy.y - selected_unit.y)) <= selected_unit.range_
                            ]
                            if enemies_in_range:
                                self.display.show_message("Enemies in range. Press A to select target.")
                                selected_enemy_index = 0
                                while True:
                                    for attack_event in pygame.event.get():
                                        if attack_event.type == pygame.KEYDOWN:
                                            if attack_event.key == pygame.K_a:
                                                selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                            elif attack_event.key == pygame.K_SPACE:
                                                enemy = enemies_in_range[selected_enemy_index]
                                                if isinstance(selected_unit, Archer):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)
                                                elif isinstance(selected_unit, Magicien):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)
                                                elif isinstance(selected_unit, Guerrier):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)    
                                                elif isinstance(selected_unit, Assassin):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)     
                                                else:
                                                    damage = selected_unit.attack(enemy)

                                                self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__}!")

                                                if enemy.vie <= 0:
                                                    self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                    self.player2_units.remove(enemy)
                                                    self.check_victory()

                                                moved_units.append(selected_unit)
                                                selected_unit = select_next_unit()
                                                return

                                            elif attack_event.key == pygame.K_ESCAPE:
                                                return
                            else:
                                self.display.show_message("No enemies in range to attack.")
                                return

                        elif event.key == pygame.K_h:
                            # Special skill for different units
                            if isinstance(selected_unit, Magicien):
                                # Healing Magicien
                                if "Healing Potion" in selected_unit.abilities:
                                    heal_amount = selected_unit.heal()
                                    self.display.show_message(f"{selected_unit.__class__.__name__} healed {heal_amount} life points.")
                                    moved_units.append(selected_unit)  # Add to the list of moved units
                                    selected_unit = select_next_unit()  # Change to the next available unit
                                    return
                                else:
                                    self.display.show_message("No skills available.")
                                    return

                            elif isinstance(selected_unit, Guerrier):
                                # Special skill for Guerrier
                                if "Powerful Blow" in selected_unit.abilities:
                                    # Activate selection mode for Powerful Blow
                                    self.display.show_message("Who do you want to throw the Powerful Blow at? Use A/D to select target and  bar space to execute.")
                                    
                                    # List of enemies in range
                                    enemies_in_range = self.player2_units  # All enemies

                                    if enemies_in_range:
                                        selected_enemy_index = 0  # First enemy
                                        selection_mode = True  # Activate selection mode

                                        while selection_mode:
                                            # Show selected target
                                            self.display.show_message(f"Selected target: {enemies_in_range[selected_enemy_index].__class__.__name__}")
                                            
                                            for attack_event in pygame.event.get():
                                                if attack_event.type == pygame.KEYDOWN:
                                                    if attack_event.key == pygame.K_a:
                                                        # Select next target
                                                        selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                        self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_d:
                                                        # Select previous enemy
                                                        selected_enemy_index = (selected_enemy_index - 1) % len(enemies_in_range)
                                                        self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_SPACE:
                                                        # Use Powerful Blow
                                                        enemy = enemies_in_range[selected_enemy_index]
                                                        
                                                        # Apply 8 of damage to the enemy
                                                        damage = 8  # Powerful Blow inflicts 8 of damage
                                                        enemy.vie -= damage
                                                        self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__} with Powerful Blow!")

                                                        if enemy.vie <= 0:
                                                            self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                            self.player2_units.remove(enemy)
                                                            self.check_victory()

                                                        moved_units.append(selected_unit)  # Add to the list of moved units
                                                        selected_unit = select_next_unit()  # Change to the next available unit
                                                        selection_mode = False  # Exit selection mode
                                                        return
                                                    
                                                    elif attack_event.key == pygame.K_ESCAPE:
                                                        # Cancel skill of Powerful Blow
                                                        self.display.show_message("You cancelled the Powerful Blow ability.")
                                                        selection_mode = False  # Exit selection mode
                                                        return

                                            # Make sure to update the display and events correctly.
                                            self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("No enemies available for Powerful Blow.")
                            elif isinstance(selected_unit, Archer):
                                # Special skill for the Archer: Flecha Curatoria / Healing arrow
                                if "Healing Arrow" in selected_unit.abilities:
                                    self.display.show_message("Who do you want to heal with the Healing Arrow? Use A/D to select target and space bar to execute")
                                    
                                    # Filter allies between the range of the archer
                                    allies_in_range = [ally for ally in self.player1_units if ally != selected_unit and
                                                    max(abs(ally.x - selected_unit.x), abs(ally.y - selected_unit.y)) <= selected_unit.range_]

                                    if allies_in_range:
                                        selected_ally_index = 0  # Starts with first ally
                                        selection_mode = True  # Activate selection mode 

                                        while selection_mode:
                                            # Show selected ally
                                            self.display.show_message(f"Selected ally: {allies_in_range[selected_ally_index].__class__.__name__}")
                                            
                                            for attack_event in pygame.event.get():
                                                if attack_event.type == pygame.KEYDOWN:
                                                    if attack_event.key == pygame.K_a:
                                                        # Select next ally
                                                        selected_ally_index = (selected_ally_index + 1) % len(allies_in_range)
                                                        self.display.show_message(f"Ally: {allies_in_range[selected_ally_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_d:
                                                        # Select previous ally
                                                        selected_ally_index = (selected_ally_index - 1) % len(allies_in_range)
                                                        self.display.show_message(f"Ally: {allies_in_range[selected_ally_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_SPACE:
                                                        # Heal selected ally
                                                        ally = allies_in_range[selected_ally_index]
                                                        
                                                        # Healing
                                                        heal_amount = selected_unit.heal_with_arrow(ally)
                                                        self.display.show_message(f"{selected_unit.__class__.__name__} healed {ally.__class__.__name__} with Healing Arrow! {heal_amount} life points recovered.")

                                                        moved_units.append(selected_unit)  # Add to the list of moved units
                                                        selected_unit = select_next_unit()  # Change to the next available unit
                                                        selection_mode = False  # Exit selection mode
                                                        return
                                                    
                                                    elif attack_event.key == pygame.K_ESCAPE:
                                                        # Cancel healing
                                                        self.display.show_message("You cancelled Healing.")
                                                        selection_mode = False  # Exit selection mode
                                                        return

                                            # Make sure to update the display and events correctly.
                                            self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("No available allies to heal.")
                            for unit in self.player1_units:
                                if isinstance(unit, Assassin):
                                    if "Critical Fang" in unit.abilities:
                                        self.display.show_message("Who do you want to attack with Critical Fang? Use A/D to select target and space bar to execute.")
                                        
                                        enemies_in_range = [enemy for enemy in self.player2_units if
                                                            max(abs(enemy.x - unit.x), abs(enemy.y - unit.y)) <= unit.range_]

                                        if enemies_in_range:
                                            selected_enemy_index = 0  # Start with first enemy
                                            selection_mode = True  # Active selection mode

                                            while selection_mode:
                                                selected_enemy = enemies_in_range[selected_enemy_index]
                                                self.display.show_message(f"Selected target: {selected_enemy.__class__.__name__}")
                                                
                                                for attack_event in pygame.event.get():
                                                    if attack_event.type == pygame.KEYDOWN:
                                                        if attack_event.key == pygame.K_a:
                                                            # Select next enemy
                                                            selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                            selected_enemy = enemies_in_range[selected_enemy_index]
                                                            self.display.show_message(f"Selected target: {selected_enemy.__class__.__name__}")
                                                        elif attack_event.key == pygame.K_d:
                                                            # Select previous enemy
                                                            selected_enemy_index = (selected_enemy_index - 1) % len(enemies_in_range)
                                                            selected_enemy = enemies_in_range[selected_enemy_index]
                                                            self.display.show_message(f"Selected target: {selected_enemy.__class__.__name__}")
                                                        elif attack_event.key == pygame.K_SPACE:
                                                            # Ejxecute 'Critical Fang'
                                                            self.execute_critical_bite(unit, selected_enemy)
                                                            selection_mode = False  # Exit selection mode
                                                            break
                                                        elif attack_event.key == pygame.K_ESCAPE:
                                                            # Cancel skill
                                                            self.display.show_message("You cancelled the Critical Fang skill.")
                                                            selection_mode = False  # Exit selection mode
                                                            break
                                                
                                                # Update screen
                                                self.display.flip_display(unit, hovered_cell)
                                        else:
                                            self.display.show_message("No available enemies to attack.")
                                    
                        def execute_critical_bite(self, selected_unit, selected_enemy):
                            """ Execute damage of Critical Fang to an enemy """
                            original_health = selected_enemy.vie  # Store original life of the enemy
                            
                            # Apply life reduction
                            reduced_health = original_health // 2
                            selected_enemy.vie = reduced_health
                            selected_enemy.turns_remaining = 3  # Indicate that the reduction will last for 3 shifts

                            # Show execution message
                            self.display.show_message(f"{selected_unit.__class__.__name__} used Critical Fang {selected_enemy.__class__.__name__}! {selected_enemy.__class__.__name__} now has {reduced_health} life points for 3 turns.")
                            
                            # Add the unit to the list of moves and select the next unit
                            self.moved_units.append(selected_unit)
                            selected_unit = self.select_next_unit()  # Change to the next available unit

                        def update_turns(self):
                            """Updates turns and restores enemy health where appropriate."""
                            for unit in self.player2_units:
                                if hasattr(unit, 'turns_remaining') and unit.turns_remaining > 0:
                                    unit.turns_remaining -= 1
                                    # If the shift counter reaches 0, restore life.
                                    if unit.turns_remaining == 0:
                                        unit.vie = unit.max_vie  # Restoring life to the fullest
                                        self.display.show_message(f"{unit.__class__.__name__} has regained its full life.")
          
                                
                                        
                    unmoved_units = [unit for unit in self.player1_units if unit not in moved_units]
                    if not unmoved_units:
                        self.display.show_message("Player 1's turn completed.")
                        return

                self.display.flip_display(selected_unit, hovered_cell)

    
    def handle_player2_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []
        proposed_x = None
        proposed_y = None

        def select_next_unit():
            unmoved_units = [unit for unit in self.player2_units if unit not in moved_units]
            if unmoved_units:
                return unmoved_units[0]
            return None

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

                    if event.key == pygame.K_TAB:
                        unmoved_units = [unit for unit in self.player2_units if unit not in moved_units]
                        if unmoved_units:
                            current_index = unmoved_units.index(selected_unit) if selected_unit in unmoved_units else -1
                            next_index = (current_index + 1) % len(unmoved_units)
                            selected_unit = unmoved_units[next_index]
                            proposed_x, proposed_y = selected_unit.x, selected_unit.y
                            hovered_cell = (proposed_x, proposed_y)
                            
                    if selected_unit:
                        # Show action options when unit is selected
                        self.display.show_message("What do you want to do? Move (M), Attack (A), Ability (H)")
                        if event.key == pygame.K_m:
                            self.display.show_message(f"You selected move with {selected_unit.__class__.__name__}. Use arrow keys to select destination.")
                            while True:
                                for move_event in pygame.event.get():
                                    if move_event.type == pygame.KEYDOWN:
                                        dx, dy = 0, 0
                                        if move_event.key == pygame.K_UP:
                                            dy = -1
                                        elif move_event.key == pygame.K_DOWN:
                                            dy = 1
                                        elif move_event.key == pygame.K_LEFT:
                                            dx = -1
                                        elif move_event.key == pygame.K_RIGHT:
                                            dx = 1

                                        if dx != 0 or dy != 0:
                                            new_x = proposed_x + dx
                                            new_y = proposed_y + dy
                                            if (abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)) <= selected_unit.mouvement:
                                                if 0 <= new_x < GRID_COLUMNS and 0 <= new_y < GRID_ROWS:
                                                    proposed_x, proposed_y = new_x, new_y
                                                    hovered_cell = (proposed_x, proposed_y)

                                        elif move_event.key == pygame.K_SPACE:
                                            final_dx = proposed_x - selected_unit.x
                                            final_dy = proposed_y - selected_unit.y
                                            if abs(final_dx) + abs(final_dy) <= selected_unit.mouvement:
                                                if not self.is_cell_occupied(proposed_x, proposed_y):
                                                    if selected_unit.move(final_dx, final_dy, self.player1_units + self.player2_units):
                                                        moved_units.append(selected_unit)
                                                        selected_unit = select_next_unit()
                                                        return
                                                    else:
                                                        self.display.show_message("You can't move, cell is occupied!")
                                                else:
                                                    self.display.show_message("You can't move, cell is occupied by an obstacle!")
                                                break

                                    self.display.flip_display(selected_unit, hovered_cell)

                        elif event.key == pygame.K_a:
                            enemies_in_range = [
                                enemy for enemy in self.player1_units
                                if max(abs(enemy.x - selected_unit.x), abs(enemy.y - selected_unit.y)) <= selected_unit.range_
                            ]
                            if enemies_in_range:
                                self.display.show_message("Enemies in range. Press A to select target.")
                                selected_enemy_index = 0
                                while True:
                                    for attack_event in pygame.event.get():
                                        if attack_event.type == pygame.KEYDOWN:
                                            if attack_event.key == pygame.K_a:
                                                selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                            elif attack_event.key == pygame.K_SPACE:
                                                enemy = enemies_in_range[selected_enemy_index]
                                                if isinstance(selected_unit, Archer):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)
                                                elif isinstance(selected_unit, Magicien):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)
                                                elif isinstance(selected_unit, Guerrier):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)    
                                                elif isinstance(selected_unit, Assassin):
                                                    damage = selected_unit.attack_with_animation(enemy, self, self.screen)     
                                                else:
                                                    damage = selected_unit.attack(enemy)

                                                self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__}!")

                                                if enemy.vie <= 0:
                                                    self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                    self.player1_units.remove(enemy)
                                                    self.check_victory()

                                                moved_units.append(selected_unit)
                                                selected_unit = select_next_unit()
                                                return

                                            elif attack_event.key == pygame.K_ESCAPE:
                                                return
                            else:
                                self.display.show_message("No enemies in range to attack.")
                                return

                        elif event.key == pygame.K_h:
                            # Special skill for the units
                            if isinstance(selected_unit, Magicien):
                                # Healing Magicien
                                if "Healing Potion" in selected_unit.abilities:
                                    heal_amount = selected_unit.heal()
                                    self.display.show_message(f"{selected_unit.__class__.__name__} healed {heal_amount} life points.")
                                    moved_units.append(selected_unit)  # Add to the list of moved units
                                    selected_unit = select_next_unit()  # Change to the next available unit
                                    return
                                else:
                                    self.display.show_message("No skills available.")
                                    return

                            elif isinstance(selected_unit, Guerrier):
                                # Special skill of Guerrier
                                if "Powerful Blow" in selected_unit.abilities:
                                    # Activate selection mode for the Powerful Blow
                                    self.display.show_message("Who do you want to throw the Powerful Blow at? Use A/D to select target and  bar space to execute.")
                                    
                                    # List of enemies in range
                                    enemies_in_range = self.player1_units  # All enemies

                                    if enemies_in_range:
                                        selected_enemy_index = 0  # Start with first enemy
                                        selection_mode = True  # Activate selection mode

                                        while selection_mode:
                                            # Show selected enemy
                                            self.display.show_message(f"Selected target: {enemies_in_range[selected_enemy_index].__class__.__name__}")
                                            
                                            for attack_event in pygame.event.get():
                                                if attack_event.type == pygame.KEYDOWN:
                                                    if attack_event.key == pygame.K_a:
                                                        # Select next enemy
                                                        selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                        self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_d:
                                                        # Select previous enemy
                                                        selected_enemy_index = (selected_enemy_index - 1) % len(enemies_in_range)
                                                        self.display.show_message(f"Target: {enemies_in_range[selected_enemy_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_SPACE:
                                                        # Use Powerful Blow
                                                        enemy = enemies_in_range[selected_enemy_index]
                                                        
                                                        # Apply 8 of damage to the enemy
                                                        damage = 8  # Powerful Blow inflicts 8 of damage
                                                        enemy.vie -= damage
                                                        self.display.show_message(f"{selected_unit.__class__.__name__} inflicted {damage} of damage to {enemy.__class__.__name__} with Powerful Blow!")

                                                        if enemy.vie <= 0:
                                                            self.display.show_message(f"{enemy.__class__.__name__} was defeated!")
                                                            self.player1_units.remove(enemy)
                                                            self.check_victory()

                                                        moved_units.append(selected_unit)  # Add to the list of moved units
                                                        selected_unit = select_next_unit()  # Change to the next available unit
                                                        selection_mode = False  # Exit selection mode
                                                        return
                                                    
                                                    elif attack_event.key == pygame.K_ESCAPE:
                                                        # Cancel skill of Powerful Blow
                                                        self.display.show_message("You cancelled the Powerful Blow skill.")
                                                        selection_mode = False  # Exit selection mode
                                                        return

                                            # Make sure to update the display and events correctly.
                                            self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("No available enemies for Powerful Blow.")
                            elif isinstance(selected_unit, Archer):
                                # Special skill for Archer: Flecha Curatoria / Healing arrow
                                if "Healing Arrow" in selected_unit.abilities:
                                    self.display.show_message("Who do you want to heal with the Healing Arrow? Use A/D to select target and space bar to execute.")
                                    
                                    # Filter allies between the range of the archer
                                    allies_in_range = [ally for ally in self.player2_units if ally != selected_unit and
                                                    max(abs(ally.x - selected_unit.x), abs(ally.y - selected_unit.y)) <= selected_unit.range_]

                                    if allies_in_range:
                                        selected_ally_index = 0  # Start with first ally
                                        selection_mode = True  # Activate selection mode

                                        while selection_mode:
                                            # Show selected ally
                                            self.display.show_message(f"Selected ally: {allies_in_range[selected_ally_index].__class__.__name__}")
                                            
                                            for attack_event in pygame.event.get():
                                                if attack_event.type == pygame.KEYDOWN:
                                                    if attack_event.key == pygame.K_a:
                                                        # Select next ally
                                                        selected_ally_index = (selected_ally_index + 1) % len(allies_in_range)
                                                        self.display.show_message(f"Ally: {allies_in_range[selected_ally_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_d:
                                                        # Select previous ally
                                                        selected_ally_index = (selected_ally_index - 1) % len(allies_in_range)
                                                        self.display.show_message(f"Ally: {allies_in_range[selected_ally_index].__class__.__name__}")

                                                    elif attack_event.key == pygame.K_SPACE:
                                                        # Heal selected ally
                                                        ally = allies_in_range[selected_ally_index]
                                                        
                                                        # Heal
                                                        heal_amount = selected_unit.heal_with_arrow(ally)
                                                        self.display.show_message(f"{selected_unit.__class__.__name__} healed {ally.__class__.__name__} with Healing Arrow! {heal_amount} life points recovered.")

                                                        moved_units.append(selected_unit)  # Add to the list of moved units
                                                        selected_unit = select_next_unit()  # Change to the next available unit
                                                        selection_mode = False  # Exit selection mode
                                                        return
                                                    
                                                    elif attack_event.key == pygame.K_ESCAPE:
                                                        # Cancel healing
                                                        self.display.show_message("You canceled Healing skill.")
                                                        selection_mode = False  # Exit selection mode
                                                        return

                                            # Make sure to update the display and events correctly.
                                            self.display.flip_display(selected_unit, hovered_cell)
                                    else:
                                        self.display.show_message("No available allies to heal.")
                            for unit in self.player2_units:
                                if isinstance(unit, Assassin):
                                    if "Critical Fang" in unit.abilities:
                                        self.display.show_message("Who do you want to attack with Critical Fang? Use A/D to select target and space bar to execute.")
                                        
                                        enemies_in_range = [enemy for enemy in self.player1_units if
                                                            max(abs(enemy.x - unit.x), abs(enemy.y - unit.y)) <= unit.range_]

                                        if enemies_in_range:
                                            selected_enemy_index = 0  # Start with first enemy
                                            selection_mode = True  # Activate selection mode

                                            while selection_mode:
                                                selected_enemy = enemies_in_range[selected_enemy_index]
                                                self.display.show_message(f"Selected enemy: {selected_enemy.__class__.__name__}")
                                                
                                                for attack_event in pygame.event.get():
                                                    if attack_event.type == pygame.KEYDOWN:
                                                        if attack_event.key == pygame.K_a:
                                                            # Select next enemy
                                                            selected_enemy_index = (selected_enemy_index + 1) % len(enemies_in_range)
                                                            selected_enemy = enemies_in_range[selected_enemy_index]
                                                            self.display.show_message(f"Selected enemy: {selected_enemy.__class__.__name__}")
                                                        elif attack_event.key == pygame.K_d:
                                                            # Select previous enemy
                                                            selected_enemy_index = (selected_enemy_index - 1) % len(enemies_in_range)
                                                            selected_enemy = enemies_in_range[selected_enemy_index]
                                                            self.display.show_message(f"Selected enemy: {selected_enemy.__class__.__name__}")
                                                        elif attack_event.key == pygame.K_SPACE:
                                                            # Execute Critical Fang
                                                            self.execute_critical_bite(unit, selected_enemy)
                                                            selection_mode = False  # Exit selection mode
                                                            break
                                                        elif attack_event.key == pygame.K_ESCAPE:
                                                            # Cancel skill
                                                            self.display.show_message("You cancelled the Critical Fang skill.")
                                                            selection_mode = False  # Exit selection mode
                                                
                                                # Update screen
                                                self.display.flip_display(unit, hovered_cell)
                                        else:
                                            self.display.show_message("No available enemies to attack.")
                                    
                        def execute_critical_bite(self, selected_unit, selected_enemy):
                            """ Execute Critical Fang damage on an enemy"""
                            original_health = selected_enemy.vie  # Save the original life of the enemy
                            
                            # Apply life reduction by half
                            reduced_health = original_health // 2
                            selected_enemy.vie = reduced_health
                            selected_enemy.turns_remaining = 3  # Indicate that the reduction will last for 3 shifts.

                            # Show execution message
                            self.display.show_message(f"{selected_unit.__class__.__name__} used Critical Fang {selected_enemy.__class__.__name__}! {selected_enemy.__class__.__name__} now has {reduced_health} life points for 3 turns.")
                            
                            # Add the unit to the list of moves and select the next unit
                            self.moved_units.append(selected_unit)
                            selected_unit = self.select_next_unit()  # Change to the next available unit

                        def update_turns(self):
                            """Updates turns and restores enemies' health when appropriate."""
                            for unit in self.player1_units:
                                if hasattr(unit, 'turns_remaining') and unit.turns_remaining > 0:
                                    unit.turns_remaining -= 1
                                    # If the shift counter reaches 0, restore life.
                                    if unit.turns_remaining == 0:
                                        unit.vie = unit.max_vie  # Restoring life to the fullest
                                        self.display.show_message(f"{unit.__class__.__name__} has regained its full life.")
          
                                
                                        
                    unmoved_units = [unit for unit in self.player1_units if unit not in moved_units]
                    if not unmoved_units:
                        self.display.show_message("Player 2's turn completed.")
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
