import numpy as np
from Ant import Ant
from util import rgbtohex, create_circle


class Nest:
    def __init__(self, world, nest_id, x, y, species_id, nAnts):
        self.world = world
        self.pos = np.array([x, y])
        self.species_id = species_id
        self.size = nAnts / 2
        self.nest_id = nest_id
        self.food = 0

        species = self.world.species[species_id]
        species.set_active()

        self.color = species.color
        self.inv_color = np.array([255 - val for val in self.color])
        hexColor = rgbtohex(self.color)
        self.canvas_id = create_circle(
            self.world.canvas, x, y, self.size, hexColor)

        self.ants = [Ant(self.world, self, i, species.speed, species.stamina, hexColor)
                     for i in range(nAnts)]

    def addFood(self, amount):
        self.food += amount
        self.world.species[self.species_id].add_food(amount)
        print(f"Nid {self.nest_id}: {self.food} food")
