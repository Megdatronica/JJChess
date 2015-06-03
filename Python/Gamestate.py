"""Contains the Gamestate class"""

import Board
import Move
from Piece import *


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

    def draw(self, canvas):
        """ Draw the gamestate to a Tkinter canvas element.

            Args:
                -canvas: the Tkinter canvas element
        """

        self.board.draw(canvas)

    def make_move(self, move):
        """ Make a given move.

            Args:
                - move: move to be made
        """

        update_counts(move)
        board.make_move(move)

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
                if(piece.colour=PieceColour.white):

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

    def is_legal_move(self, move, colour):
        """ Check if a given move is legal

            Args:
                - move: move to be checked
                - colour: colour of player making move
        """

        moves = get_all_moves(colour)

        if move in moves:
            return True
        else:
            return False

    def get_all_moves(self, colour):
        """ Return all the legal moves that the coloured player can make.

            (includes castling and en passant moves)

            Args:
                - colour: colour of the player
        """

        moves = self.get_player_moves(colour)

        if(self.w_castle_K=True):

            castle = Move((4, 7), (6, 7), castle=True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.w_castle_Q=True):

            castle = Move((4, 7), (2, 7), castle=True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.b_castle_K=True):

            castle = Move((4, 0), (6, 0), castle=True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.b_castle_Q=True):

            castle = Move((4, 0), (2, 0), castle=True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        return moves

    def get_player_moves(self, colour):
        """ Helper function to get_all_moves - returns all but castling.

            Args:
                - colour: colour of the player making the move
        """

        b_moves = []

        for i ion range(8):
            for j in range(8):

                if(self.board.get_piece(i, j).type == PieceType.pawn and
                        en_passant_sq != None):

                    b_moves.extend(self.board.get_piece_moves(i, j))

                    if(abs(i - en_passant_sq[0]) == 1 and
                            (j - en_passant_sq[1]) == 0):

                        pawn_square = (en_passant_sq[0], j)
                        b_moves.append(Move((i, j), en_passant_sq,
                                            en_passant=True,
                                            en_passant_posn=pawn_square))

                else:
                    b_moves.extend(self.board.get_piece_moves(i, j))

    def can_promote_pawn(self, colour):
        """ Check if a pawn can be promoted.

            Args:
                - colour: colour of player to check for
        """

        self.board.can_promote_pawn(colour)

    def swap_turn(self):
        """ Swap which player has the current turn.
        """

        self.is_white_turn = !is_white_turn

    def get_san(move):
        """ Return the SAN string for a given move.

            Args:
                - move: move to get SAN of
        """

        san = board.get_san(move)
