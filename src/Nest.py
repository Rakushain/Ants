import numpy as np
from Ant import Ant
from util import rgbtohex, create_circle


class Nest:
    def __init__(self, world, x, y, species_id, nAnts):
        self.world = world
        self.pos = np.array([x, y])
        self.species_id = species_id
        self.size = nAnts / 2

        species = self.world.species[species_id]

        self.color = species.color
        self.invColor = np.array([255 - val for val in self.color])
        hexColor = rgbtohex(self.color)
        self.id = create_circle(self.world.canvas, x, y, self.size, hexColor)

        # TODO: better nest ID
        self.ants = [Ant(self.world, self, i, species.speed, species.stamina, hexColor)
                     for i in range(nAnts)]
