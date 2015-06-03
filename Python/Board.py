"""Contains the Board class"""

import copy
import itertools
import Piece
import Move
from Piece import PieceType as p_type
from Piece import PieceColour as colour


class Board:

    """Contains a 2d array of pieces and methods for making/verifying moves.

    Attributes:
        - piece_array:  a 2d list of pieces

    """

    SIZE = 8
    FILE_LABELS = [a, b, c, d, e, f, g, h]

    def __init__(self):
        """Create clear board."""
        self.clear()

    def draw(self, canvas):
        """Draw the current state of the board on a canvas.

        Args:
           - canvas : Tkinter canvas object to draw the board on

        """
        # Clear the canvas
        canvas.delete("all")

        sq_width = int(canvas["width"])/8

        # white background
        canvas.create_rectangle(0, 0, sq_width*8, sq_width*8, fill="yellow")

        # black squares: for each file draw 4 black squares
        for i in range(Board.SIZE):
            for j in range(Board.SIZE/2):

                canvas.create_rectangle(i*sq_width, (2*j+(i+1) % 2)*sq_width,
                                        (i+1)*sq_width,
                                        (2*j+(i+1) % 2+1)*sq_width,
                                        fill="brown")

        # draw all pieces on the board
        for i in range(8):
            for j in range(8):

                self.piece_array[i][j].draw(canvas, i*sq_width, j*sq_width)

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

    def make_move(self, move):
        """Adjust the state of the board to reflect the passed move.

        The universe may explode if this is not a legal move.

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

    def castle(self, move):
        """Adjust the state of the board to reflect the passed castling move.

        The passed move should be a legal castling move.

        Args:
            - move: a move object which is a castling move.
        """

        # If king is moving to the right
        if move.end_posn[0] - move.start_posn[0] > 0:
            # Castling King's side
            rook_from_x = 7
            rook_to_x = 5
        else:
            # Castling Queen's side
            rook_from_x = 0
            rook_to_x = 3

        rook_y = move.start_posn[1]

        # Move the king
        self.make_move(Move(move.start_posn, move.end_posn))

        # Move the rook
        self.remove_piece(rook_from_x, rook_y)
        self.place_piece(rook_to_x, rook_y)

    def promote_pawn(self, colour, piece_type):
        """Promote a pawn of a given colour to the given piece type.

        Args:
            - colour:  a member of the PieceColour enum
            - piece_type:  a member of the PieceType enum

        Raises:
            - TypeError if there is no valid pawn to promote.

        """

        if (colour == colour.white):
            y = 0
        else:
            y = 7

        for i in range(Board.SIZE):
            if self.get_piece(i, y) == Pawn(colour):
                self.place_piece(i, y, piece_type, colour)
                break
        else:
            raise TypeError(
                "Promote Pawn called, but no pawn is available for promotion.")

    ###########################################################################
    ############################# HELPER FUNCTIONS ############################
    ###########################################################################

    def is_square(self, x, y):
        """Return true if (x, y) represents a valid square."""
        return (x < Board.SIZE and y < Board.SIZE and x >= 0 and y >= 0)

    def get_piece(self, x, y):
        """Return the piece at position x, y on the board.

        Will raise IndexError if the indices are not valid.
        """
        return self.piece_array[x][y]

    def place_piece(self, x, y, piece_type, colour):
        """Place a piece of the passed type at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to place piece
            - type:  a member of the PieceType enum
            - colour:  a member of the PieceColour enum

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.make_piece(piece_type, colour)

    def remove_piece(self, x, y):
        """Remove the piece at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to remove piece

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.Piece()

    def search_direction(self, x, y, up_down, left_right, no_legal=False):
        """Move along the board in a given direction and return information.

        Given a starting location and a direction, move along the board in
        that direction and return a tuple with information about the number of
        empty squares, the piece at the end of the search, and what moves are
        legal.

        Args:
            - x, y:  ints specifying the position on the board to start at
            - up_down:  int, positive if moving upwards (in the negative y
                        direction), negative if moving downwards
            - left_right:  int, positive if moving right (in the positive
                           x direction), negative if moving left
            - no_legal:  If this is set true, the function will skip
                         calculating a list of valid possible moves (which can
                         be slow)

        For instance, up_down = 1 and left_right = -1 would look diagonally
        up and to the left.

        Returns: a tuple containing three pieces of information:
            [0] An integer count of the number of empty squares before the
                function finds another piece. This will be zero if there is
                a piece right next to (x, y). If the function reaches the end
                of the board, this will be the number of empty squares
                between (x, y) and the edge of the board (zero if (x, y) is at
                the edge of the board).
            [1] The piece the function finds at the end of the search, or None
                if the function reaches the edge of the board without finding a
                piece
            [2] A list of moves which are valid and possible for a piece at
                (x, y) in the given direction (or empty list if no_legal is 
                true)

        Will raise ValueError if up_down == left_right == 0, or IndexError if
        x and y do not refer to a physical square on the board.

        """

        up_down = up_down/abs(up_down)
        left_right = left_right/abs(left_right)

        if up_down == 0 and left_right == 0:
            raise ValueError

        if not self.is_square(x, y):
            raise IndexError

        num_squares = 0
        found_piece = None
        move_list = []

        new_x = x
        new_y = y

        new_x += left_right
        new_y += up_down

        while(self.is_square(new_x, new_y)):

            move = Move((x, y), (new_x, new_y))
            piece_at_move = self.get_piece(new_x, new_y)

            if (not no_legal) and self.is_possible_valid_move(move):
                move_list.append(move)

            if piece_at_move.type != p_type.blank:
                found_piece = piece_at_move
                break

            num_squares += 1
            new_x += left_right
            new_y += up_down

        return (num_squares, found_piece, move_list)

    ###########################################################################
    ############################# MOVE EVALUATION #############################
    ###########################################################################

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
            return False

        return True

    def is_possible_castle_move(self, move):
        """Return true if the passed move is a castle move and is possible.

        A castling move is considered POSSIBLE if the king and rook are in the
        correct position and the space between them is empty.

        Args:
            - move:  a Move object

        """

        if not move.castle:
            return False

        king = board.get_piece(*move.start_posn)

        if king.type != p_type.king:
            return False

        if king.colour == colour.white:
            y = 7
            friendly_rook = Piece.Rook(colour.white)
        elif king.colour == colour.black:
            y = 0
            friendly_rook = Piece.Rook(colour.black)

        # If king is not at correct position for castling
        if move.start_posn != (4, y):
            return False

        if (move.end_posn[0] > move.start_posn[0]):
            # Castling King's side
            search_results = search_direction(
                move.start_posn[0], move.start_posn[1], 0, 1, no_legal=True)
            if search_results[0] != 2:
                return False
            if search_results[1] != friendly_rook:
                return False
        else:
            # Castling Queen's side
            search_results = search_direction(
                move.start_posn[0], move.start_posn[1], 0, -1, no_legal=True)
            if search_results[0] != 3:
                return False
            if search_results[1] != friendly_rook:
                return False

        return True

    def is_valid_castle_move(self, move):
        """Return true if the passed move is a castle move and is valid.

        A castling move is VALID if by making it, the king does not castle
        into, out of, or through check. Note that this function will return
        true if a castling move is valid, regardless of whether the king/rook
        has already moved.

        Args:
            - move:  a Move object

        """

        if not move.castle:
            return False

        king = board.get_piece(*move.start_posn)

        if self.is_in_check(king.colour):
            return False

        if (move.end_posn[0] > move.start_posn[0]):
            # Castling King's side
            search_results = search_direction(
                move.start_posn[0], move.start_posn[1], 0, 1)
            if len(search_results[2]) != 2:
                return False
        else:
            # Castling Queen's side
            search_results = search_direction(
                move.start_posn[0], move.start_posn[1], 0, -1)
            if len(search_results[2]) != 3:
                return False

        return True

    def is_possible_valid_move(self, move):
        """Return true if the passed move is both possible and valid."""
        return (self.is_possible_move(move) and self.is_valid_move(move))

    def is_take_move(self, move):
        """Return true if the passed move is a taking move."""
        piece_at_move = self.get_piece(*move.end_posn)

        return piece_at_move.type == p_type.blank

    ###########################################################################
    ############################## MOVE FETCHING ##############################
    ###########################################################################

    def get_piece_moves(self, x, y):
        """Return a list of available moves for the piece at (x, y).

        Given a position (x, y), return a list of moves which it is legal for
        the piece at (x, y) to make. Note that this list is not completely
        exhaustive: the function will not return any castle moves or en passant
        moves.

        """

        piece_to_move = self.get_piece(x, y)

        if piece_to_move.type == p_type.blank:
            return []
        if piece_to_move.type == p_type.king:
            return get_king_moves(x, y)
        if piece_to_move.type == p_type.queen:
            return get_queen_moves(x, y)
        if piece_to_move.type == p_type.bishop:
            return get_bishop_moves(x, y)
        if piece_to_move.type == p_type.knight:
            return get_knight_moves(x, y)
        if piece_to_move.type == p_type.rook:
            return get_rook_moves(x, y)
        if piece_to_move.type == p_type.pawn:
            return get_pawn_moves(x, y)

        return count

    def get_king_moves(self, x, y):
        """Return a list of available moves for a king at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a king at (x, y) to make, excluding castling moves. If the piece at
        (x, y) is not a king or there is more than one king of a given colour
        on the board, this function will return without error but with
        incorrect results.

        """

        move_list = []
        square_list = [(x+1, y+1), (x+1, y),   (x+1, y-1), (x, y+1),
                       (x, y-1),   (x-1, y+1), (x-1, y),   (x-1, y-1)]

        for square in square_list:
            move = Move((x, y), square)
            if self.is_possible_valid_move(move):
                move_list.append(move)

        return move_list

    def get_queen_moves(self, x, y):
        """Return a list of available moves for a queen at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a queen at (x, y) to make.

        """

        move_list = []
        move_list.extend(self.get_bishop_moves(x, y))
        move_list.extend(self.get_rook_moves(x, y))
        return move_list

    def get_bishop_moves(self, x, y):
        """Return a list of available moves for a bishop at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a bishop at (x, y) to make.

        """

        move_list = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for direction in directions:
            direction_moves = self.search_direction(
                x, y, direction[0], direction[1])
            move_list.extend(search_direction[2])

        return move_list

    def get_knight_moves(self, x, y):
        """Return a list of available moves for a knight at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a knight at (x, y) to make.

        """

        move_list = []
        square_list = [(x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                       (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)]

        for square in square_list:
            move = Move((x, y), square)
            if self.is_possible_valid_move(move):
                move_list.append(move)

        return move_list

    def get_rook_moves(self, x, y):
        """Return a list of available moves for a rook at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a rook at (x, y) to make.

        """

        move_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for direction in directions:
            direction_moves = self.search_direction(
                x, y, direction[0], direction[1])
            move_list.extend(search_direction[2])

        return move_list

    def get_pawn_moves(self, x, y):
        """Return a list of available moves for a pawn at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a pawn at (x, y) to make, excluding en passant moves.

        """

        move_list = []
        can_double = False   # True if the pawn can move two squares forward.
        pawn = self.get_piece(x, y)

        if pawn.colour == colour.white:
            m = -1  # m is a multiplier which ensures white pieces move up the
            # board (in the negative y direction) and vice versa

            if y == 6:
                can_double = True
        else if pawn.colour == colour.black:
            m = 1

            if y == 1:
                can_double == True

        one_forward = Move((x, y), (x, y + 1*m))
        two_forward = Move((x, y), (x, y + 2*m))
        left_take = Move((x, y), (x - 1, y + 1*m))
        right_take = Move((x, y), (x + 1, y + 1*m))

        if (self.is_possible_valid_move(one_forward)):
            move_list.append(one_forward)
            if (self.is_possible_valid_move(two_forward)):
                move_list.append(two_forward)

        if (self.is_possible_valid_move(left_take)):
            if (self.is_take_move(left_take)):
                move_list.append(left_take)

        if (self.is_possible_valid_move(right_take)):
            if (self.is_take_move(right_take)):
                move_list.append(right_take)

        return move_list

    ###########################################################################
    ############################ BOARD EVALUATION #############################
    ###########################################################################

    def is_in_check(self, colour):
        """Return true if the king of the passed colour is in check.

        Note that if no king of the passed colour is found, this function will
        return false.

        Args:
            colour:  a member of the Piece.PieceColour enum

        """

        # Find King
        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.get_piece(i, j)
            if piece.type == p_type.king and piece.colour == colour:
                x = i
                y = j
                break
        else:
            return False

        # Radiate outwards and check for enemy rooks, bishops and queens:

        # Vertically/Horizontally
        for dirn in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            piece = self.search_direction(
                x, y, dirn[0], dirn[1], no_legal=True)[1]
            if piece.colour != colour:
                if piece.type in (p_type.rook, p_type.queen):
                    return True

        # Diagonally
        for dirn in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            piece = self.search_direction(
                x, y, dirn[0], dirn[1], no_legal=True)[1]
            if piece.colour != colour:
                if piece.type in (p_type.bishop, p_type.queen):
                    return True

        # Look for knights
        square_list = [(x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                       (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece.colour != colour:
                if piece.type == p_type.knight:
                    return True

        # Look for pawns
        if colour == colour.white:
            square_list = [(x+1, y-1), (x-1, y-1)]
        else:
            square_list = [(x+1, y+1), (x-1, y+1)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece.colour != colour:
                if piece.type == p_type.pawn:
                    return True

        # And finally, the enemy king
        square_list = [(x+1, y+1), (x+1, y),   (x+1, y-1), (x, y+1),
                       (x, y-1),   (x-1, y+1), (x-1, y),   (x-1, y-1)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece.colour != colour:
                if piece.type == p_type.king:
                    return True

        return False

    def has_won(self, colour):
        """Return true if the team of the passed colour has won.

        Args:
            colour:  a member of the Piece.PieceColour enum

        """

        if colour == colour.white:
            enemy = colour.black
        else:
            enemy = colour.white

        return (not legal_move_exists(enemy)) and self.is_in_check(enemy)

    def legal_move_exists(self, colour):
        """Return true if the team of the passed colour can make a legal move.

        Args:
            colour:  a member of the Piece.PieceColour enum

        """

        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.get_piece(i, j)
            if piece.colour == colour:
                if len(self.get_piece_moves(i, j)) > 0:
                    return True

        return False

    def is_king_draw(self):
        """Return true if the Kings are the only pieces left on the board."""
        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.get_piece(i, j)
            if not piece.type in (p_type.king, p_type.blank):
                return False

        return True

    def can_promote_pawn(self, colour):
        """Return true if the player of passed colour can promote a pawn."""

        if (colour == colour.white):
            y = 0
        else:
            y = 7

        for i in range(Board.SIZE):
            if self.get_piece(i, y) == Pawn(colour):
                return True

        return False

    ###########################################################################
    ########################### BOARD REPRESENTATION ##########################
    ###########################################################################

    def get_san(self, move):
        """Return a SAN representation of move (ignoring checks/promotions).

           -Args:
                -move: the move to return SAN of
        """
        san = ""

        if(move.castle):

            san += "O-O"

            # Check if queenside
            if(move.end_posn == (0, 0) or move.end_posn == (0, 7)):

                san += "-O"

        else:
            piece = self.get_piece(*move.start_posn)

            if(piece.type != PieceType.pawn):
                san += piece.get_san()
                san += self.get_clar_str(move)

            else:
                # If pawn we only give the file (no clarification needed)
                san += FILE_LABELS[move.start_posn[0]]

            if(self.is_take_move(move)):

                san += "x"

            san += FILE_LABELS[move.end_posn[0]] + str(move.end_posn[1])

        return san

    def get_clar_str(self, move, piece):
        """Create a clarification string for SAN if required.

           Used to dissambiguate piece moves where more than one piece of a 
           a given type can reach the target square

           Args:
               - move: the move that has been made
               - piece: the piece being moved
        """

        clar_str = ""
        tmp_pieces = []
        need_file = False
        need_rank = False

        for i in range(board.SIZE):
            for j in range(Board.SIZE):

                if(i != move.start_posn[0] and j != move.end_posn[1]):

                    moves_list = self.get_piece_moves(i, j)

                    if(piece_array[i][j].piece_type == piece.piece_type):

                        for m in move_list:

                            if(m.end_posn == move.end_posn):

                                if(i == move.start_posn[0]):
                                    need_rank = True

                                if(j == move.start_posn[1]):
                                    need_file = True

        if(need_file):
            clar_str += FILE_LABELS[move.start_posn[0]]
        if(need_rank):
            clar_str += str(move.start_posn[1])

    def get_pictorial(self):
        """Return a pictorial string representation of the board."""
        board_str = "\n"
        board_str += "------------------\n"

        for i in range(Board.SIZE):
            board_str += "|"

            for j in range(Board.SIZE):
                board_str += self.get_piece(j, i).get_san() += " "

            board_str += "|\n"

        board_str += "------------------\n\n"

        return board_str

    def get_forsyth(self):
        """Return a string representation of the board in FEN.

        The string will have one space at the end.

        """

        forsyth = ""

        for row in range(Board.SIZE):
            column = 0

            while column < BOARD_SIZE:
                piece = self.get_piece(column, row)

                if piece.type == p_type.blank:
                    gap = self.search_direction(
                        column, row, 0, 1, no_legal=True)[0]
                    forsyth += str(gap + 1)
                    column += gap + 1
                else:
                    forsyth += piece.get_san()
                    gap = searchDirection(
                        column, row, 0, 1, no_legal=True)[0]

                    if gap > 0:
                        forsyth += str(gap)
                    column += gap + 1

            if row < BOARD_SIZE - 1:
                forsyth += "/"

        forsyth += " "
        return forsyth
