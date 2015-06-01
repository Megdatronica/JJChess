"""Contains the Piece class"""

from enum import Enum


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

    def draw(canvas):

        pass


class King(Piece):

    def __init__(self, colour):
        """Create a king piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.king


class Queen(Piece):

    def __init__(self, colour):
        """Create a queen piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.queen


class Bishop(Piece):

    def __init__(self, colour):
        """Create a bishop piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.bishop


class Knight(Piece):

    def __init__(self, colour):
        """Create a knight piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.knight


class Rook(Piece):

    def __init__(self, colour):
        """Create a rook piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.rook


class Pawn(Piece):

    def __init__(self, colour):
        """Create a pawn piece with the passed colour.

        Args:
            - colour:  a member of the PieceColour enum
        """

        self.colour = colour
        self.type = pieceType.pawn
