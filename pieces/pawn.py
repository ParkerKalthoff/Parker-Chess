from moves import *
from piece import Piece

class Pawn(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Pawn"
        self.__canEnpassant__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'P' # W
        else: 
            return 'p' # B