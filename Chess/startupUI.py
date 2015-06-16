"""Contains the startupUI class"""

from tkinter import *
from os import listdir
import Game
from Gamestate import Status

class startupUI:

    """Creates startup dialog for user to create a game.

       Attributes:
                 - ai_list: A list containing available UI scripts 
                   from ../Scripts
                 - master: see ui elements
                 - frame: see ui elements
                 - lb1 / lb2: see ui elements

       UI ELEMENTS:
                  - master: Master instance of tkinter
                  - frame: The main window self.frame configured with grid geometry
                  - p1_label: Label for the player one type list
                  - p2_label: Label for the player two type list
                  - lb1: A listbox to be populated with player one 
                         AI type options
                  - lb1: A listbox to be populated with player two 
                         AI type options
                  -start_game_button: Button to start the game with the 
                                      selected AI types

    """


    def __init__(self):

        """Populate a list of AIs and build the UI.
        """

        self.ai_list = []
        self.master = Tk()
        self.ui_draw = IntVar()

        self.populate_ai_list(self.ai_list)
        self.frame = Frame(self.master)
        self.build_ui()

        self.master.mainloop()

    def build_ui(self):

        """Build the startup UI.
        """

        self.frame.columnconfigure(0, pad=20)
        self.frame.columnconfigure(1, pad=20)


        self.frame.rowconfigure(0, pad=3)
        self.frame.rowconfigure(1, pad=3)
        self.frame.rowconfigure(2, pad=3)

        p1_label = Label(self.frame)
        p1_label["text"] = "Player 1"
        p1_label.grid(row=0, column=0)

        p2_label = Label(self.frame)
        p2_label["text"] = "Player 2"
        p2_label.grid(row=0, column=1)

        self.lb1 = Listbox(self.frame)
        for script in self.ai_list:
            self.lb1.insert(END, script)
        self.lb1.grid(row=1, column=0)

        self.lb1.selection_set(0)
        self.lb1["exportselection"] = 0

        self.lb2 = Listbox(self.frame)
        for script in self.ai_list:
            self.lb2.insert(END, script)
        self.lb2.grid(row=1, column=1)

        self.lb2.selection_set(0)
        self.lb2["exportselection"] = 0

        start_game_button = Button(self.frame)
        start_game_button["text"] = "Start Game"
        start_game_button["command"] = self.start_game
        start_game_button.grid(row=2, column=0)

        self.check_box = Checkbutton(self.frame, text="Draw UI",variable=self.ui_draw)
        self.check_box.grid(row=2,column=1)

        self.frame.pack()

    def populate_ai_list(self, list):

        """Populate the ai list with names of python scripts from "../Scripts".
        """

        list.append("Human")

        files = listdir("../Scripts")

        for filename in files:
            if filename[-3:] == ".py":

                list.append(filename[:-3])

    def start_game(self):

        """Destroy the start up window and start a game with the selected AIs.
        """

        player1 = self.lb1.get(ACTIVE)
        player2 = self.lb2.get(ACTIVE)

        self.master.destroy()
        self.master = None

        win = 0
        draw = 0
        loss = 0

        for i in range (1):

            print("Game "+str(i+1) + "\n")

            game = Game.Game(player1, player2, self.ui_draw.get())

            status = game.play()

            if status == Status.white_win:
                win += 1
            elif status == Status.black_win:
                loss += 1
            else:
                draw += 1

        print("White wins: " + str(win) + "\nDraws: " + str(draw) + "\nBlack Wins: "
               + str(loss))
