from moves import *
from piece import Piece

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
        
    def __getPotentialMoves__(self, position, board):

        moveSet = straight(position, board)
        return moveSet

       
