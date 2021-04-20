import numpy as np
from util import create_circle, rotVecteur

class Fourmi:
    speed = 4
    hasFood = False

    def __init__(self, nid, endurance, color):
        self.canvas = nid.canvas
        self.nid = nid
        self.x = nid.x
        self.y = nid.y
        self.baseEndurance = endurance
        self.endurance = endurance
        self.color = color
        self.id = create_circle(self.canvas, self.x, self.y, 2, color)
        self.direction = np.random.uniform(-1.0, 1.0, (2))

    def update(self, time, possibleDirs, poidsDirs):
        self.endurance -= 1
        if time % 5 == 0:
            if self.hasFood:
                self.direction = np.array([self.nid.x - self.x, self.nid.y - self.y])
                self.canvas.itemconfig(self.id, fill="gray")
            elif self.endurance <= 0:
                self.direction = np.array([self.nid.x - self.x, self.nid.y - self.y])
                self.canvas.itemconfig(self.id, fill="purple")
            else:
                sumPoids = np.sum(poidsDirs)
                # Si il n'y a pas de pheromones, garder la meme direction
                if sumPoids > 0:
                    self.direction = possibleDirs[np.random.choice(len(possibleDirs), p=poidsDirs/np.sum(poidsDirs))]
                else:
                    self.direction = rotVecteur(self.direction, np.random.uniform(-np.pi/4, np.pi/4))
                self.canvas.itemconfig(self.id, fill=self.color)

        x, y = self.direction / np.linalg.norm(self.direction)
        self.canvas.move(self.id, x * self.speed, y * self.speed) # TODO: optimiser (2x meme calcul)
        self.x += x * self.speed
        self.y += y * self.speed
    
    def resetEndurance(self):
        self.endurance = self.baseEndurance
    