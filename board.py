import os
import sys
from xmlrpc.client import Boolean
from pieces.abstractPiece import Piece
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
from typing import List, Optional

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

class BoardSizeError(Exception):
    """Custom exception for board size errors."""
    pass

class Board:
    def __init__(self, board_space: List[Optional[Piece]], is_whites_turn: bool, castling_rights: List[bool], enpassant_sq: int, half_move_clock: int, full_move_number: int):

        self._board_space = board_space
        self.half_move_clock = half_move_clock
        self.full_move_number = full_move_number
        self.castling = castling_rights
        self.enpassant_square = enpassant_sq
        self.is_whites_turn = is_whites_turn

        self._white_piece_indices = []
        self._black_piece_indices = []

        self._white_piece_objects = []
        self._black_piece_objects = []

        self._white_piece_vision = []
        self._black_piece_vision = []


        self._white_score = 0
        self._black_score = 0

        self.inCheck = False

        self.PIECE_VALUES = {
            Queen: 9,
            Rook: 5,
            Bishop: 3,
            Knight: 3,
            Pawn: 1,
            King: 999
        }

        self.refresh_board()

    def next_turn(self) -> None:
        self.is_whites_turn = not self.is_whites_turn

    def white_piece_indices(self) -> List[int]:
        return self._white_piece_indices

    def black_piece_indices(self) -> List[int]:
        return self._black_piece_indices

    def white_score(self) -> int:
        return self._white_score

    def black_score(self) -> int:
        return self._black_score

    def get_score(self) -> int:
        return self.white_score() - self.black_score()

    def get_turn(self) -> bool:
        return self.is_whites_turn

    def refresh_board(self, Override = True) -> int:
        """ Refreshes internal board values after piece moves """

        if len(self.get_board()) > 64:
            raise BoardSizeError("Board size exceeds 64 squares.")

        self._white_piece_indices = []
        self._black_piece_indices = []
        self._white_piece_objects = []
        self._black_piece_objects = []
        self._white_score = 0
        self._black_score = 0

        for index, piece in enumerate(self._board_space):
            if piece:
                if piece.getColor() == 'White':
                    self._white_piece_indices.append(index)
                    self._white_piece_objects.append(piece)
                    self._white_score += self.PIECE_VALUES[type(piece)]
                else:
                    self._black_piece_indices.append(index)
                    self._black_piece_objects.append(piece)
                    self._black_score += self.PIECE_VALUES[type(piece)]

    def get_board(self) -> List[Optional[Piece]]:
        return self._board_space

    def piece_moves(self, position: int) -> List[int]:
        piece = self._board_space[position]
        return piece.getMoves(position, self) if piece else []

    def get_square(self, position: int) -> Optional[Piece]:
        return self._board_space[position]

    def white_piece_objects(self) -> List[dict]:
        return self._white_piece_objects

    def black_piece_objects(self) -> List[dict]:
        return self._black_piece_objects

    def piece_objects(self) -> List[dict]:
        return self.white_piece_objects() + self.black_piece_objects()

    def __str__(self, with_chess_coords: bool = False) -> str:
        column_num = ['1', '2', '3', '4', '5', '6', '7', '8']
        output_str = " _______________________________\n"
        if with_chess_coords:
            output_str = "  " + output_str
        for row in range(8):
            row_str = "|"
            if with_chess_coords:
                row_str = column_num[row] + "-" + row_str
            for col in range(8):
                piece = self._board_space[row * 8 + col]
                row_str += f"{'_' + piece.__str__() +'_' if piece else '___'}|"
            output_str += row_str + "\n"
        if with_chess_coords:
            output_str += "    a   b   c   d   e   f   g   h"
        return output_str

    def displayBoard(self) -> str:
        return self.__str__(with_chess_coords=True)


