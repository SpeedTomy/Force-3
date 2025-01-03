from RondPion import RondPion
from Constantes import PION_BLANC

"""
The class CarrePion represents the square pawns that can
be placed on top of tiles.
"""

class CarrePion:
    # Instanciate a square pawn
    def __init__(self) -> None:
        self.rondPion = None

    # Checks if the square pawn has a circular pawn 
    def estRondPionDefini(self) -> bool:
        return self.rondPion is not None

    # returns the circular pawn placed on the square pawn
    def obtenirRondPion(self) -> RondPion:
        return self.rondPion

    """
    Set a new circular pawn on the square pawn.
    The functions uses the following parameters: 
    - playerNumber: number of the player who owns the circular pawn, playerNumber = 0 or 1
    - color: color of the new circular pawn 
    """
    def definirNouveauRondPion(self, numeroJoueur: int = 0, couleur: bool = PION_BLANC, posX: int = 0, posY: int = 0, idRondPion: int = 0) -> None:
        if couleur is not None:
            self.rondPion = RondPion(numeroJoueur, couleur, idRondPion, posX, posY)
            return self.rondPion
        else:
            self.rondPion = None
    
    """
    Set an existing circular pawn on top of the square pawn.
    The function has the following parameter:
    - circularPawn : circular pawn to place on top of the square pawn.
    """
    def definirRondPion(self, rondPion: RondPion = None) -> None:
        self.rondPion = rondPion
