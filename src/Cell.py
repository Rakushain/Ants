import numpy as np
from util import rgbtohex
from Pheromones import Pheromones


class Cell:
    def __init__(self, world, x, y):
        self.world = world
        self.world_pos = np.array([x * world.cellW, y * world.cellH])
        self.canvasId = self.world.canvas.create_rectangle(
            self.world_pos[0],
            self.world_pos[1],
            self.world_pos[0] + world.cellW,
            self.world_pos[1] + world.cellH,
            outline="")

        self.pheromones = [[] for i in range(len(world.species))]

    def addPheromones(self, species_id, pos):
        self.pheromones[species_id].append(
            Pheromones(
                self.world,
                species_id,
                pos,
                self.world.time))
        
        print(int(len(self.pheromones[species_id])))
        self.world.canvas.itemconfig(
            self.canvasId, fill=rgbtohex([
                int(len(self.pheromones[species_id])), 0, 0]))

    def resetPheromones(self):
        self.world.canvas.itemconfig(self.canvasId, fill='white')
        for species in self.pheromones:
            for pheromone in species:
                # self.world.canvas.delete(pheromone.id)
                del pheromone
