class Piece():

    def __init__(self, color) -> None:
        self.color = color
        self.pinned = False

    def getColor(self) -> str:
        return self.color

    def getMoves():
        raise NotImplemented
    
    def pin(self) -> None:
        self.pinned = True

    def isPinned(self) -> bool:
        return self.pinned
