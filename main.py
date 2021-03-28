import tkinter as tk
import numpy as np
import time
from math import sqrt, floor, sin, cos

root = tk.Tk()
root.title = "Game"
root.resizable(0,0)
root.wm_attributes("-topmost", 1)

WIDTH=500
HEIGHT=500

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()


def create_circle(canvas, x, y, r, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=color)

def rgbtohex(rgb):
    r, g, b = rgb
    return f'#{floor(r):02x}{floor(g):02x}{floor(b):02x}'

def rotVecteur(vect, angle):
    rot = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
    return np.dot(rot, vect)


class Case:
    def __init__(self, canvasId):
        self.canvasId = canvasId
        self.pheromones = np.zeros(3)

    def addPheromones(self, amount):
        self.pheromones = np.add(self.pheromones, amount)
        self.pheromones = np.clip(self.pheromones, 0, 255)


class Monde:
    nids = []
    nourriture = []

    def __init__(self, canvas, width, height):
        celluleW = WIDTH / width
        celluleH = HEIGHT / height
        self.canvas = canvas

        self.grille = np.array(
            [
                [
                    Case(canvas.create_rectangle(x * celluleW, y * celluleH, (x+1) * celluleW, (y+1) * celluleH, fill="gray"))
                    for y in range(height)
                ]
                for x in range(width)
            ]
        )

        self.width = width
        self.height = height
        self.updateNids()
        self.drawGrille()

        self.nids.append(Nid(canvas, 150, 150, 10, 80, np.array([255, 0, 0])))
        self.nids.append(Nid(canvas, 320, 400, 6, 12, np.array([0, 255, 0])))
        self.nids.append(Nid(canvas, 250, 200, 8, 25, np.array([0, 0, 255])))
        self.nourriture.append(Nourriture(canvas, 100, 150, 10))
    
    def updateNids(self):
        for nid in self.nids:
            for fourmi in nid.fourmis:
                for nourriture in self.nourriture:
                    if fourmi.hasFood:
                        if sqrt((fourmi.x - nid.x)**2 + (fourmi.y - nid.y)**2) <= nid.taille:
                            fourmi.hasFood = False
                    elif sqrt((fourmi.x - nourriture.x)**2 + (fourmi.y - nourriture.y)**2) <= nourriture.maxAmount:
                        nourriture.decrease(1)
                        fourmi.hasFood = True

                self.addPheromones(fourmi.x, fourmi.y, nid.color / 255)
                fourmi.draw()

        self.canvas.after(20, self.updateNids)
    
    def drawGrille(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grille[x, y].addPheromones(np.array([-0.25, -0.25, -0.25]))
                        
                self.canvas.itemconfig(self.grille[x, y].canvasId, fill=rgbtohex(self.grille[x, y].pheromones))
        self.canvas.after(100, self.drawGrille)

    def addPheromones(self, x, y, color):
        grilleX = int(x / WIDTH * self.width)
        grilleY = int(y / HEIGHT * self.height)

        # TODO: fourmi qui sort du canvas = crash
        if grilleX < 0 or grilleX >= self.width or grilleY < 0 or grilleY >= self.height:
            return
        self.grille[grilleX, grilleY].addPheromones(color)


class Nid:
    def __init__(self, canvas, x, y, taille, nFourmis, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.taille = taille
        self.color = color
        hexColor = rgbtohex(color)
        self.id = create_circle(canvas, x, y, taille, hexColor)

        self.fourmis = [Fourmi(self, hexColor) for _ in range(nFourmis)]


class Fourmi:
    speed = 2
    hasFood = False

    def __init__(self, nid, color):
        self.canvas = nid.canvas
        self.nid = nid
        self.x = nid.x
        self.y = nid.y
        self.id = create_circle(self.canvas, self.x, self.y, 2, color)
        self.direction = np.random.uniform(-1.0, 1.0, (2))
        self.draw()

    def draw(self):
        self.direction = np.array([self.nid.x - self.x, self.nid.y - self.y]) if self.hasFood else rotVecteur(self.direction, np.random.uniform(-np.pi/4, np.pi/4))
        x, y = self.direction / np.linalg.norm(self.direction)
        self.canvas.move(self.id, x * self.speed, y * self.speed) # TODO: optimiser (2x meme calcul)
        self.x += x * self.speed
        self.y += y * self.speed


class Nourriture:
    def __init__(self, canvas, x, y, maxAmount):
        self.canvas = canvas
        self.maxAmount = maxAmount
        self.amount = maxAmount
        self.x = x
        self.y = y
        self.idOut = create_circle(canvas, x, y, maxAmount, "gray")
        self.idIn = create_circle(canvas, x, y, maxAmount, "white")
    
    def decrease(self, amount):
        self.amount -= amount
        if (self.amount <= 0):
            return
        newScale = self.amount / (self.amount + 1)
        self.canvas.scale(self.idIn, self.x, self.y, newScale, newScale)

monde = Monde(canvas, 25, 25)
root.mainloop()