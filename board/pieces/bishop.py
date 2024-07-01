from moves import diagonals
from board.pieces.abstractPiece import Piece



class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Bishop"

        if color == 'White':
            self.piece = '♝'
            self.char = 'B'
        else:
            self.piece = '♗'
            self.char = 'b'
    
    def __str__(self):
        return self.piece
        
    def toChar(self):
        return self.char

    #override
    def updateVision(self, board) -> None:
        self._pieceVision, self.kingsight = diagonals(self, self.pos(), board)
        if self.kingsight:
            self.kingsight += [self.pos()]

        

