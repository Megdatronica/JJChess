#Tkinter graphics package
from tkinter import *

# Size of the board canvas to render
BOARD_SIZE = 400

class Game:

    def __init__(self, player1, player2):

        #  Initiate frame and canvas for board (and give it a border)
        master = Tk()
        frame = Frame(master)

        frame.columnconfigure(0, pad=3)
        frame.columnconfigure(1, pad=3)
        frame.columnconfigure(2, pad=3)
        frame.columnconfigure(3, pad=3)

        frame.rowconfigure(0, pad=3)
        frame.rowconfigure(1, pad=3)
        frame.rowconfigure(2, pad=3)
        frame.rowconfigure(3, pad=3)


        # TODO: Move to Board.draw() (and call that from gamestate?)
        board_canvas = Canvas(frame, width=BOARD_SIZE, height=BOARD_SIZE)
        board_canvas.create_line(5, 5, BOARD_SIZE - 5, 5)
        board_canvas.create_line(5, 5, 5, BOARD_SIZE - 5)
        board_canvas.create_line(BOARD_SIZE-5, 5, BOARD_SIZE-5, BOARD_SIZE-5)
        board_canvas.create_line(5, BOARD_SIZE-5, BOARD_SIZE-5, BOARD_SIZE-5)

        board_canvas.grid(row=0, column=0, rowspan=3)

        cur_player_label = Label(frame)
        cur_player_label["text"] = "White"
        cur_player_label["bg"] = "white"
        cur_player_label.grid(row=3,column=0)

        players_label = Label(frame)
        players_label["text"] = "Player 1 vs Player 2 (placeholder text)"
        players_label.grid(row=3, column=1, columnspan=3)

        resign_button = Button(frame)
        resign_button["text"] = "Resign"
        resign_button.grid(row=0,column=3)

        draw_button = Button(frame)
        draw_button["text"] = "Offer Draw"
        draw_button.grid(row=1,column=3)

        settings_button = Button(frame)
        settings_button["text"] = "Settings"
        settings_button.grid(row=2,column=3)

        frame.pack()

        master.mainloop()
