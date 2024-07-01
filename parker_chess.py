from .board import boardFactory


class Chess():
    def Board(fen_string : str = None):
        """
            for boards use .move(), Notation 'A1A2', 'A2A1=Q', 'A4O-O-O'
            for seeing the score, use .evaluate(), which returns the score, or 'White', 'Black', or 'Stalemate' if game is over
            for getting board string use .to_FEN()
            for getting moves in json, use .white_pieces_to_json() or .black_pieces_to_json()
            for getting active turn use .get_turn(), which returns 'White' or 'Black'
        """
        if fen_string:
            return boardFactory.board(fen_string)
        else:
            return boardFactory.defaultBoard()
    


if __name__ == '__main__':
    myBoard = Chess.Board()    
    print(myBoard)