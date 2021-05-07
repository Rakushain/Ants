import numpy as np
from util import create_circle


class Pheromones:
    def __init__(self, world, species_id, pos, creation_time):
        self.pos = pos
        self.species_id = species_id
        self.creation_time = creation_time

        # self.id = create_circle(world.canvas, pos[0], pos[1], 1, 'purple')

        # self.currentColor = np.zeros(3)

    # def addPheromones(self, amount):
    #     self.amount = np.clip(self.amount + amount, 0, 1)
    #     self.updateColor()

    # def reset(self):
    #     self.amount = 0
    #     self.updateColor()

    # def updateColor(self):
    #     if (len(self.world.nests) <= self.nestId):
    #         return
    #     self.currentColor = [
    # 255 - val * self.amount for val in
    # self.world.nests[self.nestId].invColor]
