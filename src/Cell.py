import numpy as np
from util import rgbtohex
from Pheromones import Pheromones

class Cell:
    def __init__(self, canvas, canvasId, maxNests):
        self.canvas = canvas
        self.canvasId = canvasId
        self.pheromones = [Pheromones(np.zeros(3), 0) for _ in range(maxNests)]

    def addPheromones(self, nestId, amount, decreaseLater=True):
        print('XDDDD')
        nest = self.pheromones[nestId]
        nest.addPheromones(amount)

        # TODO: all nests

        self.canvas.itemconfig(
            self.canvasId, fill=rgbtohex(
                self.pheromones[nestId].currentColor))

        if decreaseLater and np.sum(self.pheromones[nestId].amount) > 0:
            self.canvas.after(
                25000, lambda: self.addPheromones(nestId, -amount, False))
