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

# -----  -----  -----  -----  -----  -----  ----- 
#   Moves Moves Moves Moves Moves Moves Moves
# -----  -----  -----  -----  -----  -----  ----- 

def straight(position, board):
    result = []

    if not isValidPos(position):
        raise IndexError

    x,y = xy_Pos(position)

    # left

    for index in range(x):
        mySquare = position + (-1 * (1 + index))

        if not isValidPos(mySquare):
            break
        result.append(mySquare)
    # right
    for index in range(7-x):
        mySquare = position + (1 * (1 + index))

        if not isValidPos(mySquare):
            break
        result.append(mySquare)
    # top
    for index in range(y):
        mySquare = position + (-8 * (1 + index))

        if not isValidPos(mySquare):
            break
        result.append(mySquare)
    # bottom
    for index in range(7-y):
        mySquare = position + (8 * (1 + index))

        if not isValidPos(mySquare):
            break
        result.append(mySquare)

    result.sort()
    return result

# -------- --------  -------- --------  -------- -------- 
 
def diagonals(position, board):

    if not isValidPos(position):
        raise IndexError

    potentialMoves = []

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
        
        overflow.append(x_Pos(mySquare))
        potentialMoves.append(mySquare)

    results = []

    for index in potentialMoves:
        if index not in results:
            results.append(index)
    results.sort()
    return results

# -------- --------  -------- --------  -------- -------- 

def squareMoves(position, board):
    potentialMoves = []
    offsets = [-9, -8, -7, -1, 0, 1, 7, 8, 9]

    for offset in offsets:
        pos = position + offset
        if  isValidPos(pos):
            potentialMoves.append(position + offset)
    return potentialMoves

# -------- --------  -------- --------  -------- -------- 

def knightMoves(position, board):

    if not isValidPos(position):
        raise IndexError

    potentialMoves = []
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]

    for offset in offsets:
        pos = position + offset
        if  isValidPos(pos):
            if (pos % 8) in range((position % 8) - 2, (position % 8) + 3):
                potentialMoves.append(position + offset)
    return potentialMoves

