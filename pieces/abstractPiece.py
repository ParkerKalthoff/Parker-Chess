class Piece():

    def __init__(self, color : str) -> None:
        self.color = color
        self.pinned = False
        self._pieceVision = []
        self.valid_moves = []
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

    def updateVision(self, board):
        raise NotImplementedError

    def getVision(self) -> list:
        return self._pieceVision
    
    def visionToMoves(self):
        """ Changes piece vision to valid moves, not accounting for check on king """
        if self.pinned:
            self.valid_moves = [move for move in self._pinned_line_of_sight if move in self._pieceVision]
        else:
            self.valid_moves = self._pieceVision

    def movesPreventingCheck(self, check_on_king : list[list[int]]):
        """ takes 'valid moves' and prunes move that dont stop check, only used when in check """
        prevents_check_moves = []
        for move in self.valid_moves:
            prevents_check = True
            for moveset in check_on_king:
                if move not in moveset:
                    prevents_check = False
                    break
            if prevents_check:
                prevents_check_moves.append(move)
        self.valid_moves = prevents_check_moves

    def getMoves(self):
        return self.valid_moves

    def pin(self, pinned_line_of_sight) -> None:
        self._pinned_line_of_sight = pinned_line_of_sight
        self.pinned = True

    def unpin(self) -> None:
        self._pinned_line_of_sight = None
        self.pinned = False

    def isPinned(self) -> bool:
        return self.pinned
