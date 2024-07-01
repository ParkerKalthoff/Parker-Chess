from moves import squareMoves
from board.pieces.abstractPiece import Piece



class King(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.type = "King"
        if color == 'White':
            self.piece = '♚'
            self.char = 'K'
        else:
            self.piece = '♔'
            self.char = 'k'
    
    def __str__(self):
        return self.piece
        
    def toChar(self):
        return self.char
        
    def setCastlingCondition(self, castling_rights : list[bool] ):
        self._castling_rights = castling_rights # boards castling rights reference

    def disableCastling(self):
        if super().getColor() == "White":
            self._castling_rights[0] = False
            self._castling_rights[1] = False
        else:
            self._castling_rights[2] = False
            self._castling_rights[3] = False


    #override
    def updateVision(self, board):
        self._pieceVision = squareMoves(self, self.pos(), board)

    #override
    def visionToMoves(self, board):
        if self.getColor() == 'White':
            self.valid_moves = [move for move in self._pieceVision if move not in board.white_piece_indices() and move not in board.combine_lists(board.black_piece_vision())]
        else:
            self.valid_moves = [move for move in self._pieceVision if move not in board.black_piece_indices() and move not in board.combine_lists(board.white_piece_vision())]