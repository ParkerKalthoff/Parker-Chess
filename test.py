import boardFactory

b = boardFactory.board('3pkp2/2pppp2/3N4/8/1n6/8/2PPPP2/3PKP2 b - - 0 1')


#b = boardFactory.defaultBoard()

b.display_board()
b.print_active_moves()
print(b.to_FEN())

# TODO Stalemate by material
#   - Check chess.com for how to do
# TODO pawn promote:
#   - Check if pawn move is on 1st or 8th rank and then produce 4 variations of that move (check captures for it too)
#   - Will have to impliment safety features for this move in move