# Simulateur de file d'attente d'un magasin
## Contexte
Dans le cadre de notre cours de Système de Données, nous devions créer une application simulant des personnes faisant la queue à des caisses d'un magasin . Par Exemple : Migros ou IKEA
## Réalisation
Pour venir à bout de ce projet, j'ai voulu utiliser python avec la librairie graphique "pygame" qui permet de réaliser des applications graphiques simples avec python.

J'ai choisi d'utiliser une conception objet afin de pouvoir créer des clients et les supprimer plus facilement.

J'ai créer des objets checkout qui reprèsentent les caisses du magasin, des objets clients pour les clients du magasin et un objet Store afin de centraliser l'affichage et la gestion de l'ouverture/fermeture des caisse
## Problèmes rencontrées
### Suppression spontanée
J'ai eu des problèmes de suppression spontanée des clients.
Des clients qui n'avaient pas encore atteint la caisse étaient déjà traité comme si ils l'avaient atteint.

Après avoir cherché une erreur de pointage, il s'est avéré que l'erreur n'était pas là.

Avant de commencer le décrémentage du temps d'attente à la caisse, j'incrémentais le temps ou la caisse était inactive. A cause d'une erreur de mouvement, le client était détécté comme arrivé sans être arrivé. Ces deux problèmes mis ensembles provoquaient la disparition soudaine du premier client qui voulait se mettre en queue.
### Déplacement des clients en queue
Lorsqu'un client finissait son passage en caisse, les autres étaient sensés avancés. De plus, il fallait que les futurs clients se mettent correctement à la queue.

Pour résoudre cela, j'ai donné comme destination la dernière position aux clients qui veulent rejoindre la queue et j'ai donné comme destination le point qui correspond à la place du client dans la file pour ceux faisant partie de la queue.

En enlevant le premier client de la liste, la place de tous les autres clients se met à jour et leur destination est changée.