import math

class Piece():

    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def move():
        return None
    
def isValidPos(position):
    if position >= 1 and position <= 64:
        return True
    return False

def diagonals(position):
    potentialMoves = []
    offsets = [-9, -7, 7, 9]

    x = (position - 1) % 8
    y = math.floor((position - 1)/ 8)
    
    for index in range(max(x,y)): # top left
        pos = position + (index * -9)
        if isValidPos(pos):
            potentialMoves.append(pos)

    for index in range(max(x,7-y)): # top right
        pos = position + (index * -7)
        if isValidPos(pos):
            potentialMoves.append(pos)

    for index in range(max(7-x,y)): # bottom left
        pos = position + (index * 7)
        if isValidPos(pos):
            potentialMoves.append(pos)

    for index in range(max(7-x,7-y)): # bottom left
        pos = position + (index * 9)
        if isValidPos(pos):
            potentialMoves.append(pos)
    
    results = []

    for index in potentialMoves:
        if index not in results:
            results.append(index)
    results.sort()
    return results