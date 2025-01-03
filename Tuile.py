from CarrePion import CarrePion
from RondPion import RondPion
from Constantes import PION_BLANC

class Tuile:
    def __init__(self, posX: int, posY: int, carrePion: bool, idTuile: int) -> None:
        if carrePion:
            self.carrePion = CarrePion()
        else:
            self.carrePion = None
        self.posX = posX
        self.posY = posY
        self.idTuile = idTuile

    def definirCarrePion(self, carrePion: bool = None) -> None:
        self.carrePion = carrePion

    def obtenirCarrePion(self) -> bool:
        return self.carrePion

    def estCarrePionDefini(self) -> bool:
        return self.carrePion is not None

    def obtenirRondPion(self) -> RondPion:
        if self.estRondPionDefini():
            return self.carrePion.obtenirRondPion()
        return None

    def definirNouveauRondPion(self, numeroJoueur: int, couleur: bool, posX: int, posY: int, id: int) -> RondPion:
        if self.estCarrePionDefini():
            return self.carrePion.definirNouveauRondPion(numeroJoueur, couleur, posX, posY, id)

    def definirRondPion(self, pion: RondPion) -> None:
        if self.estCarrePionDefini():
            self.carrePion.definirRondPion(pion)

    def estRondPionDefini(self) -> bool:
        if self.estCarrePionDefini():
            return self.carrePion.estRondPionDefini()
        return False

    def obtenir_posX(self):
        return self.posX

    def definir_posX(self, nouveau_posX):
        self.posX = nouveau_posX

    def obtenir_posY(self):
        return self.posY

    def definir_posY(self, nouveau_posY):
        self.posY = nouveau_posY

    def obtenirIdTuile(self) -> int:
        return self.idTuile


