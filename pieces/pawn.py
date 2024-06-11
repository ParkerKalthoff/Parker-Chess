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
        direction = -1 if self.getColor() == "White" else 1

        rightSquare = self.pos() + (7 * direction)
        leftSquare = self.pos() + (9 * direction)

        rightValid = (rightSquare >= 0 and rightSquare < 64) and abs((rightSquare % 8) - (self.pos() % 8)) == 1
        leftValid = (leftSquare >= 0 and leftSquare < 64) and abs((leftSquare % 8) - (self.pos() % 8)) == 1

        if rightValid and leftValid:
            self._pieceVision = [rightSquare, leftSquare]
        elif rightValid:
            self._pieceVision = [rightSquare]
        elif leftValid:
            self._pieceVision = [leftSquare]
        else:
            self._pieceVision = []


    def visionToMoves(self, board):
        """ Changes piece vision to valid moves, not accounting for check on king """
        potential_moves = pawnMove(self, self.pos(), board)
        if self.pinned:
            self.valid_moves = [move for move in self._pinned_line_of_sight if move in potential_moves]
        else:
            self.valid_moves = potential_moves
        