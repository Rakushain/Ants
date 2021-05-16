import numpy as np
from util import rgb_to_hex
from Pheromones import Pheromones


class Cell:
    def __init__(self, world, x, y):
        self.is_wall = False
        self.world = world
        self.pos = np.array([x, y])
        self.world_pos = np.array([x * world.cellW, y * world.cellH])
        self.canvas_id = self.world.canvas.create_rectangle(
            self.world_pos[0],
            self.world_pos[1],
            self.world_pos[0] + world.cellW,
            self.world_pos[1] + world.cellH,
            outline="")

        self.pheromones = [[] for i in range(len(world.species))]

    def get_pheromones(self, species_id):
        total_pheromones = 0
        for pheromone in self.pheromones[species_id][:]:
            lifetime = self.world.time - pheromone.creation_time
            evaporation = lifetime / 1000
            # par defaut, les pheromones disparaissent apres 1000 frames

            if evaporation > 1:
                self.pheromones[species_id].remove(pheromone)
                del pheromone
                continue

            total_pheromones += 1 - evaporation

        return total_pheromones

    def add_pheromones(self, species_id, pos):
        self.pheromones[species_id].append(
            Pheromones(
                self.world,
                species_id,
                pos,
                self.world.time))

        self.update_color()

    def update_color(self):
        color = np.array([0, 0, 0])
        for species_id, species_pheromones in enumerate(self.pheromones):
            color += self.world.species[species_id].inv_color * \
                len(species_pheromones)

        color = np.clip(np.around(color / 100), 0, 255)
        color = np.array([255 - val for val in color])

        self.world.canvas.itemconfig(
            self.canvas_id, fill=rgb_to_hex(color))

    def reset(self):
        self.world.canvas.itemconfig(self.canvas_id, fill="white")
        for species in self.pheromones:
            for pheromone in species:
                # self.world.canvas.delete(pheromone.id)
                del pheromone

    def add_wall(self):
        self.is_wall = True
        self.world.canvas.itemconfig(
            self.canvas_id, fill="black")
