from util import create_circle
import numpy as np


class Food:
    """
    Classe représentant une Ressource
    Attributs:
        canvas:         Référence au canvas.
        x:              Position de la ressource en X.
        y:              Position de la ressource en Y.
        max_amount:     La quantité de nourriture maximum.
    """

    def __init__(self, canvas, x, y, max_amount):
        self.canvas = canvas
        self.max_amount = max_amount
        self.amount = max_amount
        self.scale = max_amount
        self.pos = np.array([x, y])
        #  identifiant de la ressource sur le canvas
        self.id = create_circle(canvas, x, y, self.scale, "white")

    def decrease(self, amount=1):
        """
        Reduit la quantité de nourriture dans la ressource lors du passage d une fourmi
        """
        self.amount -= amount
        if (self.amount <= 0):
            #  si la ressource est vide
            return
        #  taille de la ressource sur le canvas
        scale_factor = self.amount / (self.amount + amount)
        self.scale *= scale_factor
        self.canvas.scale(
            self.id,
            self.pos[0],
            self.pos[1],
            scale_factor,
            scale_factor)
