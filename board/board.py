from collections import defaultdict
from ..board.pieces.abstractPiece import Piece
from ..board.pieces.queen import Queen
from ..board.pieces.king import King
from ..board.pieces.bishop import Bishop
from ..board.pieces.knight import Knight
from ..board.pieces.rook import Rook
from ..board.pieces.pawn import Pawn

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

        self._game_finished = False
        self._game_winner = None # Stalemate, White, Black
        self._past_positions_count = defaultdict(lambda: 0) # used for threefold repition check

        self.past_positions = past_positions if past_positions else [] # game move history

        self._white_pieces = []
        self._black_pieces = []

        self._white_piece_counts = [0,0,0,0,0] # an array with a count of the pieces for stalemate determination
        self._black_piece_counts = [0,0,0,0,0] # [P, B, N, R, Q] expl : [8, 2, 2, 2, 1]

        self.white_score = 0
        self.black_score = 0

        self._inCheck = False

        self.PIECE_VALUES = {
            Queen: 9,
            Rook: 5,
            Bishop: 3,
            Knight: 3,
            Pawn: 1,
            King: 999
        }

        self._refresh_board(initialRefresh=True)

    def print_active_moves(self):
        if self.is_whites_turn:
            for piece in self._white_pieces:
                if isinstance(piece, Pawn) and 8 <= piece.pos() <= 15:
                    promote_moves = []
                    for move in piece.getMoves():
                        promote_moves += [f'{move}=B', f'{move}=N', f'{move}=R', f'{move}=Q']
                    print(
                    self.intToCoord(piece.pos()),
                    piece,
                    [f'{self.intToCoord(int(move.split("=")[0]))}={move.split("=")[1]}' for move in promote_moves])
                else:
                    print(self.intToCoord(piece.pos()), piece, [self.intToCoord(move) for move in piece.getMoves()])
        else:
            for piece in self._black_pieces:
                if isinstance(piece, Pawn) and 48 <= piece.pos() <= 55:
                    promote_moves = []
                    for move in piece.getMoves():
                        promote_moves += [f'{move}=B', f'{move}=N', f'{move}=R', f'{move}=Q']
                    print(self.intToCoord(piece.pos()), piece, [f'{self.intToCoord(int(move.split("=")[0]))}={move.split("=")[1]}' for move in promote_moves])
                else:
                    print(self.intToCoord(piece.pos()), piece, [self.intToCoord(move) for move in piece.getMoves()])



    def combine_lists(self, input_list : list[list[int]]) -> list[int]:
        """ Returns a flat representation of a 2d array """
        return [item for list in input_list for item in list]

    def _next_turn(self) -> None:
        self.is_whites_turn = not self.is_whites_turn
        self.past_positions.append(self.to_FEN())

        if self.is_whites_turn:
            self.full_move_number += 1

    def white_piece_indices(self) -> list[int]:
        return [piece.pos() for piece in self._white_pieces]

    def black_piece_indices(self) -> list[int]:
        return [piece.pos() for piece in self._black_pieces]

    def _white_score(self) -> int:
        return self.white_score

    def _black_score(self) -> int:
        return self.black_score

    def _get_score(self) -> int:
        """ Returns the material difference """
        return self._white_score() - self._black_score()
    
    def evaluate(self):
        """ Returns score, Win condition, or statemate"""

        if self._game_finished:
            if self._game_winner == 'White':
                return 1000
            if self._game_winner == 'Black':
                return -1000
            if self._game_winner == 'Stalemate':
                return 0
        return self._get_score()
    
    def _piece_to_json(self, piece_list : list[Piece]):
        return_piece_list = []
        for piece in piece_list:
            if isinstance(piece, Pawn) and 48 <= piece.pos() <= 55:
                promote_moves = []
                for move in piece.getMoves():
                    promote_moves += [f'{move}=B', f'{move}=N', f'{move}=R', f'{move}=Q']
                return_piece_list.append({
                                            'position': self.intToCoord(piece.pos()), 
                                            'piece': piece.toChar(), 
                                            'moves': [f'{self.intToCoord(int(move.split("=")[0]))}={move.split("=")[1]}' for move in promote_moves]})
            else:
                return_piece_list.append({
                                            'position': self.intToCoord(piece.pos()), 
                                            'piece': piece.toChar(), 
                                            'moves': [self.intToCoord(move) for move in piece.getMoves()]})
        return return_piece_list

    def white_piece_to_json(self):
        if self.is_whites_turn:
            return self._piece_to_json(self._white_pieces)
        else:
            obj = self._piece_to_json(self._white_pieces)

            for item in obj:
                item['moves'] = []
        return obj
    
    def black_piece_to_json(self):
        if not self.is_whites_turn:
            return self._piece_to_json(self._white_pieces)
        else:
            obj = self._piece_to_json(self._white_pieces)

            for item in obj:
                item['moves'] = []
        return obj
    
    def get_turn(self) -> str:
        return "White" if self.is_whites_turn else "Black"

    def _refresh_board(self, initialRefresh=False) -> int:
        """ Refreshes internal board values after piece moves 
            >>> InitalRefresh is to not overwrite initial values set by the same, may remove
        """

        if len(self._board_space) > 64:
            raise BoardSizeError("Board size exceeds 64 squares.")

        self._white_pieces = []
        self._black_pieces = []

        self._inCheck = False

        self.white_score = 0
        self.black_score = 0

        for index, piece in enumerate(self._board_space):
            if piece:
                if piece.getColor() == 'White':
                    piece.setPos(index)
                    self._white_pieces.append(piece)
                    self.white_score += self.PIECE_VALUES[type(piece)]
                else:  # piece.getColor() == 'Black'
                    piece.setPos(index)
                    self._black_pieces.append(piece)
                    self.black_score += self.PIECE_VALUES[type(piece)]

        self.piece_vision()

        if initialRefresh:  # set castling rights and pos
            for piece in self._white_pieces:
                if isinstance(piece, Rook):
                    if piece.pos() == 63:
                        piece.setCastlingCondition(1, self.castling)
                    elif piece.pos() == 56:
                        piece.setCastlingCondition(2, self.castling)
                    else:
                        piece.setCastlingCondition(5, self.castling)
                if isinstance(piece, King):
                    piece.setCastlingCondition(self.castling)
            for piece in self._black_pieces:
                if isinstance(piece, Rook):
                    if piece.pos() == 7:
                        piece.setCastlingCondition(3, self.castling)
                    elif piece.pos() == 0:
                        piece.setCastlingCondition(4, self.castling)
                    else:
                        piece.setCastlingCondition(5, self.castling)
                if isinstance(piece, King):
                    piece.setCastlingCondition(self.castling)

        # Check for Checks
        enemy_sight_on_king = self._checks_on_active_king()

        if enemy_sight_on_king:  # using to make code more readable, enemy_sight_on_king is either [] or [[1,2,3]] or [[1,2,3], [1,2]]
            self._inCheck = True



        # Update Legal Moves
        self._update_legal_moves()

        if not initialRefresh:
            self.enpassant_square = None

        if self._inCheck:  # culls non check preventing moves from other pieces
            if self.is_whites_turn:  # if white is active player
                for piece in self._white_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)
            else:  # if black is active
                for piece in self._black_pieces:
                    if not isinstance(piece, King):
                        piece.movesPreventingCheck(enemy_sight_on_king)

        allowed_castles = self.check_if_castling_blocked()
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

        # Check for Checkmates or Stalemates
        if not self._active_player_legal_moves():
            if self._inCheck:
                self._game_finished = True
                self._game_winner = 'White' if self.is_whites_turn else 'Black'
            else:
                self._game_finished = True
                self._game_winner = 'Stalemate'

        # Update Move History
        self.past_positions.append(self.to_FEN())

        # self.check_fifty_move_rule

        if self.half_move_clock >= 100:
            self._game_finished = True
            self._game_winner = 'Stalemate'

        if self._game_finished:
            return

        self.check_threefold_repeition()
        self.stalemateByMaterial()


    def move(self, piece_move : str):
        """ Moving piece, 
            A1 to A2 : 'A1A2'
            D1 to O-O-O : 'D1O-O-O'
            D7 to D8 Queen : 'D7D8=Q'
            """
        
        if len(piece_move) < 4:
            ValueError(f'Move Sent is {piece_move}, invalid bro')

        self.move_coord(piece_move[:2], piece_move[2:])

    def move_coord(self, original_index : str, new_index : str):
        """using strs"""

        active_piece = self.get_square(self.coordToInt(original_index))

        if isinstance(active_piece, Pawn): # checking if player is trying to move pawn to promotion
            if active_piece.getColor() == 'White' and 8 <= active_piece.pos() <= 15: # ready for promotion

                move = new_index.split('=')

                if len(move) != 2:
                    raise ValueError(f'Move should include promotion ("A1=Q"), actual move {move} ')
                
                if move[1] not in ['B', 'N', 'R', 'Q']:
                    raise ValueError(f'The promotion indicated is invalid {move[1]}')

                self._movePiece(self.coordToInt(original_index), self.coordToInt(move[0]))

                promoted_piece = None

                if move[1] == 'B':
                    promoted_piece = Bishop('White')
                elif move[1] == 'N':
                    promoted_piece = Knight('White')
                elif move[1] == 'R':
                    promoted_piece = Rook('White')
                elif move[1] == 'Q':
                    promoted_piece = Queen('White')
                else:
                    raise ValueError(f'The promotion indicated is invalid {move[1]}')

                self._board_space[self.coordToInt(move[0])] = promoted_piece

            elif active_piece.getColor() == 'Black' and 48 <= active_piece.pos() <= 55: # ready for promotion

                move = new_index.split('=')

                if len(move) != 2:
                    raise ValueError(f'Move should include promotion ("A1=Q"), actual move {move} ')
                
                if move[1] not in ['B', 'N', 'R', 'Q']:
                    raise ValueError(f'The promotion indicated is invalid {move[1]}')


                self._movePiece(self.coordToInt(original_index), self.coordToInt(move[0]))

                promoted_piece = None

                if move[1] == 'B':
                    promoted_piece = Bishop('Black')
                elif move[1] == 'N':
                    promoted_piece = Knight('Black')
                elif move[1] == 'R':
                    promoted_piece = Rook('Black')
                elif move[1] == 'Q':
                    promoted_piece = Queen('Black')
                else:
                    raise ValueError(f'The promotion indicated is invalid {move[1]}')

                self._board_space[self.coordToInt(move[0])] = promoted_piece

            else: # pawn not promoting
                self._movePiece(self.coordToInt(original_index), self.coordToInt(new_index))
        else: # normal piece
            self._movePiece(self.coordToInt(original_index), self.coordToInt(new_index))

        self._refresh_board()

    def _movePiece(self, original_index : int, new_index : int | str) -> None:
        """ Pass in Starting and ending coords (5, O-O-O), doesn't support direct promotion use other method !!
        """

        if new_index in ['O-O-O', 'O-O']: # checks if move is a castle move
            if not self.is_whites_turn and isinstance(self.get_square(4), King) and self.get_square(4).getColor() == 'Black' and new_index in self.get_square(4).getMoves():
                    if new_index == 'O-O-O': # ♜__♚____ -> _♚♜_____ 
                        self.get_square(4).disableCastling()
                        self._board_space[2] = self.get_square(4)
                        self._board_space[3] = self._board_space[0]
                        self._board_space[4] = None
                        self._board_space[0] = None
                        self.half_move_clock += 1
                        self._next_turn()
                        return
                    else: # new_index == 'O-O-O' ___♚___♜ -> ____♜♚__ 
                        self.get_square(4).disableCastling()
                        self._board_space[6] = self.get_square(4)
                        self._board_space[5] = self._board_space[7]
                        self._board_space[4] = None
                        self._board_space[7] = None
                        self.half_move_clock += 1
                        self._next_turn()
                        return
            elif self.is_whites_turn and isinstance(self.get_square(60), King) and self.get_square(60).getColor() == 'White' and new_index in self.get_square(60).getMoves():
                if new_index == 'O-O-O': # ♖___♔___ -> __♔♖____ 
                    self.get_square(60).disableCastling()
                    self._board_space[58] = self.get_square(60)
                    self._board_space[59] = self._board_space[56]
                    self._board_space[60] = None
                    self._board_space[56] = None
                    self.half_move_clock += 1
                    self._next_turn()
                    return
                else: # new_index == 'O-O' ____♔__♖ -> _____♖♔_
                    self.get_square(60).disableCastling()
                    self._board_space[62] = self.get_square(60)
                    self._board_space[61] = self._board_space[63]
                    self._board_space[60] = None
                    self._board_space[63] = None
                    self.half_move_clock += 1
                    self._next_turn()
                    return
        # Normal Move

        if not self.get_square(original_index):
            raise ValueError('Invalid: Empty Square')

        selected_piece = self.get_square(original_index)
        
        selected_piece = self.get_square(original_index)

        if selected_piece.getColor() == "White" and self.is_whites_turn:
            turn_color = "White"
        elif selected_piece.getColor() == "Black" and not self.is_whites_turn:
            turn_color = "Black"
        else:
            raise ValueError('Invalid: Wrong color piece for the current turn')

        if new_index in selected_piece.getMoves():
            moving_piece = self._board_space[original_index] # piece ref, storing in var to poop
            self._board_space[original_index] = None

            if self._board_space[new_index]:
                self.half_move_clock = 0 # capture

            if isinstance(self._board_space[new_index], Rook):
                self._board_space[new_index].disableCastling()

            self._board_space[new_index] = moving_piece
            if isinstance(moving_piece, (King, Rook)): # either king or rook disabling castling
                moving_piece.disableCastling()
            if isinstance(moving_piece, Pawn): # special rules pawns
                self.half_move_clock = 0 # pawn move
                if moving_piece.__canEnpassant__: # If pawn can enpassant
                    if abs(original_index - new_index) == 16: # if pawn enpassants
                        self.enpassant_square = new_index - (-8 if moving_piece.getColor() == 'White' else 8)
                    moving_piece.__canEnpassant__ = False # otherwise disable enpassant
                self._board_space[new_index + (8 if moving_piece.getColor() == 'White' else -8)] = None # otherwise checking if pawn takes piece by enpassant, having to remove a pawn thats a rank higher
            self.half_move_clock += 1
            self._next_turn()
            return 'Valid'
        else:
            raise ValueError(f'Invalid: Must move a {turn_color} piece')

            
        
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

        white_vision = self.combine_lists(self._white_piece_vision())
        black_vision = self.combine_lists(self._black_piece_vision())

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

    def _checks_on_active_king(self) -> list[list[int]] | None:
        """ Checks for checks on board, based on current board state and Active Player in position"""

        if self.is_whites_turn:
            # White is currently active player
            activePlayersKing = [piece for piece in self._white_pieces if isinstance(piece, King)][0]
            previousPlayerPieces = self._black_pieces
        else: 
            # Black is currently active player
            activePlayersKing = [piece for piece in self._black_pieces if isinstance(piece, King)][0]
            previousPlayerPieces = [piece for piece in self._white_pieces]

        enemies_attacking_king = [piece for piece in previousPlayerPieces if activePlayersKing.pos() in piece.getVision()]
        
        enemy_line_of_sight_on_king = []
        for piece in enemies_attacking_king:
            if isinstance(piece, Pawn):
                enemy_line_of_sight_on_king.append([activePlayersKing.pos(), piece.pos()])
            elif isinstance(piece, Knight):
                enemy_line_of_sight_on_king.append([piece.pos()])
            else:
                enemy_line_of_sight_on_king.append(piece.kingsight + [piece.pos()])

        # this is the vision lines of the enemy on active players king, this will be used to detect double checks

        return enemy_line_of_sight_on_king

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


    def _update_legal_moves(self):
        """ loops over pieces to update internal legal moves """

        if self.is_whites_turn:
            for piece in self._white_pieces:
                if isinstance(piece, (Pawn, King)):
                    piece.visionToMoves(self)
                else:
                    piece.visionToMoves()
        else:
            for piece in self._black_pieces:
                if isinstance(piece, (Pawn, King)):
                    piece.visionToMoves(self)
                else:
                    piece.visionToMoves()


    def _active_player_legal_moves(self):
        """ Returns a flat list of legal moves that can be used, mainly for checkmate detection """
        if self.is_whites_turn:
            return self.combine_lists([piece.getMoves() for piece in self._white_pieces])
        else:
            return self.combine_lists([piece.getMoves() for piece in self._black_pieces])

    def load_past_positions(self) -> bool:
        """ loads past positions, doesn't check for stalemate
        """
        for fen_string in self.past_positions:
            position_string = ''
            for index, part in enumerate(fen_string.split()): # index from 0 to 3
                if index == 4:
                    break
                position_string += part
            self._past_positions_count[f'{position_string}'] += 1

    def check_threefold_repeition(self) -> bool:
        """ Checks if position has been reached 3 times in a game, resulting in stalemate 
            >>> Returns True for stalemate and False for continued game
        """

        position_string = ''
        for index, part in enumerate(self.past_positions[-1].split()): # index from 0 to 3
            if index == 4:
                break
            position_string += part


        self._past_positions_count[f'{position_string}'] += 1
        if self._past_positions_count[f'{position_string}'] == 3:
            self._game_finished = True
            self._game_winner = 'Stalemate'


    def stalemateByMaterial(self) -> None:
        """ Checks for stalemate by lack of material
            based on : https://support.chess.com/en/articles/8705277-what-does-insufficient-mating-material-mean
            >>> Cases 

        """

        self._white_piece_counts = [0,0,0,0,0]
        self._black_piece_counts = [0,0,0,0,0]

        piece_index = {
            'p' : 0, 'P' : 0,
            'b' : 1, 'B' : 1,
            'n' : 2, 'N' : 2,
            'r' : 3, 'R' : 3,
            'q' : 4, 'Q' : 4,
        }

        for piece in self._white_pieces:
            if piece.toChar() == 'K':
                continue
            self._white_piece_counts[piece_index[piece.toChar()]] += 1

        for piece in self._black_pieces:
            if piece.toChar() == 'k':
                continue
            self._black_piece_counts[piece_index[piece.toChar()]] += 1

        if self._black_piece_counts[0] or self._white_piece_counts[0]: # has pawn
            return
        
        if self._black_piece_counts[3] or self._white_piece_counts[3] or self._black_piece_counts[4] or self._white_piece_counts[4]:
            # has rook or queen
            return

        for piece_counts in [[self._white_piece_counts, self._black_piece_counts],[self._black_piece_counts, self._white_piece_counts]]:
            if piece_counts[0] in [[0,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0]] and piece_counts[1] in [[0,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0]]:
                self._game_winner = 'Stalemate'
                self._game_finished = True
                return
            
            if piece_counts[0] == [0,0,2,0,0] and piece_counts[1] == [0,1,0,0,0]:
                return
            
            if piece_counts[0] == [0,0,2,0,0] and piece_counts[1] == [0,0,0,0,0]:
                self._game_winner = 'Stalemate'
                self._game_finished = True
                return

    def to_FEN(self) -> str:
        """ Changes board representation to FEN string"""

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

        if index in ['O-O-O', 'O-O']:
            return index
        
        if not index and not index == 0:
            return '-' 

        if not (0 <= index <= 63):
            raise ValueError(f"Index must be in the range 0-63. Index was value : {index}")
        file = chr(ord('a') + (index % 8))
        rank = str(8 - (index // 8))
        return file + rank

    def coordToInt(self, coord):

        if coord in ['O-O-O', 'O-O']:
            return coord

        if len(coord) != 2 or coord[0] not in 'abcdefgh' or coord[1] not in '12345678':
            raise ValueError("Coordinate must be in the format 'a1' to 'h8'.")
        file = coord[0]
        rank = coord[1]
        index = (ord(file) - ord('a')) + (8 - int(rank)) * 8
        return index

    def get_square(self, position: int) -> Piece | None:
        return self._board_space[position]

    def get_all_pieces(self) -> list[Piece]:
        """ Unused, leaving for now"""
        return self._white_pieces + self._black_pieces

    def _white_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of white pieces vision """
        return [piece.getVision() for piece in self._white_pieces]

    def _black_piece_vision(self) -> list[list[int]]:
        """ returns 2d array of black pieces vision """
        return [piece.getVision() for piece in self._black_pieces]

    def __str__(self) -> str:
        board = self.to_FEN().split()[0]

        output_str = ''

        for char in board:
            if char == '/':
                output_str += '\n'
                continue
            
            if char in 'pbnrqkPBNRQK':
                output_str += f'{char} '
            else:
                output_str += '. ' * int(char)

        return output_str




