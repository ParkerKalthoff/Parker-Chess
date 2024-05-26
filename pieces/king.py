from moves import squareMoves
from pieces.abstractPiece import Piece



class King(Piece):


    def __init__(self, color, castleQueenSide = True, castleKingSide = True):
        super().__init__(color)
        self.type = "King"
        self.inCheck = False
        self.__castleQueenSide__ = castleQueenSide
        self.__castleKingSide__ = castleKingSide
    
    def __str__(self):
        if super().getColor() == "White": 
            return 'K' # W
        else: 
            return 'k' # B

    def getMoves(position, board):
        
        moveSet = squareMoves(position, board)

