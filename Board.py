from Constants import WHITE_PAWN
from Tile import Tile
from Player import Player
import numpy as np
import copy

class Board:
    """ 
    Instanciate a board with the following parameters:
     - player1: first player
     - player2: second player.
    The function creates a board with 9 tiles and 8 square pawns placed 
    on top of every tile except the middle one.
    """
    def __init__(self, player1: Player, player2: Player) -> None:
        # Creation of the board
        self.board = np.empty([3, 3], dtype=Tile)
        k = 1           

        for i in range(3):
            for j in range(3):
                if(i == 1 and j == 1):
                    self.board[i][j] = Tile(i, j, False, k)
                    k = k + 1
                else:
                    self.board[i][j] = Tile(i, j, True, k)
                    k = k + 1
                    
        # Variable to keep track of where the empty tile is
        self.emptyTile = self.board[1][1]
        # Liste to store the players of the game
        self.players = [player1, player2]
        # variable that stores the number of the player if he wins
        self.winner = None

        """ 
        Variable that stores the reverse movement done by the function if the function moveSquarePawn() succeeds
        This variable is used to check if a player tries to reverse the movement done by moveSquarePawn() on the previous turn
        """
        self.squarePawnMoved = None
        """ 
        Variable that stores the reverse movement done by the function if the function move2SquarePawns() succeeds
        This variable is used to check if a player tries to reverse the movement done by move2SquarePawns() on the previous turn
        """
        self.twoSquarePawnsMoved = None

    """
    This function returns the empty tile.
    """
    def get_EmptyTile(self) -> Tile:
        return self.emptyTile

    """
    This function places a circular pawn on top of a square pawn.
    The function uses the following parameters: 
    - playerNumber: number of the player who is placing the circular pawn, playerNumber = 0 or 1
    - tile: number of tile where the circular pawn is placed, tile = a number between 0 and 8
    The function returns:
    - 0 if the circular pawn was placed on the board
    - -1 if the player doesn't have any circular pawns left
    - -2 if a circular pawn can't be placed on the choses tile.
    """
    def placeCircularPawn(self, playerNumber: int = 0, x: int = 0, y: int = 0) -> int:
        player = self.players[playerNumber]
        tile = self.board[x][y]

        if(player.isCircularPawnAvailable()):
            if(tile.isSquarePawnSet() and not tile.isCircularPawnSet()):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = None
                idCircularPawn = len(player.pawns) + 1;
                newCircularPawn = tile.setNewCircularPawn(playerNumber, player.color, x, y, idCircularPawn)
                player.pawns.append(newCircularPawn)
                return 0
            return -2
        return -1
    
    """
    This function moves a placed circular pawn to a new tile.
    The function uses the folling parameters: 
    - playerNumber: number of the player who is moving a circular pawn, playerNumber = 0 or 1
    - previousTile: number of the tile where the circular pawn the player wants to move is, previousTile = a number between 0 and 8
    - newtTile: number of the tile where the player wants to move his circular pawn, nextTile = a number between 0 and 8.
    The function returns:
    - 0 if the circular pawn is correctly moved
    - -1 if previousTile doesn't correspond to a tile that contains a circular pawn of the player.
    - -2 if nextTile corresponds to a tile that doensn't have a square pawn or already has a circular pawn placed on top of it.
    """
    def moveCircularPawn(self, playerNumber: int = 0, idPawn: int = 0, nextX: int = 0, nextY: int = 0) -> int:
        pawn = self.players[playerNumber].pawns[idPawn - 1]
        previousTile = self.board[pawn.x][pawn.y]
        nextTile = self.board[nextX][nextY]
        
        if(not nextTile.isSquarePawnSet() or nextTile.isCircularPawnSet()):
            return -1
        
        self.twoSquarePawnsMoved = None
        self.squarePawnMoved = None

        circularPawn = previousTile.getCircularPawn()
        previousTile.setCircularPawn(None)
        nextTile.setCircularPawn(circularPawn)

        # Update the pawn’s coordinates so the GUI recognizes the new position:
        pawn.x = nextX
        pawn.y = nextY

        return 0

    """
    This function moves a square pawn to an empty tile.
    The function uses the following paramater:
    - tileNumber, number of the tile that contains the square pawn we would like to move, tilNumber = a number between 0 and 8
    The function returns true if the square pawn was succesfully moved.
    """
    def moveSquarePawn(self, x: int = 0, y: int = 0, twoSquare: bool = False) -> int:
        tile = self.board[x][y]

        #can't reverse opponent's movement
        if([self.emptyTile, tile] == self.squarePawnMoved and twoSquare == False):
            return -1

        if(self.emptyTile.idTile == 1):
            if(self.board[x][y].idTile in {2, 4}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 2):
            if(self.board[x][y].idTile in {1, 3, 5}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 3):
            if(self.board[x][y].idTile in {2, 6}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 4):
            if(self.board[x][y].idTile in {1, 5, 7}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 5):
            if(self.board[x][y].idTile in {2, 4, 6, 8}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 6):
            if(self.board[x][y].idTile in {3, 5, 9}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 7):
            if(self.board[x][y].idTile in {4, 8}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 8):
            if(self.board[x][y].idTile in {5, 7, 9}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 9):
            if(self.board[x][y].idTile in {6, 8}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                circularPawn = tile.getCircularPawn() if tile.isCircularPawnSet() else None
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                if circularPawn:
                    self.emptyTile.setCircularPawn(circularPawn)
                    circularPawn.x, circularPawn.y = self.emptyTile.x, self.emptyTile.y
                self.emptyTile = tile
                return 0
            else:
                return -2
        elif(self.emptyTile.idTile == 10):  # Ajout de la condition pour la position (0, 1)
            if(self.board[x][y].idTile in {1, 2, 3, 5}):
                self.twoSquarePawnsMoved = None
                self.squarePawnMoved = [tile, self.emptyTile]
                squarePawn = tile.getSquarePawn()
                tile.setSquarePawn(None)
                self.emptyTile.setSquarePawn(squarePawn)
                self.emptyTile = tile
                return 0
            else:
                return -2

    # returns true if the player can move 2 square pawns on his turn
    def isMove2SquarePawnsPossible(self) -> bool:
        return self.emptyTile.idTile != 5
    """
    This function moves 2 square pawns.
    The function uses the following parameters:
    - firstTile: number of the tile containg the square pawn that we would like to move first, firstTile = a number between 0 and 8
    - secondTile: number of the tile containg the square pawn that we would like to move after the first square pawn, secondTile = a number between 0 and 8.
    The function returns: 
    - 0 if the 2 square pawns were successfully moved
    - -1 if the player can't move 2 square pawns on his turn
    - -2 if the player tried to reverse the positions of the 2 square pawns moved by the previous player on their last turn
    - -3 if the first selected square pawn can't be moved to the empty tile
    - -4 if the second selected square pawn can't be moved to the position of the first tile.
    """
    def move2SquarePawns(self, x: list = [0, 0], y: list = [0, 0]) -> int:
        copy_board = copy.deepcopy(self)
        firstTile = self.board[int(x[0]), int(y[0])]
        secondTile = self.board[int(x[1]), int(y[1])]

        if(not self.isMove2SquarePawnsPossible()):
            return -1

        if([firstTile, secondTile] == self.twoSquarePawnsMoved):
            return -2

        if(copy_board.moveSquarePawn(int(x[0]), int(y[0]), True) != 0):
            return -3

        if(copy_board.moveSquarePawn(secondTile.x, secondTile.y, True) != 0):
            return -4

        if(not((secondTile.x == firstTile.x and secondTile.x == self.emptyTile.x) or
            (secondTile.y == firstTile.y and secondTile.y == self.emptyTile.y))):
            return -5

        firstSquarePawn = firstTile.getSquarePawn()
        secondSquarePawn = secondTile.getSquarePawn()
        firstTile.setSquarePawn(secondSquarePawn)
        secondTile.setSquarePawn(None)
        self.emptyTile.setSquarePawn(firstSquarePawn)
        self.twoSquarePawnsMoved = [firstTile, self.emptyTile]
        self.emptyTile = secondTile
        self.squarePawnMoved = None

    # this functions prints the board on the consol used to run the programm 
    def printBoard(self) -> None:
        newLine = 0
        displayBoard = ""

        print("======================")
        print("■ = empty tile")
        print("▢ = empty square pawn")
        print("O = white circular pawn")
        print(". = black circular pawn\n")

        for i in range(4):
            for j in range(4):
                if(i == 0 and j == 0):
                    displayBoard += "   "
                elif(i == 0):
                    displayBoard += str(j - 1) + "  "
                elif(j == 0):
                    displayBoard += str(i - 1) + "  "
                elif(not self.board[i-1][j-1].isSquarePawnSet()):
                    displayBoard += "■  "
                elif(not self.board[i-1][j-1].isCircularPawnSet()):
                    displayBoard += "▢  "
                elif(self.board[i-1][j-1].getCircularPawn().getColor() == WHITE_PAWN):
                    displayBoard += "O" + str(self.board[i-1][j-1].getCircularPawn().id) + " "
                else: 
                    displayBoard += "." + str(self.board[i-1][j-1].getCircularPawn().id) + " "

                newLine += 1
                if(newLine%4 == 0):
                    displayBoard += "\n"
        
        print(displayBoard)
        print("======================\n")
    
    # returns the number of a player (0 or 1) if they've won, returns -1 otherwise.
    def checkIfWinner(self) -> int:
        circularPawns = [[], []]
        victoryConditions = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5 ,9],
            [3, 5, 7]
        ]
        for i in range(3):
            for j in range(3):
                tile = self.board[i][j]
                if(tile.isCircularPawnSet()):
                    pawn = tile.getCircularPawn()
                    circularPawns[pawn.getPlayerNumber()].append(tile.getIdTile())

        if(circularPawns[0] in victoryConditions):
            return 0
        elif(circularPawns[1] in victoryConditions):
            return 1
        else: 
            return -1

    def _get_two_square_pawn_moved(self):
        return self.twoSquarePawnsMoved

    def _get_square_pawn_moved(self):
        return self.squarePawnMoved

    def _get_board_by_coordinate(self, x: int = None, y: int = None):
        return self.board[x,y]

    def _get_circularPawn_by_board(self, x, y):
        if self.board[x, y] is not None and self.board[x, y].squarePawn is not None:
            return self.board[x, y].squarePawn.circularPawn
        return None

    def getValidCircularMoves(self, x: int, y: int):
        valid_moves = []
        # Example logic: a valid tile must have a square pawn & no circular pawn
        for i in range(3):
            for j in range(3):
                tile = self.board[i][j]
                if tile.isSquarePawnSet() and not tile.isCircularPawnSet() and not (i == x and j == y):
                    valid_moves.append((i, j))
        return valid_moves

    def getValidSquareMoves(self, x: int, y: int):
        valid_moves = []
        if not self.board[x][y].isSquarePawnSet():
            return valid_moves
        import copy
        tempBoard = copy.deepcopy(self)
        if tempBoard.moveSquarePawn(x, y) == 0:
            valid_moves.append((tempBoard.emptyTile.x, tempBoard.emptyTile.y))
        return valid_moves

    def getAllMovableSquares(self) -> list:
        squares = []
        for i in range(3):
            for j in range(3):
                tile = self.board[i][j]
                if tile.isSquarePawnSet():
                    tempBoard = copy.deepcopy(self)
                    if tempBoard.moveSquarePawn(i, j) == 0:
                        squares.append((i, j))
        return squares

# Méthode pour obtenir l'état actuel du plateau
    def get_board_state(self):
        state = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = self.board[i][j]
                if not tile.isSquarePawnSet():
                    row.append("empty")
                elif tile.isCircularPawnSet():                   
                    pawn = tile.getCircularPawn()
                    if pawn.color:
                        row.append("white")
                    else:
                        row.append("black")              
                else:
                    row.append("square")
            state.append(row)
        return state