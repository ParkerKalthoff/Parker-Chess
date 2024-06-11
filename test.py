import boardFactory

#b = boardFactory.board('4k3/pppppppp/8/3B4/8/8/PPPPPPPP/4K3 w - - 0 1')

b = boardFactory.defaultBoard()

b.movePiece('d2', 'd4')
b.refresh_board()

b.movePiece('e7', 'e5')
b.refresh_board()

b.movePiece('d4', 'e5')
b.refresh_board()

b.movePiece('a7', 'a6')
b.refresh_board()

b.movePiece('e5', 'e6')
b.refresh_board()

b.movePiece('a6', 'a5')
b.refresh_board()

b.movePiece('e6', 'f7')
b.refresh_board()

# 


b.display_board()
b.print_active_moves()

# strange issue with king, Not first getting vision and then converting to moves 