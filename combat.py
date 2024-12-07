import pygame
import random
pygame.init()

# Couleurs et dimensions pour l'affichage
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

INFO_PANEL_HEIGHT = 150

# Police pour le texte
font = pygame.font.Font(None, 36)

def display_text_centered(screen, text, y, color=WHITE):
    """Affiche un texte centré sur l'écran."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text_surface, text_rect)

def display_info_panel(screen, messages):
    """Affiche les messages dans un panneau en bas."""
    panel_rect = pygame.Rect(0, screen.get_height() - INFO_PANEL_HEIGHT, screen.get_width(), INFO_PANEL_HEIGHT)
    pygame.draw.rect(screen, WHITE, panel_rect)  # Fond blanc
    pygame.draw.rect(screen, BLACK, panel_rect, 2)  # Bordure noire
    for i, message in enumerate(messages):
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (10, screen.get_height() - INFO_PANEL_HEIGHT + 10 + i * 30))

def roll_dice(num_dice):
    """Lance un nombre de dés et retourne les résultats triés."""
    return sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)

def combat_round(screen, attacker, defender):
    """Gère un round de combat entre deux unités."""
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        # Phase 1 : Annonce du combat
        display_text_centered(screen, f"Combat entre {attacker.team} et {defender.team} !", 50)
        display_info_panel(screen, [
            f"{attacker.team} - PV: {attacker.vie}, Attaque: {attacker.attaque}, Défense: {attacker.defense}",
            f"{defender.team} - PV: {defender.vie}, Attaque: {defender.attaque}, Défense: {defender.defense}",
        ])
        pygame.display.flip()
        pygame.time.wait(2000)

        # Phase 2 : Duel
        display_text_centered(screen, f"{attacker.team} attaque {defender.team} !", 50)
        pygame.display.flip()
        pygame.time.wait(1500)

        # Lancer de dés pour les deux
        attacker_rolls = roll_dice(attacker.attaque)
        defender_rolls = roll_dice(defender.attaque)
        display_info_panel(screen, [
            f"{attacker.team} a obtenu : {attacker_rolls}",
            f"{defender.team} a obtenu : {defender_rolls}",
        ])
        pygame.display.flip()
        pygame.time.wait(2000)

        # Comparaison des dés
        attacker_max = max(attacker_rolls) if attacker_rolls else 0
        defender_max = max(defender_rolls) if defender_rolls else 0
        if attacker_max > defender_max:
            winner, loser = attacker, defender
        elif defender_max > attacker_max:
            winner, loser = defender, attacker
        else:
            winner, loser = (attacker, defender) if attacker.combat > defender.combat else (defender, attacker)

        display_text_centered(screen, f"{winner.team} gagne le duel !", 50)
        pygame.display.flip()
        pygame.time.wait(2000)

        # Phase 3 : Calcul des dégâts
        damage = max(1, winner.force - loser.defense)
        loser.vie -= damage
        display_info_panel(screen, [
            f"{winner.team} inflige {damage} dégâts à {loser.team} !",
            f"{loser.team} reste avec {loser.vie} PV.",
        ])
        pygame.display.flip()
        pygame.time.wait(2000)

        # Fin du combat si une unité est morte
        if loser.vie <= 0:
            display_text_centered(screen, f"{loser.team} a été vaincu !", 50)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        clock.tick(30)
