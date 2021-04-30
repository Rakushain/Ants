import tkinter as tk
import numpy as np
from World import World
from Food import Food
from Nest import Nest
import sys

BG_COLOR = "#F1F1F1"


class MainGUI:
    def __init__(self, canvasW, canvasH, cellsX, cellsY):
        self.root = tk.Tk()
        self.root.configure(bg=BG_COLOR)
        self.root.title("Ants")
        # root.resizable(0,0)
        self.root.wm_attributes("-topmost", 1)

        self.canvasW = canvasW
        self.canvasH = canvasH

        self.foodOrNest = tk.IntVar(0)

        self.create_frame_top()
        self.create_canvas()
        self.create_frame_bottom()

        self.world = World(self.canvas, self.canvasW, self.canvasH, 50, 50)

        self.root.mainloop()

    def create_world(self):
        self.canvas.delete("all")
        self.world.reset()
        print(sys.getrefcount(self.canvas))

    def handleCanvasClick(self, event):
        print(event.x, event.y)
        if self.world.started:
            return

        if self.foodOrNest.get() == 0:
            print('FOOD')
            self.world.addFood(Food(self.canvas, event.x, event.y, 20))
        elif self.foodOrNest.get() == 1:
            print('NEST')
            self.world.addNest(
                Nest(self.canvas, event.x, event.y, 10, 100, 200, np.array([255, 0, 0])))

    def create_canvas(self):
        frame = tk.Frame(self.root)
        
        self.canvas = tk.Canvas(
            frame,
            width=self.canvasW,
            height=self.canvasH,
            bd=0,
            bg=BG_COLOR,
            highlightthickness=0)
        self.canvas.pack(expand="yes")
        self.canvas.bind("<Button-1>", self.handleCanvasClick)

        frame.pack(fill="both", expand="yes")

    def create_frame_top(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both")

        button_new = tk.Button(
            frame,
            text="Nouveau Monde",
            command=self.create_world)
        button_new.pack(side=tk.LEFT)

        foodOrNestRadioFrame = tk.Frame(frame)

        foodRadio = tk.Radiobutton(
            foodOrNestRadioFrame,
            text="Food",
            variable=self.foodOrNest,
            value=0)
        foodRadio.pack()
        nestRadio = tk.Radiobutton(
            foodOrNestRadioFrame,
            text="Nest",
            variable=self.foodOrNest,
            value=1)
        nestRadio.pack()

        foodOrNestRadioFrame.pack()

        frame.pack(fill="both", padx=5, pady=5)

    def create_frame_bottom(self):
        frame = tk.Frame(self.root, bg='grey')

        
        button_start = tk.Button(
            frame,
            text="GO =>",
            command=lambda: self.world.start())
        button_start.pack(side=tk.LEFT)

        button_start = tk.Button(
            frame,
            text="Pas ->",
            command=lambda: self.world.next_frame())
        button_start.pack(side=tk.LEFT)

        frame.pack(side="bottom", fill="both", padx=5, pady=5)

        # button_about = tk.Button(
        #     labelframe_bottom,
        #     text="A propos",
        #     height=0,
        #     width=50)
        # button_step = tk.Button(
        #     labelframe_bottom,
        #     text="Pas",
        #     height=0,
        #     width=25)
        # button_go = tk.Button(labelframe_bottom, text="Go", height=0, width=25)

        # button_about.pack(side="left")
        # button_step.place(x=375, y=0)
        # button_go.place(x=575, y=0)

        # phero = tk.Checkbutton(labelframe_bottom, text="AfficherPhéromones")
        # phero.place(x=775, y=0)

        # labelframe_bottom.pack(side="bottom", fill="both")

        # bottom = tk.Label(labelframe_bottom, bg="grey")
        # bottom.pack(side="bottom")
