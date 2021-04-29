import tkinter as tk
import numpy as np
from Monde import Monde
from Nourriture import Nourriture
from Nid import Nid
import sys

class MainGUI:
    def __init__(self, canvasW, canvasH, cellsX, cellsY): 
        self.root = tk.Tk()
        self.root.title("Fourmis")
        # root.resizable(0,0)
        self.root.wm_attributes("-topmost", 1)

        self.canvasW = canvasW
        self.canvasH = canvasH

        self.labelframe_top()
        self.canvas = tk.Canvas(self.root, width=canvasW, height=canvasH, bd=0, highlightthickness=0)
        
        self.monde = Monde(self.canvas, self.canvasW, self.canvasH, 50, 50)
        self.canvas.bind("<Button-1>", self.handleCanvasClick)

        self.foodOrNid = tk.IntVar(0)
        foodRadio = tk.Radiobutton(self.root, text="Nourriture", variable=self.foodOrNid, value=0)
        foodRadio.pack()
        nidRadio = tk.Radiobutton(self.root, text="Nid", variable=self.foodOrNid, value=1)
        nidRadio.pack()

        self.canvas.pack()
        self.root.mainloop()


    def create_world(self):
        self.canvas.delete("all")
        self.monde.reset()
        print(sys.getrefcount(self.canvas))
        
    def handleCanvasClick(self, event):
        print(event.x, event.y)
        if self.monde.started:
            return
        
        if self.foodOrNid.get() == 0:
            print('FOOD')
            self.monde.addFood(Nourriture(self.canvas, event.x, event.y, 20))
        elif self.foodOrNid.get() == 1:
            print('NID')
            self.monde.addNid(Nid(self.canvas, event.x, event.y, 10, 100, 200, np.array([255, 0, 0])))


    def labelframe_top (self):
        labelframe = tk.LabelFrame(self.root)
        labelframe.pack(fill="both", expand="yes")

        button_new = tk.Button(labelframe, text="Nouveau Monde", command=self.create_world)
        button_new.pack(side=tk.LEFT)
        
        button_start = tk.Button(labelframe, text="GO", command=lambda: self.monde.start())
        button_start.pack(side=tk.LEFT)

        button_start = tk.Button(labelframe, text="->", command=lambda: self.monde.next_frame())
        button_start.pack(side=tk.LEFT)

        labelframe.pack(fill="both", padx=5, pady=5)


    def labelframe_bottom(self):
        labelframe_bottom = tk.LabelFrame(self.root, bg = 'grey')

        button_about =tk.Button(labelframe_bottom, text="A propos", height = 0, width = 50)
        button_step = tk.Button(labelframe_bottom, text="Pas", height = 0, width  = 25)
        button_go = tk.Button(labelframe_bottom, text="Go", height = 0, width = 25)

        button_about.pack(side = "left")
        button_step.place(x = 375, y = 0)
        button_go.place(x = 575, y = 0)

        phero = tk.Checkbutton(labelframe_bottom, text = "AfficherPhéromones")
        phero.place(x = 775, y = 0)

        labelframe_bottom.pack(side = "bottom", fill = "both")

        bottom = tk.Label(labelframe_bottom, bg = "grey")
        bottom.pack(side = "bottom")
   