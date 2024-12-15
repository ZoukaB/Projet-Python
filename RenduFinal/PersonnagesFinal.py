import pygame
import random
from UnitFinal import *
from DisplayFinal import *
  
class Guerrier(Unit):
    def __init__(self, x, y, mouvement,defense, attaque, vie, max_vie, energie,max_energie, team):
        super().__init__(x, y, mouvement, defense, attaque, vie, max_vie,energie,max_energie, team)
        self.capacités = ['Boisson du guerrier', 'Téméraire']
        self.boisson_du_guerrier = 3
        self.attack_range = 1
        self.temeraire_actif = False
        # Images of sword and warrior
        self.arrow_image = pygame.image.load("Images_armes/Espada.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))
        
        self.image_player1 = pygame.image.load("PersosBoard/warrior1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/warrior2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
  
    def attack(self, target): #10% de chance de doubler ses dégats
        pourcentage = random.randint(1,11)
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            if pourcentage <= 1 and self.temeraire_actif == False:
                damage = max(1, 2*self.attaque - target.defense)
            else:
                damage = max(1, self.attaque - target.defense)
        return damage
        
    def boisson_guerrier(self): #Regenère 3 PV
        if self.boisson_du_guerrier != 0:
            self.boisson_du_guerrier -= 1
            self.vie = min(self.vie + 3, self.max_vie)
            return "Vous venez d'utiliser une boisson du guerrier"
        else: 
            return "Vous n'avez plus de boisson du guerrier"
    
    def temeraire(self): #Assure des dégats doublé mais utilise de l'énergie
        if self.energie >= 5:
            self.temeraire_actif = True
            self.energie -= 5
            self.attaque = 2*self.attaque
            return "Téméraire activé !"
        else:
            return "Plus assez d'énergie pour activer cette capacité"   

    def desactive_temeraire(self):
        self.attaque = self.attaque // 2
        self.temeraire_actif = False
        
class Archer(Unit):
    def __init__(self, x, y, mouvement,defense, attaque, vie, max_vie, energie,max_energie, team):
        super().__init__(x, y, mouvement,defense, attaque, vie, max_vie, energie,max_energie, team)
        self.capacités = ['Fleche de soin', 'Headshot']
        self.attack_range = 5
        self.fleche_soigneuse = 3
        self.headshot_actif = False
        # Image of the arrow
        self.arrow_image = pygame.image.load("Images_armes/arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # scale image
        
        self.image_player1 = pygame.image.load("PersosBoard/archer1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/archer2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            damage = max(1, self.attaque - target.defense)
            return damage

    def fleche_de_guerison(self,target):
        #Tire un fleche qui soigne ses alliés 
        if self.fleche_soigneuse != 0:
            self.fleche_soigneuse -= 1
            if target.vie <= target.max_vie-5:
                target.vie += 5
            else:
                target.vie = target.max_vie
                return "Vous venez d'utiliser une flèche de guérison"
        else:
            return "Vous n'avez plus de flèches de guérison"
    
    def headshot(self):
        #Triple ses dégats 
        if self.energie >= 10:
            self.energie -= 6
            self.attaque = 3*self.attaque
            self.headshot_actif = True
            return "Capacité headshot activée !"
        else:
            return "Vous n'avez pas assez d'énergie pour cette attaque"
    
    def annul_headshot(self):
        self.attaque = self.attaque//3
        self.headshot_actif = False

class Magicien(Unit):
    def __init__(self, x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team):
        super().__init__(x, y, mouvement,defense, attaque, vie, max_vie,energie, max_energie, team)
        self.capacités = ["Sort de poison", "Boule de feu"]
        self.attack_range = 5
        self.stock_boule_de_feu = 3
        self.boule_de_feu_range = 5
        # Image of the fireball
        self.arrow_image = pygame.image.load("Images_armes/fireball.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # Scale image
        
        self.image_player1 = pygame.image.load("PersosBoard/wizard1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/wizard2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            damage = max(1, self.attaque - target.defense)
            return damage

    def sort_de_poison(self,target):
        #Empoisonne un ennemi pendant 3 tours
        if self.energie >= 4:
            self.energie -=4
            target.empoisonné = True
            target.compteur = 3
            return "Sort de poison lancé"
        else:
            return "Pas assez d'énergie pour utiliser ce sort"

    def boule_de_feu(self, target_x, target_y, enemies):
        #Envoie une boule de feu qui fait des dégats de zone
        if self.stock_boule_de_feu != 0:
            self.stock_boule_de_feu -= 1
            for enemy in enemies:
                if abs(enemy.x - target_x) <= 1 and abs(enemy.y - target_y) <= 1:
                    enemy.vie -= 2
            return "Vous venez de lancer une boule de feu"
        else:
            return "Plus de boules de feu"
          
class Assassin(Unit):
    def __init__(self, x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team):
        super().__init__(x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team)
        self.fatality = 1
        self.attack_range = 2
        self.capacités = ["Coup fatal", "Fuite"]
        self.coup_fatal_actif = False
                # Image to attack and character
        self.arrow_image = pygame.image.load("Images_armes/ninja.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))
        
        self.image_player1 = pygame.image.load("PersosBoard/assasin1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/assasin2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            damage = max(1, self.attaque - target.defense)
            return damage
        
    def coup_fatal(self):
        #Permet de tuer a coup sur un ennemi, mais l'affaibli bcp et utilise toute son énergie
        if self.fatality != 0 and self.energie == 10:
            self.coup_fatal_actif = True
            self.fatality = 0 
            self.attaque = self.attaque * 100
            self.vie = 2
            self.energie = 0
            return "Capacité coup fatal activée"
        else:
            return "Vous n'êtes pas en mesure d'utiliser cette capacité"
    
    def desactive_coup_fatal(self):
        self.coup_fatal_actif = False
        self.attaque = self.attaque //100
        
    def fuite(self,target_x,target_y):
        #Permet de se téléporter n'importe ou
        if self.vie <= 4 and self.energie >= 5: 
            self.x = target_x
            self.y = target_y
            return "Capacité fuite activée "
        else:
            return "Vous ne pouvez pas prendre la fuite"
 
class Infirmier(Unit):
    def __init__(self, x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team):
        super().__init__(x, y, mouvement, defense, attaque, vie, max_vie, energie,max_energie, team)
        self.potions_de_soin = 3
        self.attack_range = 1
        self.healing_range = 2
        self.potion_range = 5
        self.capacités = ["Potion de soin", "Soin intensif"]
        
        self.arrow_image = pygame.image.load("Images_armes/seringue.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # scale image
        
        self.image_player1 = pygame.image.load("PersosBoard/nurse1.png").convert_alpha()
        self.image_player1 = pygame.transform.scale(self.image_player1, (CELL_SIZE, CELL_SIZE))

        self.image_player2 = pygame.image.load("PersosBoard/nurse2.png").convert_alpha()
        self.image_player2 = pygame.transform.scale(self.image_player2, (CELL_SIZE, CELL_SIZE))
        
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= self.attack_range and abs(self.y - target.y) <= self.attack_range:
            damage = max(1, self.attaque - target.defense)
            return damage
        
    def potion_soin(self,x,y,target):
        if self.potions_de_soin != 0:
            self.potions_de_soin -= 1
            for unit in target:
                if abs(unit.x - x) <= 1 and abs(unit.y - y) <= 1:
                    if unit.vie <= unit.max_vie - 3:
                        unit.vie += 3
                    else:
                        unit.vie = unit.max_vie
            return "Vous venez d'utiliser une potion de soin"
        else:
            return "Plus de potions de soin"
            
    def soin_intensif(self, allies):
        if self.energie >= 3:
            self.energie -= 3
            healed = False  # Flag to track if at least one ally was healed

            for ally in allies:
                distance = abs(self.x - ally.x) + abs(self.y - ally.y)
                if distance <= self.healing_range:
                    ally.vie += 3
                    if ally.vie > ally.max_vie:
                        ally.vie = ally.max_vie  # Ensure the HP does not exceed max HP
                    healed = True
                    return "Soin intensif activée"

            if not healed:
                return "Aucun allié à portée pour soigner"
        else:
            return "Pas assez d'énergie pour utiliser cette capacité."
