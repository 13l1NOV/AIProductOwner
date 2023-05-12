from tkinter import *

class View:

    tk = Tk()
    tk.title('Game')
    tk.resizable(0, 0)
    tk.wm_attributes('-topmost', 1)
    canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
    canvas.pack()
    tk.update()
