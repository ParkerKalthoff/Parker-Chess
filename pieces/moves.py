import math

def isValidPos(position):
    if position >= 0 and position <= 63:
        return True
    return False

def x_Pos(position):
    return position % 8

def y_Pos(position):
    return math.floor(position/8)

def xy_Pos(position):
    x = x_Pos(position)
    y = y_Pos(position)
    return x, y

def getTeams(piece, board):
    
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

def pawnMove(piece, position, board):
    if not isValidPos(position):
        raise IndexError
    moveset = pawnForward(piece, position, board) + enpassant(piece, position, board) + pawnTake(piece, position, board)
    moveset.sort()
    return moveset

def enpassant(piece, position, board):
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

def pawnForward(piece, position, board):
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

def pawnTake(piece, position, board):
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

def straight(piece, position, board):
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
 
def diagonals(piece, position, board):

    if not isValidPos(position):
        raise IndexError

    potentialMoves = []
    friendlyPieces, enemyPieces = getTeams(piece, board)
    x, y = xy_Pos(position)

    # Top left
    overflow = []

    for index in range(max(x,y)):
        mySquare = position + (-9 * (index + 1))

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

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

        
    # Top Right
    overflow = []

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

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

    # Bottom left
    overflow = []

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

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

        
    # Bottom Right
    overflow = []

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

        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

    results = []

    for index in potentialMoves:
        if index not in results:
            results.append(index)
    results.sort()
    return results

# -------- --------  -------- --------  -------- -------- 

def squareMoves(piece, position, board):
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

def knightMoves(piece, position, board):

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

