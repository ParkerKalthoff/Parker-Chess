from pieces.piece import *

def getIndecies():
    for row in range(8):
        myRow = []
        for index in range(8):
            num = (row*8)+index
            myRow.append(f"{num:02}")
        print(myRow)

