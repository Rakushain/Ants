from util import create_circle


class Food:
    def __init__(self, canvas, x, y, maxAmount):
        self.canvas = canvas
        self.maxAmount = maxAmount
        self.amount = maxAmount
        self.x = x
        self.y = y
        self.idIn = create_circle(canvas, x, y, maxAmount, "white")

    def decrease(self, amount):
        self.amount -= amount
        if (self.amount <= 0):
            return
        newScale = self.amount / (self.amount + 1)
        self.canvas.scale(self.idIn, self.x, self.y, newScale, newScale)
