from moves import diagonals, straight
from pieces.abstractPiece import Piece

class Queen(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'Q' # W
        else: 
            return 'q' # B

    def getMoves(self, position, board):
        return diagonals(self, position, board) + straight(self, position, board)

       

