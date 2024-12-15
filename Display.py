import sys
import pygame
import random
from unit_fullscreen import *
from Personnages import *

CHARACTER_OPTIONS_p1 = [
    #
    {"name": "Guerrier", "stats": (4, 5, 4, 5,10, 10,10)},
    {"name": "Archer", "stats": (5, 4, 3, 4, 4,10,10)},
    {"name": "Magicien", "stats": (3, 3, 2, 2, 2,10,10)},
    {"name": "Assassin", "stats": (6, 4, 4, 10, 10,10,10)},
    {"name": "Infirmier", "stats": (4, 5, 4, 10,10, 10,10)},
]

CHARACTER_OPTIONS_p2 = [
    #
    {"name": "Guerrier2", "stats": (4, 5, 4, 5,10, 10,10)},
    {"name": "Archer2", "stats": (5, 4, 3, 4, 4,10,10)},
    {"name": "Magicien2", "stats": (3, 3, 2, 2, 2,10,10)},
    {"name": "Assassin2", "stats": (6, 4, 4, 10, 10,10,10)},
    {"name": "Infirmier", "stats": (4, 5, 4, 10,10, 10,10)},
]

class Display:
    def __init__(self,screen,game): 
        self.screen = screen
        self.game = game
        # Load the background image (replace with the actual image path)
        self.background_image = pygame.image.load("background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
        self.font = pygame.font.Font(None, 74)  # Usando una fuente predeterminada con tamaño 74
        # Load background image for the board
        self.BoardBackground = pygame.image.load("backgroundGame.png").convert()
        self.BoardBackground = pygame.transform.scale(self.BoardBackground, (WIDTH,HEIGHT))
        
        # Load character images (replace with actual image paths)
        self.character_images = {
            "Guerrier": pygame.image.load("Images_persos/Warrior1.png").convert_alpha(),
            "Archer": pygame.image.load("Images_persos/Archer1.png").convert_alpha(),
            "Magicien": pygame.image.load("Images_persos/Wizard1.png").convert_alpha(),
            "Assassin": pygame.image.load("Images_persos/Assasin1.png").convert_alpha(),
            "Infirmier": pygame.image.load("Images_persos/archer.jpg").convert_alpha(),
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
            "1. Chaque joueur choisit 2 personnages.",
            "2. Les joueurs déplacent leurs unités à tour de rôle.",
            "3. L'objectif est de vaincre toutes les unités adverses.",
            "4. Chaque unité a des capacités uniques.",
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
            (player1_x + 100, 600)
        ]

        player2_choice_positions = [
            (player2_x, 200), (player2_x + 200, 200),
            (player2_x, 400), (player2_x + 200, 400),
            (player2_x + 100, 600)
        ]

        # Selections for Player 1 and Player 2
        player1_selection = []
        player2_selection = []

        # Initialize starting positions for each player's units
        player1_positions = [(i, 0) for i in range(2)]
        player2_positions = [(4 - i, 4 - 1) for i in range(1, 3)]
        # player2_positions = [(GRID_COLUMNS - i, GRID_ROWS - 1) for i in range(1, 3)]

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
                                    self.game.player1_units.append(Guerrier(px, py, *option["stats"], 'player1'))
                                if option["name"] == 'Archer':
                                    self.game.player1_units.append(Archer(px, py, *option["stats"], 'player1'))
                                if option["name"] == 'Magicien':
                                    self.game.player1_units.append(Magicien(px, py, *option["stats"], 'player1'))
                                if option["name"] == 'Assassin':
                                    self.game.player1_units.append(Assassin(px, py, *option["stats"], 'player1'))
                                if option["name"] == 'Infirmier':
                                    self.game.player1_units.append(Infirmier(px, py, *option["stats"], 'player1'))


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
                                    self.game.player2_units.append(Guerrier(px, py, *option["stats"], 'player2'))
                                if option["name"] == 'Archer2':
                                    self.game.player2_units.append(Archer(px, py, *option["stats"], 'player2'))
                                if option["name"] == 'Magicien2':
                                    self.game.player2_units.append(Magicien(px, py, *option["stats"], 'player2'))
                                if option["name"] == 'Assassin2':
                                    self.game.player2_units.append(Assassin(px, py, *option["stats"], 'player2'))
                                if option["name"] == 'Infirmier':
                                    self.game.player2_units.append(Infirmier(px, py, *option["stats"], 'player2'))
                                    
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
                f"Défense: {selected_unit.defense}",
                f"Energie: {selected_unit.energie}",
                f"Energie Max: {selected_unit.max_energie}",
            ]

            for i, line in enumerate(third_column_stats):
                text = font.render(line, True, (255, 255, 255))  # White text
                self.screen.blit(text, (third_column_x + 10, menu_y + 20 + i * 30))  # Position with spacing
                
            # === Bottom Section: Special Abilities ===
            bottom_lines = []
            # First line: title
            bottom_lines.append("Capacités spéciales")

            # Determine second and third lines based on unit
            if isinstance(selected_unit,Guerrier):
                bottom_lines.append(f"  Boisson du Guerrier: {selected_unit.boisson_du_guerrier} restantes")
                bottom_lines.append(f"  Capacité téméraire: {selected_unit.temeraire_actif}")
            elif isinstance(selected_unit,Archer):
                bottom_lines.append(f"  Fleches de guérison: {selected_unit.fleche_soigneuse} restantes")
                bottom_lines.append(f"  Capacité headshot: {selected_unit.headshot_actif}")
            elif isinstance(selected_unit,Magicien):
                for unit in self.game.player2_units:
                    if unit.empoisonné:
                        bottom_lines.append(f"  Sort de poison {unit.empoisonné} sur {unit.__class__.__name__}")
                bottom_lines.append(f"   Boule de feu: {selected_unit.stock_boule_de_feu} restantes")
            elif isinstance(selected_unit,Assassin):
                bottom_lines.append(f"  Coup fatal: {selected_unit.fatality} restant")
                bottom_lines.append("  Fuite: permet de se téléporter loin des enemis")
            elif isinstance(selected_unit,Infirmier):
                bottom_lines.append(f"  Potions de soin: {selected_unit.potions_de_soin} restantes")
                bottom_lines.append(f"  Soin intensif: utilise 5 d'énergie")

            # Bigger font and spacing
            bottom_font = pygame.font.Font(None, 28)
            line_spacing = 10
            line_height = bottom_font.get_height()
            total_text_height = len(bottom_lines) * line_height + (len(bottom_lines) - 1) * line_spacing

            # Align the first line with the second column
            # We'll use second_column_x + 10 as the alignment for the first line
            # The second and third lines are already indented with spaces "  "
            # which will visually show the indentation.
            
            start_y = menu_y + menu_height - 35 - total_text_height

            for i, line in enumerate(bottom_lines):
                text_surface = bottom_font.render(line, True, (255, 255, 255))
                # First line aligned with second column
                # Following lines also start at the same x, but have leading spaces for indentation
                text_x = second_column_x + 10
                text_y = start_y + i * (line_height + line_spacing)
                self.screen.blit(text_surface, (text_x, text_y))
  
    def capacity_choice(self,selected_unit):
        # Define the text and font
        font = pygame.font.Font(None, 38)
        font1 = pygame.font.Font(None, 32)
        prompt_surface = font.render("Quelle capacité spéciale voulez-vous activer ?", True, (255, 255, 255))
        option1_surface = font1.render(f"1 - {selected_unit.capacités[0]}", True, (255, 255, 0))
        option2_surface = font1.render(f"2 - {selected_unit.capacités[1]}", True, (255, 255, 0))

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Calculate the overlay size and position to center it
        overlay_width, overlay_height = 600, 200
        overlay_x = (screen_width - overlay_width) // 2
        overlay_y = (screen_height - overlay_height) // 2

        # Create a semi-transparent background rectangle
        overlay = pygame.Surface((overlay_width, overlay_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))

        # Calculate text positions to center them within the overlay
        prompt_x = overlay_x + (overlay_width - prompt_surface.get_width()) // 2
        prompt_y = overlay_y + 20  # Slight padding from the top

        option1_x = overlay_x + (overlay_width - option1_surface.get_width()) // 2
        option1_y = overlay_y + 80

        option2_x = overlay_x + (overlay_width - option2_surface.get_width()) // 2
        option2_y = overlay_y + 130

        capacity_choice = True
        while capacity_choice:
            # Draw the current game screen
            #self.display.flip_display_basic(selected_unit)

            # Draw the overlay
            self.screen.blit(overlay, (overlay_x, overlay_y))

            # Blit the prompt and options on the screen
            self.screen.blit(prompt_surface, (prompt_x, prompt_y))
            self.screen.blit(option1_surface, (option1_x, option1_y))
            self.screen.blit(option2_surface, (option2_x, option2_y))
            
            if selected_unit.team == 'player1':
                ennemis = self.game.player2_units
                allies = self.game.player1_units
            else:
                ennemis = self.game.player1_units
                allies = self.game.player2_units

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2]:
                        # Handle special ability selection
                        if event.key == pygame.K_1:
                            
                            if isinstance(selected_unit,Guerrier):
                                selected_unit.boisson_guerrier()
                                self.affiche_message_haut(selected_unit.boisson_guerrier())
                                capacity_choice = False
                                
                            if isinstance(selected_unit,Archer):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit) 
                                self.affiche_message_centre("Veuillez sélectionner un allié à soigner")
                                self.flip_display_basic(selected_unit) 
                                pygame.display.flip()
                                wainting_selection = True
                                while wainting_selection:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            # Check if the mouse click intersects with any unit's position
                                            for unit in allies:
                                                if (abs(selected_unit.x - unit.x) <= selected_unit.attack_range and abs(selected_unit.y - unit.y) == 0) or (abs(selected_unit.y - unit.y) <= selected_unit.attack_range and abs(selected_unit.x - unit.x) ==0):
                                                    unit_rect = pygame.Rect(unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                                    if unit_rect.collidepoint(mouse_x, mouse_y):
                                                        self.affiche_message_haut(selected_unit.fleche_de_guerison(unit))
                                                        wainting_selection = False
                                                else:
                                                    self.affiche_message_centre("Allié trop loin pour pouvoir être soigné")
                                                    wainting_selection = False
                        
                            if isinstance(selected_unit,Magicien):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit) 
                                self.affiche_message_centre("Veuillez sélectionner un enemie à empoisoner")
                                self.flip_display_basic(selected_unit) 
                                pygame.display.flip()
                                wainting_selection = True
                                while wainting_selection:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            # Check if the mouse click intersects with any unit's position
                                            for unit in ennemis:
                                                if abs(selected_unit.x - unit.x) <= selected_unit.attack_range and abs(selected_unit.y - unit.y) <= selected_unit.attack_range:
                                                    unit_rect = pygame.Rect(unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                                    if unit_rect.collidepoint(mouse_x, mouse_y):
                                                        selected_unit.sort_de_poison(unit)
                                                        self.affiche_message_centre(f"{unit.__class__.__name__} empoisonné avec succès")
                                                        wainting_selection = False
                                                else:
                                                    self.affiche_message_centre("Allié trop loin pour pouvoir être soigné")
                                                    wainting_selection = False
                            
                            if isinstance(selected_unit,Assassin):
                                self.affiche_message_haut(selected_unit.coup_fatal())
                                capacity_choice = False         
                        
                            if isinstance(selected_unit,Infirmier):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit)
                                self.affiche_message_centre("Choisir qui où vous voulez lancer la potion")
                                pygame.display.flip()

                                # Waiting for the player to click on a cell
                                waiting_selection = True
                                while waiting_selection:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            target_x = mouse_x // CELL_SIZE
                                            target_y = mouse_y // CELL_SIZE

                                            # Highlight the target cell and its perimeter
                                            self.flip_display_basic(selected_unit)
                                            for dx in range(-1, 2):
                                                for dy in range(-1, 2):
                                                    cell_x = target_x + dx
                                                    cell_y = target_y + dy
                                                    if 0 <= cell_x < GRID_COLUMNS and 0 <= cell_y < GRID_ROWS:
                                                        cell_rect = pygame.Rect(cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                                        highlight = pygame.Surface((CELL_SIZE, CELL_SIZE))
                                                        highlight.set_alpha(100)
                                                        highlight.fill((0, 165, 0))  # Transparent orange
                                                        self.screen.blit(highlight, cell_rect)

                                            pygame.display.flip()
                                            # Keep the display visible for 2 seconds (2000 milliseconds)
                                            pygame.time.wait(2000)
                                            self.affiche_message_haut(selected_unit.potion_soin(target_x,target_y,allies))
                                            waiting_selection = False
                                
                        elif event.key == pygame.K_2:
                            
                            if isinstance(selected_unit,Guerrier):
                                self.affiche_message_haut(selected_unit.temeraire())
                                capacity_choice = False
                            
                            if isinstance(selected_unit,Archer):
                                self.affiche_message_haut(selected_unit.headshot())
                                capacity_choice = False
                                
                            if isinstance(selected_unit,Magicien):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit)
                                self.affiche_message_centre("Cliquez pour lancer la boule de feu")
                                pygame.display.flip()

                                # Waiting for the player to click on a cell
                                waiting_selection = True
                                while waiting_selection:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            target_x = mouse_x // CELL_SIZE
                                            target_y = mouse_y // CELL_SIZE

                                            # Highlight the target cell and its perimeter
                                            self.flip_display_basic(selected_unit)
                                            for dx in range(-1, 2):
                                                for dy in range(-1, 2):
                                                    cell_x = target_x + dx
                                                    cell_y = target_y + dy
                                                    if 0 <= cell_x < GRID_COLUMNS and 0 <= cell_y < GRID_ROWS:
                                                        cell_rect = pygame.Rect(cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                                        highlight = pygame.Surface((CELL_SIZE, CELL_SIZE))
                                                        highlight.set_alpha(100)
                                                        highlight.fill((255, 165, 0))  # Transparent orange
                                                        self.screen.blit(highlight, cell_rect)

                                            pygame.display.flip()
                                            # Keep the display visible for 2 seconds (2000 milliseconds)
                                            pygame.time.wait(2000)
                                            self.affiche_message_haut(selected_unit.boule_de_feu(target_x, target_y, ennemis))
                                            waiting_selection = False

                            if isinstance(selected_unit,Assassin):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit)
                                self.affiche_message_centre("Cliquez sur la case où vous voulez fuire")
                                pygame.display.flip()

                                # Waiting for the player to click on a cell
                                waiting_selection = True
                                while waiting_selection:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            target_x = mouse_x // CELL_SIZE
                                            target_y = mouse_y // CELL_SIZE
                                            self.affiche_message_haut(selected_unit.fuite(target_x,target_y))
                                            self.flip_display_basic(selected_unit)
                                            waiting_selection = False

                            if isinstance(selected_unit, Infirmier):
                                capacity_choice = False  # Close the capacity menu
                                self.flip_display_basic(selected_unit)
                                self.affiche_message_centre("Lancer soin intensif")

                                # Define the list of allies (assuming player1_units are allies for the Infirmier)
                                self.flip_display_basic(selected_unit)  # Redraw the basic display first

                                # Loop through all cells within the healing range
                                for dx in range(-selected_unit.healing_range, selected_unit.healing_range + 1):
                                    for dy in range(-selected_unit.healing_range, selected_unit.healing_range + 1):
                                        cell_x = selected_unit.x + dx
                                        cell_y = selected_unit.y + dy
                                        distance = abs(dx) + abs(dy)

                                        # Check if within grid boundaries and within healing range
                                        if 0 <= cell_x < GRID_COLUMNS and 0 <= cell_y < GRID_ROWS and distance <= selected_unit.healing_range:
                                            cell_rect = pygame.Rect(cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                            highlight = pygame.Surface((CELL_SIZE, CELL_SIZE))
                                            highlight.set_alpha(100)
                                            highlight.fill((0, 255, 0))  # Transparent green
                                            self.screen.blit(highlight, cell_rect)

                                # Update the display to show the highlighted area
                                pygame.display.flip()

                                # Apply the healing effect
                                self.affiche_message_haut(selected_unit.soin_intensif(allies))

                                # Wait for 2 seconds to display the highlighted area before continuing
                                pygame.time.wait(1000)
                                self.flip_display_basic(selected_unit)  # Redraw the screen to clear highlights
                                pygame.display.flip()
                                
                                
            # Update the display
            pygame.display.flip() 
            
    def show_victory_message(self, message, confetti_color=(255, 255, 255)):
        # Code for the confetti
        confetti_particles = []  # list for the confetti
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
            # After confetti end, close game
        pygame.quit()
        sys.exit()        
    
    def affiche_message_centre(self, message, taille_police=48, couleur=(255, 255, 255), duree=1000):
        # Initialiser la police
        font = pygame.font.Font(None, taille_police)

        # Créer le rendu du texte
        texte_surface = font.render(message, True, couleur)

        # Obtenir les dimensions de l'écran
        largeur_ecran, hauteur_ecran = self.screen.get_size()

        # Calculer la position pour centrer le texte
        texte_x = (largeur_ecran - texte_surface.get_width()) // 2
        texte_y = (hauteur_ecran - texte_surface.get_height()) // 2

        # Afficher le texte
        self.screen.blit(texte_surface, (texte_x, texte_y))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre pendant la durée spécifiée
        pygame.time.wait(duree)

    def affiche_message_haut(self, message, taille_police=48, couleur=(255, 255, 255), duree=1000):
        # Initialiser la police
        font = pygame.font.Font(None, taille_police)

        # Créer le rendu du texte
        texte_surface = font.render(message, True, couleur)

        # Obtenir les dimensions de l'écran
        largeur_ecran, hauteur_ecran = self.screen.get_size()

        # Calculer la position pour centrer le texte
        texte_x = (largeur_ecran - texte_surface.get_width()) // 2
        texte_y = (hauteur_ecran - texte_surface.get_height()) // 2

        # Afficher le texte
        self.screen.blit(texte_surface, (texte_x, texte_y-200))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre pendant la durée spécifiée
        pygame.time.wait(duree)

    def flip_display_feu(self, target_x, target_y):

        # Highlight the fireball target cell
        target_rect = pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (255, 100, 0), target_rect, 3)  # Orange outline for targeting
         
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



        # Draw the menu in the lower-left corner
        self.draw_menu(selected_unit)

        pygame.display.flip()
        
    def flip_display_basic(self,selected_unit):
        #self.screen.fill(BLACK)
        self.screen.blit(self.BoardBackground, (0,0)) # Board Background

        #for x in range(0, WIDTH, CELL_SIZE):
        #    for y in range(0, HEIGHT, CELL_SIZE):
        #        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        #        pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.game.player1_units + self.game.player2_units:
            unit.draw(self.screen)

        # Draw the menu in the lower-left corner
        self.draw_menu(selected_unit)

        pygame.display.flip()