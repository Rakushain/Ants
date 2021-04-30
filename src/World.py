import numpy as np
from Food import Food
from Nest import Nest
from Cell import Cell
from math import sqrt
from util import angle


class World:
    nests = []
    food = []
    started = False
    paused = True

    def __init__(self, canvas, width, height, cellsX, cellsY):
        self.cellW = width / cellsX
        self.cellH = height / cellsY
        self.canvas = canvas
        self.cellsX = cellsX
        self.cellsY = cellsY

        self.grille = np.array(
            [
                [
                    Cell(
                        canvas,
                        canvas.create_rectangle(
                            x * self.cellW,
                            y * self.cellH,
                            (x + 1) * self.cellW,
                            (y + 1) * self.cellH,
                            outline=""))
                    for y in range(height)
                ]
                for x in range(width)
            ]
        )

        self.width = width
        self.height = height

        self.reset()

    def start(self):
        self.started = True
        self.paused = False
        print("START")
        self.updateNests()

    def stop(self):
        self.started = False
        self.paused = True

    def next_frame(self):
        self.started = True
        self.paused = True
        self.updateNests()

    def reset(self):
        self.stop()

        for nest in self.nests:
            for ant in nest.ants:
                del ant
            del nest

        for food in self.food:
            del food

        self.nests = []
        self.food = []

        self.time = 0

    def addFood(self, food):
        self.food.append(food)

    def addNest(self, nest):
        self.nests.append(nest)

    def updateNests(self):
        if not self.started:
            return

        for nest in self.nests:
            for ant in nest.ants:
                x, y = self.worldToGrid(ant.x, ant.y)

                if ant.hasFood:
                    self.addPheromones(x, y, nest.color / 20)
                else:
                    for food in self.food:
                        if sqrt((ant.x - food.x)**2 + (ant.y - food.y)
                                ** 2) <= food.maxAmount and food.amount > 0:
                            food.decrease(1)
                            ant.hasFood = True

                if sqrt((ant.x - nest.x)**2 +
                        (ant.y - nest.y)**2) <= nest.taille:
                    ant.hasFood = False
                    ant.resetStamina()

                possibleDirs = []
                dirWeights = []

                for gX in range(-2, 3):
                    for gY in range(-2, 3):
                        a = np.array([x + gX, y + gY])

                        if (a[0] < 0 or a[0] >= self.width or a[1] <
                                0 or a[1] >= self.height or (gX == 0 and gY == 0)):
                            continue

                        _angle = angle(a, ant.direction)
                        if _angle < np.pi / 2 and _angle > -np.pi / 2:
                            possibleDirs.append(np.array([gX, gY]))
                            dirWeights.append(
                                self.grille[a[0], a[1]].pheromones[0])

                ant.update(self.time, possibleDirs, np.array(dirWeights))

        if self.paused:
            return

        self.time += 1
        self.canvas.after(20, self.updateNests)

    def worldToGrid(self, x, y):
        return int(x / self.cellW * self.width), int(y /
                                                     self.cellH * self.height)

    def addPheromones(self, x, y, color):
        # TODO: ant qui sort du canvas = not implemented
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.grille[x, y].addPheromones(color / 255)  # TODO: Color
