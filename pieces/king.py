from moves import squareMoves
from pieces.abstractPiece import Piece



class King(Piece):


    def __init__(self, color, castleQueenSide = True, castleKingSide = True):
        super().__init__(color)
        self.type = "King"
        self.__castleQueenSide__ = castleQueenSide
        self.__castleKingSide__ = castleKingSide
    
    def __str__(self):
        if super().getColor() == "White": 
            return '♔' # W
        else: 
            return '♚' # B
        
    def toChar(self):
        if super().getColor() == "White":
            return 'K'
        else:
            return 'k'

    #override
    def updateMoves(self, position, board):
        self._potentialMoves = squareMoves(position, board)

