from pieces.abstractPiece import Piece
from pieces.moves import *
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
import os
import sys
from boardFactory import fenToBoard, defaultBoard

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

class BoardSizeError(Exception): ... # custom exception >:D

class Board:
    def __init__(self, boardSpace : list, isWhitesTurn : bool, castlingRights : list, enpassantSq : int, halfMoveClock : int, fullMoveNumber : int):
        self.__myBoard__ = boardSpace

        self.halfMoveClock = halfMoveClock
        self.fullMoveNumber = fullMoveNumber
        self.castling = castlingRights
        self.enpassantSquare = enpassantSq
        
        self.isWhitesTurn = isWhitesTurn

        self.__whitePieceIndicies__ = []
        self.__blackPieceIndicies__ = []
        
        self.__whitePieceObjects__ = []
        self.__blackPieceObjects__ = []

        self.__whitePieceVison__ = []
        self.__blackPieceVison__ = []

        self.__whiteScore__ = 0
        self.__blackScore__ = 0

        self.PIECE_VALUES = {
            Queen: 9,
            Rook: 5,
            Bishop: 3,
            Knight: 3,
            Pawn: 1,
            King: 999
        }
        self.refreshBoard()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

    def nextTurn(self) -> None:
        self.isWhitesTurn = not self.isWhitesTurn

    def whitePieceIndcies(self) -> list[int]:
        return self.__whitePieceIndicies__
    
    def blackPieceIndcies(self) -> list[int]:
        return self.__blackPieceIndicies__

    def whiteScore(self) -> int: ## meant for engine usage, king is 999
        return self.__whiteScore__
    
    def blackScore(self) -> int:
        return self.__blackScore__

    def getScore(self) -> int:
        return self.whiteScore() - self.blackScore()

    def getTurn(self) -> bool:
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
        

    def getBoard(self) -> list[Piece]:
        return self.__myBoard__

    def pieceMoves(self, position: int) -> list[int]:
        if self.getBoard()[position] == None:
            return []
        return self.getBoard()[position].getMoves(position, self)

    def getSquare(self, position: int) -> Piece:
        return self.getBoard()[position]
    
    def whitePieceObjects(self) -> list[Piece]:
        return self.__whitePieceObjects__

    def blackPieceObjects(self) -> list[Piece]:
        return self.__blackPieceObjects__

    def pieceObjects(self) -> list[Piece]:
        return self.whitePieceObjects() + self.blackPieceObjects()
    
# --- ---  --- ---  --- ---  --- ---  --- ---  --- ---  --- ---  --- --- 

    def __str__(self, withChessCoords=False) -> str:
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

    def addCoords(self) -> str:
        return self.__str__(withChessCoords=True)
    

myBoard = defaultBoard()

print(myBoard)
    