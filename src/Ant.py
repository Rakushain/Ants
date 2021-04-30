import numpy as np
from util import create_circle, vectRot


class Ant:
    speed = 4
    hasFood = False

    def __init__(self, canvas, nestX, nestY, stamina, color):
        self.canvas = canvas
        self.nestX = nestX
        self.nestY = nestY
        self.x = nestX
        self.y = nestY
        self.baseStamina = stamina
        self.stamina = stamina
        self.color = color
        self.id = create_circle(self.canvas, self.x, self.y, 2, color)
        self.direction = np.random.uniform(-1.0, 1.0, (2))

    def update(self, time, possibleDirs, dirWeights):
        self.stamina -= 1
        if time % 5 == 0:
            if self.hasFood:
                self.direction = np.array(
                    [self.nestX - self.x, self.nestY - self.y])
                self.canvas.itemconfig(self.id, fill="gray")
            elif self.stamina <= 0:
                self.direction = np.array(
                    [self.nestX - self.x, self.nestY - self.y])
                self.canvas.itemconfig(self.id, fill="purple")
            else:
                sumPoids = np.sum(dirWeights)
                # Si il n'y a pas de pheromones, garder la meme direction
                if sumPoids > 0:
                    self.direction = possibleDirs[np.random.choice(
                        len(possibleDirs), p=dirWeights / np.sum(dirWeights))]
                else:
                    self.direction = vectRot(
                        self.direction, np.random.uniform(-np.pi / 4, np.pi / 4))
                self.canvas.itemconfig(self.id, fill=self.color)

        x, y = self.direction / np.linalg.norm(self.direction)
        # TODO: optimiser (2x meme calcul)
        self.canvas.move(self.id, x * self.speed, y * self.speed)
        self.x += x * self.speed
        self.y += y * self.speed

    def resetStamina(self):
        self.stamina = self.baseStamina
