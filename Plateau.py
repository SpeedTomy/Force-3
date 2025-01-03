from Constantes import PION_BLANC
from Tuile import Tuile
from Joueur import Joueur
import numpy as np
import copy

class Plateau:
    def __init__(self, joueur1: Joueur, joueur2: Joueur) -> None:
        self.plateau = np.empty([3, 3], dtype=Tuile)
        k = 1
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    self.plateau[i][j] = Tuile(i, j, False, k)
                    k += 1
                else:
                    self.plateau[i][j] = Tuile(i, j, True, k)
                    k += 1
        self.tuileVide = self.plateau[1][1]
        self.joueurs = [joueur1, joueur2]
        self.gagnant = None
        self.carrePionDeplace = None
        self.deuxCarrePionsDeplaces = None
        self.dernierDeplacementDeuxCarres = False
        self.deplacementDeuxCarresBloque = False
        self.cooldown = 0

    def obtenir_tuileVide(self) -> Tuile:
        return self.tuileVide

    def placerRondPion(self, numeroJoueur: int = 0, posX: int = 0, posY: int = 0) -> int:
        joueur = self.joueurs[numeroJoueur]
        tuile = self.plateau[posX][posY]
        if joueur.estRondPionDisponible():
            if tuile.estCarrePionDefini() and not tuile.estRondPionDefini():
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = None
                idRondPion = len(joueur.pions) + 1
                nouveauRondPion = tuile.definirNouveauRondPion(numeroJoueur, joueur.couleur, posX, posY, idRondPion)
                joueur.pions.append(nouveauRondPion)
                return 0
            return -2
        return -1

    def deplacerRondPion(self, numeroJoueur: int = 0, idPion: int = 0, prochainX: int = 0, prochainY: int = 0) -> int:
        pion = self.joueurs[numeroJoueur].pions[idPion - 1]
        tuilePrecedente = self.plateau[pion.posX][pion.posY]
        tuileProchaine = self.plateau[prochainX][prochainY]
        if not tuileProchaine.estCarrePionDefini() or tuileProchaine.estRondPionDefini():
            return -1
        self.deuxCarrePionsDeplaces = None
        self.carrePionDeplace = None
        rondPion = tuilePrecedente.obtenirRondPion()
        tuilePrecedente.definirRondPion(None)
        tuileProchaine.definirRondPion(rondPion)
        pion.posX = prochainX
        pion.posY = prochainY
        return 0

    def deplacerCarrePion(self, posX: int = 0, posY: int = 0, deuxCarres: bool = False) -> int:
        tuile = self.plateau[posX][posY]
        if [self.tuileVide, tuile] == self.carrePionDeplace and not deuxCarres:
            return -1
        if self.tuileVide.idTuile == 1:
            if self.plateau[posX][posY].idTuile in {2, 4}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 2:
            if self.plateau[posX][posY].idTuile in {1, 3, 5}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 3:
            if self.plateau[posX][posY].idTuile in {2, 6}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 4:
            if self.plateau[posX][posY].idTuile in {1, 5, 7}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 5:
            if self.plateau[posX][posY].idTuile in {2, 4, 6, 8}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 6:
            if self.plateau[posX][posY].idTuile in {3, 5, 9}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 7:
            if self.plateau[posX][posY].idTuile in {4, 8}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 8:
            if self.plateau[posX][posY].idTuile in {5, 7, 9}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 9:
            if self.plateau[posX][posY].idTuile in {6, 8}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                if rondPion:
                    self.tuileVide.definirRondPion(rondPion)
                    rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
                self.tuileVide = tuile
                return 0
            else:
                return -2
        elif self.tuileVide.idTuile == 10:
            if self.plateau[posX][posY].idTuile in {1, 2, 3, 5}:
                self.deuxCarrePionsDeplaces = None
                self.carrePionDeplace = [tuile, self.tuileVide]
                carrePion = tuile.obtenirCarrePion()
                tuile.definirCarrePion(None)
                self.tuileVide.definirCarrePion(carrePion)
                self.tuileVide = tuile
                return 0
            else:
                return -2

    def estDeplacement2CarrePionsPossible(self) -> bool:
        if self.cooldown > 0:
            return False
        return self.tuileVide.idTuile != 5

    def deplacer2CarrePions(self, sx, sy):
        if not self._peutDeplacerCarrePion(sx[0], sy[0]) or not self._peutDeplacerCarrePion(sx[1], sy[1]):
            return -3
        if self._inverseDeplacementPrecedent(sx, sy):
            return -2
        self._deplacerCarrePion(sx[0], sy[0], deuxCarres=True)
        self._deplacerCarrePion(sx[1], sy[1], deuxCarres=True)
        self.deuxCarrePionsDeplaces = [(self.plateau[sx[0]][sy[0]], self.plateau[sx[1]][sy[1]])]
        self.dernierDeplacementDeuxCarres = True
        self.deplacementDeuxCarresBloque = True
        self.cooldown = 2
        return 0

    def _deplacerCarrePion(self, posX, posY, deuxCarres=False):
        tuile = self.plateau[posX][posY]
        carrePion = tuile.obtenirCarrePion()
        rondPion = tuile.obtenirRondPion() if tuile.estRondPionDefini() else None
        tuile.definirCarrePion(None)
        self.tuileVide.definirCarrePion(carrePion)
        if rondPion:
            self.tuileVide.definirRondPion(rondPion)
            rondPion.posX, rondPion.posY = self.tuileVide.posX, self.tuileVide.posY
        self.tuileVide = tuile
        if not deuxCarres:
            self.carrePionDeplace = [tuile, self.tuileVide]
            if self.dernierDeplacementDeuxCarres:
                self.deplacementDeuxCarresBloque = True
            self.dernierDeplacementDeuxCarres = False

    def finTour(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def verifierSiGagnant(self) -> int:
        pionsRonds = [[], []]
        conditionsVictoire = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7]
        ]
        for i in range(3):
            for j in range(3):
                tuile = self.plateau[i][j]
                if tuile.estRondPionDefini():
                    pion = tuile.obtenirRondPion()
                    pionsRonds[pion.obtenirNumeroJoueur()].append(tuile.obtenirIdTuile())
        if pionsRonds[0] in conditionsVictoire:
            return 0
        elif pionsRonds[1] in conditionsVictoire:
            return 1
        else:
            return -1

    def obtenir_deuxCarrePionsDeplaces(self):
        return self.deuxCarrePionsDeplaces

    def obtenir_carrePionDeplace(self):
        return self.carrePionDeplace

    def obtenir_plateau_par_coordonnees(self, posX: int = None, posY: int = None):
        return self.plateau[posX, posY]

    def obtenir_rondPion_par_plateau(self, posX, posY):
        if self.plateau[posX, posY] is not None and self.plateau[posX, posY].carrePion is not None:
            return self.plateau[posX, posY].carrePion.rondPion
        return None

    def obtenirDeplacementsRondsValides(self, posX: int, posY: int):
        deplacements_valides = []
        for i in range(3):
            for j in range(3):
                tuile = self.plateau[i][j]
                if tuile.estCarrePionDefini() and not tuile.estRondPionDefini() and not (i == posX and j == posY):
                    deplacements_valides.append((i, j))
        return deplacements_valides

    def obtenirDeplacementsCarresValides(self, posX: int, posY: int):
        deplacements_valides = []
        if not self.plateau[posX][posY].estCarrePionDefini():
            return deplacements_valides
        tempPlateau = copy.deepcopy(self)
        if tempPlateau.deplacerCarrePion(posX, posY) == 0:
            deplacements_valides.append((tempPlateau.tuileVide.posX, tempPlateau.tuileVide.posY))
        return deplacements_valides

    def obtenirTousCarresDeplacables(self) -> list:
        carres = []
        for i in range(3):
            for j in range(3):
                tuile = self.plateau[i][j]
                if tuile.estCarrePionDefini():
                    tempPlateau = copy.deepcopy(self)
                    if tempPlateau.deplacerCarrePion(i, j) == 0:
                        carres.append((i, j))
        return carres

    def obtenir_etat_plateau(self):
        etat = []
        for i in range(3):
            ligne = []
            for j in range(3):
                tuile = self.plateau[i][j]
                if not tuile.estCarrePionDefini():
                    ligne.append("vide")
                elif tuile.estRondPionDefini():
                    pion = tuile.obtenirRondPion()
                    if pion.couleur:
                        ligne.append("blanc")
                    else:
                        ligne.append("noir")
                else:
                    ligne.append("carre")
            etat.append(ligne)
        return etat