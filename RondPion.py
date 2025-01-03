from Constantes import PION_BLANC
"""
The class RondPion represents the circular pawns that can
be placed on top of a square pawn.
"""

class RondPion:
    """ 
    Instanciate a circular pawn with the following parameters:
     - numeroJoueur: number of the player who owns the pawn, numeroJoueur = 0 or 1
     - couleur: color of the circular pawn
    """
    def __init__(self, numeroJoueur: int = 0, couleur: bool = PION_BLANC, id: int = 0, posX: int = 0, posY: int = 0) -> None:
        self.numeroJoueur = numeroJoueur
        self.couleur = couleur
        self.id = id
        self.posX = posX
        self.posY = posY

    # returns the color of the pawn
    def obtenirCouleur(self) -> bool:
        return self.couleur
    
    # returns the number of the player who owns the pawn
    def obtenirNumeroJoueur(self) -> int:
        return self.numeroJoueur
