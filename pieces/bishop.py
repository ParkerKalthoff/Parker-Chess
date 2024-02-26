from moves import *
from piece import Piece



class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Bishop"
    
    def __str__(self):
        if super().getColor() == "White": 
            return 'B' # W
        else: 
            return 'b' # B

    def __getPotentialMoves__(self, position):

        if isValidPos(position) == False:
            raise Exception(f"[{self.type}] Position Invalid : {position}")

        

