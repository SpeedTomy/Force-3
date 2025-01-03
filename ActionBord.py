# The class ActionBord memorises a possible action of a player
class ActionBord:
    """ 
    Instanciate the edge of the tree with the following parameters:
     - num_action: to save the action played(place/move a pawn, move a square pawn or move two square pawns)
     - posX, posY: memorise the coordinates of the action
     - id_pion: memorise the id of the pawn (for move a pawn for exemple)
    The function creates a board with 9 tiles and 8 square pawns placed 
    on top of every tile except the middle one.
    """
    def __init__(self, num_action, posX: int = None, posY: int = None, id_pion: int = None, table_posX: list = None, table_posY: list = None):
        self.num_action = num_action
        self.posX = posX                     
        self.posY = posY
        self.id_pion = id_pion
        self.table_posX = table_posX
        self.table_posY = table_posY

    
    # returns the number of the action
    def obtenir_num_action(self):
        return self.num_action
    
    # returns the x coordinate of the action
    def obtenir_posX(self):
        return self.posX
    
    # returns the y coordinate of the action
    def obtenir_posY(self):
        return self.posY
      
    # returns the id of the pawn used for the action
    def obtenir_id_pion(self):
        return self.id_pion