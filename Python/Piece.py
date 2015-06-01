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
    black = 0
    white = 1


class Piece:

    """Represents a square on the board and the piece that stands on it.

    Attributes:
        - colour:    a member of the PieceColour enum
        - type:      a member of the PieceType enum
    """

    def __init__(self, type=PieceType.blank, colour=PieceColour.white):
        """Create a blank piece.

        Args:
            - type:  a member of the PieceType enum
            - colour:  a member of the PieceColour enum
        """
        self.type = type
        self.colour = colour

    def draw(self, canvas, x, y):

        pass


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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_king)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_king)

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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_queen)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_queen)



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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_bish)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_bish)


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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_nght)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_nght)


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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_rook)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_rook)


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

            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.w_pawn)
        else:    
            canvas.create_image(x+sq_offset,y+sq_offset, image=canvas.b_pawn)
