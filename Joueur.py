from Constantes import PION_BLANC

# The class Joueur represents a player of the game.

class Joueur:
    """ 
    Instanciate a player with the following parameters:
     - numeroJoueur: number of the player, numeroJoueur = 0 or 1
     - couleur: color of the player (white or black)
     - pions: table of the player's pawn on the board
    """
    def __init__(self, numeroJoueur: int = 0, couleur: bool = PION_BLANC) -> None:
        self.numeroJoueur = numeroJoueur
        self.couleur = couleur
        self.pions = []

    # returns true if the player has a circular pawn available
    def estRondPionDisponible(self) -> bool:
        return len(self.pions) < 3
    
    """
    This function represents the action of placing a circular pawn.
    The function reduces the amout of circular pawns the player has and returns 
    the color of the circular pawn.
    """
    def placerRondPion(self) -> bool: 
        return self.couleur
    
    # returns the number of circular pawns the player hasn't placed on the board
    def obtenirNombreRondPionsDisponibles(self) -> int:
        return 3 - len(self.pions)

    # returns the player number
    def obtenirNumeroJoueur(self) -> int:
        return self.numeroJoueur