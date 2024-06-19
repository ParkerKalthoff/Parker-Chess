import boardFactory

b = boardFactory.board('3pkp2/2pppp2/3N4/8/1n6/8/2PPPP2/3PKP2 b - - 0 1')


#b = boardFactory.defaultBoard()

b.display_board()
b.print_active_moves()
print(b.to_FEN())


# TODO 50 move 
# TODO Stalemate by material
