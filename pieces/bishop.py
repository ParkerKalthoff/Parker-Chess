from moves import *
from pieces.abstractPiece import Piece



class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Bishop"
    
    def __str__(self) -> str:
        if super().getColor() == "White": 
            return 'B' # W
        else: 
            return 'b' # B

    def getMoves(self, position, board) -> list[int]:
        return diagonals(position, board)

        

