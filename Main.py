from Plateau import Plateau
from Joueur import Joueur
from Constantes import PION_NOIR, PION_BLANC
from Noeud import Noeud
import math
import numpy as np
import random
import time

def lancerJeu(plateau: Plateau, joueur1: Joueur, joueur2: Joueur, modeJeu: int = 0) -> None:
    if modeJeu == 1:
        while 1:
            actionEffectuee = False
            while not actionEffectuee:
                if plateau.estDeplacement2CarrePionsPossible():
                    actionEffectuee = choixJoueur2CarrePionsPossible(joueur1, plateau)
                else:
                    actionEffectuee = choixJoueur2CarrePionsImpossible(joueur1, plateau)
            if verifierGagnant(plateau) != -1:
                break
            actionEffectuee = False
            while not actionEffectuee:
                if plateau.estDeplacement2CarrePionsPossible():
                    actionEffectuee = choixJoueur2CarrePionsPossible(joueur2, plateau)
                else:
                    actionEffectuee = choixJoueur2CarrePionsImpossible(joueur2, plateau)
            if verifierGagnant(plateau) != -1:
                break
    elif modeJeu == 2:
        while 1:
            actionEffectuee = False
            while not actionEffectuee:
                if plateau.estDeplacement2CarrePionsPossible():
                    actionEffectuee = choixJoueur2CarrePionsPossible(joueur1, plateau)
                else:
                    actionEffectuee = choixJoueur2CarrePionsImpossible(joueur1, plateau)
            if verifierGagnant(plateau) != -1:
                break
            actionEffectuee = False
            start = time.time()
            while not actionEffectuee:
                actionEffectuee = choixIA(joueur2, joueur1, plateau)
            if verifierGagnant(plateau) != -1:
                break
    else:
        while 1:
            actionEffectuee = False
            while not actionEffectuee:
                actionEffectuee = choixIA(joueur1, joueur2, plateau)
            if actionEffectuee:
                print("tour de l'IA 1")
            if verifierGagnant(plateau) != -1:
                break
            actionEffectuee = False
            while not actionEffectuee:
                actionEffectuee = choixIA(joueur2, joueur1, plateau)
            if actionEffectuee:
                print("tour de l'IA 2")
            if verifierGagnant(plateau) != -1:
                break

def choixJoueur2CarrePionsImpossible(joueur: Joueur = None, plateau: Plateau = None) -> bool:
    action = 0
    choixAutorises = []
    print("Joueur " + str(joueur.obtenirNumeroJoueur()+1) +", veuillez choisir une action parmi les suivantes")
    if len(joueur.pions) < 3:
        print("- placer un pion rond sur un pion carré (1);")
        choixAutorises.append("1")
    if len(joueur.pions) > 0:
        print("- déplacer un de vos pions ronds (2).")
        choixAutorises.append("2")
    print("- déplacer un pion carré sur une case vide (3);")
    choixAutorises.append("3")
    print("Vous pouvez placer "+str(joueur.obtenirNombreRondPionsDisponibles()) + " pions.")
    print("Tapez le numéro entre ( ) pour choisir une action")
    while action not in choixAutorises:
        action = input()
    print()
    return choixAction(int(action), joueur, plateau)

def choixJoueur2CarrePionsPossible(joueur: Joueur = None, plateau: Plateau = None) -> bool:
    action = 0
    choixAutorises = []
    print("Joueur " + str(joueur.obtenirNumeroJoueur()+1) +", veuillez choisir une action parmi les suivantes")
    if len(joueur.pions) < 3:
        print("- placer un pion rond sur un pion carré (1);")
        choixAutorises.append("1")
    if len(joueur.pions) > 0:
        print("- déplacer un de vos pions ronds (2).")
        choixAutorises.append("2")
    print("- déplacer un pion carré sur une case vide (3);")
    choixAutorises.append("3")
    print("- déplacer 2 pions carrés (4).")
    choixAutorises.append("4")
    print("Vous pouvez placer "+str(joueur.obtenirNombreRondPionsDisponibles()) + " pions.")
    print("Tapez le numéro entre () pour choisir une action")
    while action not in choixAutorises:
        action = input()
    print()
    return choixAction(int(action), joueur, plateau)

def choixIA(joueur: Joueur = None, adversaire: Joueur = None, plateau: Plateau = None) -> bool:
    noeud = Noeud(3, joueur, adversaire, plateau)
    v = MinMaxPL(noeud, noeud.profondeur, joueur, adversaire)
    meilleure_action = []
    for i in range(len(noeud.enfant)):
        if (noeud.enfant[i].valeur == v and noeud.enfant[i].joueur.numeroJoueur != joueur.numeroJoueur and noeud.enfant[i].plateau.verifierSiGagnant() != adversaire.numeroJoueur):
            meilleure_action.append(noeud.enfant[i])
        if noeud.enfant[i].plateau.verifierSiGagnant() == 0 and noeud.enfant[i].plateau.verifierSiGagnant() == 1:
            meilleure_action.append(noeud.enfant[i])
    if len(meilleure_action) > 1:
        enfant_aleatoire = random.choice(meilleure_action)
    else:
        enfant_aleatoire = meilleure_action[0]
    if enfant_aleatoire.action.num_action == 1:
        if plateau.placerRondPion(joueur.numeroJoueur, enfant_aleatoire.action.posX, enfant_aleatoire.action.posY) == 0:
            return True
    if enfant_aleatoire.action.num_action == 2:
        if enfant_aleatoire.action.id_pion == 1:
            if plateau.deplacerRondPion(joueur.numeroJoueur, 1, enfant_aleatoire.action.posX, enfant_aleatoire.action.posY) == 0:
                return True
        elif enfant_aleatoire.action.id_pion == 2:
            if plateau.deplacerRondPion(joueur.numeroJoueur, 2, enfant_aleatoire.action.posX, enfant_aleatoire.action.posY) == 0:
                return True
        elif enfant_aleatoire.action.id_pion == 3:
            if plateau.deplacerRondPion(joueur.numeroJoueur, 3, enfant_aleatoire.action.posX, enfant_aleatoire.action.posY) == 0:
                return True
    if enfant_aleatoire.action.num_action == 3:
        if plateau.deplacerCarrePion(enfant_aleatoire.action.posX, enfant_aleatoire.action.posY) == 0:
            return True
    if enfant_aleatoire.action.num_action == 4:
        if plateau.deplacer2CarrePions(enfant_aleatoire.action.table_posX, enfant_aleatoire.action.table_posY) == 0:
            return True

def evaluer_position_pion(joueur: Joueur = None):
    position_pts = np.array([[2,1,2],[1,3,1],[2,1,2]])
    res = 0
    if len(joueur.pions) > 0:
        if len(joueur.pions) - 1 > 0:
            for i in range(len(joueur.pions)):
                res += position_pts[joueur.pions[i].posX, joueur.pions[i].posY]
        else:
            res += position_pts[joueur.pions[0].posX, joueur.pions[0].posY]
    return res

def evaluer_nb_pion(joueur: Joueur = None, autre_joueur: Joueur = None, plateau: Plateau = None):
    nb_pion_joueur = len(joueur.pions)
    nb_pion_adversaire = len(autre_joueur.pions)
    if nb_pion_joueur > nb_pion_adversaire:
        return 1
    elif nb_pion_joueur < nb_pion_adversaire:
        return -1
    else:
        return 0

def evaluer_pion_entre(joueur: Joueur = None, plateau: Plateau = None):
    res = 0
    for i in range(3):
        if (plateau.obtenir_plateau_par_coordonnees(1,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(1,i) != None 
               and plateau.obtenir_rondPion_par_plateau(1,i).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(0,i) != plateau.tuileVide  and plateau.obtenir_rondPion_par_plateau(0,i) != None 
               and plateau.obtenir_rondPion_par_plateau(0,i).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(2,i) != plateau.tuileVide  and plateau.obtenir_rondPion_par_plateau(2,i) != None 
               and plateau.obtenir_rondPion_par_plateau(2,i).couleur != joueur.couleur):
                   res = 2
        if (plateau.obtenir_plateau_par_coordonnees(i,1) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,1) != None 
               and plateau.obtenir_rondPion_par_plateau(i,1).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,0) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,0) != None 
               and plateau.obtenir_rondPion_par_plateau(i,0).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,2) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,2) != None 
               and plateau.obtenir_rondPion_par_plateau(i,2).couleur != joueur.couleur):
                   res = 2
    if (plateau.obtenir_plateau_par_coordonnees(1,1) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(1,1) != None 
               and plateau.obtenir_rondPion_par_plateau(1,1).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(0,0) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(0,0) != None 
               and plateau.obtenir_rondPion_par_plateau(0,0).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(2,2) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(2,2) != None 
               and plateau.obtenir_rondPion_par_plateau(2,2).couleur != joueur.couleur):
                   res = 2
    if (plateau.obtenir_plateau_par_coordonnees(1,1) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(1,1) != None 
               and plateau.obtenir_rondPion_par_plateau(1,1).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(0,2) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(0,2) != None 
               and plateau.obtenir_rondPion_par_plateau(0,2).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(2,0) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(2,0) != None 
               and plateau.obtenir_rondPion_par_plateau(2,0).couleur != joueur.couleur):
                   res = 2
    return res

def evaluer_alignement_pion(joueur: Joueur = None):
    res = 0
    if len(joueur.pions) >= 2:
        if joueur.pions[0].posX == joueur.pions[1].posX or joueur.pions[0].posY == joueur.pions[1].posY:
            res = 1
        if joueur.pions[0].posX == 0 and joueur.pions[0].posY == 0:
            if joueur.pions[1].posX == 1 and joueur.pions[1].posY == 1 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 2:
                res = 1
        elif joueur.pions[0].posX == 2 and joueur.pions[0].posY == 2:
            if joueur.pions[1].posX == 1 and joueur.pions[1].posY == 1 or joueur.pions[1].posX == 0 and joueur.pions[1].posY == 0:
                res = 1
        elif joueur.pions[0].posX == 0 and joueur.pions[0].posY == 2:
            if joueur.pions[1].posX == 1 and joueur.pions[1].posY == 1 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 0:
                res = 1
        elif joueur.pions[0].posX == 2 and joueur.pions[0].posY == 0:
            if joueur.pions[1].posX == 1 and joueur.pions[1].posY == 1 or joueur.pions[1].posX == 0 and joueur.pions[1].posY == 2:
                res = 1
        elif joueur.pions[0].posX == 1 and joueur.pions[0].posY == 1:
            if joueur.pions[1].posX == 0 and joueur.pions[1].posY == 0 or joueur.pions[1].posX == 0 and joueur.pions[1].posY == 2 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 0 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 2:
                res = 1
    elif len(joueur.pions) == 3:
        if joueur.pions[0].posX == joueur.pions[1].posX or joueur.pions[0].posX == joueur.pions[2].posX or joueur.pions[1].posX == joueur.pions[2].posX or joueur.pions[0].posY == joueur.pions[1].posY or joueur.pions[0].posY == joueur.pions[2].posY or joueur.pions[1].posY == joueur.pions[2].posY:
            res = 1
        if joueur.pions[0].posX == 0 and joueur.pions[0].posY == 0 or joueur.pions[1].posX == 0 and joueur.pions[1].posY == 0:
            if joueur.pions[2].posX == 1 and joueur.pions[2].posY == 1 or joueur.pions[2].posX == 2 and joueur.pions[2].posY == 2:
                res = 1
        elif joueur.pions[0].posX == 2 and joueur.pions[0].posY == 2 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 2:
            if joueur.pions[2].posX == 1 and joueur.pions[2].posY == 1 or joueur.pions[2].posX == 0 and joueur.pions[2].posY == 0:
                res = 1
        elif joueur.pions[0].posX == 0 and joueur.pions[0].posY == 2 or joueur.pions[1].posX == 0 and joueur.pions[1].posY == 2:
            if joueur.pions[2].posX == 1 and joueur.pions[2].posY == 1 or joueur.pions[2].posX == 2 and joueur.pions[2].posY == 0:
                res = 1
        elif joueur.pions[0].posX == 2 and joueur.pions[0].posY == 0 or joueur.pions[1].posX == 2 and joueur.pions[1].posY == 0:
            if joueur.pions[2].posX == 1 and joueur.pions[2].posY == 1 or joueur.pions[2].posX == 0 and joueur.pions[2].posY == 2:
                res = 1
        elif joueur.pions[0].posX == 1 and joueur.pions[0].posY == 1 or joueur.pions[1].posX == 1 and joueur.pions[1].posY == 1:
            if joueur.pions[2].posX == 0 and joueur.pions[2].posY == 0 or joueur.pions[2].posX == 0 and joueur.pions[2].posY == 2 or joueur.pions[2].posX == 2 and joueur.pions[2].posY == 0 or joueur.pions[2].posX == 2 and joueur.pions[2].posY == 2:
                res = 1
    return res

def evaluer_opposition_bord_pion(joueur: Joueur = None, plateau: Plateau = None):
    res = 0
    for i in range(3):
        if (plateau.obtenir_plateau_par_coordonnees(0,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(0,i) != None 
           and plateau.obtenir_rondPion_par_plateau(0,i).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(1,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(1,i) != None 
               and plateau.obtenir_rondPion_par_plateau(1,i).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(2,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(2,i) != None 
               and plateau.obtenir_rondPion_par_plateau(2,i).couleur != joueur.couleur):
                   res = 1
        if (plateau.obtenir_plateau_par_coordonnees(2,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(2,i) != None 
               and plateau.obtenir_rondPion_par_plateau(2,i).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(1,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(1,i) != None 
               and plateau.obtenir_rondPion_par_plateau(1,i).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(0,i) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(0,i) != None 
               and plateau.obtenir_rondPion_par_plateau(0,i).couleur != joueur.couleur):
                   res = 1
        if (plateau.obtenir_plateau_par_coordonnees(i,0) != plateau.tuileVide  and plateau.obtenir_rondPion_par_plateau(i,0) != None 
               and plateau.obtenir_rondPion_par_plateau(i,0).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,1) != plateau.tuileVide  and plateau.obtenir_rondPion_par_plateau(i,1) != None 
               and plateau.obtenir_rondPion_par_plateau(i,1).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,2) != plateau.tuileVide  and plateau.obtenir_rondPion_par_plateau(i,2) != None 
               and plateau.obtenir_rondPion_par_plateau(i,2).couleur != joueur.couleur):
                   res = 1
        if (plateau.obtenir_plateau_par_coordonnees(i,2) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,2) != None 
               and plateau.obtenir_rondPion_par_plateau(i,2).couleur == joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,1) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,1) != None 
               and plateau.obtenir_rondPion_par_plateau(i,1).couleur != joueur.couleur and
               plateau.obtenir_plateau_par_coordonnees(i,0) != plateau.tuileVide and plateau.obtenir_rondPion_par_plateau(i,0) != None 
               and plateau.obtenir_rondPion_par_plateau(i,0).couleur != joueur.couleur):
                   res = 1
    return res

def evaluation(joueur_max: Joueur = None, joueur_min: Joueur = None, plateau: Plateau = None):
    if plateau.verifierSiGagnant() == joueur_max.numeroJoueur:
        return 500
    if plateau.verifierSiGagnant() == joueur_min.numeroJoueur:
        return -500
    else:
        score = evaluer_position_pion(joueur_max)
        score += evaluer_nb_pion(joueur_max, joueur_min, plateau)
        score += evaluer_pion_entre(joueur_max, plateau)
        score += evaluer_opposition_bord_pion(joueur_max, plateau)
        score += evaluer_alignement_pion(joueur_max)
        return score

def MaxValeur(noeud, profondeur, joueur, autre_joueur):
    if noeud.plateau.verifierSiGagnant() != -1 or profondeur == 0:
        noeud.valeur = evaluation(joueur, autre_joueur, noeud.plateau)
        return noeud.valeur
    noeud.valeur = -math.inf
    for i in range(len(noeud.enfant)):
        noeud.valeur = max(noeud.valeur, MinValeur(noeud.enfant[i], profondeur-1, joueur, autre_joueur))
    return noeud.valeur

def MinValeur(noeud, profondeur, joueur, autre_joueur):
    if noeud.plateau.verifierSiGagnant() != -1 or profondeur == 0:
        noeud.valeur = evaluation(joueur, autre_joueur, noeud.plateau)
        return noeud.valeur
    noeud.valeur = math.inf
    for i in range(len(noeud.enfant)):
        noeud.valeur = min(noeud.valeur, MaxValeur(noeud.enfant[i], profondeur-1, joueur, autre_joueur))
    return noeud.valeur

def MinMaxPL(noeud, profondeur, joueur, autre_joueur):
    noeud.valeur = MaxValeur(noeud, profondeur, joueur, autre_joueur)
    return noeud.valeur

def choixAction(action: int, joueur: Joueur, plateau: Plateau) -> bool:     
    if action == 1: 
        return placerRondPion(joueur.obtenirNumeroJoueur(), plateau)
    elif action == 2:
        return deplacerRondPion(joueur, plateau)
    elif action == 3:
        return deplacerCarrePion(plateau)
    elif action == 4:
        return deplacer2CarrePions(plateau)

def placerRondPion(joueur: int, plateau: Plateau) -> bool:
    x = 0
    y = 0
    xNumerosPossibles = ["0", "1", "2"]
    yNumerosPossibles = ["0", "1", "2"]
    print("Sur quelle case souhaitez-vous placer un pion rond ?")
    print("ligne :")
    while x not in xNumerosPossibles:
        x = input()
    print("colonne :")
    while y not in yNumerosPossibles:
        y = input()
    actionReussie = plateau.placerRondPion(joueur, int(x), int(y))
    if actionReussie == -1:
        print("\nVous n'avez plus de pions ronds !\n")
        return False
    elif actionReussie == -2:
        print("\nVous ne pouvez pas placer un pion rond ici !\n")
        return False
    else:
        print("\nSuccès !\n")
        return True

def deplacerRondPion(joueur: Joueur, plateau: Plateau) -> bool:
    idPionRondPossible = []
    idPion = 0
    x = 0
    y = 0
    if len(joueur.pions) - 1 != 0:
        for i in range(len(joueur.pions)):
            idPionRondPossible.append(str(i + 1))
    else:
        idPionRondPossible = ["1"]
    xNumerosPossibles = ["0", "1", "2"]
    yNumerosPossibles = ["0", "1", "2"]
    print("Quel pion rond souhaitez-vous déplacer ?")
    print("Sélectionnez le numéro de votre pion rond : 1, 2 ou 3.")
    while idPion not in idPionRondPossible:
        idPion = input()
    print("\nOù souhaitez-vous déplacer ce pion ?")
    print("Sélectionnez une case pour la nouvelle position du pion (elle ne peut pas être la case actuelle du pion)")
    print("ligne :")
    while x not in xNumerosPossibles:
        x = input()
    print("colonne :")
    while y not in yNumerosPossibles:
        y = input()
    actionReussie = plateau.deplacerRondPion(joueur.obtenirNumeroJoueur(), int(idPion), int(x), int(y))
    if actionReussie == -1:
        print("\nVous ne pouvez pas déplacer votre pion rond sur les coordonnées ["+ x + "]["+ y + "] !\n")
        return False
    else:
        print("\nSuccès !\n")
        return True

def deplacer2CarrePions(plateau: Plateau) -> bool:
    x = [0,0]
    y = [0,0]
    xNumerosPossibles = ["0", "1", "2"]
    yNumerosPossibles = ["0", "1", "2"]
    print("Quel pion carré souhaitez-vous déplacer en premier ?")
    print("ligne :")
    while x[0] not in xNumerosPossibles:
        x[0] = input()
    print("colonne :")
    while y[0] not in yNumerosPossibles:
        y[0] = input()
    print("\nQuel est le deuxième pion carré que vous souhaitez déplacer ?")
    print("Sélectionnez une case pour choisir le pion carré")
    print("ligne :")
    while x[1] not in xNumerosPossibles:
        x[1] = input()
    print("colonne :")
    while y[1] not in yNumerosPossibles:
        y[1] = input()
    actionReussie = plateau.deplacer2CarrePions(x, y)
    if actionReussie == -1:
        print("\nVous n'êtes pas autorisé à déplacer des pions carrés !\n")
        return False
    elif actionReussie == -2:
        print("\nVous n'êtes pas autorisé à inverser les 2 mouvements que votre adversaire a effectués lors de son tour précédent !\n")
        return False
    elif actionReussie == -3:
        print("\nLa première case que vous avez choisie ne peut pas être déplacée !\n")
        return False
    elif actionReussie == -4:
        print("\nVos deux cases ne sont pas alignées l'une avec l'autre !\n")
        return False
    elif actionReussie == -5:
        print("\nVous ne pouvez pas déplacer ces deux cases de cette manière !\n")
        return False
    else:
        print("\nSuccès !\n")
        return True

def deplacerCarrePion(plateau: Plateau) -> bool:
    x = 0
    y = 0
    xNumerosPossibles = ["0", "1", "2"]
    yNumerosPossibles = ["0", "1", "2"]
    print("Pour déplacer un pion carré, sélectionnez une case contenant un pion carré et qui est à côté de la case vide")
    print("ligne :")
    while x not in xNumerosPossibles:
        x = input()
    print("colonne :")
    while y not in xNumerosPossibles:
        y = input()
    actionReussie = plateau.deplacerCarrePion(int(x), int(y))
    if actionReussie == -1:
        print("\nVous n'êtes pas autorisé à inverser le mouvement que votre adversaire a effectué lors de son tour précédent !\n")
        return False
    elif actionReussie == -2:
        print("\nVous ne pouvez pas déplacer cette case !\n")
        return False
    else: 
        print("\nSuccès !")
        return True

def verifierGagnant(plateau) -> int: 
    gagnant = plateau.verifierSiGagnant()
    if gagnant == 0:
        print("\nLe joueur 1 est le gagnant !")
        return 0
    elif gagnant == 1:
        print("\nLe joueur 2 est le gagnant !")
        return 1
    else:
        return -1

