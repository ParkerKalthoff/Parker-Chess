class Piece():

    def __init__(self, color : str) -> None:
        self.color = color
        self.pinned = False
        self._potentialMoves = []
        self._currentPosition = None

    def getColor(self) -> str:
        return self.color
    
    def pos(self) -> int:
        """ Returns current position """
        return self._currentPosition

    def setPos(self, new_position) -> None:
        int(new_position)
        self._currentPosition = new_position

    def toChar(self) -> str:
        raise NotImplementedError

    def updateMoves(self, board) -> list[int]:
        raise NotImplementedError

    def getMoves(self) -> list:
        return self._potentialMoves
    
    def pin(self) -> None:
        self.pinned = True

    def unpin(self) -> None:
        self.pinned = False

    def isPinned(self) -> bool:
        return self.pinned
