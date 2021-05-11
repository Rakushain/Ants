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

    def __init__(self, main_gui, canvas, width, height,
                 cellsX, cellsY, maxFood, maxNests):
        self.width = width
        self.height = height
        self.cellW = width / cellsX
        self.cellH = height / cellsY
        self.main_gui = main_gui
        self.canvas = canvas
        self.cellsX = cellsX
        self.cellsY = cellsY
        self.maxFood = maxFood
        self.maxNests = maxNests
        self.speed_value = 1

        self.grid = np.array(
            [
                [
                    Cell(self, x, y)
                    for y in range(self.cellsX)
                ]
                for x in range(self.cellsY)
            ]
        )

        self.reset()

    def start(self):
        self.started = True
        self.paused = False
        print("START")
        self.update()

    def stop(self):
        self.started = False
        self.paused = True

    def pause(self):
        self.started = True
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
            self.canvas.delete(nest.canvas_id)
            del nest

        for food in self.food:
            self.canvas.delete(food.id)
            del food

        self.reset_grid(self.cellsX, self.cellsY)

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

    def addWall(self, x, y):
        grid_x, grid_y = self.worldToGrid(np.array([x, y]))
        self.grid[grid_x][grid_y].addWall()

    def loadWorld(self, worldFile):
        self.reset()
        self.main_gui.button_go["text"] = "Go =>"
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
                    self, len(self.nests), nest['x'], nest['y'], nest['species'], nest['size']))

    def modifSpecies(self, speciesId, speed, stamina):
        species = self.species[speciesId]
        species.speed = speed
        species.stamina = stamina

    def reset_grid(self, size_x, size_y):
        self.cellsX = size_x
        self.cellsY = size_y
        self.cellW = self.width / self.cellsX
        self.cellH = self.height / self.cellsY

        for row in self.grid:
            for cell in row:
                cell.reset()

        # print(self.grid)

    def update(self):
        if not self.started:
            return

        self.time += self.speed_value
        self.main_gui.update_time()

        for nest in self.nests:
            for ant in nest.ants:
                ant.update()

        if self.paused:
            return

        # self.time += (1 * self.main_gui.speed_value.get())
        # self.main_gui.label_time.config(text=self.main_gui.update_time())
        self.canvas.after(20, self.update)

    def worldToGrid(self, pos):
        x, y = pos
        return np.array([int(x / self.width * self.cellsX), int(y /
                                                                self.height * self.cellsY)])
