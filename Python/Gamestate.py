"""Contains the Gamestate class"""

import Board

class Gamestate:

    """ Contains all information required to display current state of game.

        Args:
            - board: a board corresponding to the current game state
    """

    def __init__(self):

        self.board = Board.Board()
        self.board.setup()

    def draw(self, canvas):

        self.board.draw(canvas)
