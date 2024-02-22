import piece
from piece import *

class Bishop(piece.Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "Bishop"
    
    def __str__(self):
        if super().getColor() == "White": 
            return 'B' # W
        else: 
            return 'b' # B

    def __getPotentialMoves__(self, position):

        if isValidPos(position) == False:
            raise Exception(f"[{self.type}] Position Invalid : {position}")

        potentialMoves = []

        offsets = [-9, -7, 9, 7]

        for offset in offsets:
            for index in range(8):
                pos = position + (offset * index)
                if isValidPos(pos):
                    potentialMoves.append(pos)
                else:
                    break
        potentialMoves.sort()
        return potentialMoves

