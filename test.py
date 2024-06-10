import boardFactory

#b = boardFactory.board('4k3/pppppppp/8/3B4/8/8/PPPPPPPP/4K3 w - - 0 1')

b = boardFactory.defaultBoard()

b.display_board()

b.print_active_moves()


# strange issue with king, Not first getting vision and then converting to moves 