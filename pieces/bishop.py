from moves import diagonals
from pieces.abstractPiece import Piece



class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Bishop"
    
    def __str__(self) -> str:
        if super().getColor() == "White": 
            return '♝' # W
        else: 
            return '♗' # B

    def toChar(self):
        if super().getColor() == "White":
            return 'B'
        else:
            return 'b'

    #override
    #override
    def updateVision(self, board) -> None:
        self._potentialMoves, self.kingsight = diagonals(self, self.pos(), board)

        if self.kingsight:
            self.kingsight += [self.pos()]

        

