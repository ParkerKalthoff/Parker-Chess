from moves import straight
from pieces.abstractPiece import Piece

class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Rook"
        self._canCastle = True
    
    def __str__(self):
        if super().getColor() == "White": 
            return '♖' # W
        else: 
            return '♜' # B
        
    def toChar(self):
        if super().getColor() == "White":
            return 'R'
        else:
            return 'r'

    #override
    def updateMoves(self, position, board) -> None:
        self._potentialMoves = straight(self, position, board)



       
