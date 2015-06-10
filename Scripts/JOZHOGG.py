from Chess import Gamestate
from Chess import Board
from Chess import Move
from Chess import Piece
from Chess.Piece import PieceColour as p_colour
from Chess.Piece import PieceType
import random


def get_move(game_state, colour, step=0):
    """Return the move chosen by the AI module

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their move based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a move is to be chosen.

    """

    if(colour.value == p_colour.white.value):
        enemy_col = p_colour.black    
    else:
        enemy_col = p_colour.white 

    moves = game_state.get_all_moves(colour)

    cur_best_move = None

    if(colour.value == p_colour.white.value):
        cur_eval = -1000

        for m in moves:

            taken_piece = game_state.board.get_piece(*m.end_posn)

            game_state.board.make_move(m)
            tmp_eval = board_eval(game_state.board, colour)

            step += 1

            get_move(game_state, enemy_col, step)

            if(random.random() > 0.5):
                tmp_eval += 0.5

            if(tmp_eval > cur_eval):

                cur_best_move = m
                cur_eval = tmp_eval

            game_state.board.takeback_move(m, taken_piece)

    else:
        cur_eval = 1000

        for m in moves:

            taken_piece = game_state.board.get_piece(*m.end_posn)

            game_state.board.make_move(m)
            tmp_eval = board_eval(game_state.board, colour)

            if(random.random() > 0.5):
                tmp_eval -= 0.5

            if(tmp_eval < cur_eval):

                cur_best_move = m
                cur_eval = tmp_eval

            game_state.board.takeback_move(m, taken_piece)
    if
    return cur_best_move

def board_eval(board, colour):

    eval = 0

    for i in range(8):
        for j in range(8):

            piece = board.get_piece(i,j)

            piece_type = piece.type
            piece_col = piece.colour

            if (piece_type.value == PieceType.queen.value):
                if(piece_col.value == p_colour.white.value):
                    eval += 9
                else:
                    eval -= 9
            elif (piece_type.value == PieceType.bishop.value):
                if(piece_col.value == p_colour.white.value):
                    eval += 3
                else:
                    eval -= 3
            elif (piece_type.value == PieceType.knight.value):
                if(piece_col.value == p_colour.white.value):
                    eval += 3
                else:
                    eval -= 3
            elif (piece_type.value == PieceType.rook.value):
                if(piece_col.value == p_colour.white.value):
                    eval += 5
                else:
                    eval -= 5
            elif (piece_type.value == PieceType.pawn.value):
                if(piece_col.value == p_colour.white.value):
                    eval += 1
                else:
                    eval -= 1

    if colour.value == p_colour.white.value:
        if(board.is_in_check(p_colour.black)):

            eval += 2
    else:
        if(board.is_in_check(p_colour.white)):

            eval -= 2

    return eval



def get_promotion(game_state, colour):
    """Return the piece the user chooses to promote their pawn to.

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their promotion based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a promotion is to be chosen.

    """

    return Piece.Queen(colour)