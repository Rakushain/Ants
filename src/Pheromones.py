import numpy as np


class Pheromones:
    def __init__(self, world, nestId, amount):
        self.amount = amount
        self.world = world
        self.nestId = nestId
        self.currentColor = np.zeros(3)

    def addPheromones(self, amount):
        self.amount = np.clip(self.amount + amount, 0, 1)
        self.updateColor()
        
    def reset(self):
        self.amount = 0
        self.updateColor()

    def updateColor(self):
        if (len(self.world.nests) <= self.nestId):
            return
        self.currentColor = [255 - val * self.amount for val in self.world.nests[self.nestId].invColor]
