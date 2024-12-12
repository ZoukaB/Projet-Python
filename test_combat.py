import pygame
from duel import roll_dice, duel_phase
from wound import attempt_wound, get_wound_threshold

pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Polices
font = pygame.font.Font(None, 36)

# Initialisation de la fenêtre Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test Combat")

# Charger les images des dés
def load_dice_images(base_path, player_name):
    images = {}
    for i in range(1, 7):
        path = f"{base_path}/{player_name}/{i}.jpg"
        images[i] = pygame.image.load(path).convert_alpha()
    return images

DICE_IMAGES_PLAYER_A = load_dice_images("dice_images", "dice_player_a")
DICE_IMAGES_PLAYER_B = load_dice_images("dice_images", "dice_player_b")

def display_message(screen, message, y_offset=0):
    """Affiche un message au centre de l'écran avec un décalage vertical."""
    screen.fill(BLACK, (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))  # Efface le bas de l'écran
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 + y_offset))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def display_dice(screen, rolls, images, y_position):
    """Affiche les dés pour un joueur."""
    screen.fill(BLACK, (0, y_position - 50, SCREEN_WIDTH, 200))  # Efface la zone des dés
    spacing = 120  # Augmenter l'espacement horizontal entre les dés
    x_start = (SCREEN_WIDTH - len(rolls) * spacing) // 2  # Centrer les dés avec l'espacement ajusté
    for i, roll in enumerate(rolls):
        screen.blit(images[roll], (x_start + i * spacing, y_position))
    pygame.display.flip()

def wait_for_space():
    """Attend que l'utilisateur appuie sur la touche Espace pour continuer."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def test_combat(screen, char1, char2):
    """Simule un combat entre deux personnages."""
    # Efface l'écran
    screen.fill(BLACK)
    pygame.display.flip()

    # Affiche les combattants
    display_message(screen, f"Combat : {char1.name} VS {char2.name}")
    wait_for_space()

    # Phase 1 : Duel
    display_message(screen, f"{char1.name} lance {char1.attaque} dés.")
    wait_for_space()
    rolls_char1 = roll_dice(char1.attaque)
    display_dice(screen, rolls_char1, DICE_IMAGES_PLAYER_A, SCREEN_HEIGHT - 300)  # Descend les dés légèrement plus haut
    display_message(screen, f"Résultats des dés : {rolls_char1}")
    wait_for_space()
    screen.fill(BLACK)  # Efface les dés après appui sur espace
    pygame.display.flip()

    display_message(screen, f"{char2.name} lance {char2.attaque} dés.")
    wait_for_space()
    rolls_char2 = roll_dice(char2.attaque)
    display_dice(screen, rolls_char2, DICE_IMAGES_PLAYER_B, SCREEN_HEIGHT - 300)  # Même positionnement que pour le joueur 1
    display_message(screen, f"Résultats des dés : {rolls_char2}")
    wait_for_space()
    screen.fill(BLACK)  # Efface les dés après appui sur espace
    pygame.display.flip()

    # Détermine le vainqueur du duel
    duel_result = duel_phase(char1, char2)
    if duel_result == "A":
        attacker, defender = char1, char2
        display_message(screen, f"{attacker.name} remporte le duel !")
    elif duel_result == "B":
        attacker, defender = char2, char1
        display_message(screen, f"{attacker.name} remporte le duel !")
    else:
        display_message(screen, "Le duel est un match nul.")
        wait_for_space()
        return  # Le combat s'arrête si le duel est un match nul

    wait_for_space()

    # Phase 2 : Tentative de blessure
    wound_threshold = get_wound_threshold(attacker.force, defender.defense)
    display_message(
        screen,
        f"{attacker.name} tente de blesser {defender.name}. Seuil pour blesser : {wound_threshold}+."
    )
    wait_for_space()
    rolls_wound = roll_dice(attacker.attaque)
    display_dice(screen, rolls_wound, DICE_IMAGES_PLAYER_A if attacker == char1 else DICE_IMAGES_PLAYER_B, SCREEN_HEIGHT - 300)
    display_message(screen, f"Résultats des dés : {rolls_wound}")
    wait_for_space()
    screen.fill(BLACK)  # Efface les dés après appui sur espace
    pygame.display.flip()

    # Applique les blessures
    wounds, status = attempt_wound(attacker, defender)
    if status == "mort":
        display_message(screen, f"{defender.name} est mort.")
    elif status == "blessé":
        display_message(screen, f"{defender.name} est blessé. Points de vie restants : {defender.vie}")
    else:
        display_message(screen, f"{defender.name} n'a pas été blessé.")
    wait_for_space()

    # Fin du combat
    display_message(screen, "Combat terminé.")
    wait_for_space()

if __name__ == "__main__":
    # Test du combat
    from duel import Character
    char1 = Character(name="Guerrier", attaque=4, combat=6, force=4, defense=5, vie=10)
    char2 = Character(name="Archer", attaque=3, combat=5, force=3, defense=4, vie=8)

    test_combat(screen, char1, char2)
    pygame.quit()
