from unit_new import *

class Warrior(Unit):
    def __init__(self):
        super().__init__(0,0,4,6,4,4,6,3,3,5,5,'player')
        self.capacités = ['Boisson du guerrier, Cri de guerre']
        self.boisson_du_guerrier = 3
        
    def boisson_du_guerrier(self,target):
        if self.boisson_du_guerrier > 0:
            target.health += 6
            self.boisson_du_guerrier -= 1
        else: 
            print("Vous n'avez plus de boisson du guerrier")
            
    def cri_de_guerre(self,target):
        if self.energie >= 4:
            if target.defense%2 != 0:
                target.defense = (target.defense-1)/2
            else:
                target.defense = target.defense/2
            self.energie -= 4
        else:
            print("Jauge d'énergie trop faible pour utiliser cette capacité")
    
    #Dernier souffle ==> permet de forcément infliger des dégats lorsque le guerrier meurt
