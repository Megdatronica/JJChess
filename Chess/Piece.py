"""Contains the Piece class"""

from enum import Enum
from tkinter import *


class PieceType(Enum):
    blank = 0
    king = 1
    queen = 2
    bishop = 3
    knight = 4
    rook = 5
    pawn = 6


class PieceColour(Enum):
    blank = 0
    black = -1
    white = 1

def make_piece(piece_type, colour):
        """Return a piece of the correct subclass given the passed attributes.

        Args:
            - piece_type:  a member of the PieceType enum
            - colour:  a member of the PieceColour enum

        """

        if (piece_type == PieceType.king):
            return King(colour)
        elif (piece_type == PieceType.queen):
            return Queen(colour)
        elif (piece_type == PieceType.bishop):
            return Bishop(colour)
        elif (piece_type == PieceType.knight):
            return Knight(colour)
        elif (piece_type == PieceType.rook):
            return Rook(colour)
        elif (piece_type == PieceType.pawn):
            return Pawn(colour)
        else:
            return Piece()

class Piece:

    """Represents a square on the board and the piece that stands on it.

    Attributes:
        - colour:    a member of the PieceColour enum
        - piece_type:      a member of the PieceType enum
    """

    def __init__(self):
        """Create a blank piece."""
        self.type = PieceType.blank
        self.colour = PieceColour.blank

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        pass

    def __eq__(self, other):
        return (self.type == other.type
                and self.colour == other.colour)

    def __ne__(self, other):
        return not self.__eq__(other)


    def get_san(self):
        return "_"


class King(Piece):

    def __init__(self, colour):
        """Create a king piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.king

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):

            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_king)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_king)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "K"
        else:
            return "k"


class Queen(Piece):

    def __init__(self, colour):
        """Create a queen piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.queen

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_queen)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_queen)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "Q"
        else:
            return "q"


class Bishop(Piece):

    def __init__(self, colour):
        """Create a bishop piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.bishop

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):

            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_bish)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_bish)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "B"
        else:
            return "b"


class Knight(Piece):

    def __init__(self, colour):
        """Create a knight piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.knight

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):

            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_nght)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_nght)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "N"
        else:
            return "n"


class Rook(Piece):

    def __init__(self, colour):
        """Create a rook piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.rook

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):

            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_rook)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_rook)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "R"
        else:
            return "r"

class Pawn(Piece):

    def __init__(self, colour):
        """Create a pawn piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = PieceType.pawn

    def draw(self, canvas, x, y):
        """Draw the piece

           Args:
               -canvas: The canvas element to draw onto
               -x: The x coordinate of top left corner
               -y: The y coordinate of top left corner
        """

        sq_offset = int(canvas["width"])/16

        if(self.colour == PieceColour.white):

            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.w_pawn)
        else:
            canvas.create_image(x+sq_offset, y+sq_offset, image=canvas.b_pawn)

    def get_san(self):
        if self.colour == PieceColour.white:
            return "P"
        else:
            return "p"
