from pieces.piece import *

def getIndecies():
    for row in range(8):
        myRow = []
        for index in range(8):
            num = (row*8)+index+1
            myRow.append(f"{num:02}")
        print(myRow)

def __getPotentialMoves__(position):


        potentialMoves = []

        # diagonal movement
        offsets = [-9, -7, 9, 7, 1, -1, 8, -8]

        for offset in offsets:
            for index in range(8):
                pos = position + (offset * index)
                if isValidPos(pos):
                    potentialMoves.append(pos)
                else:
                    break
        potentialMoves.sort()
        return potentialMoves


print(__getPotentialMoves__(28))