from unit_new import *

class Warrior(Unit_new):
    def __init__(self):
        super().__init__(0,0,4,6,4,4,6,3,3,5,5,'player')
        self.capacités = ['Boisson du guerrier, Cri de guerre']
        self.boisson_du_guerrier = 3
    
    def attack(self, target):
        "30% de chance de doubler son attaque"
        pourcentage = random.randint(1,101)
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            if pourcentage <=  30:
                target.vie -= 2*self.attaque
            else: 
                target.vie -= self.attaque
        else:
            print("L ennemi est trop loin pour pouvoir être attaqué")
        
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
        else:
            print("Impossible d'utiliser la capacite spéciale cri de guerre")


    
    
    
    
        
