from moves import knightMoves
from pieces.abstractPiece import Piece

class Knight(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Knight"
        if color == 'White':
            self.piece = '♞'
            self.char = 'N'
        else:
            self.piece = '♘'
            self.char = 'n'

    
    def __str__(self):
        return self.piece
        
    def toChar(self):
        return self.char

    #override
    def updateVision(self, board):
        self._pieceVision = knightMoves(self, self.pos(), board)