# Tkinter graphics package
from tkinter import *
import Board
from Images import Images

# Size of the board canvas to render
BOARD_SIZE = 900


class Game:

    def __init__(self, player1, player2):

        self.master = Tk()
        self.frame = Frame(self.master)
        self.board_canvas = Canvas(self.frame, width=BOARD_SIZE,
                                   height=BOARD_SIZE)

        Images.load_images(self.board_canvas)

        self.board = Board.Board()
        self.board.setup()

        self.frame.columnconfigure(0, pad=3)
        self.frame.columnconfigure(1, pad=3)
        self.frame.columnconfigure(2, pad=3)
        self.frame.columnconfigure(3, pad=3)

        self.frame.rowconfigure(0, pad=3)
        self.frame.rowconfigure(1, pad=3)
        self.frame.rowconfigure(2, pad=3)
        self.frame.rowconfigure(3, pad=3)

        self.board.draw(self.board_canvas)
        self.board_canvas.grid(row=0, column=0, rowspan=3)

        cur_player_label = Label(self.frame)
        cur_player_label["text"] = "White"
        cur_player_label["bg"] = "white"
        cur_player_label.grid(row=3, column=0)

        players_label = Label(self.frame)
        players_label["text"] = player1 + " vs " + player2
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

        self.frame.pack()

        self.master.mainloop()
