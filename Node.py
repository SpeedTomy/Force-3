from Board import Board
from Player import Player
from EdgeAction import EdgeAction
import copy;

# Node is the class that creates the tree of possibilities for the AI
class Node():
    """ 
    Instanciate a tree of possibilities, based on the current game and with a chosen depth.
    The following parameters:
     - depth: the depth of the tree
     - player: the current player
     -other_player: the opponent
     -board: the board of the current game
     -action_played: to save the action played
     -value: value of the current node
    """
    def __init__(self, depth, player, other_player, board, action_played = None, value = None):
        self.depth = depth 
        self.player = player
        self.other_player = other_player
        self.action = action_played
        self.value = value
        self.child = []
        self.board = board
        #We created copies to prevent error
        self.copy_board = copy.deepcopy(self.board)
        self.copy_player = copy.deepcopy(self.player)
        self.copy_other_player = copy.deepcopy(self.other_player)
        self.createChild()
        
    """
    This function creates all the possible actions from the current node (if this node doesn't correspond at the
    victory of one of the players.
    The function returns the possible actions with a table of number between 1 and 4 if the action is allowed.
    - 1: to place a pawn
    - 2: to move a pawn
    - 3: to move a square pawn
    - 4: to move two square pawns
    """      
    def actions_possible(self):
        res_actions = []
        if (self.board.checkIfWinner() != 0 or self.board.checkIfWinner() != 1):
            if(len(self.player.pawns) == 0):
                res_actions = [1, 3]
            
            elif(len(self.player.pawns) > 0 and len(self.player.pawns) < 3):
                res_actions = [1, 2, 3]
            
            elif(len(self.player.pawns) == 3):
                res_actions = [2, 3]
            
            if (self.board.emptyTile.x != 1 and self.board.emptyTile.y != 1):
                res_actions.append(4)
            
        return res_actions

    """
    This function creates every possible child of a node.
    """      
    def createChild(self):   
        actions_possible = self.actions_possible()
        if self.depth > 0 and len(actions_possible) != 0:

            for i in range(len(actions_possible)):
                action = actions_possible[i]
                #Place a pawn
                if action == 1:
                    for x in range(3):
                        for y in range(3):
                            self.copy_board = copy.deepcopy(self.board)
                            self.copy_player = copy.deepcopy(self.player)
                            self.copy_other_player = copy.deepcopy(self.other_player)
                            
                            if (self.copy_board._get_board_by_coordinate(x,y) != self.copy_board.emptyTile and self.copy_board._get_circularPawn_by_board(x,y) == None):   
                                if(self.copy_board.placeCircularPawn(self.copy_player.playerNumber, int(x), int(y)) == 0):
                                    action = EdgeAction(1, x, y)
                                    self.child.append(Node(self.depth-1, self.copy_other_player, self.copy_player, self.copy_board, action))
                #Move a circular pawn                
                if action == 2:
                    for pawn in self.copy_player.pawns:
                        for x in range(3):
                            for y in range(3):
                                self.copy_board = copy.deepcopy(self.board)
                                self.copy_player = copy.deepcopy(self.player)
                                self.copy_other_player = copy.deepcopy(self.other_player)
                                    
                                if ((x,y) != (self.board.emptyTile.x, self.board.emptyTile.y) and
                                    self.board._get_circularPawn_by_board(x,y) == None):
                                    if(self.copy_board.moveCircularPawn(self.copy_player.playerNumber, pawn.id, x, y) == 0):
                                        action = EdgeAction(2, x, y, pawn.id)
                                        self.child.append(Node(self.depth-1, self.copy_other_player, self.copy_player, self.copy_board, action))
                #Move a square pawn
                if action == 3:
                    for x in range(3):
                        for y in range(3):
                            self.copy_board = copy.deepcopy(self.board)
                            self.copy_player = copy.deepcopy(self.player)
                            self.copy_other_player = copy.deepcopy(self.other_player)
                            
                            if ((x,y) != (self.copy_board.emptyTile.x, self.copy_board.emptyTile.y)):
                                if(self.copy_board.moveSquarePawn(x, y) == 0):
                                    action = EdgeAction(3, x, y)
                                    self.child.append(Node(self.depth-1, self.copy_other_player, self.copy_player, self.copy_board, action))           
                
                #Move two square pawns
                if action == 4:
                    for x in range(3):
                        for y in range(3):
                            for i in range(3):
                                for j in range(3):

                                    self.copy_board = copy.deepcopy(self.board)
                                    self.copy_player = copy.deepcopy(self.player)
                                    self.copy_other_player = copy.deepcopy(self.other_player)
                            
                                    if(self.copy_board.emptyTile.x == 1 and self.copy_board.emptyTile.y == 1):
                                        table_x.append(x)
                                        table_x.append(i)
                                        table_y.append(y)
                                        table_y.append(j)
                                        if(self.copy_board.move2SquarePawns(table_x, table_y) == 0):
                                            action = EdgeAction(4, x, y, None, table_x, table_y)
                                            self.child.append(Node(self.depth-1, self.copy_other_player, self.copy_player, self.copy_board, action))

    """
    This function permits to display a father node and its childs.
    We used this function to see and be able to understand how the IA was thinking.
    """    
    def display(self): #permet d'afficher un noeud père et ses enfants
        print("father")
        self.board.printBoard()
        print("child")
        for i in range(len(self.child)):
            self.child[i].board.printBoard()