# Projet-Othello
### Auteur
195038 THIBAUT Corentin

### Utilisation 
dans le terminal, utiliser la commande: 

`python connect.py name=<name> matricule=<matricule> <port>`

### Stratégie
IA utilisant un algoruthme de type Negamax avec Pruning et profondeur limitée:
A chaque itération, choisi une valeur dans la liste des coups possibles apportant les cases les plus intéressantes, les coins êttant les cases les plus importantes. L'heuristique construit la différence du nombre de cases possédées par les joueurs.

### Bibliothèques utilisées
json,
random,
socket,
copy,
sys,

### Source
Toute la partie du code pour connaitre la liste des coups possibles est basé sur le code de qLurkin pour le jeu Othello:
[Page Source](https://github.com/qlurkin/PI2CChampionshipRunner)

