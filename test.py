import boardFactory

b = boardFactory.board('r3k2r/8/3R4/8/8/8/8/4K3 w kq - 0 1')

#b = boardFactory.defaultBoard()

b.move('d6', 'f6')
b.move('e8', 'O-O-O')
b.move('f6', 'f8')
b.move('h8', 'f8')
b.move('e1', 'e2')
b.move('f8', 'f7')
b.move('e2', 'e1')
b.move('f7', 'e7')
b.move('e1', 'f1')
b.move('d8', 'f8')
b.move('f1', 'g2')
b.move('e7', 'g7')
b.move('g2', 'h3')
b.move('f8', 'h8')
# 


b.display_board()
b.print_active_moves()

# strange issue with king, Not first getting vision and then converting to moves 