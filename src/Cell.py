import numpy as np
from util import rgbtohex
from Pheromones import Pheromones


class Cell:
    def __init__(self, world, x, y):
        self.is_wall = False
        self.world = world
        self.pos = np.array([x, y])
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

        self.world.canvas.itemconfig(
            self.canvasId, fill=rgbtohex([
                int(255 - 10 * len(self.pheromones[species_id])), 255, 255]))

    def reset(self):
        self.world.canvas.itemconfig(self.canvasId, fill="white")
        for species in self.pheromones:
            for pheromone in species:
                # self.world.canvas.delete(pheromone.id)
                del pheromone

    def addWall(self):
        self.is_wall = True
        self.world.canvas.itemconfig(
            self.canvasId, fill="black")