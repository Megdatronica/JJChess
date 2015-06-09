import Piece
import Board

board = Board.Board()

board.test_setup()

print(board.get_pictorial())

board.promote_pawn(Piece.PieceColour.white, Piece.PieceType.queen)

print(board.get_pictorial())