import pygame
from duel import Character, roll_dice, duel_phase
from wound import attempt_wound, get_wound_threshold

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


def diviser_texte(message, largeur_max):
    mots = message.split(" ")
    lignes = []
    ligne = ""
    for mot in mots:
        if font.size(ligne + mot)[0] < largeur_max:
            ligne += mot + " "
        else:
            lignes.append(ligne)
            ligne = mot + " "
    lignes.append(ligne)
    return lignes

# message centré dans un encadré
def afficher_message(ecran, message, decalage_y=0):
    ecran.fill(NOIR, (0, HAUTEUR_ECRAN - 150, LARGEUR_ECRAN, 150))
    lignes = diviser_texte(message, LARGEUR_ECRAN - 20)
    y_offset = HAUTEUR_ECRAN - 140
    for ligne in lignes:
        surface_texte = font.render(ligne, True, BLANC)
        rect_texte = surface_texte.get_rect(center=(LARGEUR_ECRAN // 2, y_offset))
        ecran.blit(surface_texte, rect_texte)
        y_offset += 30
    pygame.display.flip()

# les résultats des dés avec les images
def afficher_resultats_des(ecran, resultats_des, images_des, y_depart):
    espacement_horizontal = 150
    x_depart = (LARGEUR_ECRAN - (len(resultats_des) * espacement_horizontal)) // 2
    for i, resultat in enumerate(resultats_des):
        ecran.blit(images_des[resultat], (x_depart + i * espacement_horizontal, y_depart))
    pygame.display.flip()

# un appui sur une touche (par défaut Espace)
def attendre_touche(touche=pygame.K_SPACE):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == touche:
                    return
                if event.key == pygame.K_ESCAPE:  # Quitter avec Échap
                    pygame.quit()
                    exit()

# Dessiner la carte
def dessiner_carte(ecran, joueur_a, joueur_b):
    ecran.fill(BLANC)
    for ligne in range(MAP_LIGNES):
        for colonne in range(MAP_COLONNES):
            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(ecran, NOIR, rect, 1)
    # Dessiner les joueurs
    pygame.draw.rect(ecran, ROUGE, (joueur_a.x * TAILLE_CASE, joueur_a.y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
    pygame.draw.rect(ecran, BLEU, (joueur_b.x * TAILLE_CASE, joueur_b.y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
    # Afficher "Combat"
    texte_combat = font.render("Combat !", True, ROUGE)
    ecran.blit(texte_combat, (LARGEUR_ECRAN // 2 - 50, 10))
    pygame.display.flip()

# Fonction principale de simulation de combat. ZECA c'est là que tu dois modifier les stats et tester les capacités !!!
def test_combat():
    # Configuration de l'écran
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Test Combat")

    # Création des personnages
    joueur_a = Character(name="Guerrier A", attaque=4, combat=6, force=4, defense=5, vie=10)
    joueur_b = Character(name="Guerrier B", attaque=3, combat=5, force=3, defense=4, vie=8)

    # Placement des joueurs sur la carte
    joueur_a.x, joueur_a.y = 5, 5
    joueur_b.x, joueur_b.y = 5, 6

    # la carte initiale
    dessiner_carte(ecran, joueur_a, joueur_b)

    # Phase 1 : Duel
    afficher_message(ecran, f"{joueur_a.name} (Joueur A), lancez {joueur_a.attaque} dés. Appuyez sur espace.")
    attendre_touche()
    resultats_a = roll_dice(joueur_a.attaque)
    afficher_message(ecran, f"Résultat : {resultats_a}")
    afficher_resultats_des(ecran, resultats_a, images_des_joueur_a, HAUTEUR_ECRAN - 110)
    attendre_touche()

    afficher_message(ecran, f"{joueur_b.name} (Joueur B), lancez {joueur_b.attaque} dés. Appuyez sur espace.")
    attendre_touche()
    resultats_b = roll_dice(joueur_b.attaque)
    afficher_message(ecran, f"Résultat : {resultats_b}")
    afficher_resultats_des(ecran, resultats_b, images_des_joueur_b, HAUTEUR_ECRAN - 110)
    attendre_touche()

    # Déterminer le gagnant du duel
    resultat = duel_phase(joueur_a, joueur_b)

    if resultat == "A":
        gagnant, perdant = joueur_a, joueur_b
        afficher_message(ecran, f"{gagnant.name} remporte le duel !")
    elif resultat == "B":
        gagnant, perdant = joueur_b, joueur_a
        afficher_message(ecran, f"{gagnant.name} remporte le duel !")
    else:
        afficher_message(ecran, "Le duel est un match nul.")
        attendre_touche()
        return

    attendre_touche()

    # Phase 2 : Blessures
    seuil_blessure = get_wound_threshold(gagnant.force, perdant.defense)
    afficher_message(ecran, f"{gagnant.name}, lancez {gagnant.attaque} dés pour blesser. Vous devez faire {seuil_blessure}+ pour infliger une blessure.")
    attendre_touche()
    resultats_blessure = roll_dice(gagnant.attaque)
    afficher_message(ecran, f"Résultats des dés : {resultats_blessure}")
    afficher_resultats_des(ecran, resultats_blessure, images_des_joueur_a if gagnant == joueur_a else images_des_joueur_b, HAUTEUR_ECRAN - 110)
    attendre_touche()

    blessures, statut = attempt_wound(gagnant, perdant)
    if statut == "mort":
        afficher_message(ecran, f"{perdant.name} a été tué.")
    elif statut == "blessé":
        afficher_message(ecran, f"{perdant.name} a été blessé. Points de vie restants : {perdant.vie}")
    else:
        afficher_message(ecran, f"{perdant.name} n'a pas été blessé.")
    attendre_touche()

    # Fin du combat
    afficher_message(ecran, "Combat terminé. Appuyez sur Échap pour quitter.")
    attendre_touche(pygame.K_ESCAPE)


if __name__ == "__main__":
    test_combat()
