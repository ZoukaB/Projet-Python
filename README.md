Statistiques personnages jouables v1


Rappel de la valeur des stats :

M = Mouvement correspond au nombre de cases que peut traverser le personnage sur la map (hors règles spéciales). 

C = Combat correspond à un nombre entre 1 et 6 (spécification des combats plus bas après les stats de personnages)

T = Tir correspond à la valeur de dé (hors règles spéciales) que le personnage doit atteindre pour réussir un tir avec une arme à distance. La distance que peut couvrir le tir et la force du tir pour blesser seront spécifiés sur l’équipement correspondant.
Ex: Archer tente de tirer à l’arc. Il doit lancer un dé et faire 3 ou + (soit une chance sur deux)
NB : certains personnages ont une valeur de tir sans posséder d’arc de base au cas où ils ramasseraient ou achèteraient un arc pendant la partie

F = Force correspond à la capacité à blesser une fois avec remporté un combat  (hors règles spéciales) (spécification des combats plus bas après les stats de personnages)

D = Défense correspond à la capacité à se défendre une fois avec remporté un combat (hors règles spéciales) (spécification des combats plus bas après les stats de personnages)

A= Attaque correspond au nombre de dés utilisés dans un combat
Ex:  Le guerrier a une valeur d’attaque de 2 il lancera donc 2 dés

PV =  points de vie correspond au nombre de blessure que peut encaisser un personnage avant de mourir. 

( stat à ajouter possiblement) 

B/I=Bravoure/Intelligence correspondrait à la capacité du personnage à ne pas paniquer face à une situation dangereuse. Elle correspond comme la valeur de tir à une valeur de dé à atteindre.
Ex: Personnage doit traverser une coulée de lave, il a une bravour de X+ et doit donc lancer un dé et faire X au minimum sans quoi son déplacement est annulé.

Elle pourrait également servir à savoir si le personnage perçoit quelque chose type Invisibilité etc.




Idéalement on pourrait utiliser le même système de stat pour les ennemis non joueurs pour réutiliser les mêmes classes.



Stats de chaque personnage : 





Description idées de règles de jeu : 

Le jeu est en tour par tour avec 2 joueurs ou plus, prenons ici l’exemple de 2 joueurs, qu’on nommera A et B.

Début de la partie : 
Joueur A et joueur B tirent un dé, celui avec le plus chiffre commence, on dira qu’il a l’initiative. S’ils font une égalité ils relancent.

Chaque joueur doit prendre X (par exemple 4 ) des 8 personnages dans l’équipe qu’il jouera. Ainsi chaque joueur aura le même nombre de personnage mais pas les mêmes (choix à l’aveugle).

Le jeu doit être en tour par tour donc dès lors on alternera entre tour du joueur A et  tour du joueur B, jusqu’à ce qu’une condition de victoire soit remplie par un des joueurs (ou les joueurs en général si on part sur un délire type coopération).

Chaque tour s’articule en 3 phases : 
Mouvement 
Tir ou Magie (pour ce qui peuvent), négociation d’alliance ou action spéciale avec PNJ à déterminer
Combat



Phase de Mouvement: 

Le joueur (disons Joueur A) qui possède l’initiative décide de déplacer un de ses personnages. Il peut se déplacer du nombre de cases spécifiées par sa valeur de déplacement (ex 4 pour le guerrier).

Ensuite c’est au joueur B de faire de même

Chaque joueur bouge un personnage chacun son tour jusqu’à ce que tous ses personnages aient bougé. Bien sûr, il peut décider de ne pas en faire bouger certains.

Si un personnage rencontre une case d’un type qu’il ne peut pas traverser (ex : lave) il doit automatiquement s’arrêter.

2 personnages ne peuvent pas se trouver sur une même case simultanément.

Si un personnage appartenant au joueur A se retrouve en contact avec un personnage appartenant au joueur B un combat est enclenché automatiquement ( qui se résolvera à la phase de combat).

Si un personnage rencontre un pnj (à savoir se retrouve sur une case adjacente au pnj), il résout les effets liés au pnj immédiatement (exemple acheter une arme)



Phase de tir/magie

S’ils ne sont pas engagé dans un combat, les personnages possédant une arme à distance (ex: arc) ou pouvant faire de la magie (ex: magicien, infirmier), peuvent tirer une flèche ou lancer un sort pendant cette phase.



Combat

S’il y a des combats, ils sont résolus pendant cette phase.

Sont considérés en combat 2 personnages ou plus n’appartenant pas au même joueur et situés sur des cases adjacentes.

 Le combat pour être fun, interactif et pas forcément joué d’avance, se décompose en 2 phases:
le duel
la blessure

Prenons comme exemple cette situation : 




Le guerrier du joueur A est en contact avec le bourrin du joueur B. Un combat s’enclenche.

Duel: le guerrier a une valeur de combat de 6 et le bourrin en a une de 4. Le guerrier a 3 attaques, le bourra en a 2.

Le joueur A lance donc 3 dés, le joueur B en lance 2.

Si le guerrier a une meilleur valeur de dé sur un des 3 dés que le bourrin (ex le guerrier fait 1 3 et 5 et le bourrin fait 1 et 4), alors il remporte le combat. 

Si leur meilleure valeur de dé est la même (ex le guerrier fait 1 3 et 5 et le bourrin fait 2 et 5) alors le guerrier gagne car il a une valeur de combat supérieur au bourrin.

La blessure : le personnage qui a gagné le duel va tenter de blesser l’adversaire et le personnage qui a perdu le duel va tenter de se défendre.

Toujours avec notre exemple, le guerrier a gagné le combat et tente de blesser le bourrin. Il va donc lancer un nombre de dés correspondant à sa valeur d’attaque (3).


Une fonction matrice prenant en compte la force du guerrier et la défense du bourrin sortira la valeur de dé minimale à sortir pour permettre de blesser l’adversaire. La voici : 



Dans notre exemple, le guerrier a une force de 4 et le bourrin a une défense de 6. Il devra donc sortir un 5 parmis ses 3 dés pour espérer le blesser.
Cas particuliers :

Un combat peut être un 1v1 mais il est tout à fait possible d’attaquer un personnage ennemi via 2 cases distinctes.



Ici le joueur A a 2 personnages en bleu qui attaquent de 2 côtés différent le joueur B en rouge. Le joueur A lancera les attaques séparément et blessera séparément s’il gagne le combat. Si le joueur B gagne le duel il décidera qui tenter de blesser entre les 2 personnages du joueur A.

Les 2v2 sont impossibles, on décompose toujours par 1v1 ou 2v1 


Ici le joueur A et le joueur B ont 2 combats côte à côte. Il y a aura donc un 1v1 à droite et un 1v1 à gauche.
















Idée de but du jeu (à compléter) : 

Pour avoir une classe type de jeu on peut implémenter plusieurs modes. 

Idée Assassinat : Le joueur A désigne en secret un personnage du joueur B à éliminer et le joueur B fait de même

Idée Traversée de la map : Un des deux joueurs tiré au sort doit faire passer tous ses personnages d’un côté à l’autre de la map et le joueur B doit l’en empêcher

Idée Capture du drapeau : Un objectif se trouve au milieu de la map et les deux joueurs doivent s’en emparer et l’emmener dans un endroit précis du côté du joueur adverse









