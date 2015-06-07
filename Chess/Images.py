'''Contains the Images class'''

from tkinter import *
import math


class Images:

    '''A class for loading and processing images

    '''

    def load_images(canvas):

        '''Load Images from ../Resources/Images for the piece icons

           Args:
               -canvas: The tkinter canvas element to laod the images to
        '''

        #The width of one square on the chess board (used for scaling)
        sq_width = int(canvas["width"])/8

        canvas.w_king = PhotoImage(file="../Resources/Images/wk.gif")
        canvas.w_king = canvas.w_king.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))
        
        canvas.b_king = PhotoImage(file="../Resources/Images/bk.gif")
        canvas.b_king = canvas.b_king.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.w_queen = PhotoImage(file="../Resources/Images/wq.gif")
        canvas.w_queen = canvas.w_queen.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.b_queen = PhotoImage(file="../Resources/Images/bq.gif")
        canvas.b_queen = canvas.b_queen.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.w_rook = PhotoImage(file="../Resources/Images/wr.gif")
        canvas.w_rook = canvas.w_rook.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.b_rook = PhotoImage(file="../Resources/Images/br.gif")
        canvas.b_rook = canvas.b_rook.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.w_bish = PhotoImage(file="../Resources/Images/wb.gif")
        canvas.w_bish = canvas.w_bish.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.b_bish = PhotoImage(file="../Resources/Images/bb.gif")
        canvas.b_bish = canvas.b_bish.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.w_nght = PhotoImage(file="../Resources/Images/wn.gif")
        canvas.w_nght = canvas.w_nght.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.b_nght = PhotoImage(file="../Resources/Images/bn.gif")
        canvas.b_nght = canvas.b_nght.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.w_pawn = PhotoImage(file="../Resources/Images/wp.gif")
        canvas.w_pawn = canvas.w_pawn.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))

        canvas.b_pawn = PhotoImage(file="../Resources/Images/bp.gif")
        canvas.b_pawn = canvas.b_pawn.zoom(math.floor(sq_width/32),
                                                math.floor(sq_width/32))