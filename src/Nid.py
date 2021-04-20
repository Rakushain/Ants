from Fourmi import Fourmi
from util import rgbtohex, create_circle

class Nid:
    def __init__(self, canvas, x, y, taille, nFourmis, endurance, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.taille = taille
        self.color = color
        hexColor = rgbtohex(color)
        self.id = create_circle(canvas, x, y, taille, hexColor)

        self.fourmis = [Fourmi(self, endurance, hexColor) for _ in range(nFourmis)]
