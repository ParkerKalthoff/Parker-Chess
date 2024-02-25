from .pieces.piece import *
import os

def getIndecies():
    for row in range(8):
        myRow = []
        for index in range(8):
            num = (row*8)+index
            myRow.append(f"{num:02}")
        print(myRow)

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

list_files(os.path.dirname(os.path.abspath(__file__)))