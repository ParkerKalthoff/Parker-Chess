import boardFactory

#b = boardFactory.board('4k3/pppppppp/8/3B4/8/8/PPPPPPPP/4K3 w - - 0 1')

b = boardFactory.defaultBoard()

print(b.display_board())

for piece in b._white_pieces:
    print(b.intToCoord(piece.pos()), piece, [b.intToCoord(move) for move in piece.getMoves()])