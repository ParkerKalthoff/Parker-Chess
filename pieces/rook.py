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

        # 0 : KR
        # 1 : QR
        # 2 : kr
        # 3 : qr

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
    def updateVision(self, position, board) -> None:
        self._potentialMoves = straight(self, self.pos(), board)



       
