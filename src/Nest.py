from Ant import Ant
from util import rgbtohex, create_circle
import weakref


class Nest:
    def __init__(self, canvas, x, y, nAnts, stamina, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = nAnts / 2
        self.color = color
        hexColor = rgbtohex(color)
        self.id = create_circle(canvas, x, y, self.size, hexColor)

        self.ants = [Ant(self.canvas, x, y, stamina, hexColor)
                     for _ in range(nAnts)]
