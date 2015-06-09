import Piece
import Gamestate
import cProfile
import Board
import Move


colour = Piece.PieceColour.white

g = Gamestate.Gamestate()

b = Board.Board()
b.setup()
m = Move.Move((1,1), (1,3))

cProfile.run("g.get_all_moves(colour)")
#cProfile.run("b.is_valid_move(m)")