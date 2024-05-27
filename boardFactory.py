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
    return board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def board(fen_string: str) -> Board:
    """ Takes in a FEN string and returns a board object after validating the FEN string """
    
    validate_fen(fen_string)

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

def validate_fen(fen: str):
    """Validates the FEN string to check for common issues."""
    parts = fen.split()

    if len(parts) != 6:
        raise ValueError(f"FEN string has {len(parts)} parts; exactly 6 required")

    # Check if the board part has 8 ranks 
    board_part = parts[0]
    ranks = board_part.split('/')
    if len(ranks) != 8:
        raise ValueError(f"FEN string board part has {len(ranks)} ranks; exactly 8 required\n\nBoard part: {ranks}")

    for i_rank, rank in enumerate(ranks):
        count = 0
        for char in rank:
            if char.isdigit():
                count += int(char)
            elif char in 'prnbqkPRNBQK':
                count += 1
            else:
                raise ValueError(f"FEN string contains invalid character in board part: {char}")
        if count != 8:
            raise ValueError(f"FEN string rank {i_rank + 1} has {count} squares; exactly 8 required")

    if parts[1] not in 'wb': # turn
        raise ValueError(f"FEN string has invalid turn indicator: {parts[1]}")

    # Check the castling availability part
    if not all(c in 'KQkq-' for c in parts[2]):
        raise ValueError(f"FEN string has invalid castling availability: {parts[2]}")

    if parts[3] != '-' and not (len(parts[3]) == 2 and parts[3][0] in 'abcdefgh' and parts[3][1] in '36'):
        raise ValueError(f"FEN string has invalid en passant target square: {parts[3]}")

    if not parts[4].isdigit():
        raise ValueError(f"FEN string has invalid half move clock value: {parts[4]}")
    
    if not parts[5].isdigit():
        raise ValueError(f"FEN string has invalid full move counter value: {parts[5]}")


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
    try:
        my_board = defaultBoard()
        print(my_board)
    except ValueError as e:
        print(e)
