from moves import squareMoves
from pieces.abstractPiece import Piece



class King(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "King"
    
    def __str__(self):
        if super().getColor() == "White": 
            return '♚' # W
        else: 
            return '♔' # B
        
    def setCastlingCondition(self, castling_rights : list[bool] ):
        self._castling_rights = castling_rights # boards castling rights reference

    def disableCastling(self):
        if super().getColor() == "White":
            self._castling_rights[0] = False
            self._castling_rights[1] = False
        else:
            self._castling_rights[2] = False
            self._castling_rights[3] = False

    def toChar(self):
        if super().getColor() == "White":
            return 'K'
        else:
            return 'k'

    #override
    def updateVision(self, board):
        self._pieceVision = squareMoves(self, self.pos(), board)

