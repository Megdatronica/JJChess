"""Contains the Game class"""

# Tkinter graphics package
from tkinter import *
import Board
import Gamestate
from Images import Images

# Size of the board canvas to render in pixels
BOARD_SIZE = 900


class Game:

    """ Interface between gamestate and AI/human input and manages UI for game.

        Attributes:
                  -master: see ui elements
                  -frame: see ui elements
                  -player1: AI type string of player 1 (either filename in 
                           ../Scripts or "human")
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

        self.master = Tk()
        self.frame = Frame(self.master)
        self.board_canvas = Canvas(self.frame, width=BOARD_SIZE,
                                   height=BOARD_SIZE)
        self.gamestate = Gamestate.Gamestate()

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

        self.gamestate.draw(self.board_canvas)
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


