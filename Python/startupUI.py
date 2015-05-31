from tkinter import *
from os import listdir
import Game

class startupUI:

    ai_list = []
    lb1 = None
    lb2 = None

    def __init__(self, master):

        ai_list = []

        self.populate_ai_list(ai_list)

        frame = Frame(master)

        frame.columnconfigure(0, pad=20)
        frame.columnconfigure(1, pad=20)


        frame.rowconfigure(0, pad=3)
        frame.rowconfigure(1, pad=3)
        frame.rowconfigure(2, pad=3)

        p1_label = Label(frame)
        p1_label["text"] = "Player 1"
        p1_label.grid(row=0, column=0)

        p2_label = Label(frame)
        p2_label["text"] = "Player 2"
        p2_label.grid(row=0, column=1)

        self.lb1 = Listbox(frame)
        for script in ai_list:
            self.lb1.insert(END, script)
        self.lb1.grid(row=1, column=0)

        self.lb1.selection_set(0)
        self.lb1["exportselection"] = 0

        self.lb2 = Listbox(frame)
        for script in ai_list:
            self.lb2.insert(END, script)
        self.lb2.grid(row=1, column=1)

        self.lb2.selection_set(0)
        self.lb2["exportselection"] = 0

        start_game_button = Button(frame)
        start_game_button["text"] = "Start Game"
        start_game_button["command"] = self.start_game
        start_game_button.grid(row=2, column=0, columnspan=2)

        frame.pack()

        master.mainloop()

    # Populate the ai_list with names of python scripts from ../Scripts
    def populate_ai_list(self, list):

        list.append("Human")

        files = listdir("../Scripts")

        for filename in files:
            if filename[-3:] == ".py":

                list.append(filename[:-3])

    def start_game(self):

        player1 = self.lb1.get(ACTIVE)
        player2 = self.lb2.get(ACTIVE)

        Game.Game(player1, player2)



master = Tk()
startupUI(master)