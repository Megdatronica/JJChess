"""Contains the Game class"""

# Tkinter graphics package
from tkinter import *
import Board
import Gamestate
import Player
import Piece
from Piece import PieceColour as colour
from Piece import PieceType as p_type
from Gamestate import Status as g_status
from Images import Images
import time

# Size of the board canvas to render in pixels
BOARD_SIZE = 900


class Game:

    """Interface between gamestate and AI/human input and manages UI for game.

    Attributes:
        -master: see ui elements
        -frame: see ui elements
        -player1: AI type string of player 1 (either filename in
                  ../Scripts or "Human")
        -player2: see above
        -listen: boolean for whether the UI should listen for user
                 click events.
        -ui_draw: true if we are drawing to the ui
        -game_state: current state of the game

    UI elements:
        - master: Master instance of tkinter
        - frame: The main window self.frame configured with
                 grid geometry
        - board_canvas: A canvas element on which to draw the board
        - cur_player_label: A label to indicate which colour's turn
                            it is
        - players_label: A label to indicate what type of players
                         are playing
        - resign_button: Button to resign the game
        - draw_button: Button to offer a draw to opponent
        - settings_button: Button to access a settings menu

    """

    def __init__(self, player1, player2):
        """ Start a game against the two selected types of player and build UI.
        """

        self.player1 = player1
        self.player2 = player2

        self.ui_draw = False
        self.board_canvas = None

        if (player1 == "Human"):
            self.white_player = Player.HumanPlayer(colour.white)
            self.listen = True
        else:
            self.white_player = Player.AIPlayer(
                Piece.PieceColour.white, player1)
            self.listen = False

        if (player2 == "Human"):
            self.black_player = Player.HumanPlayer(colour.black)
        else:
            self.black_player = Player.AIPlayer(
                Piece.PieceColour.black, player2)

        self.game_state = Gamestate.Gamestate()

        if(self.ui_draw):
            self.master = Tk()
            self.frame = Frame(self.master)
            self.board_canvas = Canvas(self.frame, width=BOARD_SIZE,
                                       height=BOARD_SIZE)
            # bind mouse event listener to board canvas
            self.board_canvas.bind("<Button-1>", self.mouse_press)

            Images.load_images(self.board_canvas)

            self.build_ui()

            self.frame.pack()

            self.master.mainloop()

        f = open("game.pgn", 'w')
        f.close()

    def build_ui(self):
        """ Build the UI window for the game.
        """

        self.frame.columnconfigure(0, pad=3)
        self.frame.columnconfigure(1, pad=3)
        self.frame.columnconfigure(2, pad=3)
        self.frame.columnconfigure(3, pad=3)

        self.frame.rowconfigure(0, pad=3)
        self.frame.rowconfigure(1, pad=3)
        self.frame.rowconfigure(2, pad=3)
        self.frame.rowconfigure(3, pad=3)

        self.game_state.draw(self.board_canvas)
        self.board_canvas.grid(row=0, column=0, rowspan=3)

        cur_player_label = Label(self.frame)
        cur_player_label["text"] = "White"
        cur_player_label["bg"] = "white"
        cur_player_label.grid(row=3, column=0)

        players_label = Label(self.frame)
        players_label["text"] = self.player1 + " vs " + self.player2
        players_label.grid(row=3, column=1, columnspan=3)

        resign_button = Button(self.frame)
        resign_button["text"] = "Resign"
        resign_button.grid(row=0, column=3)

        draw_button = Button(self.frame)
        draw_button["text"] = "Offer Draw"
        draw_button.grid(row=1, column=3)

        settings_button = Button(self.frame)
        settings_button["text"] = "Settings"
        settings_button.grid(row=2, column=3)

    def mouse_press(self, event):

        if(self.listen):

            square = Game.get_square_from_click(event)

            move = self.game_state.select_square(square, self.board_canvas)

            if(move is not None):

                self.turn_taken(move)

    def get_square_from_click(event):

        i = int(event.x*8/BOARD_SIZE)
        j = int(event.y*8/BOARD_SIZE)

        print((i, j))

        return (i, j)

    def play(self):
        """Play through a whole game, and return an enum indicating the result.

        Returns a member of the GameState.Status enum.

        """

        while(True):

            if(self.ui_draw):

                self.game_state.draw(self.board_canvas)

            current_player = self.get_current_player()

            if current_player.is_human:
                self.listen = True
                break

            else:
                self.listen = False
                status = self.take_ai_turn()

            if status not in (g_status.normal, g_status.white_check,
                              g_status.black_check):
                return status

    def get_current_player(self):
        """Return the player whose turn it currently is."""
        if self.game_state.is_white_turn:
            return self.white_player
        else:
            return self.black_player

    def take_ai_turn(self):
        """Take one turn of the game and change state.is_white_turn.

        Get a valid move from the current player, changes game_state
        to reflect the move being made (handling any pawn promotion), and
        finally changes whose turn it is. Returns the result of
        game_state.get_status() after making the move and also calls log_move.

        """

        current_player = self.get_current_player()

        move = current_player.get_move(self.game_state)
        move_SAN = self.game_state.get_san(move)
        self.game_state.make_move(move, self.board_canvas)
        promote_piece = self.ai_promote_pawn(current_player.colour)

        status = self.game_state.get_status()
        self.log_move(move_SAN, status, promote_piece)

        self.game_state.swap_turn()

        return status

    def turn_taken(self, move):

        move_SAN = self.game_state.get_san(move)
        self.game_state.make_move(move, self.board_canvas)

        promote_piece = self.human_promote_pawn()

        status = self.game_state.get_status()
        self.log_move(move_SAN, status, promote_piece)

        self.game_state.swap_turn()

        if status not in (g_status.normal, g_status.white_check,
                          g_status.black_check):
            return status
        else:
            self.play()

    def human_promote_pawn(self):
        pass

    def ai_promote_pawn(self, col):
        """Handles any pawn promotion and returns the ai's chosen promotion.

        Arguments:
            - col: the colour of the player to check promotions for

        Returns:
            - a Piece object, the piece which was chosen by the player to
              promote their pawn to. If no pawn is available for promotion,
              returns None.

        """

        if self.game_state.can_promote_pawn(col):
            current_player = self.get_current_player()
            piece = current_player.get_promotion(self.game_state)
            self.game_state.board.promote_pawn(col, piece.type)

            print("Pawn promoted!\n")
            print("Piece.type = ", piece.type)
            print(self.game_state.board.get_pictorial())

            raise KeyError("Stop")

            return piece

        return None

    def log_move(self, move_SAN, status, promote_piece):
        """Write a move into game.pgn.

        Note that this function should be called BEFORE
        state.swapTurn().

        Inputs:
            move_SAN:  a string representing the move made in SAN format,
                       without check/checkmate or promotion appended
            status:  the result of state.getStatus() after the move has
                     been made.
            promote_piece:  the piece which a pawn has been promoted to (the
                            result of calling self.promote_pawn())

        """

        f = open("game.pgn", 'a')

        # Note that state.moveCount is the number of HALF moves that have been
        # made, INCLUDING this one.
        move_number = int((self.game_state.count + 1) / 2)

        if self.game_state.is_white_turn:
            f.write(str(move_number) + ". " + move_SAN)
        else:
            f.write(move_SAN)

        if promote_piece is not None:
            if promote_piece.type == p_type.queen:
                f.write("=Q")
            elif promote_piece.type == p_type.knight:
                f.write("=K")
            elif promote_piece.type == p_type.bishop:
                f.write("=B")
            elif promote_piece.type == p_type.rook:
                f.write("=R")

        if status in (g_status.white_check, g_status.black_check):
            f.write("+ ")
        elif status == g_status.white_win:
            f.write("# 1-0")
        elif status == g_status.black_win:
            f.write("# 0-1")
        elif status in (g_status.king_draw, g_status.stalemate,
                        g_status.agreement_draw, g_status.fifty_move_draw):
            f.write(" 1/2-1/2")
        else:
            f.write(" ")

        f.close()

        g = open("boards.txt", 'a')
        g.write(self.game_state.board.get_pictorial())
        g.close()
