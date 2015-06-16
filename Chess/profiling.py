import Piece
import Gamestate
import cProfile
import Board
import Move
import Game
import pstats
import sys
import os

sys.path.insert(0, os.path.abspath(".."))

colour = Piece.PieceColour.white

def check_loop():

    for i in range(10):
        #b.is_in_check(colour)
        g = Game.Game("AI_1", "AI_1")
        g.play()

b = Board.Board()
b.test_setup()

cProfile.run("check_loop()", "profile_stats")
#cProfile.run("check_loop()", "profile_stats")

stream = open("stats.txt", "w")

p = pstats.Stats('profile_stats', stream=stream)
p.strip_dirs().sort_stats('time').print_stats()




