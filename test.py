import boardFactory

b = boardFactory.board('r3k2r/8/3R4/8/8/8/8/4K3 w KQkq - 0 1')

#b = boardFactory.defaultBoard()

b.move('d6', 'f6')
b.move('e8', 'O-O-O')
b.move('e1', 'O-O')


# 


b.display_board()
b.print_active_moves()

# strange issue with king, Not first getting vision and then converting to moves 