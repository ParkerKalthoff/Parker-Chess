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

        self.past_positions = past_positions if past_positions else [] # game move history

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

        self.refresh_board(initialRefresh=True)

    def combine_lists(self, input_list : list[list[int]]) -> list[int]:
        """ Returns a flat representation of a 2d array """
        return [item for list in input_list for item in list]

    def next_turn(self) -> None:
        self.is_whites_turn = not self.is_whites_turn
        self.past_positions.append(self.to_FEN())

        if self.is_whites_turn:
            self.full_move_number += 1

    def white_piece_indices(self) -> list[int]:
        return [piece.pos() for piece in self._white_pieces]

    def black_piece_indices(self) -> list[int]:
        return [piece.pos() for piece in self._black_pieces]

    def white_score(self) -> int:
        return self._white_score

    def black_score(self) -> int:
        return self._black_score

    def get_score(self) -> int:
        return self.white_score() - self.black_score()
    
    def get_turn(self) -> bool:
        return self.is_whites_turn

    def refresh_board(self, initialRefresh = False) -> int:
        """ Refreshes internal board values after piece moves 
            >>> InitalRefresh is to not overwrite initial values set by the same, may remove
        """

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
                else: # piece.getColor() == 'Black'
                    piece.setPos(index)
                    self._black_pieces.append(piece)
                    self._black_score += self.PIECE_VALUES[type(piece)]


        self.piece_vision()


        a = [piece for piece in self._black_pieces if isinstance(piece, King)][0]
        b = [piece for piece in self._white_pieces if isinstance(piece, King)][0]
        print(f"{a} , {a.getVision()} , {a.pos()}")
        print(f"{b} , {b.getVision()} , {b.pos()}")

        if initialRefresh: # set castling rights and pos
            for piece in self._white_pieces:
                if isinstance(piece, Rook):
                    if piece.pos() == 63:
                        piece.setCastlingCondition(1,self.castling)
                    if piece.pos() == 56:
                        piece.setCastlingCondition(2,self.castling)
            for piece in self._white_pieces:
                if isinstance(piece, Rook):
                    if piece.pos() == 7:
                        piece.setCastlingCondition(3,self.castling)
                    if piece.pos() == 0:
                        piece.setCastlingCondition(4,self.castling)

        # 3. Check for Checks
        enemy_sight_on_king = self.checks_on_active_king()

        if enemy_sight_on_king: # using to make code more readible, enemy_sight_on_king is either [] or [[1,2,3]] or [[1,2,3], [1,2]]
            print('Check!')
            self._inCheck = True

        if self._inCheck: # culls non check preventing moves from other pieces
            if self.is_whites_turn: # if white is active player
                for piece in self._white_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)
            else: # if black is active 
                for piece in self._black_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)

        allowed_castles = self.check_if_castling_blocked()

        self.update_legal_moves()
        print('ulm')


        if not self._inCheck:
            if self.is_whites_turn:
                for piece in self._white_pieces:
                    if isinstance(piece, King):
                        if allowed_castles[0]:
                            piece.valid_moves.append('O-O')    
                        if allowed_castles[1]:
                            piece.valid_moves.append('O-O-O')  
            else:
                for piece in self._black_pieces:
                    if isinstance(piece, King):
                        if allowed_castles[2]:
                            piece.valid_moves.append('O-O')    
                        if allowed_castles[3]:
                            piece.valid_moves.append('O-O-O')  
                        
        # 4. Check for Checkmates or Stalemates

        if not self.active_player_legal_moves():
            if self._inCheck:
                print('Checkmate!')
            print('Stalemate!')

    def movePiece(self, original_index : str, new_index : str) -> str:
        """ Returns 'Valid' or 'Invalid' and updates board state """
        original_index = self.coordToInt(original_index)

        if new_index not in ['O-O-O', 'O-O']: # checks if move is a castle move
            new_index = self.coordToInt(new_index) # converts new_index to a int 0-63
        else: # Castle
            if not self.is_whites_turn and isinstance(self.get_square(60), King) and self.get_square(60).getColor() == 'Black' and new_index in self.get_square(60).getMoves():
                    if new_index == 'O-O-O': # ♖___♔___ -> __♔♖____ 
                        self.get_square(60).disableCastling()
                        self._board_space[58] = self.get_square(60)
                        self._board_space[59] = self._board_space[56]
                        self._board_space[60] = None
                        self._board_space[56] = None
                    else: # new_index == 'O-O' ____♔__♖ -> _____♖♔_
                        self.get_square(60).disableCastling()
                        self._board_space[62] = self.get_square(60)
                        self._board_space[61] = self._board_space[63]
                        self._board_space[60] = None
                        self._board_space[63] = None
            elif self.is_whites_turn and isinstance(self.get_square(4), King) and self.get_square(4).getColor() == 'Black' and new_index in self.get_square(4).getMoves():
                    if new_index == 'O-O': # ♜__♚____ -> _♚♜_____ 
                        self.get_square(4).disableCastling()
                        self._board_space[2] = self.get_square(4)
                        self._board_space[3] = self._board_space[0]
                        self._board_space[4] = None
                        self._board_space[0] = None
                    else: # new_index == 'O-O-O' ___♚___♜ -> ____♜♚__ 
                        self.get_square(4).disableCastling()
                        self._board_space[6] = self.get_square(4)
                        self._board_space[5] = self._board_space[7]
                        self._board_space[4] = None
                        self._board_space[7] = None


        # Normal Move

        if not self.get_square(original_index):
            print('Invalid: Empty Square')
            return 'Invalid'

        selected_piece = self.get_square(original_index)
        
        selected_piece = self.get_square(original_index)

        if selected_piece.getColor() == "White" and self.is_whites_turn:
            turn_color = "White"
        elif selected_piece.getColor() == "Black" and not self.is_whites_turn:
            turn_color = "Black"
        else:
            print('Invalid: Wrong color piece for the current turn')
            return 'Invalid'

        if new_index in selected_piece.getMoves():
            print(f'{selected_piece} Moved {original_index} to {new_index}')
            temp = self._board_space[original_index] # piece ref, storing in var to 
            self._board_space[original_index] = None
            self._board_space[new_index] = temp
            if isinstance(self._board_space[new_index], (King, Rook)):
                self._board_space[new_index].disableCastling()
            if isinstance(self._board_space[new_index], Pawn) and self._board_space[new_index].__canEnpassant__:
                self.enpassant_square = self._board_space[new_index].pos() -  8 if self._board_space[new_index].getColor() == 'White' else -8
                self._board_space[new_index].__canEnpassant__ = False
            return 'Valid'
        else:
            print(f'Invalid: Must move a {turn_color} piece')
            return 'Invalid'

            
        
    def check_if_castling_blocked(self) -> list[bool]:
        """ 
            Returns a list of allowed Castling moves, based on enemy piece vision and friendly piece placement
            >>> Bools for [ K, Q, k, q ] castling
            trying to keep this method really general
        """
        
        white_kingside = [61,62]
        white_queenside = [57,58,59]
        black_kingside = [5,6]
        black_queenside = [1,2,3]

        castling_squares_list = [white_kingside, white_queenside, black_kingside, black_queenside]

        white_vision = self.combine_lists(self.white_piece_vision())
        black_vision = self.combine_lists(self.black_piece_vision())

        permitted_castling = []

        if self._inCheck:
            return [False, False, False, False] # no castling in check

        for list_index, castling_squares in enumerate(castling_squares_list):
            valid_to_castle = True
            for square in castling_squares:
                if list_index in [0, 1]:  # white castling indexes
                    if square in black_vision or self.get_square(square):
                        valid_to_castle = False
                        break
                elif list_index in [2, 3]:  # black castling indexes
                    if square in white_vision or self.get_square(square):
                        valid_to_castle = False
                        break
            permitted_castling.append(valid_to_castle)

    
        legal_castling = [] # Does a logical 'and' to return moves that are both not putting king in check and are legal
        for valid_castle, permitted_castle in zip(self.castling, permitted_castling):
            legal_castling.append(valid_castle and permitted_castle)

        return legal_castling

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
        

    def piece_vision(self):
        if self.is_whites_turn:
            for piece in self._black_pieces:
                piece.unpin()
            for piece in self._white_pieces:
                if not isinstance(piece, King):
                    piece.updateVision(self)
            for piece in self._white_pieces:
                piece.unpin()
            for piece in self._black_pieces:
                if not isinstance(piece, King):
                    piece.updateVision(self)
            [piece for piece in self._black_pieces if isinstance(piece, King)][0].updateVision(self)
            [piece for piece in self._white_pieces if isinstance(piece, King)][0].updateVision(self)
        else:
            for piece in self._white_pieces:
                piece.unpin()
            for piece in self._black_pieces:
                if not isinstance(piece, King):
                    piece.updateVision(self)
            for piece in self._black_pieces:
                piece.unpin()
            for piece in self._white_pieces:
                if not isinstance(piece, King):
                    piece.updateVision(self)
            [piece for piece in self._black_pieces if isinstance(piece, King)][0].updateVision(self)
            [piece for piece in self._white_pieces if isinstance(piece, King)][0].updateVision(self)


    def update_legal_moves(self):
        """ loops over pieces to update internal legal moves """

        for piece in self._white_pieces:
            piece.visionToMoves()
        for piece in self._black_pieces:
            piece.visionToMoves()

    def active_player_legal_moves(self):
        if self.is_whites_turn:
            return self.combine_lists([piece.getMoves() for piece in self._white_pieces])
        else:
            return self.combine_lists([piece.getMoves() for piece in self._black_pieces])

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

    def intToCoord(self, index):
        if not (0 <= index <= 63):
            raise ValueError("Index must be in the range 0-63.")
        file = chr(ord('a') + (index % 8))
        rank = str((index // 8) + 1)
        return file + rank

    def coordToInt(self, coord):
        if len(coord) != 2 or coord[0] not in 'abcdefgh' or coord[1] not in '12345678':
            raise ValueError("Coordinate must be in the format 'a1' to 'h8'.")
        file = coord[0]
        rank = coord[1]
        index = (ord(file) - ord('a')) + (int(rank) - 1) * 8
        return index

    def piece_moves(self, position: int) -> list[int]:
        piece = self._board_space[position]
        return piece.getMoves(position, self) if piece else []

    def get_square(self, position: int) -> Piece | None:
        return self._board_space[position]

    def get_all_pieces(self) -> list[Piece]:
        """ Unused, leaving for now"""
        return self._white_pieces + self._black_pieces

    def white_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of white pieces vision """
        return [piece.getVision() for piece in self._white_pieces]

    def black_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of black pieces vision """
        return [piece.getVision() for piece in self._black_pieces]

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


