import Gamestate
import Board
from Piece import PieceColour as co
from Piece import PieceType as ty

me = Board.Board()

me.place_piece(1, 0, ty.knight, co.black)
me.place_piece(2, 0, ty.bishop, co.black)
me.place_piece(4, 0, ty.king, co.black)
me.place_piece(0, 1, ty.rook, co.black)
me.place_piece(1, 1, ty.pawn, co.black)
me.place_piece(2, 2, ty.pawn, co.black)
me.place_piece(3, 2, ty.pawn, co.black)
me.place_piece(0, 3, ty.pawn, co.black)
me.place_piece(4, 3, ty.pawn, co.black)
me.place_piece(5, 3, ty.rook, co.black)
me.place_piece(7, 3, ty.pawn, co.black)
me.place_piece(0, 4, ty.pawn, co.white)
me.place_piece(2, 4, ty.pawn, co.white)
me.place_piece(7, 4, ty.pawn, co.white)
me.place_piece(4, 5, ty.king, co.white)
me.place_piece(5, 5, ty.knight, co.white)
me.place_piece(6, 5, ty.pawn, co.white)
me.place_piece(7, 5, ty.queen, co.black)
me.place_piece(3, 6, ty.knight, co.white)
me.place_piece(4, 6, ty.pawn, co.white)
me.place_piece(1, 7, ty.rook, co.white)
me.place_piece(3, 7, ty.knight, co.black)
me.place_piece(5, 7, ty.bishop, co.white)

print(me.get_pictorial())

print(me.is_in_check(co.white))

move_list = me.get_piece_moves(4, 6)

for move in move_list:
    print(move.start_posn, move.end_posn)


me = Gamestate.Gamestate()
me.board.clear()

me.board.place_piece(1, 0, ty.knight, co.black)
me.board.place_piece(2, 0, ty.bishop, co.black)
me.board.place_piece(4, 0, ty.king, co.black)
me.board.place_piece(0, 1, ty.rook, co.black)
me.board.place_piece(1, 1, ty.pawn, co.black)
me.board.place_piece(2, 2, ty.pawn, co.black)
me.board.place_piece(3, 2, ty.pawn, co.black)
me.board.place_piece(0, 3, ty.pawn, co.black)
me.board.place_piece(4, 3, ty.pawn, co.black)
me.board.place_piece(5, 3, ty.rook, co.black)
me.board.place_piece(7, 3, ty.pawn, co.black)
me.board.place_piece(0, 4, ty.pawn, co.white)
me.board.place_piece(2, 4, ty.pawn, co.white)
me.board.place_piece(7, 4, ty.pawn, co.white)
me.board.place_piece(4, 5, ty.king, co.white)
me.board.place_piece(5, 5, ty.knight, co.white)
me.board.place_piece(6, 5, ty.pawn, co.white)
me.board.place_piece(7, 5, ty.queen, co.black)
me.board.place_piece(3, 6, ty.knight, co.white)
me.board.place_piece(4, 6, ty.pawn, co.white)
me.board.place_piece(1, 7, ty.rook, co.white)
me.board.place_piece(3, 7, ty.knight, co.black)
me.board.place_piece(5, 7, ty.bishop, co.white)

print(me.board.get_pictorial())

print(me.board.is_in_check(co.white))

move_list = me.get_all_moves(co.white)

for move in move_list:
    print(move.start_posn, move.end_posn)
