Rapport Projet POO
Groupe: IPS-SMR - 3
BARAJAS OLAN Itzel María 
BUCLET Zeca
PHILIPPE Paul Etienne

Ce projet a pour objectif de réaliser un jeu au tour par tour pour deux joueurs en utilisant la bibliothèque Pygame. Le but du jeu est de construire sa propre équipe à partir de plusieurs personnages et de vaincre l'équipe adverse en utilisant les capacités et les compétences spécifiques de chaque personnage.

Fonctionnalités implémentées
Fonctionnalités des personnages
En initialisant une classe Unit dont tous les personnages héritent, nous avons défini les attributs de cette dernière pour initialiser les statistiques de base des personnages, à savoir : points de vie, mouvement, attaque, défense, énergie, énergie maximum, vie maximum et équipe.
Unit contient également des méthodes communes à tous les personnages telles que :

draw pour afficher l’unité sur l’écran
move pour déplacer l’unité
attack_with_animation pour gérer l’affichage des attaques
attack qui gère les dégâts infligés par une unité en fonction de la portée d’attaque
poison_actif pour gérer les unités empoisonnées
recup_energie pour régénérer l’énergie des unités à chaque fin de tour

Nous avons décidé d’implémenter cinq personnages jouables avec chacun des capacités spéciales qui leur sont propres. Ces capacités se concentrent surtout sur la modification des statistiques d’attaque, l’augmentation des points de vie et le positionnement des personnages.
Fonctionnalités d’affichage
Afin d’avoir une interface utilisateur agréable, nous avons implémenté plusieurs fonctionnalités d’affichage. Les plus notables sont notamment :

initialize_main_menu : crée un écran d'accueil avec des boutons permettant de voir les règles du jeu, les pouvoirs des personnages et de commencer le jeu.
character_choice_screen : affiche le choix des personnages à sélectionner pour le joueur 1 et le joueur 2. Lorsqu’un personnage est sélectionné, les contours de son image deviennent colorés. Possibilité de désélectionner un personnage déjà sélectionné.
draw menu : affiche les statistiques de chaque personnage lorsqu’il est sélectionné pendant son tour de jeu. Il affiche également les capacités spéciales et les utilisations restantes des objets associés aux capacités. Cet affichage est mis à jour lorsqu’une capacité spéciale est utilisée et modifie les statistiques du personnage.
capacity_choice : affiche les options de capacités spéciales à utiliser. Une fois la capacité choisie (touche 1 ou 2), l’écran disparaît.
flip_display : permet l’affichage de toutes les cases de mouvement disponibles. Cela dépend de la statistique de mouvement de chaque unité. La case ciblée est colorée en rose et est navigable avec les flèches du clavier.
Fonctionnalités de jeu
Les fonctionnalités de jeu gèrent le mouvement des unités ainsi que les attaques. Les méthodes principales sont :

handle_player_turn : permet de déplacer les unités sur le plateau. Cette fonction implémente également la manière dont le joueur interagit avec les objets du jeu ou en est affecté.
handle_playerX_attack : permet de sélectionner ou non une capacité spéciale à utiliser pendant le tour d'attaque. Elle permet également de sélectionner les personnages adverses à attaquer s’ils sont dans la portée d’attaque.










