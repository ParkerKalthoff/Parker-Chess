from moves import knightMoves
from pieces.abstractPiece import Piece

class Knight(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Knight"

    
    def __str__(self):
        if super().getColor() == "White": 
            return '♞' # W
        else: 
            return '♘' # B
    
    def toChar(self):
        if super().getColor() == "White":
            return 'N'
        else:
            return 'n'

    #override
    def updateVision(self, board):
        self._pieceVision = knightMoves(self, self.pos(), board)