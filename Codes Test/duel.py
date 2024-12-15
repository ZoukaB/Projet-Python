import random

class Character:
    """
    Classe représentant un personnage en combat.
    """
    def __init__(self, name, attaque, combat, force, defense, vie):
        self.name = name  # Nom du personnage
        self.attaque = attaque  # Nombre de dés à lancer
        self.combat = combat  # Valeur de combat
        self.force = force  # Valeur de force
        self.defense = defense  # Valeur de défense
        self.vie = vie  # Points de vie restants
        self.x = 0  # Position X sur la carte
        self.y = 0  # Position Y sur la carte


def roll_dice(num_dice):
    """
    Lance un certain nombre de dés et retourne une liste de résultats triés.
    :param num_dice: Nombre de dés à lancer.
    :return: Liste des résultats des dés triée en ordre décroissant.
    """
    return sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)

def duel_phase(character_a, character_b):
    """
    Simule une phase de duel entre deux personnages.
    :param character_a: Instance de Character représentant le joueur A.
    :param character_b: Instance de Character représentant le joueur B.
    :return: Résultat du duel ("A", "B", "draw").
    """
    print(f"{character_a.name} et {character_b.name} entrent en duel !")

    # Lance les dés pour chaque personnage
    roll_a = roll_dice(character_a.attaque)
    roll_b = roll_dice(character_b.attaque)

    print(f"{character_a.name} lance les dés : {roll_a}")
    print(f"{character_b.name} lance les dés : {roll_b}")

    # Trouve le dé le plus élevé pour chaque personnage
    highest_a = roll_a[0] if roll_a else 0
    highest_b = roll_b[0] if roll_b else 0

    # Compare les résultats des dés
    if highest_a > highest_b:
        print(f"{character_a.name} remporte le duel avec un dé de {highest_a} contre {highest_b} !")
        return "A"
    elif highest_b > highest_a:
        print(f"{character_b.name} remporte le duel avec un dé de {highest_b} contre {highest_a} !")
        return "B"
    else:
        # Si les meilleurs résultats sont identiques, compare les valeurs de combat
        print("Les meilleurs dés sont identiques, comparaison des valeurs de combat...")
        if character_a.combat > character_b.combat:
            print(f"{character_a.name} remporte le duel grâce à sa valeur de combat ({character_a.combat} > {character_b.combat}) !")
            return "A"
        elif character_b.combat > character_a.combat:
            print(f"{character_b.name} remporte le duel grâce à sa valeur de combat ({character_b.combat} > {character_a.combat}) !")
            return "B"
        else:
            # Si les valeurs de combat sont identiques, match nul
            print("Match nul ! Les deux personnages ont la même valeur de combat.")
            return "draw"


# test sans affichage
if __name__ == "__main__":
    # Création de deux personnages
    joueur_a = Character(name="Joueur A", attaque=4, combat=6)
    joueur_b = Character(name="Joueur B", attaque=3, combat=5)

    # Lancer la phase de duel
    resultat = duel_phase(joueur_a, joueur_b)

    # Affichage du résultat
    if resultat == "A":
        print("Joueur A remporte la phase de duel !")
    elif resultat == "B":
        print("Joueur B remporte la phase de duel !")
    else:
        print("La phase de duel se termine par un match nul.")