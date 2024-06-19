from util import isValidPos, x_Pos, y_Pos, xy_Pos

def getTeams(piece, board) -> tuple[list[int], list[int]]:
    if piece.getColor() == "White":
        return board.white_piece_indices(), board.black_piece_indices()
    return board.black_piece_indices(), board.white_piece_indices()

# -----  -----  -----  -----  -----  -----  -----

def pawnMove(piece, position: int, board) -> list[int]:
    if not isValidPos(position):
        raise IndexError("Invalid position")
    moveset = (pawnForward(piece, position, board) +
               enpassant(piece, position, board) +
               pawnTake(piece, position, board))
    return sorted(moveset)

def enpassant(piece, position: int, board) -> list[int]:
    if not piece.canEnpassant():
        return []

    direction = -1 if piece.getColor() == "White" else 1
    endSquare = position + (16 * direction)
    firstSquare = position + (8 * direction)

    if not isValidPos(endSquare) or board.get_square(firstSquare) or board.get_square(endSquare):
        return []
    return [endSquare]

def pawnForward(piece, position: int, board) -> list[int]:
    """Returns the forward moves for a pawn."""

    direction = -1 if piece.getColor() == "White" else 1
    firstSquare = position + (8 * direction)

    if not isValidPos(firstSquare) or board.get_square(firstSquare):
        return []
    return [firstSquare]

def pawnTake(piece, position: int, board) -> list[int]:
    """Returns the capturing moves for a pawn """
    direction = -1 if piece.getColor() == "White" else 1
    moveset = []

    rightOffset = 7 if piece.getColor() == "White" else 9
    leftOffset = 9 if piece.getColor() == "White" else 7

    rightSquare = position + (rightOffset * direction)
    leftSquare = position + (leftOffset * direction)

    if isValidPos(rightSquare):
        targetPiece = board.get_square(rightSquare)
        if targetPiece and piece.getColor() != targetPiece.getColor() and x_Pos(rightSquare) == x_Pos(position) + 1:
            moveset.append(rightSquare)
        if board.enpassant_square == rightSquare:
            moveset.append(rightSquare)

    if isValidPos(leftSquare):
        targetPiece = board.get_square(leftSquare)
        if targetPiece and piece.getColor() != targetPiece.getColor() and x_Pos(leftSquare) == x_Pos(position) - 1:
            moveset.append(leftSquare)
        if board.enpassant_square == leftSquare:
            moveset.append(leftSquare)

    return moveset



# -----  -----  -----  -----  -----  -----  -----

def straight(piece, position: int, board):
    """Returns the possible straight moves for a rook or queen and line of sight if it directly sees the enemy king."""
    result = []
    if not isValidPos(position):
        raise IndexError("Invalid position")

    offsets = [-8, 8, -1, 1]
    friendlyPieces, enemyPieces = getTeams(piece, board)
    line_of_sight_to_king = None

    for offset in offsets:
        current_line_of_sight = []
        foundEnemyKing = False
        for i in range(1, 8):
            mySquare = position + i * offset

            current_col = position % 8
            target_col = mySquare % 8
            
            # Check if the move wraps around the board horizontally
            if offset == -1 and target_col > current_col:  # Moving left
                break
            if offset == 1 and target_col < current_col:   # Moving right
                break

            if not isValidPos(mySquare):
                break
            if mySquare in friendlyPieces:
                break
            if mySquare in enemyPieces:
                targetPiece = board.get_square(mySquare)
                current_line_of_sight.append(mySquare)
                result.append(mySquare)
                if targetPiece.toChar().upper() == "K" and targetPiece.getColor() != piece.getColor():
                    foundEnemyKing = True
                    line_of_sight_to_king = current_line_of_sight[:]  # shallow copy
                else:
                    break  # Only break if we found an enemy piece that is not the king
            else:
                result.append(mySquare)
                current_line_of_sight.append(mySquare)

        if foundEnemyKing:
            piece.pin(sorted(current_line_of_sight))

    return sorted(result), line_of_sight_to_king if line_of_sight_to_king else []

# -----  -----  -----  -----  -----  -----  -----

def diagonals(piece, position: int, board):
    """Returns the possible diagonal moves for a bishop or queen and line of sight if it directly sees the enemy king."""
    if not isValidPos(position):
        raise IndexError("Invalid position")

    offsets = [-9, -7, 7, 9]
    friendlyPieces, enemyPieces = getTeams(piece, board)
    result = []
    line_of_sight_to_king = None

    for offset in offsets:
        current_line_of_sight = []
        foundEnemyKing = False

        for i in range(1, 8):
            mySquare = position + i * offset
            if not isValidPos(mySquare):
                break

            current_row, current_col = divmod(position, 8)
            target_row, target_col = divmod(mySquare, 8)
            if abs(target_row - current_row) != abs(target_col - current_col):
                break

            if mySquare in friendlyPieces:
                break
            if mySquare in enemyPieces:
                targetPiece = board.get_square(mySquare)
                current_line_of_sight.append(mySquare)
                result.append(mySquare)
                if targetPiece.toChar().upper() == 'K' and targetPiece.getColor() != piece.getColor():
                    foundEnemyKing = True
                    line_of_sight_to_king = current_line_of_sight[:]
                else:
                    break
            else:
                result.append(mySquare)
                current_line_of_sight.append(mySquare)

        if foundEnemyKing:
            piece.pin(sorted(current_line_of_sight))

    return sorted(result), line_of_sight_to_king if line_of_sight_to_king else []

# -----  -----  -----  -----  -----  -----  -----

def squareMoves(piece, position: int, board) -> list[int]:
    """ returns the possible moves for a king """
    if not isValidPos(position):
        raise IndexError("Invalid position")

    friendlyPieces, enemyPieces = getTeams(piece, board)

    # offsets = [-9, -8, -7, 
    #            -1, |K|  1, 
    #             7,  8,  9]
    output = [-9, -8, -7, -1, 1, 7, 8, 9]

    if position // 8 == 0: # top of the board
        for i in [-9, -8, -7]:
            try:
                output.remove(i)
            except ValueError:
                continue

    if position // 8 == 7: # bottom
        for i in [7, 8, 9]:
            try:
                output.remove(i)
            except ValueError:
                continue

    if position % 8 == 0:  # right side of board
        for i in [-9, -1, 7]:
            try:
                output.remove(i)
            except ValueError:
                continue

    if position % 8 == 7:  # left side of board 
        for i in [-7, 1, 9]:
            try:
                output.remove(i)
            except ValueError:
                continue

    return sorted([index + position for index in output])

# -----  -----  -----  -----  -----  -----  -----

def knightMoves(piece, position: int, board) -> list[int]:
    """ returns the possible moves for a knight """
    if not isValidPos(position):
        raise IndexError("Invalid position")

    friendlyPieces, enemyPieces = getTeams(piece, board)

    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    potentialMoves = [position + offset for offset in offsets if isValidPos(position + offset) and x_Pos(position + offset) in range(x_Pos(position) - 2, x_Pos(position) + 3) and (position + offset) not in friendlyPieces]

    return sorted(potentialMoves)
