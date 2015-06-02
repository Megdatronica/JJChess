"""Contains the Gamestate class"""

import Board
import Move
from Piece import *

class Gamestate:

    """ Contains all information required to display current state of game.

        Args:
            - board: a board corresponding to the current game state
    """

    def __init__(self):

        self.board = Board.Board()
        self.board.setup()

        #Set castling to true
        self.w_castle_K = True
        self.w_castle_Q = True
        self.b_castle_K = True
        self.b_castle_Q = True

        #Set moves counts to start of game
        self.count = 0
        self.fifty_move_count = 0;

        self.en_passant_sq = None

    def draw(self, canvas):

        self.board.draw(canvas)

    def make_move(self, move):

        update_counts(move)
        board.make_move(move)

    def update_counts(self, move):

        piece = self.board.get_piece(*move.start_posn)

        #increment move counter
        self.count += 1

        #reset en passant square
        en_passant_sq = None

        #Check whether the king has moved
        if(piece.type == PieceType.king):

            if(piece.colour == PieceColour.white):

                self.w_castle_K = False
                self.w_castle_Q = False
            else:

                self.b_castle_K = False
                self.b_castle_Q = False

        #Check whether a corner rook has moved
        #Note: It is unnecessary to check piece colour
        #as, for example, a white rook on A8 means the 
        #black rook must have moved
        if(piece.type == PieceType.rook):

            if(move.start_posn == (0,0)):

                self.b_castle_Q = False

            elif(move.start_posn == (7,0)):

                self.b_castle_K = False

            elif(move.start_posn == (0,7)):

                self.w_castle_Q = False

            elif(move.start_posn == (7,7)):

                self.w_castle_K = False

        #Check if we need to store an en passant square

        if(piece.type == PieceType.pawn):
            #check if double move
            if(abs(move.start_posn[1] - move.end_posn[1]) == 2):
                if(piece.colour = PieceColour.white):

                    self.en_passant_sq = (move.start_posn[0], 
                                          move.start_posn[1] - 1)
                else:

                    self.en_passant_sq = (move.start_posn[0], 
                                          move.start_posn[1] + 1)

        #check whether there has been a capture

        if(self.board.is_take_move(move)):

            #reset counter
            self.fifty_move_count = 0
        else:

            self.fifty_move_count += 1