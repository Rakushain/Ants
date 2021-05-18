import numpy as np
from util import rgb_to_hex
from Pheromones import Pheromones


class Cell:
    """
    Classe représentant une Cellule
    Attributs:
        world:          Référence au monde.
        x:              Position de la cellule en X.
        y:              Position de la cellule en Y.
    """

    def __init__(self, world, x, y):
        self.is_wall = False
        self.world = world
        self.pos = np.array([x, y])
        self.world_pos = np.array([x * world.cellW, y * world.cellH])
        #  identifiant de la case sur le canvas
        self.canvas_id = self.world.canvas.create_rectangle(
            self.world_pos[0],
            self.world_pos[1],
            self.world_pos[0] + world.cellW,
            self.world_pos[1] + world.cellH,
            outline="")
        # liste de liste, chaque sous liste represente les pheromones de chaque
        # espece
        self.pheromones = [[] for i in range(len(world.species))]

    def get_pheromones(self, species_id):
        """
        Fonction qui permet de savoir la quantite de pheromones sur une case
        """
        total_pheromones = 0
        for pheromone in self.pheromones[species_id][:]:
            #  duree de vie des pheromones
            lifetime = self.world.time - pheromone.creation_time
            self.evaporation = (
                lifetime / self.world.species[species_id].evaporation)
            # par defaut, les pheromones disparaissent apres 1000 frames

            if self.evaporation > 1:
                #  les phéromones ne sont plus actives
                self.pheromones[species_id].remove(pheromone)
                del pheromone
                continue
            total_pheromones += 1 - self.evaporation

        return total_pheromones

    def add_pheromones(self, species_id, pos):
        """
        Fonction qui ajoute les pheromones sur la cellule
        """
        self.pheromones[species_id].append(
            Pheromones(
                self.world,
                species_id,
                pos,
                self.world.time))

        self.update_color()

    def update_color(self):
        """
        Fonction qui met a jour la couleur de la cellule sur le canvas
        """
        color = np.array([0, 0, 0])
        for species_id, species_pheromones in enumerate(self.pheromones):
            # intensifie la couleur en fonction du nombre de pheromones sur la
            # case
            color += self.world.species[species_id].inv_color * \
                len(species_pheromones)
        #  couleur inversee (noir vers couleur inversee de l espece)
        color = np.clip(np.around(color / 100), 0, 255)
        #  on reinverse la couleur( blanc vers couleur de l espece)
        color = np.array([255 - val for val in color])
        # on met a jour la couleur de la case
        self.world.canvas.itemconfig(
            self.canvas_id, fill=rgb_to_hex(color))

    def reset(self):
        """
        Fonction qui supprime toutes les pheromones des cases
        Utilise lors de la reinitialisation du monde
        """
        self.world.canvas.itemconfig(self.canvas_id, fill="white")
        for species in self.pheromones:
            for pheromone in species:
                del pheromone

    def add_wall(self):
        """
        Fonction qui permet d ajouter un mur sur une cellule
        """
        self.is_wall = True
        self.world.canvas.itemconfig(
            self.canvas_id, fill="black")
