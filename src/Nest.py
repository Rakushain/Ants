from Ant import Ant
from util import rgbtohex, create_circle
import weakref


class Nest:
    def __init__(self, canvas, x, y, taille, nAnts, stamina, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.taille = taille
        self.color = color
        hexColor = rgbtohex(color)
        self.id = create_circle(canvas, x, y, taille, hexColor)

        self.ants = [Ant(self.canvas, x, y, stamina, hexColor)
                     for _ in range(nAnts)]
