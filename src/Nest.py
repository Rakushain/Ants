import numpy as np
from Ant import Ant
from util import rgb_to_hex, create_circle


class Nest:
    """
    Classe représentant un Nid
    Attributs:
        world:          Référence au monde.
        nest_id         Identifiant du nid.
        x:              Position de la ressource en X.
        y:              Position de la ressource en Y.
        species_id:     Identifiant de l espece.
        nAnts:          Population du nid
    """

    def __init__(self, world, nest_id, x, y, species_id, nAnts):
        self.world = world
        self.pos = np.array([x, y])
        self.species_id = species_id
        self.scale = nAnts / 2
        self.size = nAnts
        self.nest_id = nest_id
        self.food = 0

        species = self.world.species[species_id]
        #  quand un nid d une espece est pose sur le canvas, on active l espece
        species.set_active()

        self.color = species.color
        hex_color = rgb_to_hex(self.color)
        self.canvas_id = create_circle(
            self.world.canvas, x, y, self.scale, hex_color)
        #  remplissage du nid
        self.ants = [Ant(self.world, self, i, hex_color)
                     for i in range(nAnts)]

    def add_food(self, amount):
        """
        Fonction qui ajoute de la nourriture au nid
        """
        self.food += amount
        self.world.species[self.species_id].add_food(amount)
