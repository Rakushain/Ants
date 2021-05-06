import numpy as np
from Ant import Ant
from util import rgbtohex, create_circle


class Nest:
    def __init__(self, world, x, y, speciesId, nAnts):
        self.world = world
        self.x = x
        self.y = y
        self.speciesId = speciesId
        self.size = nAnts / 2

        species = self.world.species[speciesId]

        self.color = species.color
        self.invColor = np.array([255 - val for val in self.color])
        hexColor = rgbtohex(self.color)
        self.id = create_circle(self.world.canvas, x, y, self.size, hexColor)

        self.ants = [Ant(self.world.canvas, x, y, species.speed, species.stamina, hexColor)
                     for _ in range(nAnts)]
