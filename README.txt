1. Fonctionnement du programme:
1.1 Programme de base:

Premi�rement, le programme regarde si des arguments ont �t� rentr� en param�tre. Si oui, il modifie les variables ralentTemps et controlOrdi qui vont respectivement controler le ralentissement de la balle et le fait que ce soit l'ordinateur qui controle la raquette ou l'utilisateur.
Ensuite, le programme va cr�er une fen�tre en prenant en compte la zone de jeu et la zone d'information � droite de la zone de jeu.
Puis, toutes les variables relatives � la balle, la raquette et les briques sont initialis�es. 
La liste des briques est initialis�e avec la fonction creation_briques() qui va cr�er une liste de tuple en fonction de la taille des briques qui d�pend du nombre de briques par ligne et du nombre de ligne voulues. Puis les briques sont affich�es.

Le programme rentre dans sa boucle principale qui va s'executer tant que l'utilisateur poss�de des balles en r�serve. Avant de rentrer dans la boucle qui va faire tourner le jeu, le programme va tout effacer et va r�initialiser la position de la balle en r�initialisant les variables vx, vy, xBalle et yBalle et va l'afficher avec la fonction cercle() du module upemtk.
Il va ensuite r�initialiser la position de la raquette en r�initialisant la variable ax puis va l'afficher avec la fonction raquette().
Le programme va ensuite r�afficher les briques avec la fonction affichage_briques() qui prend en param�tre la liste des briques et il va afficher la zone d'information avec la fonction affichage_hud() � droite de la zone de jeu. Le programme va afficher differemment cette zone d'information quand c'est la premi�re entr�e dans la boucle afin d'initialiser le timer � 0.

On rentre ensuite dans la boucle qui va "faire tourner" le jeu. Cette boucle va s'executer infiniment jusqu'� ce que l'utilisateur perde une balle ou jusqu'� ce qu'il gagne.
Dans cette fonction, on va premi�rement modifier la position de la raquette avec la fonction mouvement_raquette(). Si au lancement du programme l'utilisateur a d�cid� que l'ordinateur contr�le la raquette, alors la variable ax correspondant � la position de la raquette sur l'axe x est d�finie en fonction de la position x de la balle et d'une variable al�atoire qui va changer � chaque colision de la balle et de la raquette.
Ensuite, si il y a eu une collision avec les briques dans la boucle pr�c�dente, on actualise l'affichage des briques et l'affichage de l'HUD. On actualise aussi ces deux affichages toutes les 10 unit�s de temps (lorsque temps%10==0).
Il y a ensuite la d�tection de toutes les collisions: fen�tre, raquette et briques.
Il y a ensuite l'actualisation de l'affichage de la raquette et de la balle.
Enfin, le programme d�tecte si l'utilisateur a gagn� ou si il a perdu une balle. Si il a gagn� (la liste de brique est vide), on affiche sur l'�cran qu'il a gagn� et on attend que l'utilisateur appuie sur une touche pour fermer la fen�tre.

1.2 Optimisation du programme:

Bonus/Malus:

Lors de la destruction d'une brique, il y a une chance sur 3 qu'un bonus ou un malus appara�t.
Les bonus impl�ment�s dans le jeu sont: augmentation de la taille de la raquette (boule verte), balle supl�mentaire (boule bleue), bonus de score de 50 points (boule orange).
Les malus impl�ment�s dans le jeu sont: diminution de la taille de la raquette (boule rouge), perte d'une balle (boule noire), malus de score de 50 points (boule violette).

Zone d'information:

Une zone d'information a �t� impl�ment�e � droite de la zone de jeu.
Dans cette zone d'information, on peut retrouver: le nombre de briques restantes, le score, le temps pass� en jeu, le nombre de balles restantes, le dernier bonus/malus obtenu.

Effet dans la balle:

Lorsque l'utilisateur contr�le la raquette, il peut donner de l'effet � la balle en d�placement rapidement la raquette avant que la balle touche la raquette.
La balle va aller dans le m�me direction que celle de la raquette.
Pour faire cela, le programme calcule la diff�rence entre la position de la raquette et la position de la raquette avant. Il stocke ces 5 derniers r�sultats dans une liste et en fait une moyenne. Ensuite, lors de la collision entre la raquette et la balle, on rajoute cette moyenne/2 au vecteur x de la balle afin de lui donner de l'effet.

2. Probl�mes rencontr�s:
2.1 Collision sur les coins des briques:

On a eu des probl�mes lors de la collision sur les coins des briques, la balle passait � travers la brique.
Pour supprimmer ce probl�me, on a am�liorer notre fonction qui d�tecte la collision de la balle avec les briques.

2.2 Probl�mes d'optimisation du programme:

Le programme est lent � s'executer, c'est pourquoi la balle est lente. On a remarqu� que le fait d'effacer les briques et de les r�afficher demandait beaucoups de ressources et ralentissait le programme. 
Pour r�gler ce probl�me, on a changer la boucle du programme afin de supprimmer le r�affichage permanent des briques. Les briques sont supprim�es et r�affich�es seulement lorsqu'il y a collision entre la balle et une briques et toutes les 10 unit�s de temps.

3. Lancement du programme:

Il faut soit lancer le programme avec exactement 3 param�tres en ligne de commande ou soit sans param�tres.
. Lancement du programme avec arguments:
Il faut utiliser les deux premiers param�tres pour modifier la vitesse de la balle.
Le premier argument correspond � l'augmentation de la vitesse de la balle (il faut augmenter la valeur pour augmenter la vitesse de la balle, la valeur minimum � rentrer est 1)
Le deuxi�me argument correspond au ralentissement de la balle (il faut augmenter cette valeur pour ralentir la balle et la baisser pour la faire acc�l�rer avec 1 comme minimum)
Le troisi�me argument permet de dire si c'est l'ordinateur qui joue ou si c'est l'utilisateur (1 = ordinateur qui contr�le, 0 = utilisateur qui contr�le)
. Lancement sans arguments:
Par d�faut, si le programme est lanc� sans arguments, la variable permettant d'augmenter la vitesse de la balle est initialis�e � 1, la variable qui permet de ralentir la balle est initialis�e � 1, celle permettant de choisir qui contr�le la balle est initialis�e � 0. 

4. Jouabilit�:

La raquette se contr�le avec la souris. L'utilisateur poss�de 3 balles et il doit d�truire les briques le plus rapidement possible afin d'obtenir le meilleur score. Il peut obtenir un score n�gatif.
La collision avec une brique rapporte 10 points, la destruction d'une brique rapporte un bonus de 5 points en plus des points rapport�s par la collision. Chaque vie restante rapporte 75 points. 
Le temps �coul� fait diminuer le score, l'utilisateur perd 1 point par seconde pass� en jeu.
L'utilisateur peut obtenir un bonus rapportant 50 points et un malus qui lui enl�ve 50 points.