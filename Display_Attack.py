import sys
import pygame
import random
from unit_fullscreen_attack import *

CHARACTER_OPTIONS_p1 = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
]

CHARACTER_OPTIONS_p2 = [
    {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
]

TEXT_COLOR = (255, 255, 255)  # color white for the text
class Display:
    def __init__(self,screen,game): 
        self.BUTTON_COLOR = (0, 255, 0)  # Define the colour of the button here
        
        self.screen = screen
        self.game = game
        # Load the background image (replace with the actual image path)
        self.background_image = pygame.image.load("background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
        self.objects = []  # List of objects 
        # initialize font
        self.font = pygame.font.Font(None, 74)  # default size
        self.small_font = pygame.font.Font(None, 36)  # add a small font if needed
        self.message = ""  # initialize attribute 'message'
        self.message_timer = 0 
        
        
        # Load background image for the board
        self.BoardBackground = pygame.image.load("backgroundGame.png").convert()
        self.BoardBackground = pygame.transform.scale(self.BoardBackground, (WIDTH,HEIGHT))
        
        # Load character images (replace with actual image paths)
        self.character_images = {
            "Guerrier": pygame.image.load("Images_persos/Warrior1.png").convert_alpha(),
            "Archer": pygame.image.load("Images_persos/Archer1.png").convert_alpha(),
            "Magicien": pygame.image.load("Images_persos/Wizard1.png").convert_alpha(),
            "Assassin": pygame.image.load("Images_persos/Assasin1.png").convert_alpha(),
            "Guerrier2": pygame.image.load("Images_persos/Warrior2.png").convert_alpha(),
            "Archer2": pygame.image.load("Images_persos/Archer2.png").convert_alpha(),
            "Magicien2": pygame.image.load("Images_persos/Wizard2.png").convert_alpha(),
            "Assassin2": pygame.image.load("Images_persos/Assasin2.png").convert_alpha(),
        }
        
    def draw_semi_transparent_background(self):
        """Draws a semi-transparent background image."""
        # Create a semi-transparent surface
        transparent_surface = self.background_image.copy()
        transparent_surface.set_alpha(128)  # 50% opacity (0 = fully transparent, 255 = fully opaque)

        # Blit the semi-transparent background onto the screen
        self.screen.blit(transparent_surface, (0, 0))
        
    def initialize_main_menu(self):
        """Displays the main menu with options to view rules, character powers, and start the game."""
        # Font for title and buttons
        title_font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 36)

        # Buttons for the main menu
        rules_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
        powers_button = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 50)
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

        # Main loop for the main menu
        running = True
        while running:
            #self.screen.fill(BLACK)
            self.draw_semi_transparent_background()  # Draw the semi-transparent background

            # Draw the game title
            title_text = title_font.render("Mon Jeu de Stratégie", True, WHITE)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

            # Draw the buttons
            pygame.draw.rect(self.screen, WHITE, rules_button)
            pygame.draw.rect(self.screen, WHITE, powers_button)
            pygame.draw.rect(self.screen, WHITE, start_button)

            rules_text = button_font.render("Règles du Jeu", True, BLACK)
            powers_text = button_font.render("Pouvoirs des Personnages", True, BLACK)
            start_text = button_font.render("Démarrer", True, BLACK)

            self.screen.blit(rules_text, (rules_button.x + (rules_button.width - rules_text.get_width()) // 2, rules_button.y + 10))
            self.screen.blit(powers_text, (powers_button.x + (powers_button.width - powers_text.get_width()) // 2, powers_button.y + 10))
            self.screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 10))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if rules_button.collidepoint(mouse_pos):
                        self.show_rules()

                    if powers_button.collidepoint(mouse_pos):
                        self.show_powers()

                    if start_button.collidepoint(mouse_pos):
                        running = False  # Proceed to the character choice menu
                        
            pygame.display.flip()
    
    def show_rules(self):
        """Displays the game rules screen centered in the middle of the screen."""
        font = pygame.font.Font(None, 32)  # Slightly larger font size for better readability
        back_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

        # List of rules to display
        rules_text_lines = [
            "Règles du Jeu:",
            "1. Chaque joueur choisit 2 personnages dans l'écran de sélection. Chaque personnage possède des statistiques et capacités spéciales propre.",
            "2. Les joueurs déplacent leurs unités à tour de rôle à l'aide des flèches et de la commande espace. S'ils sont dans la range équivalente, ils peuvent ensuite lancer une attaque ou charger un ennemi ",
            "3. L'objectif est de vaincre les deux unités adverses.",
        ]

        # Calculate the total height of the text block
        line_height = font.get_height() + 10
        total_text_height = len(rules_text_lines) * line_height

        # Calculate starting y-position to center the text vertically
        start_y = (HEIGHT - total_text_height) // 2

        running = True
        while running:
            self.screen.fill(BLACK)

            # Display the rules text centered
            for i, line in enumerate(rules_text_lines):
                text_surface = font.render(line, True, WHITE)
                text_x = (WIDTH - text_surface.get_width()) // 2  # Center horizontally
                text_y = start_y + i * line_height  # Line spacing
                self.screen.blit(text_surface, (text_x, text_y))

            # Draw back button
            pygame.draw.rect(self.screen, WHITE, back_button)
            back_text = font.render("Retour", True, BLACK)
            self.screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                         back_button.y + (back_button.height - back_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(mouse_pos):
                        running = False  # Go back to the main menu

            pygame.display.flip()
    
    def show_powers(self):
        
        """Displays the character powers screen."""
        font = pygame.font.Font(None, 28)
        back_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

        running = True
        while running:
            self.screen.fill(BLACK)

            # Display character powers text
            powers_text_lines = [
                "Pouvoirs des Personnages:",
                "Guerrier: Puissant en attaque rapprochée. Il a des potions pour décupler sa vitalité et peut sacrifier de l'énergie pour plus de létalité",
                "Archer: Spécialiste des attaques à distance. Il a concocté des flèches aux pouvoirs régénérateurs pour ses alliées et d'autres bien plus mortelles pour ses ennemis",
                "Magicien: Adepte de sortilèges mortifère. Dans son arsenal magique, il possède une boule de feu et une vapeur empoisonnée",
                "Assassin: Roublard agile et rusé. Il préférera peut être s'enfuir d'un combat désavantageux, mais s'il décide vraiment de combattre, une seule petite blessure lui suffira pour tuer son ennemi",
            ]

            for i, line in enumerate(powers_text_lines):
                text_surface = font.render(line, True, WHITE)
                self.screen.blit(text_surface, (50, 100 + i * 40))

            # Draw back button
            pygame.draw.rect(self.screen, WHITE, back_button)
            back_text = font.render("Retour", True, BLACK)
            self.screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                         back_button.y + (back_button.height - back_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(mouse_pos):
                        running = False  # Go back to the main menu

            pygame.display.flip()
        
    def character_choice_screen(self):
        # Font for button and text
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 32)
        
        # Button to go back to the menu
        back_button = pygame.Rect(WIDTH - 170, HEIGHT - 70, 140, 50)

        # Button for starting the game
        start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 60)

        # Resize character images to fit larger squares
        IMAGE_SIZE = 120  # New image size (increased from 100)
        for key in self.character_images:
            self.character_images[key] = pygame.transform.scale(self.character_images[key], (IMAGE_SIZE, IMAGE_SIZE))

        # Positions for Player 1 and Player 2 character choices (two vertical columns)
        player1_x = WIDTH // 4 - 80  # Center Player 1's columns on the left quarter of the screen
        player2_x = 3 * WIDTH // 4 - 40  # Center Player 2's columns on the right quarter of the screen
        
        player1_choice_positions = [
            (player1_x, 200), (player1_x + 200, 200),
            (player1_x, 400), (player1_x + 200, 400),
        ]

        player2_choice_positions = [
            (player2_x, 200), (player2_x + 200, 200),
            (player2_x, 400), (player2_x + 200, 400),
        ]

        # Selections for Player 1 and Player 2
        player1_selection = []
        player2_selection = []

        # Initialize starting positions for each player's units
        player1_positions = [(i, 0) for i in range(2)]
        #player2_positions = [(4 - i, 4 - 1) for i in range(1, 3)]
        player2_positions = [(GRID_COLUMNS - i, GRID_ROWS - 1) for i in range(1, 3)]

        # Main loop for the home screen
        running = True
        while running:
            self.draw_semi_transparent_background()  # Draw the semi-transparent background

            # Draw instructions
            instructions = font.render("Select 2 Characters Each", True, WHITE)
            self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 25))

            # Draw Player 1's character choices
            player1_text = font.render("Player 1", True, BLUE)
            self.screen.blit(player1_text, (player1_x + 50, 50))
            for i, option in enumerate(CHARACTER_OPTIONS_p1):
                x, y = player1_choice_positions[i]
                pygame.draw.rect(self.screen, WHITE, (x - 60, y - 60, IMAGE_SIZE, IMAGE_SIZE), 2)
                self.screen.blit(self.character_images[option["name"]], (x - 60, y - 60))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                self.screen.blit(name_text, (x - name_text.get_width() // 2, y + 70))

                # Highlight selection
                if option["name"] in player1_selection:
                    pygame.draw.rect(self.screen, BLUE, (x - 60, y - 60, IMAGE_SIZE, IMAGE_SIZE), 4)

            # Draw Player 2's character choices
            player2_text = font.render("Player 2", True, RED)
            self.screen.blit(player2_text, (player2_x + 50, 50))
            for i, option in enumerate(CHARACTER_OPTIONS_p2):
                x, y = player2_choice_positions[i]
                pygame.draw.rect(self.screen, WHITE, (x - 60, y - 60, IMAGE_SIZE, IMAGE_SIZE), 2)
                self.screen.blit(self.character_images[option["name"]], (x - 60, y - 60))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                self.screen.blit(name_text, (x - name_text.get_width() // 2, y + 70))

                # Highlight selection
                if option["name"] in player2_selection:
                    pygame.draw.rect(self.screen, RED, (x - 60, y - 60, IMAGE_SIZE, IMAGE_SIZE), 4)

            # Draw the Start button
            pygame.draw.rect(self.screen, WHITE, start_button)
            start_text = font.render("Start", True, BLACK)
            self.screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
                                          start_button.y + (start_button.height - start_text.get_height()) // 2))

            # Draw back button
            pygame.draw.rect(self.screen, WHITE, back_button)
            back_text = font.render("Retour", True, BLACK)
            self.screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                         back_button.y + (back_button.height - back_text.get_height()) // 2))

            pygame.display.flip()


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
    
                    # Check if a Player 1 character was clicked
                    for i, option in enumerate(CHARACTER_OPTIONS_p1):
                        x, y = player1_choice_positions[i]
                        rect = pygame.Rect(x - 50, y - 50, 100, 100)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] in player1_selection:  # Unselect if already selected
                                player1_selection.remove(option["name"])
                                self.game.player1_units.pop()  # Remove the last unit added
                            elif option["name"] not in player1_selection and len(player1_selection) < 2:
                                player1_selection.append(option["name"])
                                px, py = player1_positions[len(player1_selection) - 1]
                                if option["name"] == 'Guerrier':
                                    self.game.player1_units.append(Guerrier(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Archer':
                                    self.game.player1_units.append(Archer(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Magicien':
                                    self.game.player1_units.append(Magicien(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Assassin':
                                    self.game.player1_units.append(Assassin(px, py, *option["stats"][2:], 'player1'))

                    # Check if a Player 2 character was clicked
                    for i, option in enumerate(CHARACTER_OPTIONS_p2):
                        x, y = player2_choice_positions[i]
                        rect = pygame.Rect(x - 50, y - 50, 100, 100)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] in player2_selection:  # Unselect if already selected
                                player2_selection.remove(option["name"])
                                self.game.player2_units.pop()  # Remove the last unit added
                            elif option["name"] not in player2_selection and len(player2_selection) < 2:
                                player2_selection.append(option["name"])
                                px, py = player2_positions[len(player2_selection) - 1]
                                if option["name"] == 'Guerrier2':
                                    self.game.player2_units.append(Guerrier(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Archer2':
                                    self.game.player2_units.append(Archer(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Magicien2':
                                    self.game.player2_units.append(Magicien(px, py, *option["stats"][2:], 'player2'))
                                    
                    if back_button.collidepoint(mouse_pos):  
                        self.initialize_main_menu()
                        
                    # Check if the Start button was clicked
                    if start_button.collidepoint(mouse_pos):
                        if len(player1_selection) == 2 and len(player2_selection) == 2:
                            running = False  # Exit the home screen loop to start the game

            pygame.display.flip()
            
    def draw_menu(self, selected_unit):
        """Draws the unit information menu in the lower-left corner, including the character's image."""
        menu_width = WIDTH // 2
        menu_height = HEIGHT // 4  # Increased height to accommodate the character display
        menu_x = 0
        menu_y = HEIGHT - menu_height

        # Draw the menu background
        pygame.draw.rect(self.screen, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))  # Black background
        pygame.draw.rect(self.screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 2)  # White border

        if selected_unit:
            font = pygame.font.Font(None, 28)

            # Column widths for the three sections
            column_width = menu_width // 3

            # === First Column: Character Image and Health Bar ===
            char_center_x = menu_x + column_width // 2  # Center character in the first column
            char_center_y = menu_y + 60  # Position the character near the top

            unit_name = selected_unit.__class__.__name__
            unit_team = selected_unit.team
            if unit_team == "player2":
                unit_name += '2'
            image = self.character_images.get(unit_name)

            if image:
                image = pygame.transform.scale(image, (80, 80))  # Resize the image to 80x80
                image_rect = image.get_rect(center=(char_center_x, char_center_y))
                self.screen.blit(image, image_rect)
            else:
                # Fallback placeholder if the image is not found
                if selected_unit.team == 'player1':
                    pygame.draw.circle(self.screen, (0, 0, 255), (char_center_x, char_center_y), 40)  # Blue circle for player 1
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), (char_center_x, char_center_y), 40)  # Red circle for player 2

            # Draw the health bar below the character
            health_bar_width = 100  # Fixed width for the health bar
            health_bar_height = 10
            health_bar_x = char_center_x - health_bar_width // 2  # Center the health bar
            health_bar_y = char_center_y + 50  # Position below the character image

            # Calculate the width of the green health bar based on the unit's health
            health_ratio = selected_unit.vie / selected_unit.max_vie
            health_fill_width = int(health_ratio * health_bar_width)

            # Draw the health bar background (gray)
            pygame.draw.rect(self.screen, (128, 128, 128), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            # Draw the health bar foreground (green) clipped to current health
            pygame.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, health_fill_width, health_bar_height))

            # === Second Column: 3 of the 5 stats ===
            second_column_x = menu_x + column_width
            second_column_stats = [
                f"Attaque: {selected_unit.attaque}",
                f"Vie: {selected_unit.vie}",
            ]

            for i, line in enumerate(second_column_stats):
                text = font.render(line, True, (255, 255, 255))  # White text
                self.screen.blit(text, (second_column_x + 10, menu_y + 20 + i * 30))  # Position with spacing

            # === Third Column: Remaining 2 stats ===
            third_column_x = menu_x + 2 * column_width
            third_column_stats = [
                f"Force: {selected_unit.force}",
                f"Combat: {selected_unit.combat}",
                f"Vie max: {selected_unit.max_vie}",
            ]

            for i, line in enumerate(third_column_stats):
                text = font.render(line, True, (255, 255, 255))  # White text
                self.screen.blit(text, (third_column_x + 10, menu_y + 20 + i * 30))  # Position with spacing

            # === Bottom Section: Instructions or Additional Text ===
            bottom_text = "Informations sur les capacités spéciales"
            bottom_font = pygame.font.Font(None, 18)
            text_surface = bottom_font.render(bottom_text, True, (255, 255, 255))  # White text

            # Center the text in the bottom section
            text_x = menu_x + menu_width // 2 - text_surface.get_width() // 2
            text_y = menu_y + menu_height - 45  # Leave some padding from the bottom
            self.screen.blit(text_surface, (text_x, text_y))
    
    def show_message(self, message, duration=2000):
        """Shows message on the screen for a given time (in milisecond)."""
        self.message = message
        self.message_timer = pygame.time.get_ticks() + duration  # Store time duration of the message

    def draw_message(self):
        """Draw message on the screen if there's one."""
        if self.message and pygame.time.get_ticks() < self.message_timer:
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)        
            
    def show_victory_message(self, message, confetti_color=(255, 255, 255)):
        # Code for confetti
        confetti_particles = []  # list for confetti
        for _ in range(150):
            x = random.randint(0, WIDTH)
            y = random.randint(-HEIGHT, 0)
            speed = random.uniform(2, 5)
            size = random.randint(2, 5)
            confetti_particles.append({"x": x, "y": y, "speed": speed, "size": size})  
        # Show message and animation
        start_time = pygame.time.get_ticks()
        duration = 10000
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)
            text = self.font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            self.screen.blit(text, text_rect)

            for particle in confetti_particles:
                particle["y"] += particle["speed"]
                if particle["y"] > HEIGHT:
                    particle["y"] = random.randint(-HEIGHT, 0)
                    particle["x"] = random.randint(0, WIDTH)
                pygame.draw.circle(self.screen, confetti_color, (particle["x"], int(particle["y"])), particle["size"])

            pygame.display.flip()
            pygame.time.delay(30)        
            # After confetti finish, end game
        pygame.quit()
        sys.exit()
        
       
    def show_ability_menu(unit, screen):
        """Muestra el menú de habilidades del mago."""
        if isinstance(unit, Magicien):  # Show menu if unit is wizard
            font = pygame.font.SysFont("Arial", 20)
        
            # Draw background for the menu
            menu_width = 200
            menu_height = 100
            menu_x = unit.x * CELL_SIZE + CELL_SIZE  # Location of the menu, at the right of the unit
            menu_y = unit.y * CELL_SIZE
        
            pygame.draw.rect(screen, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))
            pygame.draw.rect(screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 2)  # menu edge
        
            # show options
            heal_text = font.render("Use potion (C)", True, (255, 255, 255))
            screen.blit(heal_text, (menu_x + 10, menu_y + 10))

    
            
    def flip_display(self, selected_unit=None, hovered_cell=None):
        #self.screen.fill(BLACK)
        self.screen.blit(self.BoardBackground, (0,0)) # Board Background

        #for x in range(0, WIDTH, CELL_SIZE):
        #    for y in range(0, HEIGHT, CELL_SIZE):
        #        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        #        pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.game.player1_units + self.game.player2_units:
            unit.draw(self.screen)

        if selected_unit:
            movement_range = set()

            for dx in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                for dy in range(-selected_unit.mouvement, selected_unit.mouvement + 1):
                    if abs(dx) + abs(dy) <= selected_unit.mouvement:
                        target_x, target_y = selected_unit.x + dx, selected_unit.y + dy

                        if (target_x, target_y) == (selected_unit.x, selected_unit.y):
                            continue

                        if 0 <= target_x < GRID_COLUMNS and 0 <= target_y < GRID_ROWS:
                            movement_range.add((target_x, target_y))
            
            purple_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            purple_surface.fill((128, 100, 128, 128))
            
            for cell in movement_range:
                rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.screen.blit(purple_surface, rect)

            if hovered_cell in movement_range:
                rect = pygame.Rect(hovered_cell[0] * CELL_SIZE, hovered_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (200, 160, 255), rect)

        
        
        # Draw objects (rocks, fire, water, etc.)
        for obj in self.objects:
            obj.draw(self.screen)
        
        
        # Draw message (if there's one)
        self.draw_message()
        
        # Draw the menu in the lower-left corner
        self.draw_menu(selected_unit)


        pygame.display.flip()