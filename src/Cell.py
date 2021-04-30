import numpy as np
from util import rgbtohex

class Cell:
    def __init__(self, canvas, canvasId):
        self.canvas = canvas
        self.canvasId = canvasId
        self.pheromones = np.zeros(3)

    def addPheromones(self, amount, decreaseLater=True):
        self.pheromones = np.add(self.pheromones, amount)
        self.pheromones = np.clip(self.pheromones, 0, 1)

        # if self.refresh % 10 == 0:
        self.canvas.itemconfig(self.canvasId, fill=rgbtohex(self.pheromones * 255))

        if decreaseLater and np.sum(self.pheromones) > 0:
            self.canvas.after(25000, lambda: self.addPheromones(-amount, False))

