import pygame
from pieces.piece import *
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn

class Board:

# fix import issues

    def setBoard(self):
        # White Back Rank, capital letters
        self.__myBoard__.insert(0, Rook("White"))
        self.__myBoard__.insert(1, Knight("White"))
        self.__myBoard__.insert(2, Bishop("White"))
        self.__myBoard__.insert(3, King("White"))
        self.__myBoard__.insert(4, Queen("White"))
        self.__myBoard__.insert(5, Bishop("White"))
        self.__myBoard__.insert(6, Knight("White"))
        self.__myBoard__.insert(7, Rook("White"))

        # White Pawns
        for index in range(8,16):
            self.__myBoard__.insert(index, Pawn("White"))

        # Black Back Rank, lowercase letters
            
        self.__myBoard__.insert(56, Rook("Black"))
        self.__myBoard__.insert(57, Knight("Black"))
        self.__myBoard__.insert(58, Bishop("Black"))
        self.__myBoard__.insert(59, King("Black"))
        self.__myBoard__.insert(60, Queen("Black"))
        self.__myBoard__.insert(61, Bishop("Black"))
        self.__myBoard__.insert(62, Knight("Black"))
        self.__myBoard__.insert(63, Rook("Black"))

        # Black Pawns
        for index in range(48,56):
            self.__myBoard__.insert(index, Pawn("Black"))

    def refreshBoard(self):
        p = 0

    def __init__(self):
            self.__myBoard__ = []
            self.isWhitesTurn = True
            self.setBoard()


    