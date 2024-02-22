import piece
from piece import *

class King(piece.Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "King"
        self.__canCastle__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'K' # W
        else: 
            return 'k' # B

    def __getPotentialMoves__(position):
        potentialMoves = []

        offsets = [-9, -8, -7, -1, 0, 1, 7, 8, 9]

        for offset in offsets:
            pos = position + offset
            if  isValidPos(pos):
                potentialMoves.append(position + offset)
        return potentialMoves

