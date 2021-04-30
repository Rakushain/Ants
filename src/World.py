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

    def __init__(self, canvas, width, height, cellsX, cellsY, maxFood, maxNests):
        self.cellW = width / cellsX
        self.cellH = height / cellsY
        self.canvas = canvas
        self.cellsX = cellsX
        self.cellsY = cellsY
        self.maxFood = maxFood
        self.maxNests = maxNests

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
                            outline=""), maxNests)
                    for y in range(cellsX)
                ]
                for x in range(cellsY)
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
        if (len(self.food) >= self.maxFood):
            return
        self.food.append(food)

    def addNest(self, nest):
        if (len(self.nests) >= self.maxNests):
            return
        self.nests.append(nest)
    
    def loadMap(self, nests, food):
        # TODO: xd
        # self.nests = nests.copy()
        # self.food = food.copy()
        self.addFood(Food(self.canvas, 366, 167, 20))
        self.addFood(Food(self.canvas, 278, 285, 20))
        self.addFood(Food(self.canvas, 490, 447, 20))
        self.addFood(Food(self.canvas, 573, 263, 20))

        self.addNest(Nest(self.canvas, 443, 289, 20, 200, np.array([255, 0, 0])))

    def updateNests(self):
        if not self.started:
            return

        for nestId, nest in enumerate(self.nests):
            for ant in nest.ants:
                x, y = self.worldToGrid(ant.x, ant.y)

                if ant.hasFood:
                    self.addPheromones(x, y, nestId)
                else:
                    for food in self.food:
                        if sqrt((ant.x - food.x)**2 + (ant.y - food.y)
                                ** 2) <= food.maxAmount and food.amount > 0:
                            food.decrease(1)
                            ant.hasFood = True

                if sqrt((ant.x - nest.x)**2 +
                        (ant.y - nest.y)**2) <= nest.size:
                    ant.hasFood = False
                    ant.resetStamina()

                possibleDirs = []
                dirWeights = []

                for gX in range(-2, 3):
                    for gY in range(-2, 3):
                        a = np.array([x + gX, y + gY])

                        if (a[0] < 0 or a[0] >= self.cellsX or a[1] <
                                0 or a[1] >= self.cellsY or (gX == 0 and gY == 0)):
                            continue

                        _angle = angle(a, ant.direction)
                        if _angle < np.pi / 2 and _angle > -np.pi / 2:
                            possibleDirs.append(np.array([gX, gY]))
                            dirWeights.append(
                                self.grille[a[0], a[1]].pheromones[nestId].amount)

                ant.update(self.time, possibleDirs, np.array(dirWeights))

        if self.paused:
            return

        self.time += 1
        self.canvas.after(20, self.updateNests)

    def worldToGrid(self, x, y):
        return int(x / self.width * self.cellsX), int(y /
                                                     self.height * self.cellsY)

    def addPheromones(self, x, y, nestId):
        # TODO: fourmi qui sort du canvas => not implemented
        print("LOL1")
        if x < 0 or x > self.cellsX or y < 0 or y > self.cellsY:
            print("LOLTAMER")
            return
        print("LOL2")
        # TODO: variable amount
        self.grille[x, y].addPheromones(nestId, 0.1)  # TODO: Color
