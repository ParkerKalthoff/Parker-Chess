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

    #override
    def updateMoves(self, board) -> list[int]:
        self._potentialMoves = diagonals(self.pos(), board)

        

