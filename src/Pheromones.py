import numpy as np
from util import create_circle


class Pheromones:
    def __init__(self, world, species_id, pos, creation_time):
        self.pos = pos
        self.species_id = species_id
        self.creation_time = creation_time
