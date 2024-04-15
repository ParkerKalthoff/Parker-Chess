from moves import *
from pieces.abstractPiece import Piece

class Rook(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Rook"
        self.__canCastle__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'R' # W
        else: 
            return 'r' # B
        
    def getMoves(self, position, board):
        return straight(self, position, board)

       
