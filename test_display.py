import sys
import pygame
from unit_fullscreen import *
from duel import roll_dice, duel_phase
from wound import attempt_wound, get_wound_threshold
from tir import phase_tir

CHARACTER_OPTIONS = [
    {"name": "Guerrier", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
    {"name": "Guerrier2", "stats": (0, 10, 4, 4, 4, 4, 5, 4, 10, 10)},
    {"name": "Archer2", "stats": (0, 0, 5, 3, 5, 3, 4, 3, 4, 4)},
    {"name": "Magicien2", "stats": (0, 0, 3, 6, 2, 5, 3, 2, 2, 2)},
    {"name": "Assassin2", "stats": (0, 0, 6, 2, 4, 4, 4, 4, 10, 10)},
]

class Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.background_image = pygame.image.load("background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.BoardBackground = pygame.image.load("backgroundGame.png").convert()
        self.BoardBackground = pygame.transform.scale(self.BoardBackground, (WIDTH, HEIGHT))
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

    def afficher_message(self, message):
        """
        Affiche un message dans un encadré en bas de l'écran.
        """
        font = pygame.font.Font(None, 36)
        self.screen.fill((0, 0, 0), (0, HEIGHT - 150, WIDTH, 150))
        lignes = self.diviser_texte(message, WIDTH - 20)
        y_offset = HEIGHT - 140
        for ligne in lignes:
            text_surface = font.render(ligne, True, (255, 255, 255))
            rect_text = text_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text_surface, rect_text)
            y_offset += 30
        pygame.display.flip()

    def diviser_texte(self, message, largeur_max):
        """
        Divise un message long en plusieurs lignes adaptées à la largeur maximale.
        """
        mots = message.split(" ")
        lignes = []
        ligne = ""
        for mot in mots:
            if pygame.font.Font(None, 36).size(ligne + mot)[0] < largeur_max:
                ligne += mot + " "
            else:
                lignes.append(ligne.strip())
                ligne = mot + " "
        lignes.append(ligne.strip())
        return lignes

    def attendre_touche(self, touche=pygame.K_SPACE):
        """
        Attend qu'une touche spécifique soit pressée.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == touche:
                    return

    def detect_combat_or_tir(self, selected_unit):
        """
        Détecte si un combat ou un tir peut être déclenché, et déclenche la phase correspondante.
        """
        if not selected_unit:
            return

        # Si un Archer est sélectionné
        if selected_unit.__class__.__name__.lower() == "archer":
            for unit in self.game.player1_units + self.game.player2_units:
                if unit.team != selected_unit.team:
                    distance = abs(unit.x - selected_unit.x) + abs(unit.y - selected_unit.y)
                    if distance <= 3:  # Portée de tir
                        self.afficher_message(f"{selected_unit.name} peut tirer ! Appuyez sur Espace pour tirer.")
                        self.attendre_touche()
                        phase_tir()
                        return

        # Vérifie les ennemis adjacents pour déclencher un combat
        for unit in self.game.player1_units + self.game.player2_units:
            if unit.team != selected_unit.team and abs(unit.x - selected_unit.x) + abs(unit.y - selected_unit.y) == 1:
                self.afficher_message(f"Combat entre {selected_unit.name} et {unit.name}.")
                self.attendre_touche()
                duel_phase(selected_unit, unit)  # Appel au combat
                attempt_wound(selected_unit, unit)  # Appel à la phase de blessure
                return

    def flip_display(self, selected_unit=None, hovered_cell=None):
        """
        Met à jour l'affichage principal, détecte les phases de combat ou de tir.
        """
        self.screen.blit(self.BoardBackground, (0, 0))

        for unit in self.game.player1_units + self.game.player2_units:
            unit.draw(self.screen)

        if selected_unit:
            self.detect_combat_or_tir(selected_unit)

        pygame.display.flip()

    def initialize_main_menu(self):
        """
        Affiche le menu principal avec les options pour voir les règles, les pouvoirs et commencer le jeu.
        """
        title_font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 36)

        rules_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
        powers_button = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 50)
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            title_text = title_font.render("Mon Jeu de Stratégie", True, (255, 255, 255))
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

            pygame.draw.rect(self.screen, (255, 255, 255), rules_button)
            pygame.draw.rect(self.screen, (255, 255, 255), powers_button)
            pygame.draw.rect(self.screen, (255, 255, 255), start_button)

            rules_text = button_font.render("Règles du Jeu", True, (0, 0, 0))
            powers_text = button_font.render("Pouvoirs des Personnages", True, (0, 0, 0))
            start_text = button_font.render("Démarrer", True, (0, 0, 0))

            self.screen.blit(rules_text, (rules_button.x + (rules_button.width - rules_text.get_width()) // 2, rules_button.y + 10))
            self.screen.blit(powers_text, (powers_button.x + (powers_button.width - powers_text.get_width()) // 2, powers_button.y + 10))
            self.screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 10))

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
                        running = False  # Quitte le menu principal pour commencer le jeu

            pygame.display.flip()

    def show_rules(self):
        """
        Affiche l'écran des règles du jeu.
        """
        font = pygame.font.Font(None, 32)
        back_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

        rules_text_lines = [
            "Règles du Jeu:",
            "1. Chaque joueur choisit 2 personnages.",
            "2. Les joueurs déplacent leurs unités à tour de rôle.",
            "3. L'objectif est de vaincre toutes les unités adverses.",
            "4. Chaque unité a des capacités uniques.",
        ]

        line_height = font.get_height() + 10
        total_text_height = len(rules_text_lines) * line_height
        start_y = (HEIGHT - total_text_height) // 2

        running = True
        while running:
            self.screen.fill((0, 0, 0))

            for i, line in enumerate(rules_text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_x = (WIDTH - text_surface.get_width()) // 2
                text_y = start_y + i * line_height
                self.screen.blit(text_surface, (text_x, text_y))

            pygame.draw.rect(self.screen, (255, 255, 255), back_button)
            back_text = font.render("Retour", True, (0, 0, 0))
            self.screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                         back_button.y + (back_button.height - back_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(mouse_pos):
                        running = False

            pygame.display.flip()

    def show_powers(self):
        """
        Affiche l'écran des pouvoirs des personnages.
        """
        font = pygame.font.Font(None, 28)
        back_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

        running = True
        while running:
            self.screen.fill((0, 0, 0))

            powers_text_lines = [
                "Pouvoirs des Personnages:",
                "Guerrier: Puissant en attaque rapprochée.",
                "Archer: Attaque à distance avec précision.",
                "Magicien: Utilise des sorts puissants.",
                "Assassin: Agile et rapide en déplacement.",
            ]

            for i, line in enumerate(powers_text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, 100 + i * 40))

            pygame.draw.rect(self.screen, (255, 255, 255), back_button)
            back_text = font.render("Retour", True, (0, 0, 0))
            self.screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                         back_button.y + (back_button.height - back_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(mouse_pos):
                        running = False

            pygame.display.flip()
