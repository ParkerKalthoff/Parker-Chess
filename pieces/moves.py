import math
from pieces.abstractPiece import *
from pieces.moves import *
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
from board import Board

def isValidPos(position: int) -> bool:
    if position >= 0 and position <= 63:
        return True
    return False

def x_Pos(position : int) -> int:
    return position % 8

def y_Pos(position : int) -> int:
    return math.floor(position/8)

def xy_Pos(position : int) -> tuple[int, int]:
    x = x_Pos(position)
    y = y_Pos(position)
    return x, y

def getTeams(piece : Piece, board : Board) -> tuple[list[Piece], list[Piece]]:
    
    if piece.getColor() == "White":
        friendlyPieces = board.whitePieceIndcies()
        enemyPieces = board.blackPieceIndcies()
    else:
        friendlyPieces = board.blackPieceIndcies()
        enemyPieces = board.whitePieceIndcies()

    return friendlyPieces, enemyPieces
# -----  -----  -----  -----  -----  -----  ----- 
#   Moves Moves Moves Moves Moves Moves Moves
# -----  -----  -----  -----  -----  -----  ----- 

def pawnMove(piece : Pawn, position : int, board : list[Piece]) -> list[int]:
    if not isValidPos(position):
        raise IndexError
    moveset = pawnForward(piece, position, board) + enpassant(piece, position, board) + pawnTake(piece, position, board)
    moveset.sort()
    return moveset

def enpassant(piece : Pawn, position : int, board : Board) -> list[int]:
    if not piece.canEnpassant():
        return []
    
    direction = 1
    if piece.getColor() == "Black":
        direction = -1
    endSquare = position + (16 * direction)
    firstSquare = position + (8 * direction)

    if not isValidPos(endSquare):
        return []
    if board.getSquare(firstSquare) is not None or board.getSquare(endSquare) is not None:
        return []
    return [endSquare]

def pawnForward(piece : Pawn, position : int, board : Board) -> list[int]:
    if not piece.canEnpassant():
        return []
    
    direction = 1
    if piece.getColor() == "Black":
        direction = -1
    firstSquare = position + (8 * direction)

    if not isValidPos(firstSquare):
        return []
    if board.getSquare(firstSquare) is not None:
        return []
    return [firstSquare]

def pawnTake(piece : Pawn, position : int, board : Board) -> list[int]:
    direction = 1
    if piece.getColor() == "Black":
        direction = -1
    rightSquare = position + (7 * direction)
    leftSquare = position + (9 * direction)

    moveset = []

    if isValidPos(rightSquare):
        targetPiece = board.getSquare(rightSquare)
        # Checks if there is a target piece, checks the target square for board wrapping, 
        #   then checks that the piece colors are different
        if targetPiece and rightSquare % 8 == position % 8 + 1 and piece.getColor() != targetPiece.getColor():
                moveset.append(rightSquare)

    if isValidPos(leftSquare):
        targetPiece = board.getSquare(leftSquare)
        if targetPiece and piece.getColor() == targetPiece.getColor() and leftSquare % 8 == position % 8 - 1:
                moveset.append(leftSquare)
    
    return moveset

# -- -- -- -- -- -- -- -- -- --

def straight(piece : Rook | Queen, position : int, board : Board) -> list[int]:
    result = []

    if not isValidPos(position):
        raise IndexError

    x,y = xy_Pos(position)

    friendlyPieces, enemyPieces = getTeams(piece, board)

    # left

    for index in range(x):
        mySquare = position + (-1 * (1 + index))

        if not isValidPos(mySquare):
            break

        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            result.append(mySquare)
            break

        result.append(mySquare)
    # right
    for index in range(7-x):
        mySquare = position + (1 * (1 + index))

        if not isValidPos(mySquare):
            break

        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            result.append(mySquare)
            break

        result.append(mySquare)
    # top
    for index in range(y):
        mySquare = position + (-8 * (1 + index))

        if not isValidPos(mySquare):
            break

        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            result.append(mySquare)
            break

        result.append(mySquare)
    # bottom
    for index in range(7-y):
        mySquare = position + (8 * (1 + index))

        if not isValidPos(mySquare):
            break

        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            result.append(mySquare)
            break

        result.append(mySquare)

    result.sort()
    return result

# -------- --------  -------- --------  -------- -------- 
 
def diagonals(piece : Bishop | Queen, position : int, board : Board) -> list[int]:

    if not isValidPos(position):
        raise IndexError

    potentialMoves = []
    friendlyPieces, enemyPieces = getTeams(piece, board)
    x, y = xy_Pos(position)

    # Top left
    overflow = []
    targetPieceFound = False

    for index in range(max(x,y)):
        mySquare = position + (-9 * (index + 1))

        if not isValidPos(mySquare):
            break

        if len(overflow) > 0:
            if max(overflow) < x_Pos(mySquare):
                break
        
        if mySquare in friendlyPieces:
            break

        if not targetPieceFound and mySquare in enemyPieces :
            potentialMoves.append(mySquare)
            targetPieceFound = True
            potential_pinned_piece = mySquare

        if targetPieceFound:
            if  isinstance(board.getBoard()[mySquare], King) and board.getBoard()[mySquare].getColor() != piece.getColor():
                board.getBoard()[potential_pinned_piece].pin()

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

        
    # Top Right
    overflow = [] # clear overflow
    targetPieceFound = False

    for index in range(max(7-x,y)):
        mySquare = position + (-7 * (index + 1))

        if not isValidPos(mySquare):
            break

        if len(overflow) > 0:
            if max(overflow) > x_Pos(mySquare):
                break
        
        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            potentialMoves.append(mySquare)
            break

        if not targetPieceFound and mySquare in enemyPieces :
            potentialMoves.append(mySquare)
            targetPieceFound = True
            potential_pinned_piece = mySquare

        if targetPieceFound:
            if  isinstance(board.getBoard()[mySquare], King) and board.getBoard()[mySquare].getColor() != piece.getColor():
                board.getBoard()[potential_pinned_piece].pin()

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

    # Bottom left
    overflow = []
    targetPieceFound = False

    for index in range(max(x,7-y)):
        mySquare = position + (7 * (index + 1))

        if not isValidPos(mySquare):
            break

        if len(overflow) > 0:
            if max(overflow) < x_Pos(mySquare):
                break
        
        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            potentialMoves.append(mySquare)
            break

        if not targetPieceFound and mySquare in enemyPieces :
            potentialMoves.append(mySquare)
            targetPieceFound = True
            potential_pinned_piece = mySquare

        if targetPieceFound:
            if  isinstance(board.getBoard()[mySquare], King) and board.getBoard()[mySquare].getColor() != piece.getColor():
                board.getBoard()[potential_pinned_piece].pin()

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

        
    # Bottom Right
    overflow = []
    targetPieceFound = False

    for index in range(max(7-x,7-y)):
        mySquare = position + (9 * (index + 1))

        if not isValidPos(mySquare):
            break

        if len(overflow) > 0:
            if max(overflow) > x_Pos(mySquare):
                break
        
        if mySquare in friendlyPieces:
            break

        if mySquare in enemyPieces:
            potentialMoves.append(mySquare)
            break

        if not targetPieceFound and mySquare in enemyPieces :
            potentialMoves.append(mySquare)
            targetPieceFound = True
            potential_pinned_piece = mySquare

        if targetPieceFound:
            if  isinstance(board.getBoard()[mySquare], King) and board.getBoard()[mySquare].getColor() != piece.getColor():
                board.getBoard()[potential_pinned_piece].pin()

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

    results = []

    for index in potentialMoves:
        if index not in results:
            results.append(index)
    results.sort()

    return results

# -------- --------  -------- --------  -------- -------- 

def squareMoves(piece : King, position : int, board : Board) -> list[int]:
    if not isValidPos(position):
        raise IndexError

    friendlyPieces, enemyPieces = getTeams(piece, board)

    potentialMoves = []
    offsets = [-9, -8, -7, -1, 0, 1, 7, 8, 9]

    for offset in offsets:
        pos = position + offset
        if  isValidPos(pos) and (pos not in friendlyPieces):
            potentialMoves.append(position + offset)
    return potentialMoves

# -------- --------  -------- --------  -------- -------- 

def knightMoves(piece : Knight, position : int, board : Board) -> list[int]:

    if not isValidPos(position):
        raise IndexError

    friendlyPieces, enemyPieces = getTeams(piece, board)


    potentialMoves = []
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]

    for offset in offsets:
        pos = position + offset
        if isValidPos(pos):
            if (pos % 8) in range((position % 8) - 2, (position % 8) + 3) and (pos not in friendlyPieces):
                potentialMoves.append(position + offset)
    return potentialMoves

