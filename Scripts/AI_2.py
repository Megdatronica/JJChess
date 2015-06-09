from Chess import Gamestate
from Chess import Board
from Chess import Move
from Chess import Piece
from Chess.Piece import PieceColour as p_colour
import random


def get_move(game_state, colour):
    """Return the move chosen by the AI module

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their move based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a move is to be chosen.

    """

    moves = game_state.get_all_moves(colour)

    for m in moves:
        if game_state.board.is_take_move(m):
            return m
    else:
        return random.choice(moves)


def get_promotion(game_state, colour):
    """Return the piece the user chooses to promote their pawn to.

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their promotion based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a promotion is to be chosen.

    """

    return Piece.Queen(colour)
