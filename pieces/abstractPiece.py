class Piece():

    def __init__(self, color : str) -> None:
        self.color = color
        self.pinned = False
        self._potentialMoves = []

    def getColor(self) -> str:
        return self.color
    
    def updateMoves(self) -> None:
        raise NotImplementedError

    def getMoves(self) -> list:
        return self._potentialMoves
    
    def pin(self) -> None:
        self.pinned = True

    def unpin(self) -> None:
        self.pinned = False

    def isPinned(self) -> bool:
        return self.pinned
