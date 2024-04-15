from pieces import pawn, bishop, knight, rook, queen, king, abstractPiece
from board import Board

def defaultBoard() -> Board:
    return fenToBoard('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def fenToBoard(fenString : str) -> Board:
    # boardSpace : list, isWhitesTurn : bool, castlingRights : list, enPassantSq : int, halfMoveClock : int, fullMoveNumber : int
    temp = fenString.split() 
    boardSpace = []

    for i in temp[0]: # set board
        if i == '/':
            continue
        boardSpace += charToPiece(i)

    isWhitesTurn = temp[1] == 'w'

    castlingRights = castlingList(temp[2])
    enpassant = coordinateToIndex(temp[3])
    halfMoveClock = int(temp[4])
    fullMoveNumber = int(temp[5])

    return Board(boardSpace, isWhitesTurn, castlingRights, enpassant, halfMoveClock, fullMoveNumber)


def coordinateToIndex(coord : str) -> int:
    index = 0
    letter = coord[0]

    letterToNumber = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    index = letterToNumber[letter]

    index += (int(coord[1]) - 1) * 8

    return index


def castlingList(string : str) -> list[bool]:
    wk = 'K' in string
    wq = 'Q' in string
    bk = 'k' in string
    bq = 'q' in string

    return [wk, wq, bk, bq]

def charToPiece(char : str) -> abstractPiece.Piece | None:
    
    if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        boardSpace = [None] * int(char)
        return boardSpace
    
    if char == char.capitalize():
        color = 'White'
    else:
        color = 'Black'

    char = char.capitalize()

    switch = {
        'P': pawn.Pawn(color),
        'B': bishop.Bishop(color),
        'R': rook.Rook(color),
        'N': knight.Knight(color),
        'Q': queen.Queen(color),
        'K': king.King(color)
    }

    return [switch[char]]