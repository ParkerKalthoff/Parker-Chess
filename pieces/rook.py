from moves import straight
from pieces.abstractPiece import Piece

class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Rook"
        if color == 'White':
            self.piece = '♜'
            self.char = 'R'
        else:
            self.piece = '♖'
            self.char = 'r'
    
    def setCastlingCondition(self, side : int, castling_rights : list[bool] ):
        self._side = side
        self._castling_rights = castling_rights

        # 0 : White kings rook
        # 1 : White queens rook
        # 2 : black kings rook
        # 3 : black queens rook

    def disableCastling(self):

        if self._side not in [0,1,2,3]:
            return

        self._castling_rights[self._side] = False

    def __str__(self):
        return self.piece
        
    def toChar(self):
        return self.char
    
    #override
    def updateVision(self, board) -> None:
        self._pieceVision, self.kingsight = straight(self, self.pos(), board)




       
