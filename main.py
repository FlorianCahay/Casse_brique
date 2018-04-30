 ##### IMPORTS #####

from upemtk import *
from random import randint
import sys
import os
from time import clock
from math import ceil
import pickle

##### FONCTIONS #####

def ready(hauteur, largeur):
    """Affiche un massage à l'écran et attend que l'utilisateur soit prêt quand il appuie sur une touche."""
    texte(largeur//2,hauteur//2,'Appuyer sur une touche','red','center',taille='30',tag='pret')
    attente_touche()
    efface('pret')

def bord_fenêtre_cotes(xBalle, yBalle, vx, rayon, largeurFenetre):
    """ Vérifie si la balle touche un côté de la fenêtre, si oui la fait rebondir. """
    if xBalle+rayon > largeurFenetre and vx>0:
        return -vx
    if xBalle-rayon < 0 and vx<0:
        return -vx
    return vx

def bord_fenetre_haut(xBalle, yBalle, vy, rayon):
    """ Vérifie si la balle touche le bord supérieur de la fenêtre,
         si oui la fait rebondir. """
    if yBalle < rayon:
        return -vy
    return vy

def perdu(yBalle, rayon):
    """ Vérifie si la balle a touché le bas de la fenêtre, si oui retourne True
         sinon retourne False. """
    if yBalle+rayon >= hauteurFenetre:
        return True
    else:
        return False

def victoire(lstBrique):
    """Verifie si toutes les briques ont été détruites, si oui renvoie True sinon False."""
    if len(lstBrique) == 0:
        return True
    else:
        return False

def raquette(ax, ay, largeur, hauteur):
    """ Affiche la raquette du jeu """
    rectangle(ax, ay, ax+largeur, ay-hauteur, couleur='black', remplissage='gold', epaisseur=1, tag='raquette')

def mouvement_raquette(largeurFenetre, largeurRaquette, ax):
    """ Déplace la raquette en fonction du mouvement du curseur. """
    ev=donne_evenement()
    if type_evenement(ev) in ['ClicDroit','ClicGauche','Deplacement']:
        if clic_x(ev)>largeurFenetre-largeurRaquette//2:
            return largeurFenetre-largeurRaquette-1
        if clic_x(ev)<largeurRaquette//2:
            return 0
        return clic_x(ev)-(largeurRaquette//2)
    return ax

def collision_raquette(xBalle, yBalle, xRaquette, yRaquette, largeurRaquette, hauteurRaquette, rayonBalle, vYballe, vXballe, coefModifvx):
    """ Vérifie si il y a une collision entre la balle et la raquette, le rebond prend en compte le déplacement de la raquette pour donner un effet. 
    Renvoie le vecteur X et Y de la balle et 1 si il y a eu une collision sinon 0. """
    if (yBalle+rayonBalle>=yRaquette-hauteurRaquette) and (yBalle+rayonBalle<=yRaquette) and (xBalle>xRaquette) and (xBalle<xRaquette+largeurRaquette) and (vYballe>0):
        return -vYballe, vx+coefModifvx, 1
    else:
        return vYballe, vXballe, 0

def collision_raquette2(xBalle, yBalle, xRaquette, yRaquette, largeurRaquette, hauteurRaquette, rayonBalle, vYballe, vXballe, coefModifvx):
    """ Même chose que la fonction collision_raquette(), mais cette fonction sert pour le mode avec l'ordinateur en ne prenant pas en compte 
    le déplacement de la raquette pour donner un effet. """
    if (yBalle+rayonBalle>=yRaquette-hauteurRaquette) and (yBalle+rayonBalle<=yRaquette) and (xBalle>xRaquette) and (xBalle<xRaquette+largeurRaquette) and (vYballe>0):
        return -vYballe, (xBalle-(xRaquette+(largeurRaquette//2)))/30+coefModifvx, 1
    else:
        return vYballe, vXballe, 0

def creation_briques_fichier(nomFichier, xBrique, yBrique):
    """Creation de la liste contenant les informations sur les briques"""
    global score
    global lstBonus
    global lstBrique
    if nomFichier == 'save.txt':
        fichier = open('save.txt','rb')
        tempsPLUS = pickle.load(fichier)
        score = pickle.load(fichier)
        lstBonus = pickle.load(fichier)
        nbreBriqueParLigne = pickle.load(fichier)
        nbreLigne = pickle.load(fichier)
        lstBrique = pickle.load(fichier)
        fichier.close()
        return nbreBriqueParLigne, nbreLigne, tempsPLUS
    else:
        fichier = open(nomFichier)
        i = 0
        for ligne in fichier:
            if i == 0:
                nbreBriqueParLigne = int(ligne[:-1])
            elif i == 1:
                nbreLigne = int(ligne[:-1])
            i += 1
            if i == 2:
                break
        largeurBrique = largeurFenetre//nbreBriqueParLigne
        hauteurBrique = (hauteurFenetre//3)//nbreLigne
        for x in range(nbreLigne):
            ay = x*hauteurBrique
            by = ay+hauteurBrique
            ligneBriqueFichier = fichier.readline()
            ligneBriqueFichier = ligneBriqueFichier[:-1]
            for y in range(nbreBriqueParLigne):
                ax = y*largeurBrique
                bx = ax+largeurBrique
                if ligneBriqueFichier[y*4] == '-':
                    continue
                resistance = int(ligneBriqueFichier[y*4])
                lstBrique.append((ax, ay, bx, by, resistance, int(ligneBriqueFichier[y*4+2])))
        fichier.close()
        return nbreBriqueParLigne, nbreLigne, 0


def creation_briques(lstBrique, xBrique, yBrique, largeurBrique, hauteurBrique, nbreBriqueParLigne, nbreLigne):
    """ Permet de créer une liste contenant les coordonnées des rectangles
        représentant les briques et sa couleur en fonction de sa résistance. """
    for x in range(nbreLigne):
        ay = x * hauteurBrique
        by = ay + hauteurBrique
        for y in range(nbreBriqueParLigne):
            ax = y * largeurBrique
            bx = ax + largeurBrique
            resistance = randint(1, 3)
            lstBrique.append((ax, ay, bx, by, resistance,0))
    return 0

def affichage_briques(lstBrique):
    """Affichage des briques avec la bonne résistance. """
    efface('brique')
    for i in range(len(lstBrique)):
        ax, ay, bx, by, resistance = lstBrique[i][:5]
        if resistance == 1:
            x = 'yellow'
        elif resistance == 2:
            x = 'orange'
        elif resistance == 3:
            x = 'red'
        elif resistance == 4:
            x = 'brown'
        elif resistance == 5:
            x = 'black'
        rectangle(ax, ay, bx, by, couleur='black', remplissage=x, epaisseur=1, tag='brique')

def collision_briques(lstBrique, xBalle, yBalle, vx, vy, rayon):
    """ Détecte si il y a une collision entre la balle et une brique et renvoie le vecteur X et Y de la balle 
    en fonction de l'endroit où elle touche la brique. Et renvoie 1 si il y a eu une collision, sinon 0. """
    global score

    for i in range(len(lstBrique)):
        ax, ay, bx, by, resistance = lstBrique[i][:5]
        #gauche
        if (ax<=xBalle+rayon<=bx and ay<=yBalle<=by) and (xBalle+rayon-vx)<ax:
            destruction_briques(i)
            score += 10
            return vy, -vx, 1
        #droite
        elif (ax<=xBalle-rayon<=bx and ay<=yBalle<=by) and (xBalle-rayon-vx)>bx:
            destruction_briques(i)
            score += 10
            return vy, -vx, 1
        #haut
        elif (ax<=xBalle<=bx and ay<=yBalle+rayon<=by) and (yBalle+rayon-vy)<ay:
            destruction_briques(i)
            score += 10
            return -vy, vx, 1
        #bas
        elif (ax<=xBalle<=bx and ay<=yBalle-rayon<=by) and (yBalle-rayon-vy)>by:
            destruction_briques(i)
            score += 10
            return -vy, vx, 1
        elif (ax<=xBalle<=bx and ay<=yBalle<=by):
            destruction_briques(i)
            score += 10
            return -vy, -vx, 1
    return vy, vx, 0

def destruction_briques(i):
    """Met à jour la liste de briques et ajoute un bonus à la liste des bonus si un bonus a été retourné par la fonction bonus()"""
    global lstBonus
    global lstBrique
    global score

    ax, ay, bx, by, resistance,bon = lstBrique[i][:6]

    if resistance > 1:
        lstBrique[i] = (ax,ay,bx,by,resistance-1,bon)
        return None
    elif resistance == 1:
        if lstBrique[i][5] != 0:
            isBonus = bonus((ax+bx)//2,by,lstBrique[i][5])
            lstBonus.append(isBonus)
        else:
            isBonus = bonus((ax+bx)//2,by,0)
            if isBonus != None:
                lstBonus.append(isBonus)
        score += 5
        lstBrique.pop(i)

def bonus(x, y, pre):
    """ A une chance sur 3 de retourner un bonus choisi au hasard. """
    liste_chances = [1,2,3,4,5,6]
    if pre != 0:
        a = pre
    else:
        a = 7
        # a=randint(1,len(liste_chances)*3)
    if a in liste_chances:
        if a == 1:
            return ('PetitRaquette',x,y,'red')
        elif a == 2:
            return ('GrandRaquette',x,y,'green')
        elif a == 3:
            return ('ViePlus',x,y,'blue')
        elif a == 4:
            return ('ScoreBonus',x,y,'orange')
        elif a == 5:
            return ('VieMoins',x,y,'black')
        elif a == 6:
            return ('ScoreMalus',x,y,'purple')

def majBonus(rayon):
    """ Affiche les bonus et met à jour les positions. """
    global lstBonus
    efface('Bonus')
    for i in range(len(lstBonus)):
        cercle(lstBonus[i][1], lstBonus[i][2]+1, rayon, couleur=lstBonus[i][3], remplissage=lstBonus[i][3], epaisseur=1, tag='Bonus')
        lstBonus[i] = (lstBonus[i][0],lstBonus[i][1],lstBonus[i][2]+1,lstBonus[i][3])


def collision_bonus(xRaquette, yRaquette, largeurRaquette, hauteurRaquette, rayon, vies, score, lastBonus):
    """ Vérifie si il y a une collision entre la raquette et le bonus qui descend. """
    global lstBonus

    if len(lstBonus) > 0:
        for i in range(len(lstBonus)):
            if (lstBonus[i][1]>=xRaquette) and (lstBonus[i][1]<=xRaquette+largeurRaquette) and (lstBonus[i][2]+rayon>=yRaquette-hauteurRaquette) and (lstBonus[i][2]+rayon<=yRaquette):
                if lstBonus[i][0] == 'PetitRaquette':
                    lstBonus.pop(i)
                    return 'Raquette -', largeurRaquette-largeurRaquette//5, vies, score
                elif lstBonus[i][0] == 'GrandRaquette':
                    lstBonus.pop(i)
                    return 'Raquette +', largeurRaquette+largeurRaquette//5, vies, score
                elif lstBonus[i][0] == 'ViePlus':
                    lstBonus.pop(i)
                    return 'Balle +', largeurRaquette, vies+1, score
                elif lstBonus[i][0] == 'ScoreBonus':
                    lstBonus.pop(i)
                    return 'Score +', largeurRaquette, vies, score+50
                elif lstBonus[i][0] == 'VieMoins':
                    lstBonus.pop(i)
                    return 'Balle -', largeurRaquette, vies-1, score
                elif lstBonus[i][0] == 'ScoreMalus':
                    lstBonus.pop(i)
                    return 'Score -', largeurRaquette, vies, score-50
    return lastBonus, largeurRaquette, vies, score

def affichage_hud(largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus,initialisation):
    """ Permet d'afficher la zone d'information à droite de la fenêtre du jeu qui comprend:
    le nombre de briques restantes, le score, le temps écoulé et le dernier bonus attrapé. """
    global score
    if initialisation == 1:
        ligne(largeurFenetre, 0, largeurFenetre, hauteurFenetre, couleur='black', epaisseur=1, tag='hudFIX')
        texte(largeurFenetre+100, 65, 'Nombre Briques:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 155, 'Score:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 245, 'Temps:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 245, 'Temps:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 335, 'Balles:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 425, 'Dernier bonus/malus:', couleur='black', ancrage='center', taille='15', tag='hudFIX')
        texte(largeurFenetre+100, 550, 'Pause (p)', couleur='grey', ancrage='center', taille='15', tag='txtPAUSE')
        rectangle(largeurFenetre+15,525, largeurFenetre+185, 575, couleur='grey', remplissage='', epaisseur=1, tag='rectPAUSE')
    else:
        efface('hud')
    texte(largeurFenetre+100, 190, score-ceil(clock()-tempsAretirer), couleur='black', ancrage='center', taille='15', tag='hud')
    texte(largeurFenetre+100, 100, len(lstBrique), couleur='black', ancrage='center', taille='15', tag='hud')
    texte(largeurFenetre+100, 280, ceil(clock()-tempsAretirer), couleur='black', ancrage='center', taille='15', tag='hud')
    texte(largeurFenetre+100, 370, vies,couleur='black', ancrage='center', taille='15', tag='hud')    
    texte(largeurFenetre+100, 460, lastBonus, couleur='black', ancrage='center', taille='15', tag='hud')

def maj_highscore():
    """Met à jour les meilleurs scores dans le fichier highscore.txt"""
    global score
    fichier = open('highscore.txt')
    h, liste = 1, []
    ajout = 0
    for ligne in fichier:
        if score >= int(ligne[:-1]) and ajout != 1:
            ajout = 1
            liste.append(score)
            h += 1
            if h == 6:
                break
        liste.append(int(ligne[:-1]))
        h += 1
        if h == 6:
            break
    fichier.close()
    fichier = open('highscore.txt','w')
    for elt in liste:
        fichier.write(str(elt)+'\n')
    fichier.close()

def affichage_highscore(largeurFenetre, hauteurFenetre):
    """Affiche les meilleurs scores sur l'écran de fin de jeu"""
    texte(largeurFenetre//2, hauteurFenetre//2-10, 'Meilleurs scores:', couleur='orange', ancrage='center', taille='25', tag='highscore')
    fichier = open('highscore.txt')
    listeScores = []
    for ligne in fichier:
        listeScores.append(ligne[:-1])
    fichier.close()
    for i in range(len(listeScores)):
        texte(largeurFenetre//2-80, (hauteurFenetre//2)+50*(i+1), str(i+1)+'.', couleur='orange', ancrage='e', taille='20')
        texte(largeurFenetre//2-75, (hauteurFenetre//2)+50*(i+1), str(listeScores[i]), couleur='orange', ancrage='w', taille='20')

def affichage_debut(hauteurFenetre,largeurFenetre):
    """Affiche le menu principal au lancement du programme"""
    temps = clock()
    while True:
        efface_tout()
        if 'save.txt' in os.listdir():
            rectangle(largeurFenetre//25, hauteurFenetre-(hauteurFenetre//25), largeurFenetre//4, hauteurFenetre-(hauteurFenetre//7), couleur='orange', remplissage='', epaisseur=2, tag='rectSAVE')
            texte(((largeurFenetre//25)+(largeurFenetre//4))//2, ((hauteurFenetre-(hauteurFenetre//25))+(hauteurFenetre-(hauteurFenetre//7)))//2, 'Save', couleur='orange', ancrage='center', taille=20, tag='textSAVE')
        rectangle((largeurFenetre//4)*3+200, hauteurFenetre-(hauteurFenetre//25), largeurFenetre-(largeurFenetre//25)+200, hauteurFenetre-(hauteurFenetre//7), couleur='black', remplissage='', epaisseur=2, tag='')
        texte((((largeurFenetre//4)*3+200)+(largeurFenetre-(largeurFenetre//25)+200))//2, ((hauteurFenetre-(hauteurFenetre//25))+(hauteurFenetre-(hauteurFenetre//7)))//2, 'Quitter', couleur='black', ancrage='center', taille=20,tag='')
        texte(largeurFenetre//2+100, 70, 'Choix du niveau', couleur='blue', ancrage='center', taille=30, tag='')
        rectangle(60, (hauteurFenetre//2)-40, largeurFenetre-60+200, (hauteurFenetre//2)-140, couleur='green', remplissage='', epaisseur=2, tag='')
        rectangle(60, (hauteurFenetre//2)+140, largeurFenetre-60+200,(hauteurFenetre//2)+40, couleur='red', remplissage='', epaisseur=2, tag='')
        texte((largeurFenetre//2)+100, (hauteurFenetre//2)-90, 'Aleatoire', couleur='green', ancrage='center', taille=20, tag='')
        texte((largeurFenetre//2)+100, (hauteurFenetre//2)+90, 'A partir d\'un fichier', couleur='red', ancrage='center', taille=20, tag='')
        while ceil(clock()-temps) != 11:
            ev = donne_evenement()
            mise_a_jour()
            if type_evenement(ev) in ['ClicDroit','ClicGauche']:
                if clic_x(ev)>=60 and clic_x(ev)<=largeurFenetre-60+200 and clic_y(ev)<(hauteurFenetre//2)-40 and clic_y(ev)>(hauteurFenetre//2)-140:
                    return None
                elif clic_x(ev)>=(largeurFenetre//4)*3+200 and clic_x(ev)<=largeurFenetre-(largeurFenetre//25)+200 and clic_y(ev)<=hauteurFenetre-(hauteurFenetre//25) and clic_y(ev)>=hauteurFenetre-(hauteurFenetre//7):
                    ferme_fenetre()
                    exit()
                elif clic_x(ev)>=largeurFenetre//25 and clic_x(ev)<=largeurFenetre//4 and clic_y(ev)<=hauteurFenetre-(hauteurFenetre//25) and clic_y(ev)>=hauteurFenetre-(hauteurFenetre//7) and 'save.txt' in os.listdir():
                    return 'save.txt'
                elif clic_x(ev)>=60 and clic_x(ev)<=largeurFenetre-60+200 and clic_y(ev)<(hauteurFenetre//2)+140 and clic_y(ev)>(hauteurFenetre//2)+40:
                    listeFichiers = []
                    for fichiers in os.listdir():
                        if fichiers[0:7] == 'briques':
                            listeFichiers.append(fichiers)
                    if len(listeFichiers) != 0:
                        retourne = affichage_fichiers(listeFichiers, hauteurFenetre, largeurFenetre, 1)
                        if retourne == 'back':
                            break
                        return retourne

def affichage_fichiers(listeFichiers, hauteurFenetre, largeurFenetre, currentPage):
    """Affiche l'écran de sélection des niveaux"""
    efface_tout()
    rectangle(largeurFenetre//25, hauteurFenetre//7, largeurFenetre//4, hauteurFenetre//25, couleur='red', remplissage='', epaisseur=2, tag='rectBACK')
    texte(((largeurFenetre//25)+(largeurFenetre//4))//2,((hauteurFenetre//7)+(hauteurFenetre//25))//2, 'Retour', couleur='red', ancrage='center', taille=20, tag='textBACK')
    texte(largeurFenetre//2+100, hauteurFenetre//10, 'Fichiers disponibles', couleur='blue', ancrage='center', taille=30, tag='')
    if len(listeFichiers)%3 != 0:
        nbrePage = 1+len(listeFichiers)//3
    else:   
        nbrePage = len(listeFichiers)//3
    temps = clock()
    texte(largeurFenetre//2+100, hauteurFenetre-40, 'Page '+str(currentPage)+'/'+str(nbrePage), couleur='blue', ancrage='center', taille=20, tag='')
    while True:
        if currentPage != nbrePage:
            for i in range(3):
                rectangle(10+100, int((2+i)*(1/5)*hauteurFenetre)-10, largeurFenetre-10+100, int((1+i)*(1/5)*hauteurFenetre)+10, couleur='green', remplissage='', epaisseur=2, tag='rectanglefic')
                texte(((10+100)+(largeurFenetre-10+100))//2, ((int((2+i)*(1/5)*hauteurFenetre)-10)+(int((1+i)*(1/5)*hauteurFenetre)+10))//2, listeFichiers[(currentPage-1)*3+i][7:-4], couleur='blue', ancrage='center', taille=20, tag='fic')
            if currentPage != 1:
                rectangle(60, hauteurFenetre-10, largeurFenetre//2, hauteurFenetre-70, couleur='blue', remplissage='', epaisseur=2, tag='casePREC')
                texte((60+largeurFenetre//2)//2, ((hauteurFenetre-10)+(hauteurFenetre-70))//2, 'Précédent', couleur='blue', ancrage='center', taille=20, tag='textePREC')
            if currentPage<nbrePage:
                rectangle(largeurFenetre//2+200, hauteurFenetre-10, largeurFenetre+200-60,hauteurFenetre-70, couleur='blue', remplissage='', epaisseur=2, tag='caseSUIV')
                texte(((largeurFenetre//2+200)+(largeurFenetre+200-60))//2, ((hauteurFenetre-10)+(hauteurFenetre-70))//2, 'Suivant', couleur='blue', ancrage='center', taille=20, tag='texteSUIV')
            #Clic:
            ev = donne_evenement()
            if type_evenement(ev) in ['ClicDroit','ClicGauche']:
                #Choix 1
                if clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+0)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+0)*(1/5)*hauteurFenetre)+10:
                    return listeFichiers[(currentPage-1)*3+0]
                #Choix 2
                elif clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+1)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+1)*(1/5)*hauteurFenetre)+10:
                    return listeFichiers[(currentPage-1)*3+1]
                #Choix 3
                elif clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+2)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+2)*(1/5)*hauteurFenetre)+10:
                    return listeFichiers[(currentPage-1)*3+2]
                #Précédent
                if clic_x(ev)>=60 and clic_x(ev)<=largeurFenetre//2 and clic_y(ev)<=hauteurFenetre-10 and clic_y(ev)>=hauteurFenetre-70 and currentPage!=1:
                    return affichage_fichiers(listeFichiers, hauteurFenetre, largeurFenetre, currentPage-1)
                #Suivant
                elif clic_x(ev)>=largeurFenetre//2+200 and clic_x(ev)<=largeurFenetre+200-60 and clic_y(ev)<=hauteurFenetre-10 and clic_y(ev)>=hauteurFenetre-70:
                    return affichage_fichiers(listeFichiers, hauteurFenetre, largeurFenetre, currentPage+1)
                #Retour
                elif clic_x(ev)>=largeurFenetre//25 and clic_x(ev)<=largeurFenetre//4 and clic_y(ev)<=hauteurFenetre//7 and clic_y(ev)>=hauteurFenetre//25:
                    return 'back'
        else:
            portee = len(listeFichiers)%3
            if portee == 0:
                portee = 3
            for i in range(portee):
                rectangle(10+100, int((2+i)*(1/5)*hauteurFenetre)-10, largeurFenetre-10+100, int((1+i)*(1/5)*hauteurFenetre)+10, couleur='green', remplissage='', epaisseur=2, tag='rectanglefic')
                texte(((10+100)+(largeurFenetre-10+100))//2, ((int((2+i)*(1/5)*hauteurFenetre)-10)+(int((1+i)*(1/5)*hauteurFenetre)+10))//2, listeFichiers[(currentPage-1)*3+i][7:-4], couleur='blue', ancrage='center', taille=20, tag='fic')
            if currentPage != 1:
                    rectangle(60, hauteurFenetre-10, largeurFenetre//2, hauteurFenetre-70, couleur='blue', remplissage='', epaisseur=2, tag='casePREC')
                    texte((60+largeurFenetre//2)//2, ((hauteurFenetre-10)+(hauteurFenetre-70))//2, 'Précédent', couleur='blue', ancrage='center', taille=20, tag='textePREC')
            ev = donne_evenement()
            if type_evenement(ev) in ['ClicDroit','ClicGauche']:
                #Précédent
                if clic_x(ev)>=60 and clic_x(ev)<=largeurFenetre//2 and clic_y(ev)<=hauteurFenetre-10 and clic_y(ev)>=hauteurFenetre-70 and currentPage!=1:
                    return affichage_fichiers(listeFichiers, hauteurFenetre, largeurFenetre, currentPage-1)
                #Choix 1
                if clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+0)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+0)*(1/5)*hauteurFenetre)+10:
                    return listeFichiers[(currentPage-1)*3+0]
                #Choix 2
                elif clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+1)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+1)*(1/5)*hauteurFenetre)+10 and portee>=2:
                    return listeFichiers[(currentPage-1)*3+1]
                #Choix 3
                elif clic_x(ev)>=10+100 and clic_x(ev)<=largeurFenetre-10+100 and clic_y(ev)<=int((2+2)*(1/5)*hauteurFenetre)-10 and clic_y(ev)>=int((1+2)*(1/5)*hauteurFenetre)+10 and portee==3:
                    return listeFichiers[(currentPage-1)*3+2] 
                #Retour
                elif clic_x(ev)>=largeurFenetre//25 and clic_x(ev)<=largeurFenetre//4 and clic_y(ev)<=hauteurFenetre//7 and clic_y(ev)>=hauteurFenetre//25:
                    return 'back'   
        mise_a_jour()

def affichage_fin(texteFin, largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus):
    """Affiche l'écran de fin."""
    global score
    efface_tout()
    texte(largeurFenetre//2, 70, texteFin[0], couleur=texteFin[1], ancrage='center', taille='35', tag='textePerdu')
    affichage_hud(largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus, 1)
    score = score-ceil(clock()-tempsAretirer)
    maj_highscore()
    affichage_highscore(largeurFenetre, hauteurFenetre)
    rectangle((largeurFenetre//2)-220, (hauteurFenetre//2)-80, (largeurFenetre//2)-20, (hauteurFenetre//2)-180, couleur='green', remplissage='', epaisseur=2, tag='recoOUI')
    texte((largeurFenetre//2)-120, (hauteurFenetre//2)-130, 'Retour menu', couleur='green', ancrage='center', taille='17', tag='recoOUI')
    rectangle((largeurFenetre//2)+20, (hauteurFenetre//2)-80, (largeurFenetre//2)+220, (hauteurFenetre//2)-180, couleur='red', remplissage='', epaisseur=2, tag='recoNON')
    texte((largeurFenetre//2)+120, (hauteurFenetre//2)-130, 'Quitter', couleur='red', ancrage='center', taille='17', tag='recoTextNon')
    while True:
        mise_a_jour()
        ev = donne_evenement()
        if type_evenement(ev) in ['ClicDroit','ClicGauche']:
            if clic_x(ev)>=(largeurFenetre//2)-220 and clic_x(ev)<=(largeurFenetre//2)-20 and clic_y(ev)<=(hauteurFenetre//2)-80 and clic_y(ev)>=(hauteurFenetre//2)-180:
                return 1
            elif clic_x(ev)>=(largeurFenetre//2)+20 and clic_x(ev)<=(largeurFenetre//2)+220 and clic_y(ev)<=(hauteurFenetre//2)-80 and clic_y(ev)>=(hauteurFenetre//2)-180:
                return 0
    return 0

def valeur_ligne_config(ligne):
    """Permet de récupérer la valeur de la ligne donnée en parametre lors de la lecture du fichier config."""
    h = 1
    while True:
        h += 1
        if ligne[-h] == ' ':
            break
    return int(ligne[-(h-1):-1])

def config_init():
    """Initialise certaines variables du jeu et notament grace au fichier config.txt"""
    global nbreLigne, nbreBriqueParLigne, quitter, largeurRaquette, hauteurRaquette, xBalle, yBalle, rayon, largeurFenetre, hauteurFenetre, vx, vy, ralentTemps, historiqueRaquette, ax, ay, axAvant, xBrique, yBrique, score

    fichier = open("config.txt")
    i = 0
    for ligne in fichier:
        if i == 0:
            largeurFenetre = valeur_ligne_config(ligne)*100
        elif i == 1:
            hauteurFenetre = valeur_ligne_config(ligne)*100
        elif i == 2:
            largeurRaquette = largeurFenetre//valeur_ligne_config(ligne)
        elif i == 3:
            rayon = valeur_ligne_config(ligne)
        elif i == 4:
            vy = valeur_ligne_config(ligne)
        elif i == 5:
            ralentTemps = valeur_ligne_config(ligne)
        elif i == 6:
            hauteurRaquette = valeur_ligne_config(ligne)
        elif i == 7:
            nbreBriqueParLigne = valeur_ligne_config(ligne)
        elif i == 8:
            nbreLigne = valeur_ligne_config(ligne)
        i += 1
    fichier.close()

    vx = 0
    ax = (largeurFenetre//2)-(largeurRaquette//2)
    ay = hauteurFenetre-hauteurRaquette
    axAvant = ax
    xBrique, yBrique = 0, 0
    historiqueRaquette = [0,0,0,0,0,0,0]
    xBalle = largeurFenetre//2
    yBalle = hauteurFenetre//1.5
    quitter = 0

def pause(hauteurFenetre, largeurFenetre, lstBrique, nbreBriqueParLigne, nbreLigne, tempsAretirer):
    """Met le jeu en pause et affiche l'écran de pause."""
    temps = clock()
    efface('raquette')
    efface('balle')
    efface('brique')
    efface('Bonus')
    rectangle(100, (hauteurFenetre//3)-45, largeurFenetre-100, 45, couleur='green', remplissage='', epaisseur=3, tag='pause')
    texte(((100)+(largeurFenetre-100))//2, (((hauteurFenetre//3)-45)+(45))//2, 'Reprendre', couleur='green', ancrage='center', taille='22', tag='pause')
    rectangle(100, (hauteurFenetre//3)*2-45, largeurFenetre-100, (hauteurFenetre//3)+45, couleur='orange', remplissage='', epaisseur=3, tag='pause')
    texte(((100)+(largeurFenetre-100))//2, (((hauteurFenetre//3)*2-45)+((hauteurFenetre//3)+45))//2, 'Sauvegarder', couleur='orange', ancrage='center', taille='22', tag='pause')
    rectangle(100, hauteurFenetre-45, largeurFenetre-100, (hauteurFenetre//3)*2+45, couleur='red', remplissage='', epaisseur=3, tag='pause')
    texte((100+(largeurFenetre-100))//2, ((hauteurFenetre-45)+((hauteurFenetre//3)*2+45))//2, 'Quitter', couleur='red', ancrage='center', taille='22', tag='pause')
    while True:
        mise_a_jour()
        ev = donne_evenement()
        if type_evenement(ev) in ['ClicDroit','ClicGauche']:
            if clic_x(ev)>=100 and clic_x(ev)<=largeurFenetre-100 and clic_y(ev)<=(hauteurFenetre//3)-45 and clic_y(ev)>=45:
                efface('pause')
                return 0, tempsAretirer+clock()-temps
            elif clic_x(ev)>=100 and clic_x(ev)<=largeurFenetre-100 and clic_y(ev)<=(hauteurFenetre//3)*2-45 and clic_y(ev)>=(hauteurFenetre//3)+45:
                sauvegarder(hauteurFenetre, largeurFenetre, lstBrique, nbreBriqueParLigne, nbreLigne, clock()-(tempsAretirer+clock()-temps))
            elif clic_x(ev)>=100 and clic_x(ev)<=largeurFenetre-100 and clic_y(ev)<=hauteurFenetre-45 and clic_y(ev)>=(hauteurFenetre//3)*2+45:
                return 1, tempsAretirer+clock()-temps

def sauvegarder(hauteurFenetre, largeurFenetre, lstBrique, nbreBriqueParLigne, nbreLigne, temps):
    """Sauvegarde l'état du niveau dans le fichier save.txt"""
    texte(largeurFenetre//2, (hauteurFenetre//3)*2, 'La partie a été sauvegardée', couleur='orange', ancrage='center', taille='17', tag='pause')
    fichier = open('save.txt','wb')
    pickle.dump(temps, fichier)
    pickle.dump(score, fichier)
    pickle.dump(lstBonus, fichier)
    pickle.dump(nbreBriqueParLigne, fichier)
    pickle.dump(nbreLigne, fichier)
    pickle.dump(lstBrique, fichier)
    fichier.close()

##### MAIN #####

if __name__ == '__main__':
    # Analyse arguments en ligne de commande
    if len(sys.argv) > 1:
        controlOrdi = int(sys.argv[1])
    else:
        controlOrdi = 0
    if controlOrdi == 1:
        collision_raquette = collision_raquette2

    config_init()
    cree_fenetre(largeurFenetre+200, hauteurFenetre)
    rejouer = 1
    while rejouer != 0:
        nomFichier = affichage_debut(hauteurFenetre, largeurFenetre)
        quitter = 0
        lstBrique = []
        lstBonus = []
        collision = 0
        collisionRaquette = 0
        temps = 0
        VariableRandomRaquette = randint(1,largeurRaquette-1)
        premier = 1
        vies = 1
        gagne = 0
        score = 0
        lastBonus = 'Aucun'
        if nomFichier == None:
            largeurBrique = largeurFenetre//nbreBriqueParLigne
            hauteurBrique = (hauteurFenetre//3)//nbreLigne
            tempsPLUS = creation_briques(lstBrique, xBrique, yBrique, largeurBrique, hauteurBrique, nbreBriqueParLigne, nbreLigne)
        else:
            nbreBriqueParLigne, nbreLigne, tempsPLUS = creation_briques_fichier(nomFichier, xBrique, yBrique)
        affichage_briques(lstBrique)

        while vies != 0:
            if quitter == 1:
                break

            if gagne == 1:
                break
            config_init()
            efface_tout()
            raquette(ax, ay, largeurRaquette, hauteurRaquette)
            cercle(xBalle, yBalle, rayon, couleur='black', remplissage='grey', tag='balle')
            affichage_briques(lstBrique)
            affichage_hud(largeurFenetre, hauteurFenetre, 0, vies, lastBonus, 1)
            ready(hauteurFenetre, largeurFenetre)

            if premier == 1:
                #Cette variable correspond au temps que l'utilisateur a pris pour lancer le jeu
                tempsAretirer = clock()-tempsPLUS
                premier = 0

            while True:
                ax = mouvement_raquette(largeurFenetre, largeurRaquette, ax)
                if controlOrdi == 1:
                    if collisionRaquette == 1:
                        VariableRandomRaquette = randint(1, largeurRaquette-1)
                    ax = xBalle-VariableRandomRaquette
                    if xBalle > ax+largeurRaquette:
                        ax = xBalle-largeurRaquette+1
                    if ax < 0:
                        ax = 0
                    if ax+largeurRaquette > largeurFenetre:
                        ax = largeurFenetre-largeurRaquette
                if collision == 1:
                    affichage_briques(lstBrique)
                    affichage_hud(largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus,0)
                    collision = 0
                elif temps%10 == 0:
                    affichage_briques(lstBrique)
                    affichage_hud(largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus,0)
                    rafraichi = 1
                else:
                    rafraichi = 0
                temps += 1

                if temps%ralentTemps == 0:
                    vx = bord_fenêtre_cotes(xBalle, yBalle, vx, rayon, largeurFenetre)
                    vy = bord_fenetre_haut(xBalle, yBalle, vy, rayon)
                    #Effet balle
                    historiqueRaquette.append(ax-axAvant)
                    historiqueRaquette.pop(0)
                    axAvant = ax
                    totalHisto = 0
                    for histo in historiqueRaquette:
                        totalHisto += histo
                    coefEffet = (totalHisto/len(historiqueRaquette))/2
                    if yBalle > hauteurFenetre//2:
                        vy, vx,collisionRaquette = collision_raquette(xBalle, yBalle, ax, ay, largeurRaquette, hauteurRaquette, rayon, vy, vx, coefEffet)
                    else:
                        vy,vx,collision = collision_briques(lstBrique, xBalle, yBalle, vx, vy, rayon)
                    xBalle += vx
                    yBalle += vy
                    if temps%(ralentTemps*2) == 0:
                        majBonus(rayon)
                        lastBonus, largeurRaquette, vies, score = collision_bonus(ax, ay, largeurRaquette, hauteurRaquette, rayon, vies, score, lastBonus)

                if rafraichi == 0:
                    efface('raquette')
                    efface('balle')
                raquette(ax, ay, largeurRaquette, hauteurRaquette)
                cercle(xBalle, yBalle, rayon, couleur='black', remplissage='grey', tag='balle')

                if victoire(lstBrique):
                    gagne = 1
                    break
                if perdu(yBalle, rayon):
                    vies -= 1
                    break

                #Pause               
                ev = donne_evenement()
                if type_evenement(ev) in ['ClicDroit','ClicGauche']:
                    if clic_x(ev)>=largeurFenetre+15 and clic_x(ev)<=largeurFenetre+185 and clic_y(ev)<=575 and clic_y(ev)>=525:
                        quitter, tempsAretirer = pause(hauteurFenetre, largeurFenetre, lstBrique, nbreBriqueParLigne, nbreLigne, tempsAretirer)
                elif type_evenement(ev) == 'Touche':
                    if touche(ev) == 'p':
                        quitter, tempsAretirer = pause(hauteurFenetre, largeurFenetre, lstBrique, nbreBriqueParLigne, nbreLigne, tempsAretirer)
                if quitter == 1:
                    break
                mise_a_jour()

        efface_tout()
        if gagne == 0 and quitter==0:
            rejouer = affichage_fin(('Perdu','red'), largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus)
        elif gagne == 1 and quitter == 0:
            score += vies*75
            rejouer = affichage_fin(('Gagné', 'green'), largeurFenetre, hauteurFenetre, tempsAretirer, vies, lastBonus)
    ferme_fenetre() 
    exit()
