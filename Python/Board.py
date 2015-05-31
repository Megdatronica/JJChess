import Piece
from Piece import PieceType as type
from Piece import PieceColour as colour

"""Contains the Board class"""

class Board:
    """Contains a 2d array of pieces and methods for making/verifying moves.
    
    Attributes:
        - piece_array:  a 2d list of pieces
    
    """
    
    SIZE = 8
    
    def __init__(self):
        """Create clear board."""
        self.clear()
        
        
    def clear(self):
        """Initialise piece_array as an 8 x 8 array of blank pieces."""
        piece_array = [ [Piece() for i in range(SIZE)] for i in range(SIZE)]
        
        
    def setup(self):
        """Set the board to the arrangement for the beginning of a game."""
        
        self.clear()
        for x in range(SIZE):
            piece_array[x][1] = Pawn(colour.black)
            piece_array[x][6] = Pawn(colour.white)
        
        piece_array[0][0] = Rook(colour.black)
        piece_array[7][0] = Rook(colour.black)
        piece_array[1][0] = Knight(colour.black)
        piece_array[6][0] = Knight(colour.black)
        piece_array[2][0] = Bishop(colour.black)
        piece_array[5][0] = Bishop(colour.black)
        piece_array[3][0] = Queen(colour.black)
        piece_array[4][0] = King(colour.black)
        
        piece_array[0][7] = Rook(colour.white)
        piece_array[7][7] = Rook(colour.white)
        piece_array[1][7] = Knight(colour.white)
        piece_array[6][7] = Knight(colour.white)
        piece_array[2][7] = Bishop(colour.white)
        piece_array[5][7] = Bishop(colour.white)
        piece_array[3][7] = Queen(colour.white)
        piece_array[4][7] = King(colour.white)


    def get_piece(self, x, y):
        """Returns the piece at position x, y on the board."""
        return self.piece_array[x][y]
    
        
    def place_piece(self, x, y, type, colour):
        """Places a piece of the passed type at the passed location.
        
        Args:
            - x, y:  ints specifying the position on the board to place piece
            - type:  a member of the PieceType enum
            - colour:  a member of the PieceColour enum
        """
        
        self.piece_array[x][y] = Piece(type, colour)
        
        
    def remove_piece(self, x, y):
        """Removes the piece at the passed location.
        
        Args:
            - x, y:  ints specifying the position on the board to remove piece
        """
        
        self.piece_array[x][y] = Piece()
        
        
    def make_move(self, move):
        """Adjusts the state of the board to reflect the passed move."""
        if move.castle:
            castle(move)
            
        if move.en_passant:
            self.remove_piece(*move.start_posn)
            
        piece = self.get_piece(*move.start_posn)
    
        self.remove_piece(*move.start_posn)
        self.place_piece(*move.end_posn, piece.type, piece.colour)

    def 







