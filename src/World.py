import numpy as np
from Food import Food
from Nest import Nest
from Cell import Cell
from math import sqrt
from util import angle
from Species import Species
import json


class World:
    nests = []
    food = []
    started = False
    paused = True
    time = 0

    species = [
        Species(np.array([255, 0, 0]), 1, 300),
        Species(np.array([0, 255, 0]), 1, 300),
        Species(np.array([0, 0, 255]), 1, 300),
        Species(np.array([255, 255, 0]), 1, 300),
    ]

    def __init__(self, canvas, width, height,
                 cellsX, cellsY, maxFood, maxNests):
        self.cellW = width / cellsX
        self.cellH = height / cellsY
        self.canvas = canvas
        self.cellsX = cellsX
        self.cellsY = cellsY
        self.maxFood = maxFood
        self.maxNests = maxNests

        self.grid = np.array(
            [
                [
                    Cell(self, x, y)
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
        self.time = 0
        print("START")
        self.update()

    def stop(self):
        self.started = False
        self.paused = True

    def next_frame(self):
        self.started = True
        self.paused = True
        self.update()

    def reset(self):
        self.stop()

        for nest in self.nests:
            for ant in nest.ants:
                self.canvas.delete(ant.view_arc)
                self.canvas.delete(ant.ant_circle)
                del ant
            self.canvas.delete(nest.id)
            del nest

        for food in self.food:
            self.canvas.delete(food.id)
            del food

        for x in range(self.cellsY):
            for y in range(self.cellsX):
                self.grid[x][y].resetPheromones()

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

    def loadWorld(self, worldFile):
        self.reset()
        with open(f"worlds/{worldFile}") as file:
            data = file.read()
            world_data = json.loads(data)

            for food in world_data['food']:
                self.addFood(
                    Food(
                        self.canvas,
                        food['x'],
                        food['y'],
                        food['size']))

            for nest in world_data['nests']:
                self.addNest(Nest(
                    self, nest['x'], nest['y'], nest['species'], nest['size']))

    def modifSpecies(self, speciesId, speed, stamina):
        species = self.species[speciesId]
        species.speed = speed
        species.stamina = stamina

    def update(self):
        if not self.started:
            return

        for nest in self.nests:
            for ant in nest.ants:
                ant.update()

        if self.paused:
            return

        self.time += 1
        self.canvas.after(20, self.update)

    def worldToGrid(self, pos):
        x, y = pos
        return np.array([int(x / self.width * self.cellsX), int(y /
                                                                self.height * self.cellsY)])
