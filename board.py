
from pieces.abstractPiece import Piece
from pieces.queen import Queen
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn

class BoardSizeError(Exception):
    """Custom exception for board size errors."""
    pass

class Board:
    def __init__(self, board_space: list[Piece], is_whites_turn: bool, castling_rights: list[bool], enpassant_sq: int, half_move_clock: int, full_move_number: int, past_positions : list[str] = None):
        """ 
            Variables : 
                board_space : a 64 length list of type Piece or None 
                is_whites_turn: a bool of whites turn or not
                castling_rights: 
                enpassant_sq: int, 
                half_move_clock: int, 
                full_move_number: int, 
                past_positions : list[str] 
        """

        self._board_space = board_space
        self.half_move_clock = half_move_clock
        self.full_move_number = full_move_number
        self.castling = castling_rights
        self.enpassant_square = enpassant_sq
        self.is_whites_turn = is_whites_turn

        self.past_positions = past_positions # game move history

        self._white_piece_indices = []
        self._black_piece_indices = []

        self._white_pieces = []
        self._black_pieces = []

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

    def white_piece_indices(self) -> list[int]:
        return self._white_piece_indices

    def black_piece_indices(self) -> list[int]:
        return self._black_piece_indices

    def white_score(self) -> int:
        return self._white_score

    def black_score(self) -> int:
        return self._black_score

    def get_score(self) -> int:
        return self.white_score() - self.black_score()

    def get_turn(self) -> bool:
        return self.is_whites_turn

    def refresh_board(self, InitialRefresh = False) -> int:
        """ Refreshes internal board values after piece moves """

        if len(self._board_space) > 64:
            raise BoardSizeError("Board size exceeds 64 squares.")

        self._white_piece_indices = []
        self._black_piece_indices = []
        self._white_pieces = []
        self._black_pieces = []

        self._inCheck = False

        self._white_score = 0
        self._black_score = 0

        for index, piece in enumerate(self._board_space):
            if piece:
                if piece.getColor() == 'White':
                    piece.setPos(index)
                    self._white_pieces.append(piece)
                    self._white_score += self.PIECE_VALUES[type(piece)]
                else:
                    piece.setPos(index)
                    self._black_pieces.append(piece)
                    self._black_score += self.PIECE_VALUES[type(piece)]

        if self.is_whites_turn: # this step might need to be refactored for clarity (idk if it matters whose turn)
            for piece in self._white_pieces:
                piece.unpin()
            for position, piece in zip(self._black_piece_indices, self._black_pieces):
                piece.updateVision(position, self)
            for piece in self._black_pieces:
                piece.unpin()
            for position, piece in zip(self._white_piece_indices, self._white_pieces):
                piece.updateVision(position, self)
        else:
            for piece in self._black_pieces:
                piece.unpin()
            for position, piece in zip(self._white_piece_indices, self._white_pieces):
                piece.updateVision(position, self)
            for piece in self._white_pieces:
                piece.unpin()
            for position, piece in zip(self._black_piece_indices, self._black_pieces):
                piece.updateVision(position, self)

        # 3. Check for Checks
        enemy_sight_on_king = self.checks_on_active_king()

        if enemy_sight_on_king: # If there is sight line on king, this will be false
            self._inCheck = True

        if self._inCheck: # culls non check preventing moves from other pieces
            if self.is_whites_turn:
                for piece in self._white_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)
            else:
                for piece in self._black_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)

        # 4. Check for Checkmates or Stalemates

        # 5. Update Legal Moves

        # 6. Promote Pawns

        # 7. Threefold Repetition and Fifty-Move Rule (if applicable)

    def movePiece(self, original_index : str, new_index : str):
        
        if new_index in ['O-O', 'O-O-O']:
            
            if self.is_whites_turn:

                raise ValueError()
        
        
        

    def checks_on_active_king(self) -> list[list[int]] | None:
        """ Checks for checks on board, based on current board state and Active Player in position"""

        if self.is_whites_turn:
            # White is currently active player
            activePlayersKing = [piece for piece in self._white_pieces if isinstance(piece, King)][0]
            previousPlayerVision = self.black_piece_vision()
        else: 
            # Black is currently active player
            activePlayersKing = [piece for piece in self._black_pieces if isinstance(piece, King)][0]
            previousPlayerVision = self.white_piece_vision()

        enemy_line_of_sight_on_king = [pieceVision for pieceVision in previousPlayerVision if activePlayersKing.pos() in pieceVision]
        # this is the vision lines of the enemy on active players king, this will be used to detect double checks

        return enemy_line_of_sight_on_king

    def check_for_no_remaining_moves(self) -> bool:
        """ Checks if no remaining moves are allowed, in tandem with check_for_checks, this can detect checkmate or stalemate """
        pass

    def update_legal_moves(self):
        """ loops over pieces to update internal legal moves """
        pass

    def check_threefold_repeition(self) -> bool:
        """ Checks if position has been reached 3 times in a game, resulting in stalemate 
            >>> Returns True for stalemate and False for continued game
        """
        pass

    def check_fifty_move_rule(self) -> bool:
        """ Checks if no pawns have moved and no captures in 50 moves """
        pass

    def stalemateByMaterial(self) -> bool:
        """ Checks for stalemate by lack of material
            >>> Cases 
        """

    def to_FEN(self) -> str:
        """ Changes board representation to FEN string"""

        # board string

        board_string = ''
        rank_board_string = ''
        empty_space_count = 0

        for index, square in enumerate(self._board_space):
            if index % 8 == 7:  # End of the rank
                if square:

                    if empty_space_count:

                        rank_board_string += str(empty_space_count)
                        empty_space_count = 0
                    rank_board_string += square.toChar()

                else:

                    empty_space_count += 1
                    if empty_space_count:
                        rank_board_string += str(empty_space_count)
                        empty_space_count = 0
                board_string += rank_board_string

                if index != 63:  # cant add / at end of board string
                    board_string += '/'
                rank_board_string = ''
                empty_space_count = 0

            else:
                if square:
                    if empty_space_count:
                        rank_board_string += str(empty_space_count)
                        empty_space_count = 0
                    rank_board_string += square.toChar()
                else:
                    empty_space_count += 1

    # Ensure empty spaces at the end of the last rank are accounted for
        if empty_space_count:
            rank_board_string += str(empty_space_count)

        turn_string = 'w' if self.is_whites_turn else 'b'

        castling_rights = ''
        if self.castling[0]: castling_rights += 'K'
        if self.castling[1]: castling_rights += 'Q'
        if self.castling[2]: castling_rights += 'k'
        if self.castling[3]: castling_rights += 'q'
        if not castling_rights: castling_rights = '-'

        enpassant_string = ''
        if self.enpassant_square:
            enpassant_string = f'{chr((self.enpassant_square % 8) + 97)}{(self.enpassant_square // 8) + 1}'
        else:
            enpassant_string = '-'

        return f'{board_string} {turn_string} {castling_rights} {enpassant_string} {self.half_move_clock} {self.full_move_number}'

    def piece_moves(self, position: int) -> list[int]:
        piece = self._board_space[position]
        return piece.getMoves(position, self) if piece else []

    def get_square(self, position: int) -> Piece | None:
        return self._board_space[position]

    def get_all_pieces(self) -> list[Piece]:
        """ Unused, leaving for now"""
        return self._white_pieces + self._black_pieces

    def combine_lists(input_list : list[list[int]]) -> list[int]:
        """ Returns a flat representation of a 2d array """
        return [item for list in input_list for item in list]

    def white_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of white pieces vision """
        return [piece.getMoves() for piece in self._white_pieces]

    def black_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of black pieces vision """
        return [piece.getMoves() for piece in self._black_pieces]

    def __str__(self, with_chess_coords: bool = False) -> str:
        column_num = ['1', '2', '3', '4', '5', '6', '7', '8']
        output_str = " _______________________________________\n"
        if with_chess_coords:
            output_str = "  " + output_str
        for row in range(8):
            row_str = "|"
            if with_chess_coords:
                row_str = column_num[row] + "-" + row_str
            for col in range(8):
                piece = self._board_space[row * 8 + col]
                row_str += f"{'_' + piece.__str__() +'__' if piece else '____'}|"
            output_str += row_str + "\n"
        if with_chess_coords:
            output_str += "     a    b    c    d    e    f    g    h"
            output_str += f"\n Score : {self.get_score()}, Active turn : {'w' if self.is_whites_turn else 'b'}, Turn : {self.full_move_number}"
        return output_str

    def display_board(self) -> str:
        return self.__str__(with_chess_coords=True)


