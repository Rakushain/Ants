from util import create_circle
import numpy as np


class Food:
    def __init__(self, canvas, x, y, max_amount):
        self.canvas = canvas
        self.max_amount = max_amount
        self.amount = max_amount
        self.scale = max_amount
        self.pos = np.array([x, y])
        self.id = create_circle(canvas, x, y, self.scale, "white")

    def decrease(self, amount=1):
        self.amount -= amount
        if (self.amount <= 0):
            return
        scale_factor = self.amount / (self.amount + amount)
        self.scale *= scale_factor
        self.canvas.scale(
            self.id,
            self.pos[0],
            self.pos[1],
            scale_factor,
            scale_factor)
