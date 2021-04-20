import tkinter as tk
import numpy as np
from Monde import Monde

root = tk.Tk()
root.title("Fourmis")
# root.resizable(0,0)
root.wm_attributes("-topmost", 1)

WIDTH=500
HEIGHT=500

labelframe = tk.LabelFrame(root, text="This is a LabelFrame")
labelframe.pack(fill="both", expand="yes")
 
left = tk.Label(labelframe, text="Inside the LabelFrame")
left.pack()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()

monde = Monde(canvas, WIDTH, HEIGHT, 50, 50)
root.mainloop()