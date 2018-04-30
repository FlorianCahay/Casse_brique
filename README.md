# casse_brique
Réalisation d'un jeu de casse-briques en Python

1. Fonctionnement du programme:

1.1 Programme de base:

Premièrement, le programme regarde si des arguments ont été rentré en paramètre. Si oui, il modifie les variables ralentTemps et controlOrdi qui vont respectivement controler le ralentissement de la balle et le fait que ce soit l'ordinateur qui controle la raquette ou l'utilisateur.
Ensuite, le programme va créer une fenêtre en prenant en compte la zone de jeu et la zone d'information à droite de la zone de jeu.
Puis, toutes les variables relatives à la balle, la raquette et les briques sont initialisées. 
La liste des briques est initialisée avec la fonction creation_briques() qui va créer une liste de tuple en fonction de la taille des briques qui dépend du nombre de briques par ligne et du nombre de ligne voulues. Puis les briques sont affichées.

Le programme rentre dans sa boucle principale qui va s'executer tant que l'utilisateur possède des balles en réserve. Avant de rentrer dans la boucle qui va faire tourner le jeu, le programme va tout effacer et va réinitialiser la position de la balle en réinitialisant les variables vx, vy, xBalle et yBalle et va l'afficher avec la fonction cercle() du module upemtk.
Il va ensuite réinitialiser la position de la raquette en réinitialisant la variable ax puis va l'afficher avec la fonction raquette().
Le programme va ensuite réafficher les briques avec la fonction affichage_briques() qui prend en paramètre la liste des briques et il va afficher la zone d'information avec la fonction affichage_hud() à droite de la zone de jeu. Le programme va afficher differemment cette zone d'information quand c'est la première entrée dans la boucle afin d'initialiser le timer à 0.

On rentre ensuite dans la boucle qui va "faire tourner" le jeu. Cette boucle va s'executer infiniment jusqu'à ce que l'utilisateur perde une balle ou jusqu'à ce qu'il gagne.
Dans cette fonction, on va premièrement modifier la position de la raquette avec la fonction mouvement_raquette(). Si au lancement du programme l'utilisateur a décidé que l'ordinateur contrôle la raquette, alors la variable ax correspondant à la position de la raquette sur l'axe x est définie en fonction de la position x de la balle et d'une variable aléatoire qui va changer à chaque colision de la balle et de la raquette.
Ensuite, si il y a eu une collision avec les briques dans la boucle précédente, on actualise l'affichage des briques et l'affichage de l'HUD. On actualise aussi ces deux affichages toutes les 10 unités de temps (lorsque temps%10==0).
Il y a ensuite la détection de toutes les collisions: fenêtre, raquette et briques.
Il y a ensuite l'actualisation de l'affichage de la raquette et de la balle.
Enfin, le programme détecte si l'utilisateur a gagné ou si il a perdu une balle. Si il a gagné (la liste de brique est vide), on affiche sur l'écran qu'il a gagné et on attend que l'utilisateur appuie sur une touche pour fermer la fenêtre.

1.2 Optimisation du programme:

Bonus/Malus:

Lors de la destruction d'une brique, il y a une chance sur 3 qu'un bonus ou un malus apparaît.
Les bonus implémentés dans le jeu sont: augmentation de la taille de la raquette (boule verte), balle suplémentaire (boule bleue), bonus de score de 50 points (boule orange).
Les malus implémentés dans le jeu sont: diminution de la taille de la raquette (boule rouge), perte d'une balle (boule noire), malus de score de 50 points (boule violette).

Zone d'information:

Une zone d'information a été implémentée à droite de la zone de jeu.
Dans cette zone d'information, on peut retrouver: le nombre de briques restantes, le score, le temps passé en jeu, le nombre de balles restantes, le dernier bonus/malus obtenu.

Effet dans la balle:

Lorsque l'utilisateur contrôle la raquette, il peut donner de l'effet à la balle en déplacement rapidement la raquette avant que la balle touche la raquette.
La balle va aller dans le même direction que celle de la raquette.
Pour faire cela, le programme calcule la différence entre la position de la raquette et la position de la raquette avant. Il stocke ces 5 derniers résultats dans une liste et en fait une moyenne. Ensuite, lors de la collision entre la raquette et la balle, on rajoute cette moyenne/2 au vecteur x de la balle afin de lui donner de l'effet.

2. Problèmes rencontrés:

2.1 Collision sur les coins des briques:

On a eu des problèmes lors de la collision sur les coins des briques, la balle passait à travers la brique.
Pour supprimmer ce problème, on a améliorer notre fonction qui détecte la collision de la balle avec les briques.

2.2 Problèmes d'optimisation du programme:

Le programme est lent à s'executer, c'est pourquoi la balle est lente. On a remarqué que le fait d'effacer les briques et de les réafficher demandait beaucoups de ressources et ralentissait le programme. 
Pour régler ce problème, on a changer la boucle du programme afin de supprimmer le réaffichage permanent des briques. Les briques sont supprimées et réaffichées seulement lorsqu'il y a collision entre la balle et une briques et toutes les 10 unités de temps.

3. Lancement du programme:

Il faut soit lancer le programme avec exactement 3 paramètres en ligne de commande ou soit sans paramètres.
. Lancement du programme avec arguments:
Il faut utiliser les deux premiers paramètres pour modifier la vitesse de la balle.
Le premier argument correspond à l'augmentation de la vitesse de la balle (il faut augmenter la valeur pour augmenter la vitesse de la balle, la valeur minimum à rentrer est 1)
Le deuxième argument correspond au ralentissement de la balle (il faut augmenter cette valeur pour ralentir la balle et la baisser pour la faire accélérer avec 1 comme minimum)
Le troisième argument permet de dire si c'est l'ordinateur qui joue ou si c'est l'utilisateur (1 = ordinateur qui contrôle, 0 = utilisateur qui contrôle)
. Lancement sans arguments:
Par défaut, si le programme est lancé sans arguments, la variable permettant d'augmenter la vitesse de la balle est initialisée à 1, la variable qui permet de ralentir la balle est initialisée à 1, celle permettant de choisir qui contrôle la balle est initialisée à 0. 

4. Jouabilité:

La raquette se contrôle avec la souris. L'utilisateur possède 3 balles et il doit détruire les briques le plus rapidement possible afin d'obtenir le meilleur score. Il peut obtenir un score négatif.
La collision avec une brique rapporte 10 points, la destruction d'une brique rapporte un bonus de 5 points en plus des points rapportés par la collision. Chaque vie restante rapporte 75 points. 
Le temps écoulé fait diminuer le score, l'utilisateur perd 1 point par seconde passé en jeu.
L'utilisateur peut obtenir un bonus rapportant 50 points et un malus qui lui enlève 50 points.
