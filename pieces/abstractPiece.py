class Piece():

    def __init__(self, color) -> None:
        self.color = color
        self.pinned = False

    def getColor(self) -> str:
        return self.color

    def getMoves() -> None:
        raise NotImplemented
    
    def pin(self) -> None:
        self.pinned = True

    def unpin(self) -> None:
        self.pinned = False

    def isPinned(self) -> bool:
        return self.pinned
