import sys
import pygame
import random
from unit import *
from Guerrier import *
from unit import Unit

# Constantes
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
# Character names and image file paths (replace with actual image paths)
# Character options with their stats
CHARACTER_OPTIONS = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 4)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 8, 4)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 7, 4)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 9, 4)}
]
# A terme, remplacer par vraies statistiques des personnages dans la fonction remplacer Unit par nos classes Personnages

# Define objects list
OBJECT_TYPES = ['piedra']

class GameObject:
    def __init__(self, x, y, obj_type):
        self.x = x
        self.y = y
        self.obj_type = obj_type  # Object type: 'rock', 'water', etc.
        
        # Upload image of the object
        if obj_type == "piedra":
            try:
                self.image = pygame.image.load("rock.png")  # Make sure the image is in the folder
                self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Adjust size 
                self.rect = self.image.get_rect(topleft=(self.x * CELL_SIZE, self.y * CELL_SIZE))
            except pygame.error as e:
                print(f"Error uploading image for type {obj_type}: {e}")
        
        # If the image doesn't upload, configure image or error
        if not self.image:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  # Creates a default surface
            self.image.fill((255, 0, 0))  # Error sign (in red)
            self.rect = self.image.get_rect(topleft=(self.x * CELL_SIZE, self.y * CELL_SIZE))

    def draw(self, screen):
        """Draw object in the screen"""
        if self.image:  # Verify image is uploaded
            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
    
    def is_occupied(self):
        """Verify if the object is in the cell"""
        return True  # Always True because the rocks occupies a cell
    
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1_units = []
        self.player2_units = []
        # game background
        self.background_image = pygame.image.load("smallmap.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH,HEIGHT))
        self.objects = []  # List to store objects
        self.generate_objects()  # Call function that generates objects
        self.font = pygame.font.Font(None, 36) # View messages
        self.message = "" # message
        self.message_timer = 0 # time to show message

    def generate_objects(self):
        """Generates random objects in the map."""
        for _ in range(10):  # Number of objects
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            obj_type = random.choice(OBJECT_TYPES)  # Choose random object from the list
            new_object = GameObject(x, y, obj_type)
            self.objects.append(new_object)
        
    def initialize_home_screen(self):
        # pygame.init()
        # screen_info = pygame.display.Info()
        # WIDTH = screen_info.current_w
        # HEIGHT = screen_info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
        pygame.display.set_caption("Character Selection")

        # Font for button and text
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Button for starting the game
        start_button = pygame.Rect(WIDTH // 2 - 62 , HEIGHT - 70, 125, 50)

        # Load and display the unit's image based on its class name
        character_images = {
            "Guerrier": pygame.image.load("Images_persos/Warrior1.png").convert_alpha(),
            "Archer": pygame.image.load("Images_persos/Archer1.png").convert_alpha(),
            "Magicien": pygame.image.load("Images_persos/Wizard1.png").convert_alpha(),
            "Assassin": pygame.image.load("Images_persos/Assasin1.png").convert_alpha(),
            "Guerrier2": pygame.image.load("Images_persos/Warrior2.png").convert_alpha(),
            "Archer2": pygame.image.load("Images_persos/Archer2.png").convert_alpha(),
            "Magicien2": pygame.image.load("Images_persos/Wizard2.png").convert_alpha(),
            "Assassin2": pygame.image.load("Images_persos/Assasin2.png").convert_alpha(),
        }

        # Resize character images to fit the smaller squares
        for key in character_images:
            character_images[key] = pygame.transform.scale(character_images[key], (60, 60))

        # Positions for Player 1 and Player 2 character choices
        player1_choice_positions = [
            (100, 150), (100, 250), (100, 350), (100, 450)
        ]
        player2_choice_positions = [
            (WIDTH - 100, 150), (WIDTH - 100, 250), (WIDTH - 100, 350), (WIDTH - 100, 450)
        ]

        # Selections for Player 1 and Player 2
        player1_selection = []
        player2_selection = []

        # Initialize starting positions for each player's units
        player1_positions = [(i, 0) for i in range(2)]
        player2_positions = [(GRID_SIZE - i, GRID_SIZE - 1) for i in range(1,3)]

        # Main loop for the home screen
        running = True
        while running:
            screen.fill(BLACK)

            # Draw instructions
            instructions = font.render("Select 2 Characters Each", True, WHITE)
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 25))

            # Draw Player 1's character choices
            player1_text = font.render("Player 1", True, GREEN)
            screen.blit(player1_text, (100 - player1_text.get_width() // 2, 75))
            for i, option in enumerate(CHARACTER_OPTIONS):
                x, y = player1_choice_positions[i]
                pygame.draw.rect(screen, WHITE, (x - 35, y - 35, 70, 70), 2)
                screen.blit(character_images[option["name"]], (x - 30, y - 30))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                screen.blit(name_text, (x - name_text.get_width() // 2, y + 40))

                # Highlight selection
                if option["name"] in player1_selection:
                    pygame.draw.rect(screen, GREEN, (x - 35, y - 35, 70, 70), 4)

            # Draw Player 2's character choices
            player2_text = font.render("Player 2", True, BLUE)
            screen.blit(player2_text, (WIDTH - 100 - player2_text.get_width() // 2, 75))
            for i, option in enumerate(CHARACTER_OPTIONS):
                x, y = player2_choice_positions[i]
                pygame.draw.rect(screen, WHITE, (x - 35, y - 35, 70, 70), 2)
                screen.blit(character_images[option["name"]], (x - 30, y - 30))

                # Draw character name below the image
                name_text = small_font.render(option["name"], True, WHITE)
                screen.blit(name_text, (x - name_text.get_width() // 2, y + 40))

                # Highlight selection
                if option["name"] in player2_selection:
                    pygame.draw.rect(screen, BLUE, (x - 35, y - 35, 70, 70), 4)

            # Draw the Start button
            pygame.draw.rect(screen, WHITE, start_button)
            start_text = font.render("Start", True, BLACK)
            screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
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
                        rect = pygame.Rect(x - 35, y - 35, 70, 70)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] not in player1_selection and len(player1_selection) < 2:
                                player1_selection.append(option["name"])
                                px, py = player1_positions[len(player1_selection) - 1]
                                self.player1_units.append(Unit(px, py, *option["stats"][2:], 'player1'))

                    # Check if a Player 2 character was clicked
                    for i, option in enumerate(CHARACTER_OPTIONS):
                        x, y = player2_choice_positions[i]
                        rect = pygame.Rect(x - 35, y - 35, 70, 70)

                        if rect.collidepoint(mouse_pos):
                            if option["name"] not in player2_selection and len(player2_selection) < 2:
                                player2_selection.append(option["name"])
                                print(player2_selection)
                                px, py = player2_positions[len(player2_selection) - 1]
                                self.player2_units.append(Unit(px, py, *option["stats"][2:], 'player2'))

                    # Check if the Start button was clicked
                    if start_button.collidepoint(mouse_pos):
                        if len(player1_selection) == 2 and len(player2_selection) == 2:
                            running = False  # Exit the home screen loop to start the game

            pygame.display.flip()
    
    def is_cell_occupied(self, x, y):
        # check if cell is occupied by an pbject
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                return True
        return False

    def show_message(self, message, duration=2000): # cell ocuppied (message)
        self.message = message
        self.message_timer = pygame.time.get_ticks() + duration
    
    def draw_message(self):
        # show message on the screen
        if self.message and pygame.time.get_ticks() < self.message_timer:
            text = self.font.render(self.message, True, (255, 255, 255))  # white
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # center text
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 20))  # black background
            self.screen.blit(text, text_rect)  # show text
        elif pygame.time.get_ticks() >= self.message_timer:
            self.message = ""
        
    def check_victory(self): #verify the winner
        # verify if there is a winner and show message with confetti animation
        if not self.player1_units:
            self.show_victory_message("Player 2 wins!", confetti_color=(255, 0, 0)) # red for player 2
        elif not self.player2_units:
            self.show_victory_message("Player 1 wins!", confetti_color=(0, 0, 255)) # blue for player 1
    
    def show_victory_message(self, message, confetti_color=(255, 255, 255)):
        # show victory message and cofetti animation
        confetti_particles = [] # list for confetti

        # create confetti
        for _ in range(100): # to show more or less confetti
            x = random.randint(0, WIDTH)
            y = random.randint(-HEIGHT, 0)
            speed = random.uniform(2,5) # speed of confetti 
            size = random.randint(2,5) # size of the particle of the confetti
            confetti_particles.append({"x": x, "y": y, "speed": speed, "size":size})
        
        # show message and animation
        start_time = pygame.time.get_ticks()
        duration = 5000 # 5 seconds
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # draw background and message
            self.screen.fill(BLACK)
            text = self.font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            self.screen.blit(text, text_rect)

            # refresh and draw confetti
            for particle in confetti_particles:
                particle["y"] += particle["speed"]  # move down
                if particle["y"] > HEIGHT:
                    particle["y"] = random.randint(-HEIGHT, 0)  # re
                    particle["x"] = random.randint(0, WIDTH)
                pygame.draw.circle(self.screen, confetti_color, (particle["x"], int(particle["y"])), particle["size"])

            pygame.display.flip()
            pygame.time.delay(30)  # control speed of the animation

        pygame.quit()
        sys.exit()



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

                    # Select a unit player 1
                    if not selected_unit:
                        for unit in self.player1_units:
                            if unit.x == grid_x and unit.y == grid_y and unit not in moved_units:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move unit or attack
                    elif selected_unit:
                        #attack
                        for enemy in self.player2_units:
                            if enemy.x == grid_x and enemy.y == grid_y:
                                if selected_unit.is_in_range(enemy):
                                    damage = selected_unit.attack(enemy)
                                    self.show_message(f"{selected_unit.team} attacked and inflicted {damage} of damage.")
                                    if enemy.vie <= 0:
                                        self.show_message(f"{enemy.team} was defeated.")
                                        self.player2_units.remove(enemy)
                                    selected_unit.is_selected = False
                                    return # end turn after attacking

                        # move if there was not attack
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if not self.is_cell_occupied(grid_x, grid_y): # verify if cell is occupied
                             if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None
                            else:
                                self.show_message("You can't move, there is an obstacle!") # shows a message indicating there's an object

            if len(moved_units) == len(self.player1_units):
                self.check_victory() # verify winner after all movements
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
                            if unit.x == grid_x and unit.y == grid_y:
                                selected_unit = unit
                                selected_unit.is_selected = True
                                break

                    # Move unit or attack
                    elif selected_unit:
                        # Attack
                        for enemy in self.player1_units:
                            if enemy.x == grid_x and enemy.y == grid_y:
                                if selected_unit.is_in_range(enemy):
                                    damage = selected_unit.attack(enemy)
                                    self.show_message(f"{selected_unit.team} attacked and inflicted {damage} of damage.")
                                    if enemy.vie <= 0:
                                        self.show_message(f"{enemy.team} was defeated.")
                                        self.player1_units.remove(enemy)
                                    selected_unit.is_selected = False
                                    return
                        
                        # move if there was not attack
                        dx = grid_x - selected_unit.x
                        dy = grid_y - selected_unit.y

                        if abs(dx) + abs(dy) <= selected_unit.mouvement:
                            if not self.is_cell_occupied(grid_x, grid_y):
                             if selected_unit.move(dx, dy, self.player1_units + self.player2_units):
                                selected_unit.is_selected = False
                                moved_units.append(selected_unit)
                                selected_unit = None
                            else:
                                self.show_message("You can't move, there is an obstacle!")
                    
            if len(moved_units) == len(self.player2_units):
                self.check_victory() # verify winner
                break  

            self.flip_display(selected_unit, hovered_cell)      
    
    def draw_menu(self, selected_unit):
        """Draws the unit information menu in the lower-left corner, including the character's image."""
        menu_width = WIDTH // 2
        menu_height = HEIGHT // 4  # Increased height to accommodate the character display
        menu_x = 0
        menu_y = HEIGHT - menu_height

    def flip_display(self, selected_unit=None, hovered_cell=None):
    # First, draw the background
     self.screen.blit(self.background_image, (0, 0))  # Adjust position if necessary

    # Draw the units
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

                    if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
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
     self.draw_message()

    # Draw objects (stones, fire, water, etc.)
     for obj in self.objects:
        obj.draw(self.screen)

    # Move pygame.display.flip() outside of all loops, at the end of the method
     pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)
    game.initialize_home_screen()

    while True:
        game.handle_player1_turn()
        game.handle_player2_turn()

if __name__ == "__main__":
    main()
