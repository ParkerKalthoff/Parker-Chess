import piece
from piece import *

class Rook(piece.Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Rook"
        self.__canCastle__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'R' # W
        else: 
            return 'r' # B