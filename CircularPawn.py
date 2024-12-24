from Constants import WHITE_PAWN
"""
The class CircularPawn represents the circular pawns that can
be placed on top of a square pawn.
"""

class CircularPawn:
    """ 
    Instanciate a circular pawn with the following parameters:
     - playerNumber: number of the player who owns the pawn, playerNumber = 0 or 1
     - color: color of the circular pawn
    """
    def __init__(self, playerNumber: int = 0, color: bool = WHITE_PAWN, id: int = 0, x: int=0, y: int=0) -> None:
        self.playerNumber = playerNumber
        self.color = color
        self.id = id
        self.x = x
        self.y = y

    # returns the color of the pawn
    def getColor(self) -> bool:
        return self.color
    
    # returns the number of the player who owns the pawn
    def getPlayerNumber(self) -> int:
        return self.playerNumber
