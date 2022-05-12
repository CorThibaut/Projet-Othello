# Projet-Othello
### Auteur
195038 THIBAUT Corentin

### Utilisation 
dans le terminal, utiliser la commande, (name, matricule et port sont optionnels): 

`python connect.py name=<name> matricule=<matricule> <port>`

##### valeur par defaut:
Co, 195038, 3088

##### exemple valide:
-python connect.py 3001
>l'IA se connecte avec le nom Co, matricule "195038" et avec le port 3001
### Stratégie
IA utilisant un algorithme de type Negamax avec Pruning et profondeur limitée:
A chaque itération, choisi un  dans la liste des coups possibles apportant les cases les plus intéressantes, les coins êtant les cases les plus importantes. L'heuristique construit la différence du nombre de cases possédées par les joueurs.

### Bibliothèques utilisées
-json
-random
-socket
-copy
-sys

### Source
Toute la partie du code pour connaitre la liste des coups possibles est basé sur le code de qLurkin pour le jeu Othello:
[Page Source](https://github.com/qlurkin/PI2CChampionshipRunner)

