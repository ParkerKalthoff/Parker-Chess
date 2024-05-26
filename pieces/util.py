# utils.py

def isValidPos(position: int) -> bool:
    """Checks if a position is valid on an 8x8 chessboard."""
    return 0 <= position <= 63

def x_Pos(position: int) -> int:
    """Returns the x-coordinate (file) of a given position."""
    return position % 8

def y_Pos(position: int) -> int:
    """Returns the y-coordinate (rank) of a given position."""
    return position // 8

def xy_Pos(position: int) -> tuple[int, int]:
    """Returns the (x, y) coordinates of a given position."""
    return x_Pos(position), y_Pos(position)
