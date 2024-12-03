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
            
    def fire_barrier(self,orientation,screen):
        self.fire_barrier_strength = 3
        """
        Place une barrière de feu de troix cases de long 

        Parameters:
        - target_x, target_y: Coordinates of the starting square of the barrier.
        - orientation: 'horizontal' or 'vertical' orientation of the barrier.
        - all_units: List of all units on the battlefield.
        - current_turn: The current turn number in the game.
        """
        # Define barrier squares based on orientation, donner le choix au personnage lors de l'utilisation de sa capacité
        barrier_squares = []
        for i in range(3):
            if orientation == 'horizontal':
                barrier_squares.append((self.x+1 + i, self.y+1))
            elif orientation == 'vertical':
                barrier_squares.append((self.x+1, self.y+1 + i))
            else:
                print("Invalid orientation! Use 'horizontal' or 'vertical'.")
    
        print(f"Fire Barrier placed at {barrier_squares} for 3 turns!")
        #Displays fire barrier in Red
        for x, y in barrier_squares:
            pygame.draw.rect(screen, RED, (x * CELL_SIZE,
                              y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
        self.capacités = ["Mine","Fuite"]
        self.mine = 3
        self.position_mine = ()
        
    def attack(self,target,other_targets):
    #Peut lancer une bombe sur un joueur a maximum 3 case de lui qui fait des degats sur toutes les cases autour de l'ennemi
        if (abs(self.x - target.x) <= 3 and abs(self.y - target.y)<=3):
            target.vie -= self.attaque
            for unit in other_targets:
                if unit == target:
                    continue
                if abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 1:
                    unit.vie -= self.attaque
        else:
            print("L'ennemi est trop loin pour pouvoir être attaqué")
    
    def mine(self,screen):
    #Peut poser une mine sur sa case, explose lorsque quelqu'un se déplace sur cette case ==> a implémenter plus tard
        ORANGE = (255, 165, 0)
        self.position_mine = (self.x,self.y)
        if self.mine != 0:
            pygame.draw.rect(screen, ORANGE, (self.x * CELL_SIZE,
                              self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            self.mine -= 1
        else:
            print("Stock de mines épuisé !")
        
    def mine_active(self,target):
        if target.x == self.position_mine[0] and target.y == self.position_mine[1]:
            self.position_mine = ()
            target.vie -= 5
    
    def fuite(self,enemy_units):
        nb_unit = 0
        for units in enemy_units:
            if (abs(self.x - units.x) <= 2 and abs(self.y - units.y)<=2):
                nb_unit += 1
        if nb_unit >= 2:
            while self.is_selected == True:
                initial_movement = self.mouvement
                self.mouvement = 7
            self.movement = initial_movement
        else:
            "Impossible d'utiliser fuite dans ces conditions"
        
class Bourrin(Unit_new):
    def __init__(self):
        super().__init__(0,0,4,4,5,6,6,2,4,5,5,'player')
        self.capacités = ["Massue","Defense de fer"]
    
    def attack(self,target):
        if (abs(self.x - target.x) <=2 and abs(self.y - target.y)<=2):
            target.vie -= self.attaque
        else:
            print("L'ennemi est trop loin pour être attaqué !")
    
    def massue(self,target):
        #Peu importe le résultat des dés le bourrin peut infliger des dégats une fois tous les 3 tours 
        if self.energie >= 3: 
            if (abs(self.x - target.x) <=1 and abs(self.y - target.y)<=1):
                target.vie -= 5
            else:
                print("L'ennemi est trop loin pour être attaqué !")
        else:
            print("Vous n'avez pas assez d'énergie pour utiliser cette attaque !")

    def defense_de_fer(self,enemy):
        self.defense_de_fer = False
        # Une chance sur 5 de bloquer une attaque ennemi
        pourcentage = random.randint(1,6)
        if pourcentage == 1:
            self.defense_de_fer = True
        #Implémenter dans le handling player turn que si defense_de_fer = True 
        #alors l'attaque et bloqué et defense_de_fer passe a False     
    

class Infirmier(Unit_new):
    def __init__(self):
        super().__init__(0,0,6,3,4,2,3,1,1,5,5,'player')
        self.capacités = ["Soin","Potion de soin"] #"Boost de vie"
        self.potions = 3
        
    def attack(self,target):
        if (abs(self.x - target.x) <=1 and abs(self.y - target.y)<=1):
            target.vie -= self.attaque
        else:
            print("L'ennemi est trop loin pour être attaqué !")   
    
    def soin(self,target):
        #Implémenter dans tour joueur le choix de soigner ses alliés seulement
        if (abs(self.x - target.x) <=1 and abs(self.y - target.y)<=1):
            target.vie += 1
        else:
            print("L'ennemi est trop loin pour être soigné !") 
    
    def potion(self,target,other_targets):     
    #Peut lancer une potion qui soigne ses alliés sur toutes les cases autour du target
        if self.potions != 0:
            self.potions -= 1
            if (abs(self.x - target.x) <= 2 and abs(self.y - target.y)<=2):
                target.vie += 3
                for unit in other_targets:
                    if unit == target:
                        continue
                    if abs(unit.x - target.x) <= 1 and abs(unit.y - target.y) <= 1:
                        unit.vie += 3
            else:
                print("L'ennemi est trop loin pour pouvoir être attaqué")
        else:
            print("Vous n'avez plus de potions de soin !")
        
class Negociateur(Unit_new):
    def __init__(self):
        super().__init__(0,0,5,3,5,2,4,1,1,5,5,'player')
        
class Assassin(Unit_new):
    def __init__(self):
        super().__init__(0,0,6,6,3,3,4,3,1,5,5,'player')
    
    
    
    
        
