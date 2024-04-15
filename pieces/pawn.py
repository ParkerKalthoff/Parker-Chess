from moves import *
from pieces.abstractPiece import Piece



class Pawn(Piece):

    def promote(self, board):
        return 0

    def __init__(self, color):
        super().__init__(color)
        self.type = "Pawn"
        self.__canEnpassant__ = True

    def canEnpassant(self):
        return self.__canEnpassant__
    
    def __str__(self):
        if self.getColor() == "White": 
            return 'P' # W
        else: 
            return 'p' # B
        
    def getMoves(self, position, board):
        moveset = pawnMove(self, position, board)
        self.__canEnpassant__ = False
        return moveset
        