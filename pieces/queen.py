from moves import diagonals, straight
from pieces.abstractPiece import Piece

class Queen(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"

    
    def __str__(self):
        if super().getColor() == "White": 
            return '♛' # W
        else: 
            return '♕' # B

    def toChar(self):
        if super().getColor() == "White":
            return 'Q'
        else:
            return 'q' 

    #override
    def updateVision(self, board):
        potential_moves_diagonal, kingsight_diagonal = diagonals(self, self.pos(), board)
        potential_moves_straight, kingsight_straight = straight(self, self.pos(), board)
        
        self._potentialMoves = potential_moves_diagonal + potential_moves_straight
        self.kingsight = kingsight_diagonal if kingsight_diagonal else kingsight_straight if kingsight_straight else None
       

