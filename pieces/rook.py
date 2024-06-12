from moves import straight
from pieces.abstractPiece import Piece

class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Rook"
        self._canCastle = True
    
    def setCastlingCondition(self, side : int, castling_rights : list[bool] ):
        self._side = side
        self._castling_rights = castling_rights

        # 0 : White kings rook
        # 1 : White queens rook
        # 2 : black kings rook
        # 3 : black queens rook

    def disableCastling(self):
        self._castling_rights[self._side] = False

    def __str__(self):
        if super().getColor() == "White": 
            return '♜' # W
        else: 
            return '♖' # B
        
    def toChar(self):
        if super().getColor() == "White":
            return 'R'
        else:
            return 'r'

    #override
    def updateVision(self, board) -> None:
        self._potentialMoves, self.kingsight = straight(self, self.pos(), board)



       
