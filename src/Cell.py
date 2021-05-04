import numpy as np
from util import rgbtohex
from Pheromones import Pheromones


class Cell:
    def __init__(self, world, x, y):
        self.world = world
        self.canvasId = self.world.canvas.create_rectangle(
            x * world.cellW,
            y * world.cellH,
            (x + 1) * world.cellW,
            (y + 1) * world.cellH,
            outline=""),
        self.pheromones = [
            Pheromones(
                world, i, 0) for i in range(
                world.maxNests)]

    def addPheromones(self, nestId, amount, decreaseLater=True):
        nest = self.pheromones[nestId]
        nest.addPheromones(amount)

        # TODO: all nests

        self.world.canvas.itemconfig(
            self.canvasId, fill=rgbtohex(
                self.pheromones[nestId].currentColor))

        if decreaseLater and np.sum(self.pheromones[nestId].amount) > 0:
            self.world.canvas.after(
                25000, lambda: self.addPheromones(nestId, -amount, False))

    def resetPheromones(self):
        self.world.canvas.itemconfig(self.canvasId, fill='white')
        for pheromone in self.pheromones:
            pheromone.reset()
