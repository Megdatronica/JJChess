"""Contains the Gamestate class"""

from enum import Enum
import Board
import Move
from Piece import *
from Piece import PieceColour as colour
from Piece import PieceType as p_type
# Tkinter graphics package
from tkinter import *


class Status(Enum):
    normal = 0

    white_check = 1
    black_check = -1

    white_win = 2
    black_win = -2

    stalemate = 3
    fifty_move_draw = 4
    king_draw = 5
    agreement_draw = 6


class Gamestate:

    """ Contains all information required to display current state of game.

        Attributes:
                  - board: a board corresponding to the current game state
                  - w_castle_K: True if white can castle king-side
                  - b_castle_K: True if black can castle king-side
                  - w_castle_Q: True if white can castle queen-side
                  - b_castle_Q: True if black can castle queen-side
                  - count: counts which move we are on (Note: this is the 
                     number of half moves in chess move counting)
                  - fifty_move_count: counts as above the number of moves 
                     since last capture
                  - en_passant_sq: if an en passant move is possible, this
                     is the square behind the pawn to be captured. If en 
                     passant is not possible, set to None
                  - is_white_turn: true if it is white's turn
                  - selected_piece_moves: list of moves available to the 
                     selected piece
                  - selected_piece: position of the selected piece
    """

    def __init__(self):
        """ Constructor for the game state - defaults to start of a game.
        """

        self.board = Board.Board()
        self.board.setup()

        # Set castling to true
        self.w_castle_K = True
        self.w_castle_Q = True
        self.b_castle_K = True
        self.b_castle_Q = True

        # Set moves counts to start of game
        self.count = 0
        self.fifty_move_count = 0

        self.en_passant_sq = None
        self.selected_piece = None
        self.selected_piece_moves = []

        self.king_in_check = False
        self.is_white_turn = True

    def draw(self, canvas):
        """ Draw the gamestate to a Tkinter canvas element.

            Args:
                -canvas: the Tkinter canvas element
        """

        # Clear the canvas
        canvas.delete("all")

        self.board.draw_board(canvas)

        # highlights king red if in check
        if(self.king_in_check):
            # TODO: Draw code for king in check
            pass

        # Creates a move from the piece to itself to draw
        if(self.selected_piece != None):
            Move.Move(self.selected_piece,
                      self.selected_piece).draw(canvas)

        for move in self.selected_piece_moves:

            if(self.board.is_take_move(move)):

                move.set_taking_move()

            move.draw(canvas)

        self.board.draw_pieces(canvas)

    def select_square(self, square, canvas):

        for move in self.selected_piece_moves:

            if move.end_posn == square:

                self.selected_piece = None
                self.selected_piece_moves = []

                return move

        piece = self.board.get_piece(*square)

        if piece.type != PieceType.blank and self.is_turn(piece.colour):

            if(self.selected_piece == square):
                self.selected_piece = None
                self.selected_piece_moves = []
            else:
                self.selected_piece = square
                self.selected_piece_moves = \
                    self.get_piece_moves(square)
        else:
            self.selected_piece = None
            self.selected_piece_moves = []

        print(self.selected_piece_moves)

        self.draw(canvas)

        return None

    def is_turn(self, colour):

        if self.is_white_turn and colour is PieceColour.white:

            return True

        if not self.is_white_turn and colour is PieceColour.black:

            return True

        else:
            return False

    def make_move(self, move, canvas):
        """ Make a given move.

            Args:
                - move: move to be made
                - canvas: canvas to be drawn onto
        """


        print("move made")

        self.update_counts(move)
        self.board.make_move(move)

    def update_counts(self, move):
        """ Update counters and set en passant square if appropriate.

            Args:
                - move: move that is GOING (called before move made) to be made
        """

        piece = self.board.get_piece(*move.start_posn)

        # increment move counter
        self.count += 1

        # reset en passant square
        en_passant_sq = None

        # Check whether the king has moved
        if(piece.type == PieceType.king):

            if(piece.colour == PieceColour.white):

                self.w_castle_K = False
                self.w_castle_Q = False
            else:

                self.b_castle_K = False
                self.b_castle_Q = False

        # Check whether a corner rook has moved
        # Note: It is unnecessary to check piece colour
        # as, for example, a white rook on A8 means the
        # black rook must have moved
        if(piece.type == PieceType.rook):

            if(move.start_posn == (0, 0)):

                self.b_castle_Q = False

            elif(move.start_posn == (7, 0)):

                self.b_castle_K = False

            elif(move.start_posn == (0, 7)):

                self.w_castle_Q = False

            elif(move.start_posn == (7, 7)):

                self.w_castle_K = False

        # Check if we need to store an en passant square

        if(piece.type == PieceType.pawn):
            # check if double move
            if(abs(move.start_posn[1] - move.end_posn[1]) == 2):
                if(piece.colour == PieceColour.white):

                    self.en_passant_sq = (move.start_posn[0],
                                          move.start_posn[1] - 1)
                else:

                    self.en_passant_sq = (move.start_posn[0],
                                          move.start_posn[1] + 1)

        # check whether there has been a capture

        if(self.board.is_take_move(move)):

            # reset counter
            self.fifty_move_count = 0
        else:

            self.fifty_move_count += 1

    def get_piece_moves(self, square):

        p_moves = []
        piece = self.board.get_piece(*square)

        p_moves.extend(self.board.get_piece_moves(*square))

        print(self.en_passant_sq)

        if piece.type == p_type.pawn and self.en_passant_sq is not None:

            if(abs(square[0] - self.en_passant_sq[0]) == 1 and
               abs(square[1] - self.en_passant_sq[1]) == 1):

                pawn_square = (self.en_passant_sq[0], square[1])

                p_moves.append(Move.Move((square[0], square[1]),
                                         self.en_passant_sq,
                                         en_passant=True,
                                         en_passant_posn=pawn_square,
                                         take_move=True))

        if(piece.type == p_type.king):

            if(self.w_castle_K == True):

                castle = Move.Move((4, 7), (6, 7), castle=True)
                if(self.board.is_possible_valid_move(castle)):

                    p_moves.append(castle)

            if(self.w_castle_Q == True):

                castle = Move.Move((4, 7), (2, 7), castle=True)
                if(self.board.is_possible_valid_move(castle)):

                    p_moves.append(castle)

            if(self.b_castle_K == True):

                castle = Move.Move((4, 0), (6, 0), castle=True)
                if(self.board.is_possible_valid_move(castle)):

                    p_moves.append(castle)

            if(self.b_castle_Q == True):

                castle = Move.Move((4, 0), (2, 0), castle=True)
                if(self.board.is_possible_valid_move(castle)):

                    p_moves.append(castle)

        return p_moves

    def get_all_moves(self, colour):
        """ Return all the legal moves that the coloured player can make.
            (includes castling and en passant moves)

            Args:
                - colour: colour of the player
        """

        moves = self.get_player_moves(colour)

        if(self.w_castle_K == True):
            castle = Move.Move((4, 7), (6, 7), castle=True)
            if(self.board.is_possible_valid_move(castle)):
                moves.append(castle)

        if(self.w_castle_Q == True):
            castle = Move.Move((4, 7), (2, 7), castle=True)
            if(self.board.is_possible_valid_move(castle)):
                moves.append(castle)

        if(self.b_castle_K == True):
            castle = Move.Move((4, 0), (6, 0), castle=True)
            if(self.board.is_possible_valid_move(castle)):
                moves.append(castle)

        if(self.b_castle_Q == True):
            castle = Move.Move((4, 0), (2, 0), castle=True)
            if(self.board.is_possible_valid_move(castle)):
                moves.append(castle)

        return moves

    def get_player_moves(self, colour):
        """ Helper function to get_all_moves - returns all but castling.

            Args:
                - colour: colour of the player making the move
        """

        b_moves = []

        for i in range(8):
            for j in range(8):

                if(self.board.get_piece(i, j).type == PieceType.pawn and
                        self.en_passant_sq != None):

                    b_moves.extend(self.board.get_piece_moves(i, j))

                    if(abs(i - self.en_passant_sq[0]) == 1 and
                            abs(j - self.en_passant_sq[1]) == 1):

                        pawn_square = (self.en_passant_sq[0], j)

                        b_moves.append(Move.Move((i, j),
                                         self.en_passant_sq,
                                         en_passant=True,
                                         en_passant_posn=pawn_square,
                                         take_move=True))

                else:
                    b_moves.extend(self.board.get_piece_moves(i, j))

        return b_moves

    def can_promote_pawn(self, colour):
        """ Check if a pawn can be promoted.

            Args:
                - colour: colour of player to check for
        """

        self.board.can_promote_pawn(colour)

    def swap_turn(self):
        """ Swap which player has the current turn.
        """

        self.is_white_turn = not self.is_white_turn

    def is_piece_selected(self):

        if(selected_piece is not None):

            return True

        else:

            return False

    def get_san(self, move):
        """ Return the SAN string for a given move.

            Args:
                - move: move to get SAN of
        """

        return self.board.get_san(move)

    def legal_move_exists(self, colour):

        # if statement returns true if list of moves is empty
        if(not self.get_player_moves(colour)):
            return False
        else:
            return True

    def get_status(self):
        """Return a member of the Status enum."""

        if self.is_white_turn:
            check = Status.white_check
            win = Status.white_win
            enemy_colour = colour.black
        else:
            check = Status.black_check
            win = Status.black_win
            enemy_colour = colour.white

        # Note that fiftyMoveRuleCount is effectively incremented twice for
        # each full move(once per player)
        if self.fifty_move_count == 100:
            return Status.fifty_move_draw
        if self.board.is_king_draw():
            return Status.king_draw

        in_check = self.board.is_in_check(enemy_colour)
        legal_move_exists = self.legal_move_exists(enemy_colour)

        if (not legal_move_exists) and in_check:
            return win
        if not legal_move_exists:
            return Status.stalemate
        if in_check:
            self.king_in_check = check
            return check
        else:
            self.king_in_check = Status.normal

        return Status.normal
