import piece
from piece import *

class Knight(piece.Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Knight"

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'N' # W
        else: 
            return 'n' # B