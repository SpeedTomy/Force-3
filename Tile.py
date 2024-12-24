from SquarePawn import SquarePawn
from CircularPawn import CircularPawn
from Constants import WHITE_PAWN

# The Tile class represents the tiles of the board.

class Tile:
    """ 
    Instanciate a tile with the following parameters:
     - SquarePawnSet: if true, creates a new empty square pawn
     -x, y: horizontal and vertical coordonny (previous ...: the square pawn is instanfied)
     - idTile: number of the tile, idTile = a number between 1 and 9 
    """
    def __init__(self, x, y, squarePawnSet: bool = False, idTile: int = 0) -> None:
        if(squarePawnSet):
            self.squarePawn = SquarePawn()
        else:
            self.squarePawn = None
        self.x = x
        self.y = y
        self.idTile = idTile

    # set a squarePawn on the tile or remove the current one (with None)
    def setSquarePawn(self, squarePawn: SquarePawn = None) -> None:
        self.squarePawn = squarePawn

    # returns the squarePawn of the tile
    def getSquarePawn(self) -> SquarePawn:
        return self.squarePawn

    # Checks if the tile has a square pawn
    def isSquarePawnSet(self) -> bool:
        return self.squarePawn is not None

    # returns the circular pawn of the tile if it exists
    def getCircularPawn(self) -> CircularPawn:
        if(self.isCircularPawnSet()):
            return self.squarePawn.getCircularPawn()

        return None
    
    """
    Set a new circular pawn on the tile if it contains a square pawn.
    The functions uses the following parameters: 
    - playerNumber: number of the player who owns the circular pawn, playerNumber = 0 or 1
    - color: color of the new circular pawn 
    """
    def setNewCircularPawn(self, playerNumber: int = 0, color: bool = WHITE_PAWN, x: int = 0, y: int = 0, idCircularPawn: int = 0) -> CircularPawn:
        if(self.isSquarePawnSet()):
            return self.squarePawn.setNewCircularPawn(playerNumber, color, x, y, idCircularPawn)

    """
    Set an existing circular pawn on top of tile if it contains a square pawn.
    The function has the following parameter:
    - circularPawn : circular pawn to place on top of the square pawn.
    """
    def setCircularPawn(self, circularPawn: CircularPawn = None) -> None:
        if(self.isSquarePawnSet()):
            self.squarePawn.setCircularPawn(circularPawn)

    # checks if circular pawn exists
    def isCircularPawnSet(self) -> bool:
        if(self.isSquarePawnSet()):
            return self.squarePawn.isCircularPawnSet()

        return False

    # returns the horizontal coordinate
    def _get_x(self):
        return self._x
    # sets the horizontal coordinate
    def _set_x(self, new_x):
        self._x = new_x
    
    # returns the vertical coordinate    
    def _get_y(self):
        return self._y
    # sets the vertical coordinate
    def _set_y(self, new_y):
        self._y = new_y

    # returns the tile number
    def getIdTile(self) -> int:
        return self.idTile


