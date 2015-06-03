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

        self.w_castle_K = True
        self.w_castle_Q = True
        self.b_castle_K = True
        self.b_castle_Q = True

        self.count = 0
        self.fifty_move_count = 0;

        self.en_passant_sq = None

        self.is_white_turn = True

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

    def is_legal_move(self, move, colour):

        moves = get_all_moves(colour)

        if(move in moves)
            return True

        else:
            return False

    def get_all_moves(self, colour):

        moves = self.get_player_moves(colour)

        if(self.w_castle_K = True):

            castle = Move((4,7), (6,7), castle = True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.w_castle_Q = True):

            castle = Move((4,7), (2,7), castle = True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.b_castle_K = True):

            castle = Move((4,0), (6,0), castle = True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        if(self.b_castle_Q = True):

            castle = Move((4,0), (2,0), castle = True)
            if(self.board.is_possible_legal_move(castle)):

                moves.append(castle)

        return moves


    def get_player_moves(self, colour):

        b_moves = []

        for i ion range(8):
            for j in range(8):


                if(self.board.get_piece(i,j).type == PieceType.pawn and 
                    en_passant_sq != None):

                    b_moves.extend(self.board.get_piece_moves(i,j))

                    if(abs(i - en_passant_sq[0]) == 1 and 
                        (j - en_passant_sq[1]) == 0):

                        pawn_square = (en_passant_sq[0], j)
                        b_moves.append(Move((i, j), en_passant_sq, 
                                       en_passant = True, 
                                       en_passant_posn = pawn_square))

                else:
                    b_moves.extend(self.board.get_piece_moves(i,j))


    def swap_turn(self):

        self.is_white_turn = !is_white_turn

    def get_san(move):

        san = board.get_san(move)
        

