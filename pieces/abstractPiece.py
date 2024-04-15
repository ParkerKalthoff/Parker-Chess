class Piece():

    def __init__(self, color):
        self.color = color
        self.pinned = False

    def getColor(self):
        return self.color

    def getMoves():
        raise NotImplemented
    
    def pin(self):
        self.pinned = True

    def isPinned(self):
        return self.pinned
