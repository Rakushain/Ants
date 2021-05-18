import numpy as np
from util import create_circle


class Pheromones:
    """
    Classe représentant une Pheromone
    Attributs:
        world:          Référence au monde.
        species_id      Identifiant de l espece
        pos             Position en x et y de la Pheromone
        creation_time   Instant de creation d une Pheromone
    """

    def __init__(self, world, species_id, pos, creation_time):
        self.pos = pos
        self.species_id = species_id
        self.creation_time = creation_time
