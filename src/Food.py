from util import create_circle
import numpy as np


class Food:
    def __init__(self, canvas, x, y, maxAmount):
        self.canvas = canvas
        self.maxAmount = maxAmount
        self.amount = maxAmount
        self.scale = maxAmount
        self.pos = np.array([x, y])
        self.id = create_circle(canvas, x, y, self.scale, "white")

    def decrease(self, amount=1):
        self.amount -= amount
        if (self.amount <= 0):
            return
        self.scale = self.amount / (self.amount + 1)
        self.canvas.scale(
            self.id,
            self.pos[0],
            self.pos[1],
            self.scale,
            self.scale)
