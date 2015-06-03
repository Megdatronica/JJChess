"""Contains the Game class"""

# Tkinter graphics package
from tkinter import *
import Board
import Gamestate
import Player
import Piece
from Piece import PieceColour as colour
from Gamestate import Status as status
from Images import Images

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

        if (player1 == "Human"):
            self.white_player = Player.HumanPlayer(colour.white)
        else:
            self.white_player = Player.AIPlayer(colour.white, player1)

        if (player2 == "Human"):
            self.black_player = Player.HumanPlayer(colour.black)
        else:
            self.black_player = Player.AIPlayer(colour.black, player2)

        self.master = Tk()
        self.frame = Frame(self.master)
        self.board_canvas = Canvas(self.frame, width=BOARD_SIZE,
                                   height=BOARD_SIZE)
        # bind mouse event listener to board canvas
        self.board_canvas.bind("<Button-1>", self.mouse_press)

        self.game_state = Gamestate.Gamestate()

        Images.load_images(self.board_canvas)

        self.build_ui()

        self.frame.pack()

        self.master.mainloop()

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

        square = Game.get_square_from_click(event)

<<<<<<< HEAD
        self.game_state.select_square(square, self.board_canvas)

=======
>>>>>>> 64da11d6974bf2f263c1f43bc2496f775e387d3c
    def get_square_from_click(event):

        print(event.x)
        print(event.y)

    def play(self):
        """Play through a whole game, and return an enum indicating the result.

        Returns a member of the GameState.Status enum.

        """

        while(true):
            status = self.take_turn()

            if status not in (
                    status.normal, status.white_check, status.black_check):
                return status

    def get_current_player(self):
        """Return the player whose turn it currently is."""
        if self.game_state.is_white_turn:
            return self.white_player
        else:
            return self.black_player

    def take_turn(self):
        """Take one turn of the game and change state.is_white_turn.

        Get a valid move from the current player, changes game_state
        to reflect the move being made (handling any pawn promotion), and
        finally changes whose turn it is. Returns the result of 
        game_state.get_status() after making the move and also calls log_move.

        """

        current_player = self.get_current_player()

        if current_player.is_human:
            raise NotImplementedError("JOE THIS BIT IS YOURS")
        else:
            move = current_player.get_move(game_state)
            move_SAN = state.get_san(move)
            state.make_move(move)

            promote_piece = promotePawn()

        status = state.get_status()
        self.logMove(move_SAN, status, promote_piece)

        state.swapTurn()

        return statusInt

    def promote_pawn(self):
        """Handles any pawn promotion and returns the chosen promotion.

        Returns:
            - a Piece object, the piece which was chosen by the player to
              promote their pawn to. If no pawn is available for promotion,
              returns None.

        """

        if self.game_state.can_promote_pawn():
            current_player = self.get_current_player()
            piece = current_player.get_promotion(game_state)
            game_state.promote_pawn(piece)
            return piece

        return None

    def log_move(self, move_SAN, status, promote_val):
