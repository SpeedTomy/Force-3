from Plateau import Plateau
from Joueur import Joueur
from ActionBord import ActionBord
import copy

class Noeud:
    def __init__(self, profondeur, joueur, autre_joueur, plateau, action_jouee = None, valeur = None):
        self.profondeur = profondeur
        self.joueur = joueur
        self.autre_joueur = autre_joueur
        self.action = action_jouee
        self.valeur = valeur
        self.enfant = []
        self.plateau = plateau
        self.copie_plateau = copy.deepcopy(self.plateau)
        self.copie_joueur = copy.deepcopy(self.joueur)
        self.copie_autre_joueur = copy.deepcopy(self.autre_joueur)
        self.creerEnfant()

    def actions_possibles(self):
        res_actions = []
        if self.plateau.verifierSiGagnant() != 0 or self.plateau.verifierSiGagnant() != 1:
            if len(self.joueur.pions) == 0:
                res_actions = [1, 3]
            elif len(self.joueur.pions) > 0 and len(self.joueur.pions) < 3:
                res_actions = [1, 2, 3]
            elif len(self.joueur.pions) == 3:
                res_actions = [2, 3]
            if self.plateau.tuileVide.posX != 1 and self.plateau.tuileVide.posY != 1:
                res_actions.append(4)
        return res_actions

    def creerEnfant(self):
        actions_possibles = self.actions_possibles()
        if self.profondeur > 0 and len(actions_possibles) != 0:
            for i in range(len(actions_possibles)):
                action = actions_possibles[i]
                if action == 1:
                    for x in range(3):
                        for y in range(3):
                            self.copie_plateau = copy.deepcopy(self.plateau)
                            self.copie_joueur = copy.deepcopy(self.joueur)
                            self.copie_autre_joueur = copy.deepcopy(self.autre_joueur)
                            if self.copie_plateau.obtenir_plateau_par_coordonnees(x, y) != self.copie_plateau.tuileVide and self.copie_plateau.obtenir_rondPion_par_plateau(x, y) == None:
                                if self.copie_plateau.placerRondPion(self.copie_joueur.numeroJoueur, int(x), int(y)) == 0:
                                    action = ActionBord(1, x, y)
                                    self.enfant.append(Noeud(self.profondeur-1, self.copie_autre_joueur, self.copie_joueur, self.copie_plateau, action))
                if action == 2:
                    for pion in self.copie_joueur.pions:
                        for x in range(3):
                            for y in range(3):
                                self.copie_plateau = copy.deepcopy(self.plateau)
                                self.copie_joueur = copy.deepcopy(self.joueur)
                                self.copie_autre_joueur = copy.deepcopy(self.autre_joueur)
                                if (x, y) != (self.plateau.tuileVide.posX, self.plateau.tuileVide.posY) and self.plateau.obtenir_rondPion_par_plateau(x, y) == None:
                                    if self.copie_plateau.deplacerRondPion(self.copie_joueur.numeroJoueur, pion.id, x, y) == 0:
                                        action = ActionBord(2, x, y, pion.id)
                                        self.enfant.append(Noeud(self.profondeur-1, self.copie_autre_joueur, self.copie_joueur, self.copie_plateau, action))
                if action == 3:
                    for x in range(3):
                        for y in range(3):
                            self.copie_plateau = copy.deepcopy(self.plateau)
                            self.copie_joueur = copy.deepcopy(self.joueur)
                            self.copie_autre_joueur = copy.deepcopy(self.autre_joueur)
                            if (x, y) != (self.copie_plateau.tuileVide.posX, self.copie_plateau.tuileVide.posY):
                                if self.copie_plateau.deplacerCarrePion(x, y) == 0:
                                    action = ActionBord(3, x, y)
                                    self.enfant.append(Noeud(self.profondeur-1, self.copie_autre_joueur, self.copie_joueur, self.copie_plateau, action))
                if action == 4:
                    for x in range(3):
                        for y in range(3):
                            for i in range(3):
                                for j in range(3):
                                    self.copie_plateau = copy.deepcopy(self.plateau)
                                    self.copie_joueur = copy.deepcopy(self.joueur)
                                    self.copie_autre_joueur = copy.deepcopy(self.autre_joueur)
                                    if self.copie_plateau.tuileVide.posX == 1 and self.copie_plateau.tuileVide.posY == 1:
                                        table_x.append(x)
                                        table_x.append(i)
                                        table_y.append(y)
                                        table_y.append(j)
                                        if self.copie_plateau.deplacer2CarrePions(table_x, table_y) == 0:
                                            action = ActionBord(4, x, y, None, table_x, table_y)
                                            self.enfant.append(Noeud(self.profondeur-1, self.copie_autre_joueur, self.copie_joueur, self.copie_plateau, action))

    def afficher(self):
        print("père")
        self.plateau.afficherPlateau()
        print("enfant")
        for i in range(len(self.enfant)):
            self.enfant[i].plateau.afficherPlateau()