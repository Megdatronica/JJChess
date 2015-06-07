"""Contains the Player class"""

import importlib
import Gamestate
import Board
import Move
import Piece
from Piece import PieceColour as colour


class Player:

    """Contains functions for selecting moves and pawn promotions.

    Attributes:
        - colour:  a member of the Piece.PieceColour enum
        - is_human:  True if the player is a human player

    """

    def __init__(self, colour, is_human=False, location=None):
        """Initialise a player with the passed parameters."""
        self.colour = colour
        self.is_human = is_human
        self.location = location

    def make_player(colour, is_human=False, location=None):
        """Return a player of the correct type given the passed parameters.

        Args:
            - colour:  a member of the Piece.PieceColour enum
            - is_human:  True if the player is a human player
            - location:  If the player is not a human player, this should
                         be the name of the python file containing the
                         functions that determine the AI.

        Raises:
            - ValueError if both is_human is false and location is None.

        """

        if (is_human):
            return HumanPlayer(colour)
        elif location is not None:
            return AIPlayer(colour, location)
        else:
            raise ValueError(
                "Cannot have both is_human=False and location=None")

    def get_move(self, game_state):
        """Virtual function: should return a legal move given a game state."""
        raise NotImplementedError

    def get_promotion(self, game_state):
        """Virtual function: should return a legal pawn promotion.

        Given a game state for which a player may promote a pawn of their
        colour, this function should return a Piece of the type to which the
        pawn is to be promoted.

        """
        raise NotImplementedError


class HumanPlayer(Player):

    """Handles display and selection of moves via the user interface."""

    def __init__(self, colour):
        """Create a human player with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum.

        """

        super(HumanPlayer, self).__init__(colour, is_human=True)

    def get_move(self, game_state):
        """Display available moves and returns the move the user picked.

        Args:
            - game_state:  an instance of GameState - the human will choose
                           their move based on this

        """

        pass

    def get_promotion(self, game_state):
        """Return the piece the user chooses to promote their pawn to.

        Args:
            - game_state:  an instance of GameState - the human will choose
                           their promotion based on this

        """

        pass


class AIPlayer(Player):

    """Handles selection of moves by the relevant AI module."""

    def __init__(self, colour, location):
        """Create a AI based on the python file at the given location.

        Args:
            - colour:  a member of the PieceColour enum (the AI Player will
                       be assigned this colour)
            - location:  a string which is the name of the python file
                         containing the AI module to use (WITHOUT the .py)

        """

        super(AIPlayer, self).__init__(colour, location=location)

        AI = importlib.import_module("Scripts." + location)

    def get_move(self, game_state):
        """Return the move chosen by the AI module

        Args:
            - game_state:  an instance of GameState - the AI will choose
                           their move based on this

        """

        return AI.get_move(game_state, self.colour)

    def get_promotion(self, game_state):
        """Return the piece the user chooses to promote their pawn to.

        Args:
            - game_state:  an instance of GameState - the AI will choose
                           their promotion based on this

        """

        return AI.get_promotion(game_state, self.colour)
