class Character:
    """
    Classe représentant un personnage en combat.
    """
    def __init__(self, name, attaque, force, defense, vie):
        self.name = name  # Nom du personnage
        self.attaque = attaque  # Nombre de dés à lancer pour les actions
        self.force = force  # Valeur de force
        self.defense = defense  # Valeur de défense
        self.vie = vie  # Points de vie restants

def roll_dice(num_dice):
    """
    Lance un certain nombre de dés et retourne une liste de résultats triés.
    :param num_dice: Nombre de dés à lancer.
    :return: Liste des résultats des dés triée en ordre décroissant.
    """
    import random
    return sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)

def get_wound_threshold(force, defense):
    """
    Récupère le seuil requis pour blesser en fonction de la force et de la défense
    en se basant sur la matrice de blessure.
    :param force: Force de l'attaquant.
    :param defense: Défense du défenseur.
    :return: Seuil pour blesser (int), ou None si aucune blessure possible.
    """
    wound_matrix = {
        1: [4, 5, 5, 5, 6, 6, 6, 6, None, None],
        2: [4, 4, 5, 5, 5, 6, 6, 6, 6, None],
        3: [3, 4, 4, 5, 5, 5, 6, 6, 6, 6],
        4: [3, 3, 4, 4, 5, 5, 5, 6, 6, 6],
        5: [3, 3, 3, 4, 4, 5, 5, 5, 6, 6],
        6: [3, 3, 3, 3, 4, 4, 5, 5, 5, 5],
        7: [3, 3, 3, 3, 3, 4, 4, 5, 5, 5],
        8: [3, 3, 3, 3, 3, 3, 4, 4, 5, 5],
        9: [3, 3, 3, 3, 3, 3, 3, 4, 4, 5],
        10: [3, 3, 3, 3, 3, 3, 3, 3, 4, 4],
    }
    if force > 10 or defense > 10 or force < 1 or defense < 1:
        return None  # Force ou défense hors des limites de la table
    return wound_matrix[force][defense - 1]

def attempt_wound(attacker, defender):
    """
    Tente de blesser un défenseur en fonction des règles.
    :param attacker: Le personnage attaquant (gagnant du duel).
    :param defender: Le personnage défenseur (perdant du duel).
    :return: Tuple contenant le nombre de blessures infligées et le statut du défenseur.
    """
    # Obtenir le seuil requis pour blesser
    threshold = get_wound_threshold(attacker.force, defender.defense)
    if threshold is None:
        print(f"{attacker.name} ne peut pas blesser {defender.name} avec ses dés.")
        return 0, "intact"

    # Lancer les dés
    rolls = roll_dice(attacker.attaque)
    print(f"{attacker.name} lance ses dés : {rolls}")
    wounds = sum(1 for roll in rolls if roll >= threshold)

    if wounds == 0:
        print(f"{attacker.name} n'a pas réussi à blesser {defender.name}.")
        return 0, "intact"

    # Appliquer les blessures
    print(f"{attacker.name} inflige {wounds} blessure(s) à {defender.name} !")
    defender.vie -= wounds

    if defender.vie <= 0:
        print(f"{defender.name} a été tué !")
        return wounds, "mort"
    else:
        print(f"{defender.name} survit avec {defender.vie} point(s) de vie.")
        return wounds, "blessé"

# Exemple d'utilisation
if __name__ == "__main__":
    # Création des personnages
    attaquant = Character(name="Attaquant", attaque=4, force=4, defense=3, vie=5)
    defenseur = Character(name="Défenseur", attaque=3, force=3, defense=6, vie=3)

    # Simulation de la tentative de blessure
    print(f"Début de la phase de blessure entre {attaquant.name} et {defenseur.name}.")
    wounds, status = attempt_wound(attaquant, defenseur)
    print(f"Résultat : {defenseur.name} est {status}.")
