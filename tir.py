import pygame
from duel import Character, roll_dice

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
LARGEUR_ECRAN, HAUTEUR_ECRAN = 800, 600
TAILLE_CASE = 50
MAP_LIGNES, MAP_COLONNES = HAUTEUR_ECRAN // TAILLE_CASE, LARGEUR_ECRAN // TAILLE_CASE

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)

# Polices
font = pygame.font.Font(None, 36)

# Charger les images des dés
def charger_images_des(chemin_base, joueur):
    images_des = {}
    for i in range(1, 7):
        chemin_image = f"{chemin_base}/{joueur}/{i}.jpg"
        images_des[i] = pygame.image.load(chemin_image)
    return images_des

CHEMIN_IMAGES = "dice_images"
images_des_joueur_a = charger_images_des(CHEMIN_IMAGES, "dice_player_a")
images_des_joueur_b = charger_images_des(CHEMIN_IMAGES, "dice_player_b")

# Diviser un message long en plusieurs lignes
def diviser_texte(message, largeur_max):
    mots = message.split(" ")
    lignes = []
    ligne = ""
    for mot in mots:
        if font.size(ligne + mot)[0] < largeur_max:
            ligne += mot + " "
        else:
            lignes.append(ligne.strip())
            ligne = mot + " "
    lignes.append(ligne.strip())
    return lignes

# Afficher un message centré
def afficher_message(ecran, message):
    ecran.fill(NOIR, (0, HAUTEUR_ECRAN - 150, LARGEUR_ECRAN, 150))
    lignes = diviser_texte(message, LARGEUR_ECRAN - 20)
    y_offset = HAUTEUR_ECRAN - 140
    for ligne in lignes:
        surface_texte = font.render(ligne, True, BLANC)
        rect_texte = surface_texte.get_rect(center=(LARGEUR_ECRAN // 2, y_offset))
        ecran.blit(surface_texte, rect_texte)
        y_offset += 30
    pygame.display.flip()

# Afficher les résultats des dés avec les images
def afficher_resultats_des(ecran, resultats_des, images_des, y_depart):
    espacement_horizontal = 150
    x_depart = (LARGEUR_ECRAN - (len(resultats_des) * espacement_horizontal)) // 2
    for i, resultat in enumerate(resultats_des):
        ecran.blit(images_des[resultat], (x_depart + i * espacement_horizontal, y_depart))
    pygame.display.flip()

# Attendre un appui sur une touche
def attendre_touche(touche=pygame.K_SPACE):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == touche:
                return

# Déplacer le curseur avec les flèches pour sélectionner une cible
def selectionner_cible(ecran, archer, personnages):
    cible = None
    x, y = archer.x, archer.y
    while True:
        ecran.fill(BLANC)
        # Dessiner la carte
        for ligne in range(MAP_LIGNES):
            for colonne in range(MAP_COLONNES):
                rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                pygame.draw.rect(ecran, NOIR, rect, 1)

        # Dessiner les personnages
        pygame.draw.rect(ecran, ROUGE, (archer.x * TAILLE_CASE, archer.y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        for perso in personnages:
            if perso != archer:
                pygame.draw.rect(ecran, BLEU, (perso.x * TAILLE_CASE, perso.y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

        # Dessiner la sélection
        pygame.draw.rect(ecran, VERT, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 2)

        afficher_message(ecran, "Sélectionnez une cible. Appuyez sur Entrée pour valider.")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y > 0:
                    y -= 1
                elif event.key == pygame.K_DOWN and y < MAP_LIGNES - 1:
                    y += 1
                elif event.key == pygame.K_LEFT and x > 0:
                    x -= 1
                elif event.key == pygame.K_RIGHT and x < MAP_COLONNES - 1:
                    x += 1
                elif event.key == pygame.K_RETURN:
                    for perso in personnages:
                        if perso.x == x and perso.y == y:
                            cible = perso
                            return cible


# Fonction principale de tir
def phase_tir():
    # Configuration de l'écran
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Phase de Tir")

    # Création des personnages
    archer = Character(name="Archer", attaque=1, combat=3, force=3, defense=2, vie=5)
    cible1 = Character(name="Cible 1", attaque=2, combat=4, force=4, defense=3, vie=8)
    cible1.x, cible1.y = 5, 5
    archer.x, archer.y = 3, 3

    # Liste des personnages
    personnages = [archer, cible1]

    # Dessiner la carte initiale
    afficher_message(ecran, "Phase de tir : sélectionnez une cible.")
    cible = selectionner_cible(ecran, archer, personnages)

    if not cible:
        afficher_message(ecran, "Aucune cible sélectionnée. Annulation du tir.")
        attendre_touche()
        pygame.quit()
        return

    # Phase de tir : Lancer pour toucher
    afficher_message(ecran, f"{archer.name} tire sur {cible.name}. Appuyez sur espace pour lancer.")
    attendre_touche()
    resultat_tir = roll_dice(1)[0]  # Lancer un dé
    afficher_message(ecran, f"Résultat du tir : {resultat_tir}")
    afficher_resultats_des(ecran, [resultat_tir], images_des_joueur_a, HAUTEUR_ECRAN - 110)
    attendre_touche()

    if resultat_tir < 3:
        afficher_message(ecran, f"{archer.name} rate son tir.")
        attendre_touche()
        pygame.quit()
        return

    # Phase de blessure : Relancer pour blesser
    afficher_message(ecran, f"Tir réussi ! Appuyez sur espace pour tenter de blesser.")
    attendre_touche()
    resultat_blessure = roll_dice(1)[0]
    afficher_message(ecran, f"Résultat du jet pour blesser : {resultat_blessure}")
    afficher_resultats_des(ecran, [resultat_blessure], images_des_joueur_a, HAUTEUR_ECRAN - 110)
    attendre_touche()

    if resultat_blessure < 5:
        afficher_message(ecran, f"{archer.name} n'a pas réussi à blesser {cible.name}.")
        attendre_touche()
    else:
        cible.vie -= 1
        if cible.vie <= 0:
            afficher_message(ecran, f"{cible.name} a été tué par {archer.name} !")
        else:
            afficher_message(ecran, f"{cible.name} est blessé. Points de vie restants : {cible.vie}")
        attendre_touche()

    # Fin de la phase de tir
    afficher_message(ecran, "Phase de tir terminée. Appuyez sur Échap pour quitter.")
    attendre_touche(pygame.K_ESCAPE)

# Lancer la phase de tir
if __name__ == "__main__":
    phase_tir()
