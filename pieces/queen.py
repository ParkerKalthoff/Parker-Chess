import piece
from piece import *

class King(piece.Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"
        self.__canCastle__ = True

    
    def __str__(self):
        if super().getColor() == "White": 
            return 'Q' # W
        else: 
            return 'q' # B

    def __getPotentialMoves__(self, position):

        if isValidPos(position) == False:
            raise Exception(f"[{self.type}] Position Invalid : {position}")

        potentialMoves = []

        # diagonal movement
        offsets = [-9, -7, 9, 7, 1, -1, 8, -8]

        for offset in offsets:
            for index in range(8):
                pos = position + (offset * index)
                if isValidPos(pos):
                    potentialMoves.append(pos)
                else:
                    break

        return potentialMoves

