
from pieces.piece import *
from pieces.moves import *
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn



class Board:

# fix import issues
    def __init__(self, fenString=None):
        self.__myBoard__ = [None]*64
        self.isWhitesTurn = True
        if fenString == None:
            self.setBoard()

    def setBoard(self):
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

    def refreshBoard(self):
        p = 0

    def __str__(self):
        output_str = " _______________________________\n"
        for row in range(8):
            temp = "|"
            for index in range(8):
                if self.__myBoard__[(row*8)+index] == None:
                    temp += "___|"
                else:
                    temp += f"_{self.__myBoard__[(row*8)+index].__str__()}_|"
            temp += "\n"
            output_str += temp
        return output_str


b = Board()

print(b)