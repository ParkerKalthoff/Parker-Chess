import boardFactory

#b = boardFactory.board('4k3/8/8/8/1n6/8/3PPP2/3PKP2 b - f2 0 1')


b = boardFactory.defaultBoard()

b.move_coord('g1', 'f3')
b.move_coord('g8', 'f6')
b.move_coord('f3', 'h4')
b.move_coord('f6', 'g8')
b.move_coord('h4', 'f5')
b.move_coord('g8', 'f6')
b.move_coord('f5', 'd6')

b.display_board()
b.print_active_moves()


# TODO 50 move 
# TODO Stalemate by material
# TODO Fix Horsey
