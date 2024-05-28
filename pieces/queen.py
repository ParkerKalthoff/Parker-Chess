from moves import diagonals, straight
from pieces.abstractPiece import Piece

class Queen(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"

    
    def __str__(self):
        if super().getColor() == "White": 
            return '♕' # W
        else: 
            return '♛' # B

    def toChar(self):
        if super().getColor() == "White":
            return 'Q'
        else:
            return 'q'

    #override
    def updateMoves(self, position, board):
        self._potentialMoves = diagonals(self, position, board) + straight(self, position, board)
       

