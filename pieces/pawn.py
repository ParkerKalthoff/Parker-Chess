from moves import pawnMove
from pieces.abstractPiece import Piece

class Pawn(Piece):

    def promote(self, board):
        raise NotImplementedError

    def __init__(self, color, canEnpassant = True):
        super().__init__(color)
        self.type = "Pawn"
        self.__canEnpassant__ = canEnpassant

    def canEnpassant(self):
        return self.__canEnpassant__
    
    def __str__(self):
        if self.getColor() == "White": 
            return '♟' # W
        else: 
            return '♙' # B
    
    def toChar(self):
        if super().getColor() == "White":
            return 'P'
        else: 
         # super().getColor() == "Black":
            return 'p'

    #override
    def updateVision(self, board):
        self._potentialMoves = pawnMove(self, self.pos(), board)
        