# The class EdgeAction memorises a possible action of a player
class EdgeAction():
    """ 
    Instanciate the edge of the tree with the following parameters:
     - num_action: to save the action played(place/move a pawn, move a square pawn or move two square pawns)
     - x, y: memorise the coordinates of the action
     - id_pawn: memorise the id of the pawn (for move a pawn for exemple)
    The function creates a board with 9 tiles and 8 square pawns placed 
    on top of every tile except the middle one.
    """
    def __init__(self, num_action, x: int = None, y: int = None, id_pawn: int = None, table_x: list = None, table_y: list = None):
        self.num_action = num_action
        self.x = x                     
        self.y = y
        self.id_pawn = id_pawn
        self.table_x = table_x
        self.table_y = table_y

    
    # returns the number of the action
    def _get_num_action(self):
        return self.num_action
    
    # returns the x coordinate of the action
    def _get_x(self):
        return self.x
    
    # returns the y coordinate of the action
    def _get_y(self):
        return self.y
      
    # returns the id of the pawn used for the action
    def _get_id_pawn(self):
        return self.id_pawn 