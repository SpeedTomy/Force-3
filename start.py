from Main import runGame
from Player import Player
from Board import Board
from Constants import BLACK_PAWN, WHITE_PAWN

# Launches the game
def start():
    decisionPlayer = 0
    decisionPossibilities = ["1", "2", "3"]
    print("What mode of game do you want ?")
    print("-(1): Player VS Player\n-(2): Player VS IA\n-(3): IA VS IA")
    while decisionPlayer not in decisionPossibilities:
        decisionPlayer = input()

    if(int(decisionPlayer) == 1):
        player_vs_player(int(decisionPlayer))
    elif(int(decisionPlayer) == 2):
        player_vs_ia(int(decisionPlayer))
    else:
        ia_vs_ia(int(decisionPlayer))

# This function is used to create 2 human players for the game
def player_vs_player(decisionPlayer) -> None:
    playerColor = None
    player1 = None
    player2 = None

    # Asks what color the first player wants
    while(playerColor != "1" and playerColor != "2"):
        playerColor = input("Player 1 is white (1) or black (2)? (Type 1 or 2)\n")
        print()

    # Creates the players
    if(playerColor == "1"):
        player1 = Player(0, WHITE_PAWN)
        player2 = Player(1, BLACK_PAWN)
        print("Player 1 is white\nPlayer 2 is black\n")
    else: 
        player1 = Player(0, BLACK_PAWN)
        player2 = Player(1, WHITE_PAWN)
        print("Player 1 is black\nPlayer 2 is white\n")

    runGame(Board(player1, player2), player1, player2, decisionPlayer)

# This function is used to create a human player and a computer player for the game
def player_vs_ia(decisionPlayer) -> None:
    playerColor = None
    player1 = None
    player2 = None

    # Asks what color the first player wants
    while(playerColor != "1" and playerColor != "2"):
        playerColor = input("Player 1 (you) is white (1) or black (2)? (Type 1 or 2)\n")
        print()

    # Creates the players
    if(playerColor == "1"):
        player1 = Player(0, WHITE_PAWN)
        player2 = Player(1, BLACK_PAWN)
        print("Player 1 is white\nPlayer 2 is black\n")
    else: 
        player1 = Player(0, BLACK_PAWN)
        player2 = Player(1, WHITE_PAWN)
        print("Player 1 is black\nPlayer 2 is white\n")
    # runs the game
    runGame(Board(player1, player2), player1, player2, decisionPlayer)

# This function is used to create 2 computer players for the game
def ia_vs_ia(decisionPlayer) -> None:
    player1 = Player(0, WHITE_PAWN)
    player2 = Player(1, BLACK_PAWN)
    print("Player 1 is white\nPlayer 2 is black\n")

    runGame(Board(player1, player2), player1, player2, decisionPlayer)

# Call the function that launches the game
start()
