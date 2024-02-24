import math

class Piece():

    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def move():
        return None
    
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
# -------- --------  -------- --------  -------- -------- 
 
def diagonals(position, board):

    if not isValidPos(position):
        raise IndexError

    potentialMoves = []
    offsets = [-9, -7, 7, 9]

    x, y = xy_Pos(position)

# --  --  --  --  -- 

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

    
# --  --  --  --  -- 
        
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

# --  --  --  --  -- 

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

    
# --  --  --  --  -- 
        
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
    
# --  --  --  --  -- 

    results = []

    for index in potentialMoves:
        if index not in results:
            results.append(index)
    results.sort()
    return results
