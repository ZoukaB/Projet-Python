import sys
import pygame
import random
from unit_fullscreen import *

# Character names and image file paths (replace with actual image paths)
# Character options with their stats
CHARACTER_OPTIONS = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
    {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)}
]
# A terme, remplacer par vraies statistiques des personnages dans la fonction remplacer Unit par nos classes Personnages

class Game:
    def __init__(self, screen):
        self.screen = screen

        self.background_image = pygame.image.load("forest.jpg").convert()
        # so the image is the same size as the screen
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH,HEIGHT))
        
        self.player1_units = []

        self.player2_units = []
        
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
        
    def initialize_home_screen(self):
        # Font for button and text
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Button for starting the game
        start_button = pygame.Rect(WIDTH // 2 - 62, HEIGHT - 70, 125, 50)

        # Resize character images to fit larger squares
        for key in self.character_images:
            self.character_images[key] = pygame.transform.scale(self.character_images[key], (100, 100))

        # Positions for Player 1 and Player 2 character choices (two columns each)
        player1_choice_positions = [
            (100, 150), (250, 150),
            (100, 300), (250, 300),
            (100, 450), (250, 450),
            (100, 600), (250, 600)
            
        ]
        player2_choice_positions = [
            (WIDTH - 300, 150), (WIDTH - 150, 150),
            (WIDTH - 300, 300), (WIDTH - 150, 300),
            (WIDTH - 300, 450), (WIDTH - 150, 450),
            (WIDTH - 300, 600), (WIDTH - 150, 600)
        ]

        # Selections for Player 1 and Player 2
        player1_selection = []
        player2_selection = []

        # Initialize starting positions for each player's units
        player1_positions = [(i, 0) for i in range(2)]
        player2_positions = [(GRID_COLUMNS - i, GRID_ROWS - 1) for i in range(1, 3)]

        # Main loop for the home screen
        running = True
        while running:
            self.screen.fill(BLACK)

            # Draw instructions
            instructions = font.render("Select 2 Characters Each", True, WHITE)
            self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 25))

            # Draw Player 1's character choices
            player1_text = font.render("Player 1", True, GREEN)
            self.screen.blit(player1_text, (150 - player1_text.get_width() // 2, 50))
            for i, option in enumerate(CHARACTER_OPTIONS):
                x, y = player1_choice_positions[i]
                pygame.draw.rect(self.screen, WHITE, (x - 50, y - 50, 100, 100), 2)
                self.screen.blit(self.character_images[option["name"]], (x - 50, y - 50))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                self.screen.blit(name_text, (x - name_text.get_width() // 2, y + 60))

                # Highlight selection
                if option["name"] in player1_selection:
                    pygame.draw.rect(self.screen, GREEN, (x - 50, y - 50, 100, 100), 4)

            # Draw Player 2's character choices
            player2_text = font.render("Player 2", True, BLUE)
            self.screen.blit(player2_text, (WIDTH - 200 - player2_text.get_width() // 2, 50))
            for i, option in enumerate(CHARACTER_OPTIONS):
                x, y = player2_choice_positions[i]
                pygame.draw.rect(self.screen, WHITE, (x - 50, y - 50, 100, 100), 2)
                self.screen.blit(self.character_images[option["name"]], (x - 50, y - 50))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                self.screen.blit(name_text, (x - name_text.get_width() // 2, y + 60))

                # Highlight selection
                if option["name"] in player2_selection:
                    pygame.draw.rect(self.screen, BLUE, (x - 50, y - 50, 100, 100), 4)

            # Draw the Start button
            pygame.draw.rect(self.screen, WHITE, start_button)
            start_text = font.render("Start", True, BLACK)
            self.screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
                                          start_button.y + (start_button.height - start_text.get_height()) // 2))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a Player 1 character was clicked
                    for i, option in enumerate(CHARACTER_OPTIONS):
                        x, y = player1_choice_positions[i]
                        rect = pygame.Rect(x - 50, y - 50, 100, 100)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] not in player1_selection and len(player1_selection) < 2:
                                player1_selection.append(option["name"])
                                px, py = player1_positions[len(player1_selection) - 1]
                                if option["name"] == 'Guerrier':
                                    self.player1_units.append(Guerrier(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Archer':
                                    self.player1_units.append(Archer(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Magicien':
                                    self.player1_units.append(Magicien(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Assassin':
                                    self.player1_units.append(Assassin(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Guerrier2':
                                    self.player1_units.append(Guerrier(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Archer2':
                                    self.player1_units.append(Archer(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Magicien2':
                                    self.player1_units.append(Magicien(px, py, *option["stats"][2:], 'player1'))
                                if option["name"] == 'Assassin2':
                                    self.player1_units.append(Assassin(px, py, *option["stats"][2:], 'player1'))


                    # Check if a Player 2 character was clicked
                    for i, option in enumerate(CHARACTER_OPTIONS):
                        x, y = player2_choice_positions[i]
                        rect = pygame.Rect(x - 50, y - 50, 100, 100)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] not in player2_selection and len(player2_selection) < 2:
                                player2_selection.append(option["name"])
                                px, py = player2_positions[len(player2_selection) - 1]
                                if option["name"] == 'Guerrier':
                                    self.player2_units.append(Guerrier(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Archer':
                                    self.player2_units.append(Archer(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Magicien':
                                    self.player2_units.append(Magicien(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Assassin':
                                    self.player2_units.append(Assassin(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Guerrier2':
                                    self.player2_units.append(Guerrier(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Archer2':
                                    self.player2_units.append(Archer(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Magicien2':
                                    self.player2_units.append(Magicien(px, py, *option["stats"][2:], 'player2'))
                                if option["name"] == 'Assassin2':
                                    self.player2_units.append(Assassin(px, py, *option["stats"][2:], 'player2'))

                    # Check if the Start button was clicked
                    if start_button.collidepoint(mouse_pos):
                        if len(player1_selection) == 2 and len(player2_selection) == 2:
                            running = False  # Exit the home screen loop to start the game

            pygame.display.flip()


    def handle_player1_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                    # Select a unit if no unit is currently selected
                    if not selected_unit:
                        for unit in self.player1_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move the selected unit if one is selected
                    elif selected_unit:
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

            if len(moved_units) == len(self.player1_units):
                break  

            self.flip_display(selected_unit, hovered_cell)
    
    def handle_player2_turn(self):
        selected_unit = None
        hovered_cell = None
        moved_units = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                    # Select a unit if no unit is currently selected
                    if not selected_unit:
                        for unit in self.player2_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move the selected unit if one is selected
                    elif selected_unit:
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)
                    
            if len(moved_units) == len(self.player2_units):
                break  

            self.flip_display(selected_unit, hovered_cell)      
    
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
                f"Défense: {selected_unit.defense}",
                f"Tir: {selected_unit.tir}",
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


    def flip_display(self, selected_unit=None, hovered_cell=None):
        #self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0,0))

        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player1_units + self.player2_units:
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
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)
    game.initialize_home_screen()

    while True:
        game.handle_player1_turn()
        game.handle_player2_turn()

if __name__ == "__main__":
    main()
