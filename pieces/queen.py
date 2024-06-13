from moves import diagonals, straight
from pieces.abstractPiece import Piece

class Queen(Piece):


    def __init__(self, color):
        super().__init__(color)
        self.type = "Queen"
        if color == 'White':
            self.piece = '♛'
            self.char = 'K'
        else:
            self.piece = '♕'
            self.char = 'k'

    
    def __str__(self):
        return self.piece
        
    def toChar(self):
        return self.char
    
    #override
    def updateVision(self, board):
        potential_moves_diagonal, kingsight_diagonal = diagonals(self, self.pos(), board)
        potential_moves_straight, kingsight_straight = straight(self, self.pos(), board)
        self._pieceVision = potential_moves_diagonal + potential_moves_straight
        self.kingsight = kingsight_diagonal if kingsight_diagonal else kingsight_straight if kingsight_straight else None
       

