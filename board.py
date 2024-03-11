
from pieces.piece import *
from pieces.moves import *
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

class BoardSizeError(Exception): ...

class Board:

# fix import issues
    def __init__(self, fenString=None):
        self.__myBoard__ = [None]*64

        self.__whitePieceIndicies__ = []
        self.__blackPieceIndicies__ = []
        
        self.__whitePieceObjects__ = []
        self.__blackPieceObjects__ = []

        self.__whiteScore__ = 0
        self.__blackScore__ = 0

        self.PIECE_VALUES = {
            Queen: 9,
            Rook: 5,
            Bishop: 3,
            Knight: 3,
            Pawn: 1,
            King: 0
        }
        self.isWhitesTurn = True

        if fenString == None:
            self.setBoardDefault()
        self.refreshBoard()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

    def setBoardDefault(self):
        # White Back Rank, capital letters
        self.__myBoard__[0] = Rook("White")
        self.__myBoard__[1] = Knight("White")
        self.__myBoard__[2] = Bishop("White")
        self.__myBoard__[3] = King("White")
        self.__myBoard__[4] = Queen("White")
        self.__myBoard__[5] = Bishop("White")
        self.__myBoard__[6] = Knight("White")
        self.__myBoard__[7] = Rook("White")

        # White Pawns
        for index in range(8,16):
            self.__myBoard__[index] = Pawn("White")

        # Black Back Rank, lowercase letters
            
        self.__myBoard__[56] =  Rook("Black")
        self.__myBoard__[57] =  Knight("Black")
        self.__myBoard__[58] =  Bishop("Black")
        self.__myBoard__[59] =  King("Black")
        self.__myBoard__[60] =  Queen("Black")
        self.__myBoard__[61] =  Bishop("Black")
        self.__myBoard__[62] =  Knight("Black")
        self.__myBoard__[63] =  Rook("Black")

        # Black Pawns
        for index in range(48,56):
            self.__myBoard__[index] = Pawn("Black")

    def nextTurn(self):
        self.isWhitesTurn = not self.isWhitesTurn

    def whitePieceIndcies(self):
        return self.__whitePieceIndicies__
    
    def blackPieceIndcies(self):
        return self.__blackPieceIndicies__

    def whiteScore(self):
        return self.__whiteScore__
    
    def blackScore(self):
        return self.__blackScore__

    def getScore(self):
        return self.whiteScore() - self.blackScore()

    def getTurn(self):
        return self.isWhitesTurn

    def refreshBoard(self):
        if len(self.getBoard()) > 64:
            raise BoardSizeError("Board size exceeds 64")

        self.__whitePieceIndicies__ = []
        self.__blackPieceIndicies__ = []
        self.__whitePieceObjects__ = []
        self.__blackPieceObjects__ = []
        self.__whiteScore__ = 0
        self.__blackScore__ = 0

        for index, indexValue in enumerate(self.__myBoard__):
            if indexValue is not None:
                if Piece.getColor(indexValue) == "White":
                    self.__whitePieceIndicies__.append(index)
                    self.__whiteScore__ += self.PIECE_VALUES[type(indexValue)]
                    self.__whitePieceObjects__.append({"Piece": indexValue, "Position": index, "Color": "White"})
                else:
                    self.__blackPieceIndicies__.append(index)
                    self.__blackScore__ += self.PIECE_VALUES[type(indexValue)]
                    self.__blackPieceObjects__.append({"Piece": indexValue, "Position": index, "Color": "Black"})
        

    def getBoard(self):
        return self.__myBoard__

    def pieceMoves(self, position):
        if self.getBoard()[position] == None:
            return []
        return self.getBoard()[position].getMoves(position, self)

    def getSquare(self, position):
        return self.getBoard()[position]
    
    def whitePieceObjects(self):
        return self.__whitePieceObjects__

    def blackPieceObjects(self):
        return self.__blackPieceObjects__

    def pieceObjects(self):
        return self.whitePieceObjects() + self.blackPieceObjects()
    
# --- ---  --- ---  --- ---  --- ---  --- ---  --- ---  --- ---  --- --- 

    def __str__(self, withChessCoords=False):
        columnNum = ['1','2','3','4','5','6','7','8']
        output_str = " _______________________________\n"
        if withChessCoords:
            output_str = "  " + output_str
        for row in range(8):
            temp = "|"
            if withChessCoords:
                temp = columnNum[row]+ "-" + temp
            
            for index in range(8):
                if self.__myBoard__[(row*8)+index] == None:
                    temp += "___|"
                else:
                    temp += f"_{self.__myBoard__[(row*8)+index].__str__()}_|"
            temp += "\n"
            output_str += temp
        if withChessCoords:
            output_str += "    a   b   c   d   e   f   g   h"
        return output_str

    def addCoords(self):
        return self.__str__(withChessCoords=True)
    
    def stats(self):
        if self.getTurn():
            turn = "White"
        else:
            turn = "Black"
        return {"Turn": turn, "Score": self.getScore}
    
