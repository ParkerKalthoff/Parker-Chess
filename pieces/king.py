from moves import *
from piece import Piece



class King(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "King"
        self.__canCastle__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'K' # W
        else: 
            return 'k' # B

    def getMoves(position, board):
        
        moveSet = squareMoves(position, board)

