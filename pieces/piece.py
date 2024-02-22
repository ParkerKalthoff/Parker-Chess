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