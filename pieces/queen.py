from moves import *
from piece import Piece

class Queen(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'Q' # W
        else: 
            return 'q' # B

    def __getPotentialMoves__(self, position, board):

        moveSet = diagonals(position, board) + straight(position, board)

       

