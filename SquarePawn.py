from CircularPawn import CircularPawn
from Constants import WHITE_PAWN

"""
The class SquarePawn represents the square pawns that can
be placed on top of tiles.
"""

class SquarePawn:
    # Instanciate a square pawn
    def __init__(self) -> None:
        self.circularPawn = None

    # Checks if the square pawn has a circular pawn 
    def isCircularPawnSet(self) -> bool:
        return self.circularPawn is not None

    # returns the circular pawn placed on the square pawn
    def getCircularPawn(self) -> CircularPawn:
        return self.circularPawn

    """
    Set a new circular pawn on the square pawn.
    The functions uses the following parameters: 
    - playerNumber: number of the player who owns the circular pawn, playerNumber = 0 or 1
    - color: color of the new circular pawn 
    """
    def setNewCircularPawn(self,  playerNumber: int = 0, color: bool = WHITE_PAWN, x: int = 0, y: int = 0, idCircularPawn: int =0) -> None:
        if(color is not None):
            self.circularPawn = CircularPawn(playerNumber, color, idCircularPawn, x, y)
            return self.circularPawn
        else:
            self.circularPawn = None
    
    """
    Set an existing circular pawn on top of the square pawn.
    The function has the following parameter:
    - circularPawn : circular pawn to place on top of the square pawn.
    """
    def setCircularPawn(self, circularPawn: CircularPawn = None) -> None:
        self.circularPawn = circularPawn
