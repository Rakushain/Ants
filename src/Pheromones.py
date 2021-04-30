import numpy as np

class Pheromones:
    def __init__(self, color, amount):
        self.color = color
        self.currentColor = np.zeros(3)
        self.amount = amount
    
    def addPheromones(self, amount):
        self.amount += amount
        self.updateColor()
    
    def updateColor(self):
        self.currentColor = self.color * self.amount