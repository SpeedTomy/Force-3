from Board import Board
from Player import Player
from Constants import BLACK_PAWN, WHITE_PAWN
from Node import Node
import math
import numpy as np
import random
import time

# Contains the main function of the programm


"""
This function runs the game by asking turn by turn what action a player wishes to do.
The function uses the following parameters:
- board: Board of the game
- player1: first player of the game
- player2: second player of the game.
- modeGame: 
    -1: Player VS Player
    -2: Player VS IA
    -3: IA VS IA
"""
def runGame(board: Board, player1: Player, player2: Player, modeGame: int = 0) -> None:
    # This function runs untill a player wins.
    #Player VS Player
    if(modeGame == 1):
        while(1):
            # Asks what the first player wants to do
            actionDone = False
            while(not actionDone):
                if(board.isMove2SquarePawnsPossible()):
                    actionDone = twoSquarePawnsPossiblePlayerChoices(player1, board)
                else: 
                    actionDone = twoSquarePawnsImpossiblePlayerChoices(player1, board)
            # check if a player has wone
            if(checkWinner(board) != -1):
                break
            
            # Asks what the second player wants to do
            actionDone = False
            while(not actionDone):
                if(board.isMove2SquarePawnsPossible()):
                    actionDone = twoSquarePawnsPossiblePlayerChoices(player2, board)
                else: 
                    actionDone = twoSquarePawnsImpossiblePlayerChoices(player2, board)
            # check if a player has wone
            if(checkWinner(board) != -1):
                break
    #Player VS Ia
    elif(modeGame == 2):
        while(1):
            # Asks what the first player wants to do
            actionDone = False
            while(not actionDone):
                if(board.isMove2SquarePawnsPossible()):
                    actionDone = twoSquarePawnsPossiblePlayerChoices(player1, board)
                else: 
                    actionDone = twoSquarePawnsImpossiblePlayerChoices(player1, board)
            # check if a player has wone
            if(checkWinner(board) != -1):
                break
            
            # Asks what the second player wants to do
            actionDone = False
            start = time.time()
            while(not actionDone):
                actionDone = IAChoices(player2, player1, board)

            # check if a player has wone
            if(checkWinner(board) != -1):
                break
    #IA VS IA
    else:
        while(1):
            # Asks what the first player wants to do
            actionDone = False
            while(not actionDone):
                actionDone = IAChoices(player1, player2, board)
            if(actionDone):
                print("tour de l'IA 1")
                board.printBoard()
            # check if a player has wone
            if(checkWinner(board) != -1):
                break
            
            # Asks what the IA wants to do
            actionDone = False
            while(not actionDone):
                actionDone = IAChoices(player2, player1, board)
            if(actionDone):
                print("tour de l'IA 2")
                board.printBoard()
            # check if a player has wone
            if(checkWinner(board) != -1):
                break

"""
This function is used when the player has 2 possible actions when they begin.
The function uses the following parameters:
- player: player who choices an action
- board: board of the game.
Returns true if the action of the player succeeded.
"""
def twoSquarePawnsImpossiblePlayerChoices(player: Player = None, board: Board = None) -> bool:
    action = 0
    allowedChoices = []
    board.printBoard()
    print("Player " + str(player.getPlayerNumber()+1) +", please choose an action between the following actions")

    if(len(player.pawns) < 3):
        print("- place a circular pawn on a square pawn (1);")
        allowedChoices.append("1");

    if(len(player.pawns) > 0):
        print("- move one of your circular pawns (2).")
        allowedChoices.append("2")

    print("- move a square pawn to an empty tile (3);")
    allowedChoices.append("3")

    print("You can place "+str(player.getNumberOfCircularPawnsAvailable()) + " pawns.")
    print("Type the number between ( ) to choose an action")
    while(action not in allowedChoices):
        action = input()
    print()

    return actionChoice(int(action), player, board)

"""
This function is used when the player has 4 possible actions during his turn.
The function uses the following parameters:
- player: plyaer who choices an action
- board: board of the game.
Returns true if the action of the player succeeded.
"""
def twoSquarePawnsPossiblePlayerChoices(player: Player = None, board: Board = None) -> bool:
    action = 0
    allowedChoices = []
    board.printBoard()
    print("Player " + str(player.getPlayerNumber()+1) +", please choose an action between the following actions")

    if(len(player.pawns) < 3):
        print("- place a circular pawn on a square pawn (1);")
        allowedChoices.append("1");

    if(len(player.pawns) > 0):
        print("- move one of your circular pawns (2).")
        allowedChoices.append("2")

    print("- move a square pawn to an empty tile (3);")
    allowedChoices.append("3")

    print("- move 2 square pawns (4).")
    allowedChoices.append("4")

    print("You can place "+str(player.getNumberOfCircularPawnsAvailable()) + " pawns.")
    print("Type the number between () to choose an action")
    while(action not in allowedChoices):
        action = input()
    print()

    return actionChoice(int(action), player, board)

"""
This function is used when the player has 4 possible actions during his turn.
The function uses the following parameters:
- player: IA who choices an action
- board: board of the game.
Returns true if the action of the player succeeded.
"""
def IAChoices(player: Player = None, opponent: Player = None, board: Board = None) -> bool:
    node = Node(3, player, opponent, board)
    v = MinMaxPL(node, node.depth, player, opponent)
    best_action = []
    for i in range(len(node.child)):
        if ((node.child[i].value == v) and (node.child[i].player.playerNumber != player.playerNumber) and (node.child[i].board.checkIfWinner() != opponent.playerNumber)):
            best_action.append(node.child[i])
        
        if (node.child[i].board.checkIfWinner() == 0 and node.child[i].board.checkIfWinner() == 1):
            best_action.append(node.child[i])

    if len(best_action) > 1:
        rand_child = random.choice(best_action)

    else:
        rand_child = best_action[0]
    #Place a pawn
    if rand_child.action.num_action == 1:
        if(board.placeCircularPawn(player.playerNumber, rand_child.action.x, rand_child.action.y) == 0):
            return True
    #Move a pawn
    if rand_child.action.num_action == 2:
        if rand_child.action.id_pawn == 1:
            if(board.moveCircularPawn(player.playerNumber, 1, rand_child.action.x, rand_child.action.y) == 0):
                return True
        elif rand_child.action.id_pawn == 2:
            if(board.moveCircularPawn(player.playerNumber, 2, rand_child.action.x, rand_child.action.y) == 0):
                return True
        elif rand_child.action.id_pawn == 3:
            if(board.moveCircularPawn(player.playerNumber, 3, rand_child.action.x, rand_child.action.y) == 0):
                return True
    #Move a square pawn
    if rand_child.action.num_action == 3:
        if(board.moveSquarePawn(rand_child.action.x, rand_child.action.y) == 0):
            return True
    #Move two square pawns
    if rand_child.action.num_action == 4:
        if(board.move2SquarePawns(rand_child.action.table_x, rand_child.action.table_y) == 0):
            return True

# Evaluates the positions of circular pawns         
def eval_position_pawn(player: Player = None):
    #Values of the tiles depending of their position
        position_pts= np.array([[2,1,2],[1,3,1],[2,1,2]])
        res = 0
        if(len(player.pawns) > 0):
            #two or more pawns
            if(len(player.pawns) - 1 > 0):
                for i in range(len(player.pawns)):
                    res += position_pts[player.pawns[i].x, player.pawns[i].y]
            #one pawn
            else:
                res += position_pts[player.pawns[0].x, player.pawns[0].y]
        return res

"""
This function send back +1 if the player have more pawns than his/her opponent, -1 if he/she has less, otherwise zero.
The function uses the following parameters:
- board: Board of the game.
- player: the player.
- other_player: the opponent.
"""     
def eval_nb_pawn(player: Player = None, other_player: Player = None, board: Board = None):
    nb_pawn_player = len(player.pawns)
    nb_pawn_opponent = len(other_player.pawns)
                        
    if(nb_pawn_player > nb_pawn_opponent):
        return 1
        
    elif(nb_pawn_player < nb_pawn_opponent):
        return -1
        
    else:
        return 0  


"""
This function send back +2 if the player places one of its pawn between two pawns from its opponent.
The function uses the following parameters:
- player: the player.
- board: Board of the game.
"""
def eval_pawn_between(player: Player = None, board: Board = None):
    res = 0
    for i in range(3):
    #if the player's pawn is between two opponent's pawns on the 3 first lines
        if (board._get_board_by_coordinate(1,i) != board.emptyTile and board._get_circularPawn_by_board(1,i) != None 
               and board._get_circularPawn_by_board(1,i).color == player.color and
               board._get_board_by_coordinate(0,i) != board.emptyTile  and board._get_circularPawn_by_board(0,i) != None 
               and board._get_circularPawn_by_board(0,i).color != player.color and
               board._get_board_by_coordinate(2,i) != board.emptyTile  and board._get_circularPawn_by_board(2,i) != None 
               and board._get_circularPawn_by_board(2,i).color != player.color):
                   res = 2
    #Same on the 3 first columns         
        if (board._get_board_by_coordinate(i,1) != board.emptyTile and board._get_circularPawn_by_board(i,1) != None 
               and board._get_circularPawn_by_board(i,1).color == player.color and
               board._get_board_by_coordinate(i,0) != board.emptyTile and board._get_circularPawn_by_board(i,0) != None 
               and board._get_circularPawn_by_board(i,0).color != player.color and
               board._get_board_by_coordinate(i,2) != board.emptyTile and board._get_circularPawn_by_board(i,2) != None 
               and board._get_circularPawn_by_board(i,2).color != player.color):
                   res = 2
    #Same on the left diagonal
    if (board._get_board_by_coordinate(1,1) != board.emptyTile and board._get_circularPawn_by_board(1,1) != None 
               and board._get_circularPawn_by_board(1,1).color == player.color and
               board._get_board_by_coordinate(0,0) != board.emptyTile and board._get_circularPawn_by_board(0,0) != None 
               and board._get_circularPawn_by_board(0,0).color != player.color and
               board._get_board_by_coordinate(2,2) != board.emptyTile and board._get_circularPawn_by_board(2,2) != None 
               and board._get_circularPawn_by_board(2,2).color != player.color):
                   res = 2

    #Same on the right diagonal
    if (board._get_board_by_coordinate(1,1) != board.emptyTile and board._get_circularPawn_by_board(1,1) != None 
               and board._get_circularPawn_by_board(1,1).color == player.color and
               board._get_board_by_coordinate(0,2) != board.emptyTile and board._get_circularPawn_by_board(0,2) != None 
               and board._get_circularPawn_by_board(0,2).color != player.color and
               board._get_board_by_coordinate(2,0) != board.emptyTile and board._get_circularPawn_by_board(2,0) != None 
               and board._get_circularPawn_by_board(2,0).color != player.color):
                   res = 2
    return res

"""
This function send back +2 if the player places one of its pawn between two pawns from its opponent.
The function uses the following parameters:
- player: the player.
- board: Board of the game.
"""
def eval_pawn_alignment(player: Player = None):
    res = 0

    if(len(player.pawns) >= 2):
        #If the pawn 1 and pawn 2 are on the same line or the same colum, return +1
        if(player.pawns[0].x == player.pawns[1].x or player.pawns[0].y == player.pawns[1].y):
            res = 1
        #Left diagonal with pawn 1 in [0][0] and pawn 2 somewhere in this diagonal
        if(player.pawns[0].x == 0 and player.pawns[0].y == 0):
            if(player.pawns[1].x == 1 and player.pawns[1].y == 1) or (player.pawns[1].x == 2 and player.pawns[1].y == 2):
                res = 1
        #Left diagonal with pawn 1 in [2][2] and pawn 2 somewhere in this diagonal
        elif(player.pawns[0].x == 2 and player.pawns[0].y == 2):
            if(player.pawns[1].x == 1 and player.pawns[1].y == 1) or (player.pawns[1].x == 0 and player.pawns[1].y == 0):
                res = 1
        #Right diagonal with pawn 1 in [0][2] and pawn 2 somewhere in this diagonal
        elif(player.pawns[0].x == 0 and player.pawns[0].y == 2):
            if(player.pawns[1].x == 1 and player.pawns[1].y == 1) or (player.pawns[1].x == 2 and player.pawns[1].y == 0):
                res = 1
        #Right diagonal with pawn 1 in [2][2] and pawn 2 somewhere in this diagonal
        elif(player.pawns[0].x == 2 and player.pawns[0].y == 0):
            if(player.pawns[1].x == 1 and player.pawns[1].y == 1) or (player.pawns[1].x == 0 and player.pawns[1].y == 2):
                res = 1
        #Any diagonal when the pawn 1 is in the middle [1][1]
        elif(player.pawns[0].x == 1 and player.pawns[0].y == 1):
            if(player.pawns[1].x == 0 and player.pawns[1].y == 0) or (player.pawns[1].x == 0 and player.pawns[1].y == 2) or (player.pawns[1].x == 2 and player.pawns[1].y == 0) or (player.pawns[1].x == 2 and player.pawns[1].y == 2):
                res = 1

    elif(len(player.pawns) == 3):
        #If pawns are on the same line or the same colum, return +1
        if((player.pawns[0].x == player.pawns[1].x or player.pawns[0].x == player.pawns[2].x or player.pawns[1].x == player.pawns[2].x) or 
        (player.pawns[0].y == player.pawns[1].y or player.pawns[0].y == player.pawns[2].y or player.pawns[1].y == player.pawns[2].y)):
            res = 1
        #Left diagonal with pawn 1 or 2 in [0][0] and pawn 3 somewhere in this diagonal
        if(player.pawns[0].x == 0 and player.pawns[0].y == 0) or (player.pawns[1].x == 0 and player.pawns[1].y == 0):
            if(player.pawns[2].x == 1 and player.pawns[2].y == 1) or (player.pawns[2].x == 2 and player.pawns[2].y == 2):
                res = 1
        #Left diagonal with pawn 1 or 2 in [2][2] and pawn 3 somewhere in this diagonal
        elif(player.pawns[0].x == 2 and player.pawns[0].y == 2) or (player.pawns[1].x == 2 and player.pawns[1].y == 2):
            if(player.pawns[2].x == 1 and player.pawns[2].y == 1) or (player.pawns[2].x == 0 and player.pawns[2].y == 0):
                res = 1
        #Right diagonal with pawn 1 or 2 in [0][2] and pawn 3 somewhere in this diagonal
        elif(player.pawns[0].x == 0 and player.pawns[0].y == 2) or (player.pawns[1].x == 0 and player.pawns[1].y == 2):
            if(player.pawns[2].x == 1 and player.pawns[2].y == 1) or (player.pawns[2].x == 2 and player.pawns[2].y == 0):
                res = 1
        #Right diagonal with pawn 1 or 2 in [2][2] and pawn 3 somewhere in this diagonal
        elif(player.pawns[0].x == 2 and player.pawns[0].y == 0) or (player.pawns[1].x == 2 and player.pawns[1].y == 0):
            if(player.pawns[2].x == 1 and player.pawns[2].y == 1) or (player.pawns[2].x == 0 and player.pawns[2].y == 2):
                res = 1
        #Any diagonal when the pawn 1 or 2 is in the middle [1][1]
        elif(player.pawns[0].x == 1 and player.pawns[0].y == 1) or (player.pawns[1].x == 1 and player.pawns[1].y == 1):
            if(player.pawns[2].x == 0 and player.pawns[2].y == 0) or (player.pawns[2].x == 0 and player.pawns[2].y == 2) or (player.pawns[2].x == 2 and player.pawns[2].y == 0) or (player.pawns[2].x == 2 and player.pawns[2].y == 2):
                res = 1

    return res

"""
This function sends back +1 if the player places one of its pawns next to two consecutive pawns of the opponent.
The function uses the following parameters:
- player: the player.
- board: Board of the game.
"""
def eval_opposition_edge_pawn(player: Player = None, board: Board = None):
    res = 0
       
    for i in range(3):
        #pawn player on the first column
        if (board._get_board_by_coordinate(0,i) != board.emptyTile and board._get_circularPawn_by_board(0,i) != None 
           and board._get_circularPawn_by_board(0,i).color == player.color and
               board._get_board_by_coordinate(1,i) != board.emptyTile and board._get_circularPawn_by_board(1,i) != None 
               and board._get_circularPawn_by_board(1,i).color != player.color and
               board._get_board_by_coordinate(2,i) != board.emptyTile and board._get_circularPawn_by_board(2,i) != None 
               and board._get_circularPawn_by_board(2,i).color != player.color):
                   res = 1
        #pawn player on the last column           
        if (board._get_board_by_coordinate(2,i) != board.emptyTile and board._get_circularPawn_by_board(2,i) != None 
               and board._get_circularPawn_by_board(2,i).color == player.color and
               board._get_board_by_coordinate(1,i) != board.emptyTile and board._get_circularPawn_by_board(1,i) != None 
               and board._get_circularPawn_by_board(1,i).color != player.color and
               board._get_board_by_coordinate(0,i) != board.emptyTile and board._get_circularPawn_by_board(0,i) != None 
               and board._get_circularPawn_by_board(0,i).color != player.color):
                   res = 1
        #pawn player on the first line    
        if (board._get_board_by_coordinate(i,0) != board.emptyTile  and board._get_circularPawn_by_board(i,0) != None 
               and board._get_circularPawn_by_board(i,0).color == player.color and
               board._get_board_by_coordinate(i,1) != board.emptyTile  and board._get_circularPawn_by_board(i,1) != None 
               and board._get_circularPawn_by_board(i,1).color != player.color and
               board._get_board_by_coordinate(i,2) != board.emptyTile  and board._get_circularPawn_by_board(i,2) != None 
               and board._get_circularPawn_by_board(i,2).color != player.color):
                   res = 1
        #pawn player on the last line           
        if (board._get_board_by_coordinate(i,2) != board.emptyTile and board._get_circularPawn_by_board(i,2) != None 
               and board._get_circularPawn_by_board(i,2).color == player.color and
               board._get_board_by_coordinate(i,1) != board.emptyTile and board._get_circularPawn_by_board(i,1) != None 
               and board._get_circularPawn_by_board(i,1).color != player.color and
               board._get_board_by_coordinate(i,0) != board.emptyTile and board._get_circularPawn_by_board(i,0) != None 
               and board._get_circularPawn_by_board(i,0).color != player.color):
                   res = 1
    return res

# Calculates the score of the players for a specific board state
def evaluation(player_max: Player = None, player_min: Player = None, board: Board = None):
        
        if(board.checkIfWinner() == player_max.playerNumber):
            return 500

        if(board.checkIfWinner() == player_min.playerNumber):
            return -500
        
        else:
            score = eval_position_pawn(player_max)
            score += eval_nb_pawn(player_max, player_min, board)
            score += eval_pawn_between(player_max, board)
            score += eval_opposition_edge_pawn(player_max, board)
            score += eval_pawn_alignment(player_max)
            return  score    
                
##======================================================================#
##=======================Function MinMax================================#
##======================================================================#      
# Calculates the max value         
def MaxValue(node, depth, player, other_player):
    if(node.board.checkIfWinner() != -1 or depth == 0 ):
        node.value = evaluation(player, other_player, node.board)
        return node.value
    node.value = -math.inf
    for i in range (len(node.child)):
        node.value = max(node.value, MinValue(node.child[i], depth-1, player, other_player))
         
    return node.value

# Calculates the min value
def MinValue(node, depth, player, other_player):
    if(node.board.checkIfWinner() != -1 or depth == 0 ):
        node.value = evaluation(player, other_player, node.board)
        return node.value
    node.value = math.inf
    for i in range (len(node.child)):
        node.value = min(node.value, MaxValue(node.child[i], depth-1, player, other_player))
        
    return node.value
                 
def MinMaxPL(node, depth, player, other_player):
    node.value = MaxValue(node, depth, player, other_player)
    return node.value 

##======================================================================#
##=======================Fonction MinMax utilisant alpha_beta===========#
##============================Fonction non retenue======================#
"""
def MaxValue(node, depth, player, other_player, alpha, beta):
    
    if(node.board.checkIfWinner() != -1 or depth == 0 ):
        node.value = evaluation(player, other_player, node.board)
        return node.value
    node.value = -math.inf
    for i in range (len(node.child)):
         
        node.value = max(node.value, MinValue(node.child[i], depth-1, player, other_player, alpha, beta))
       
        if node.value >= beta:
            return node.value
        alpha = max(alpha, node.value)
        
    return node.value

def MinValue(node, depth, player, other_player, alpha, beta):
    
    if(node.board.checkIfWinner() != -1 or depth == 0 ):  
        node.value = evaluation(player, other_player, node.board)
        return node.value
    node.value = math.inf
    for i in range (len(node.child)):
        
        node.value = min(node.value, MaxValue(node.child[i], depth-1, player, other_player, alpha, beta))
        
        if node.value <= alpha:
            return node.value
        beta = min(beta, node.value)
    return node.value
                
        
def MinMaxPL(node, depth, player, other_player):
    node.value = MaxValue(node,depth, player, other_player, -math.inf, math.inf)
    return node.value 
"""

"""
This function calls one of the possible actions of the player.
The function uses the following parameters: 
- action: number of the action to execute, action = 1, 2, 3 or 4
- player: number of the player who is going to do the action, player = 0 or 1
- board: board of the game
Returns true if the action succeeded.
"""
def actionChoice(action: int, player: Player, board: Board) -> bool:     
    if(action == 1): 
        return placeCircularPawn(player.getPlayerNumber(), board)
    elif(action == 2):
        return moveCircularPawn(player, board)
    elif(action == 3):
        return moveSquarePawn(board)
    elif(action == 4):
        return move2SquarePawns(board)


"""
placeCircularPawn corresponds to the following action : place a circular pawn onto the board
This function asks the player where to place a new cicurlar pawn then places it onto the board.
The function uses the following parameters:
- player: number of the player who is placing the circular pawn, player = 0 or 1
- board: board of the game.
Returns True if the action succeeded.
"""
def placeCircularPawn(player: int, board: Board) -> bool:
        x = 0
        y = 0
        xNumbersPossible = ["0", "1", "2"]
        yNumbersPossible = ["0", "1", "2"]
        print("On which tile would you like to place a circular pawn ?")
        print("line :")

        while(x not in xNumbersPossible):
            x = input()

        print("column :")

        while(y not in yNumbersPossible):
            y = input()
        actionSuccess = board.placeCircularPawn(player, int(x), int(y))

        if(actionSuccess == -1):
            print("\nYou don't have any circular pawns left!\n")
            return False
        elif(actionSuccess == -2):
            print("\nYou can't place a circular pawn there!\n")
            return False
        else:
            print("\nSuccess!\n")
            return True



"""
moveCircularPawn corresponds to the following action : move a placed circular pawn onto a free square pawn
This function asks the player which circular pawn he would like to move and where he would like to move it.
Afterwards, the function moves the circular pawn.
The function uses the following parameters:
- player: number of the player who is moving a circular pawn, player = 0 or 1
- board: board of the game.
Returns True if the action succeeded.
"""
def moveCircularPawn(player: Player, board: Board) -> bool:
        circularPawnIdPossible = []
        idPawn = 0
        x = 0
        y = 0
        if((len(player.pawns) - 1) != 0):
            for i in range(len(player.pawns)):
                circularPawnIdPossible.append(str(i + 1))
        else:
            circularPawnIdPossible = ["1"]

        xNumbersPossible = ["0", "1", "2"]
        yNumbersPossible = ["0", "1", "2"]

        print("Which one of your circular pawns would you like to move ?")
        print("Select the number of your circular pawn: 1, 2 or 3.")

        while(idPawn not in circularPawnIdPossible):
            idPawn = input()

        print("\nWhere would you like to move this pawn ?")
        print("Select a tile for the new location of the pawn (it can't be the current tile of the pawn)")

        print("line:")
        while(x not in xNumbersPossible):
            x = input()

        print("column:")
        while(y not in yNumbersPossible):
            y = input()

        actionSuccess = board.moveCircularPawn(player.getPlayerNumber(), int(idPawn), int(x), int(y))

        if(actionSuccess == -1):
            print("\nYou can't move your circular pawn onto the coordinate ["+ x + "]["+ y + "] !\n")
            return False
        else:
            print("\nSuccess!\n")
            return True

"""
move2SquarePawns corresponds to the following action : 
move 2 square pawns if the empty tile isn't in the middle, this action can't be used to reverse 
the positions of the 2 square pawns moved by the previous player on their last turn.
This function asks the player which 2 square pawn he would like to move and then moves them.
The function uses the following parameter:
- board: board of the game.
Returns True if the action succeeded.
"""
def move2SquarePawns(board: Board) -> bool:
        x = [0,0]
        y = [0,0]
        xNumbersPossible = ["0", "1", "2"]
        yNumbersPossible = ["0", "1", "2"]
        print("Which square pawn would you like to move first ?")
        
        print("line :")
        while(x[0] not in xNumbersPossible):
            x[0] = input()

        print("column :")
        while(y[0] not in yNumbersPossible):
            y[0] = input()
    

        print("\nWhat is the second square pawn that you would like to move?")
        print("Select a tile to choose the square pawn")

        print("line :")
        while(x[1] not in xNumbersPossible):
            x[1] = input()

        print("column :")
        while(y[1] not in yNumbersPossible):
            y[1] = input()

        actionSuccess = board.move2SquarePawns(x, y)

        if(actionSuccess == -1):
            print("\nYou aren't allowed to do move square pawns!\n")
            return False
        elif(actionSuccess == -2):
            print("\nYou aren't allowed to reverse the 2 movements you opponent did on their previous turn!\n")
            return False
        elif(actionSuccess == -3):
            print("\nThe first tile you chose can't move!\n")
            return False
        elif(actionSuccess == -4):
            print("\nYour two tiles are not align with each other!\n")
            return False
        elif(actionSuccess == -5):
            print("\nYou can't move this two tiles like this!\n")
            return False
        else:
            print("\nSuccess!\n")
            return True

"""
moveSquarePawn corresponds to the following action : move a square pawn onto the the empty tile.
the positions of the 2 square pawns moved by the previous player on their last turn.
This function asks the player which square pawn he would like to move and then moves it.
The function uses the following parameter:
- board: board of the game.
Returns True if the action succeeded.
"""
def moveSquarePawn(board: Board) -> bool:
        x = 0
        y = 0
        xNumbersPossible = ["0", "1", "2"]
        yNumbersPossible = ["0", "1", "2"]

        print("To move a square pawn, select a tile that contains a square pawn and that is next to the empty tile")
        print("line :")
        while(x not in xNumbersPossible):
            x = input()

        print("column :")
        while(y not in xNumbersPossible):
            y = input()

        actionSuccess = board.moveSquarePawn(int(x), int(y))

        if(actionSuccess == -1):
            print("\nYou aren't allowed to reverse the movement your opponent did on their previous turn!\n")
            return False
        elif(actionSuccess == -2):
            print("\nYou can't move this tile!\n")
            return False
        else: 
            print("\nSuccess!")
            return True


# returns true if a player has wone
def checkWinner(board) -> int: 
    winner = board.checkIfWinner()
    if(winner == 0):
        print("\nPlayer 1 is the winner!")
        board.printBoard()
        return 0
    elif(winner == 1):
        board.printBoard()
        print("\nPlayer 2 is the winner!")
        return 1
    else:
        return -1

