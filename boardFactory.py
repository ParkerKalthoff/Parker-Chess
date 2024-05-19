from pieces.queen import Queen
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.abstractPiece import Piece
from board import Board
from typing import List, Union, Optional

def defaultBoard() -> Board:
    """Creates a default board with the standard starting position."""
    return fenToBoard('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def fenToBoard(fen_string: str) -> Board:
    """Converts a FEN string to a Board object."""
    parts = fen_string.split()
    board_space = []

    for char in parts[0]:
        if char == '/':
            continue
        board_space.extend(charToPiece(char))

    is_whites_turn = parts[1] == 'w'
    castling_rights = parse_castling_rights(parts[2])
    en_passant_square = coordinateToIndex(parts[3]) if parts[3] != '-' else -1
    half_move_clock = int(parts[4])
    full_move_number = int(parts[5])

    return Board(board_space, is_whites_turn, castling_rights, en_passant_square, half_move_clock, full_move_number)

def coordinateToIndex(coord: str) -> int:
    """Converts board coordinates (e.g., 'e4') to a board index (0-63)."""
    if coord == '-':
        return -1

    file_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    file, rank = coord[0], coord[1]
    
    index = file_to_index[file] + (8 * (int(rank) - 1))
    return index

def parse_castling_rights(castling_string: str) -> List[bool]:
    """Parses the castling rights string into a list of booleans."""
    return [
        'K' in castling_string,  # White kingside
        'Q' in castling_string,  # White queenside
        'k' in castling_string,  # Black kingside
        'q' in castling_string   # Black queenside
    ]

def charToPiece(char: str) -> List[Optional[Piece]]:
    """Converts a FEN character to a list containing the corresponding Piece or None."""
    piece_dict = {
        'P': Pawn,
        'B': Bishop,
        'R': Rook,
        'N': Knight,
        'Q': Queen,
        'K': King
    }
    
    if char.isdigit():
        return [None] * int(char)

    color = 'White' if char.isupper() else 'Black'
    piece_type = piece_dict[char.upper()]
    return [piece_type(color)]

if __name__ == "__main__":
    my_board = defaultBoard()
    print(my_board)
