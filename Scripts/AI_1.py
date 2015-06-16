from Chess import Gamestate
from Chess import Board
from Chess import Move
from Chess import Piece
from Chess.Piece import PieceColour as p_colour
import random

random.seed(100)


def get_move(game_state, colour):
    """Return the move chosen by the AI module

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their move based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a move is to be chosen.

    """

    return random.choice(game_state.get_all_moves(colour))


def get_promotion(game_state, colour):
    """Return the piece the user chooses to promote their pawn to.

    Args:
        - game_state:  an instance of GameState - the AI will choose
                       their promotion based on this
        - colour:  an member of the Chess.Piece.PieceColour enum, the colour
                   the player for which a promotion is to be chosen.

    """

    return Piece.Queen(colour)
