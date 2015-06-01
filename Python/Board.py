"""Contains the Board class"""

import copy
import Piece
from Piece import PieceType as p_type
from Piece import PieceColour as colour


class Board:

    """Contains a 2d array of pieces and methods for making/verifying moves.

    Attributes:
        - piece_array:  a 2d list of pieces

    """

    SIZE = 8

    def __init__(self):
        """Create clear board."""
        self.clear()

    def draw(canvas):
        """Draw the current state of the board. Called by the main instance of Game

        Args:
           - canvas : Tkinter canvas object to draw the board on

        """

        canvas.create_line(5, 5, BOARD_SIZE - 5, 5)
        canvas.create_line(5, 5, 5, BOARD_SIZE - 5)
        canvas.create_line(BOARD_SIZE-5, 5, BOARD_SIZE-5, BOARD_SIZE-5)
        canvas.create_line(5, BOARD_SIZE-5, BOARD_SIZE-5, BOARD_SIZE-5)

    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        """Initialise piece_array as an 8 x 8 array of blank pieces."""
        self.piece_array = [[Piece.Piece() for i in range(Board.SIZE)]
                            for i in range(Board.SIZE)]

    def setup(self):
        """Set the board to the arrangement for the beginning of a game."""

        self.clear()
        for x in range(Board.SIZE):
            self.piece_array[x][1] = Piece.Pawn(colour.black)
            self.piece_array[x][6] = Piece.Pawn(colour.white)

        self.piece_array[0][0] = Piece.Rook(colour.black)
        self.piece_array[7][0] = Piece.Rook(colour.black)
        self.piece_array[1][0] = Piece.Knight(colour.black)
        self.piece_array[6][0] = Piece.Knight(colour.black)
        self.piece_array[2][0] = Piece.Bishop(colour.black)
        self.piece_array[5][0] = Piece.Bishop(colour.black)
        self.piece_array[3][0] = Piece.Queen(colour.black)
        self.piece_array[4][0] = Piece.King(colour.black)

        self.piece_array[0][7] = Piece.Rook(colour.white)
        self.piece_array[7][7] = Piece.Rook(colour.white)
        self.piece_array[1][7] = Piece.Knight(colour.white)
        self.piece_array[6][7] = Piece.Knight(colour.white)
        self.piece_array[2][7] = Piece.Bishop(colour.white)
        self.piece_array[5][7] = Piece.Bishop(colour.white)
        self.piece_array[3][7] = Piece.Queen(colour.white)
        self.piece_array[4][7] = Piece.King(colour.white)

    ###########################################################################
    ############################# HELPER FUNCTIONS ############################
    ###########################################################################

    def get_piece(self, x, y):
        """Return the piece at position x, y on the board.

        Will raise IndexError if the indices are not valid.
        """
        return self.piece_array[x][y]

    def place_piece(self, x, y, type, colour):
        """Place a piece of the passed type at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to place piece
            - type:  a member of the PieceType enum
            - colour:  a member of the PieceColour enum

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.Piece(type, colour)

    def remove_piece(self, x, y):
        """Remove the piece at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to remove piece

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.Piece()

    def search_direction(self, x, y, up_down, left_right):
        pass

    ###########################################################################
    ############################### MOVE LOGIC ################################
    ###########################################################################

    def make_move(self, move):
        """Adjust the state of the board to reflect the passed move.

        Args:
            - move:  a Move object
        """
        if move.castle:
            self.castle(move)

        if move.en_passant:
            self.remove_piece(*move.start_posn)

        piece = self.get_piece(*move.start_posn)

        self.remove_piece(*move.start_posn)
        self.place_piece(move.end_posn[0], move.end_posn[1],
                         piece.type, piece.colour)

    def is_possible_move(self, move):
        """Return True if the passed move is possible.

        A move is POSSIBLE if it takes a piece to a square that:
          - exists on the board, and
          - does not contain another piece of the same colour.

        A castling move is considered POSSIBLE if the king and rook are in the
        correct position and the space between them is empty.

        Args:
            - move:  a Move object

        """

        if move.castle:
            return self.is_possible_castle_move(move)

        piece_moving = self.get_piece(*move.start_posn)

        try:
            piece_at_move = self.get_piece(*move.end_posn)
        except IndexError:
            return False

        if (piece_at_move.colour == piece_moving.colour):
            return False

        return True

    def is_valid_move(self, move):
        """Return true if the passed move is valid.

        A move is valid if after is it made, the king of the player who made it
        is not in check.

        Args:
            - move:  a Move object

        """

        if move.castle:
            return self.is_valid_castle_move(move)

        piece_moving = self.get_piece(*move.start_posn)

        new_board = self.copy()
        new_board.make_move(move)

        if newBoard.isInCheck(piece_moving.colour):
            return false

        return true

    def is_possible_castle_move(self, move):
        """Return true if the passed move is a castle move and is possible.

        A castling move is considered POSSIBLE if the king and rook are in the
        correct position and the space between them is empty.

        Args:
            - move:  a Move object which should be verified to be a castling
                     move.

        """
        pass
