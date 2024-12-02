from unit_new import *
from unit import *

class Warrior(Unit_new):
    def __init__(self):
        super().__init__(0,0,4,6,4,4,6,3,3,5,5,'player')
        self.capacités = ['Boisson du guerrier, Cri de guerre']
        self.boisson_du_guerrier = 3
    
    def attack(self, target):
        #30% de chance de doubler son attaque
        pourcentage = random.randint(1,101)
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            if pourcentage <=  30:
                target.vie -= 2*self.attaque
            else: 
                target.vie -= self.attaque
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
        
    def boisson_du_guerrier(self,target):
        if self.boisson_du_guerrier > 0:
            target.health += 6
            self.boisson_du_guerrier -= 1
        else: 
            print("Vous n'avez plus de boisson du guerrier")
            
    def cri_de_guerre(self,target):
        if abs(self.x - target.x) <= 3 and abs(self.y - target.y) <= 3: #incorporer affichage ??
            if target.defense%2 != 0:
                target.defense = (target.defense-1)/2
            else:
                target.defense = target.defense/2
            self.energie -= 4
        else:
            print("Impossible d'utiliser la capacite spéciale cri de guerre")

class Magicien(Unit_new):
    def __init__(self):
        super().__init__(0,0,5,3,4,2,4,1,2,5,5,'player')
        self.capacités = ["Sort de guérison","Barrière de feu"]
        self.fire_barrier_strength = 0
    
    def attack(self,target,other_targets):
        #Peut lancer un sort jusqu'à 5 cases devant lui mais seulement dans la direction x
        if (abs(self.x - target.x) <= 5 and abs(self.y - target.y) == 0) or (abs(self.x - target.x) == 0 and abs(self.y - target.y) <= 5):
            target.vie -= self.attaque
            for unit in other_targets:
                if unit == target:
                    continue
                if abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 2:
                    unit.vie -= self.attaque // 2 # Half damage for splash
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
    
    def sort_de_guerison(self,target):
        #Se soigne d'1 pv et inflige des dégats directes 
        if abs(self.x - target.x) <= 2 and abs(self.y - target.y) <= 2:
            if self.energie >= 2:
                self.energie -= 2
                target.vie -= self.attaque 
                self.vie += 1
            else:
                print("Jauge d'énergie trop faible pour utiliser ce sort")
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
            
    def fire_barrier(self,orientation,all_units, current_turn):
        """
        Place une barrière de feu de troix cases de long 

        Parameters:
        - target_x, target_y: Coordinates of the starting square of the barrier.
        - orientation: 'horizontal' or 'vertical' orientation of the barrier.
        - all_units: List of all units on the battlefield.
        - current_turn: The current turn number in the game.
        """
        # Define barrier squares based on orientation
        barrier_squares = []
        for i in range(3):
            if orientation == 'horizontal':
                barrier_squares.append((self.x+1 + i, self.y+1))
            elif orientation == 'vertical':
                barrier_squares.append((self.x+1, self.y+1 + i))
            else:
                print("Invalid orientation! Use 'horizontal' or 'vertical'.")
        
        self.fire_barrier_strength = 3
        #Implémenter un -1 à chaque fin de tour
        print(f"Fire Barrier placed at {barrier_squares} for 3 turns!")

class Archer(Unit_new):
    def __init__(self):
        super().__init__(0,0,6,4,2,3,4,2,2,5,5,'player')
        self.capacités = ["Flèche de guérison","Headshot"]
        self.flèches_soigneuses = 3
    
    def attack(self,target):
        #Peut tirer une flèche jusqu'à 5 cases devant lui mais seulement dans la direction x
        if (abs(self.x - target.x) <= 5 and abs(self.y - target.y) == 0) or (abs(self.x - target.x) == 0 and abs(self.y - target.y) <= 5):
            target.vie -= self.attaque
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
    
    def fleche_de_guerison(self,target):
        #Tire un fleche qui soigne ses aliés 
        if (abs(self.x - target.x) <= 5 and abs(self.y - target.y) == 0) or (abs(self.x - target.x) == 0 and abs(self.y - target.y) <= 5):
            if self.flèches_soigneuses != 0:
                self.flèches_soigneuses -= 1
                target.vie += 5
            else:
                print("Vous n'avez plus de flèches de guérison")
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
    
    def headshot(self,target):
        if (abs(self.x - target.x) <= 5 and abs(self.y - target.y) == 0) or (abs(self.x - target.x) == 0 and abs(self.y - target.y) <= 5):
            if self.energie >= 3:
                self.energie -= 3
                target.vie -= 10 
            else:
                print("Vous n'avez pas assez d'énergie pour cette attaque")
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
        
class Mineur(Unit_new):
    def __init__(self):
        super().__init__(0,0,5,4,5,5,5,2,3,5,5,'player')
        
class Bourrin(Unit_new):
    def __init__(self):
        super().__init__(0,0,4,4,5,6,6,2,4,5,5,'player')

class Infirmier(Unit_new):
    def __init__(self):
        super().__init__(0,0,6,3,4,2,3,1,1,5,5,'player')
        
class Negociateur(Unit_new):
    def __init__(self):
        super().__init__(0,0,5,3,5,2,4,1,1,5,5,'player')
        
class Assassin(Unit_new):
    def __init__(self):
        super().__init__(0,0,6,6,3,3,4,3,1,5,5,'player')
    
    
    
    
        
