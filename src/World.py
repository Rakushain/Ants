import numpy as np
from tkinter.filedialog import asksaveasfile
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
    wall = []
    started = False
    paused = True
    time = 0
    charged = 0

    species = [
        Species(0, np.array([255, 0, 0]), 4, 350, 1000, 10, 0.1, 0, 0, 0, 0),
        Species(1, np.array([0, 255, 0]), 4, 350, 1000, 10, 0.1, 0, 0, 0, 0),
        Species(2, np.array([0, 0, 255]), 4, 350, 1000, 10, 0.1, 0, 0, 0, 0),
        Species(3, np.array([255, 255, 0]), 4, 350, 1000, 10, 0.1, 0, 0, 0, 0)
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
        
        self.main_gui.button_go.configure(text = "Go =>")
        self.main_gui.speciesId.set(0)

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

        for species in self.species:
            species.reset()

        self.reset_grid(self.cellsX, self.cellsY)

        self.nests = []
        self.food = []
        self.wall = np.zeros((self.cellsX, self.cellsY))
        self.time = 0

    def add_food(self, food):
        if (len(self.food) >= self.maxFood):
            return
        self.food.append(food)

    def add_nest(self, nest):
        if (len(self.nests) >= self.maxNests):
            return
        self.nests.append(nest)

    def add_wall(self, grid_x, grid_y):
        self.grid[grid_x][grid_y].add_wall()
        self.wall[grid_x, grid_y] = True

    def loadWorld(self, worldFile):
        self.reset()
        self.main_gui.button_go["text"] = "Go =>"
        if self.charged > 0:
            self.main_gui.on_modif_state_change()
        self.charged += 1
        
        with open(f"worlds/{worldFile}") as file:
            data = file.read()
            world_data = json.loads(data)
            try:
                for food in world_data['food']:
                    self.add_food(
                        Food(
                            self.canvas,
                            food['x'],
                            food['y'],
                            food['size']))

                for nest in world_data['nests']:
                    self.add_nest(Nest(
                        self, len(self.nests), nest['x'], nest['y'], nest['species'], nest['size']))

                if (world_data["wall"]):
                    for wall in world_data["wall"]:
                        self.add_wall(wall[0], wall[1])

            except BaseException:
                pass
        

    def write_to_json(self, path, data):
        json.dump(data, path)

    def save_world(self):
        self.stop()
        data = {}
        data["nests"] = [{'x': int(nest.pos[0]), 'y': int(
            nest.pos[1]), 'size': nest.size, "species": nest.species_id} for nest in self.nests]
        data["food"] = [{'x': int(food.pos[0]), 'y': int(
            food.pos[1]), 'size': food.max_amount} for food in self.food]

        only_walls = []
        for x in range(self.cellsX):
            for y in range(self.cellsY):
                if self.wall[x][y]:
                    only_walls.append([x, y])
        data["wall"] = only_walls

        files = [('JSON File', '*.json')]
        filepos = asksaveasfile(filetypes=files, defaultextension=".json")
        if filepos is not None:
            self.write_to_json(filepos, data)
        else:
            return
        

    def modif_species(self, speciesId, speed, stamina, evaporation, view_distance, exploration, comeback, wander_chance, deposit, random_move):
        species = self.species[speciesId]
        species.speed = speed
        species.stamina = stamina
        species.evaporation = evaporation
        species.view_distance = view_distance
        species.exploration = exploration
        species.comeback = comeback
        species.wander_chance = wander_chance
        species.deposit = deposit
        species.random_move = random_move

    def reset_grid(self, size_x, size_y):
        self.cellsX = size_x
        self.cellsY = size_y
        self.cellW = self.width / self.cellsX
        self.cellH = self.height / self.cellsY

        for row in self.grid:
            for cell in row:
                cell.reset()

        #print(self.grid)

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
        self.main_gui.update_species_food()
        # self.time += (1 * self.main_gui.speed_value.get())
        # self.main_gui.label_time.config(text=self.main_gui.update_time())
        self.canvas.after(20, self.update)

    def world_to_grid(self, pos):
        x, y = pos
        return np.array([int(x / self.width * self.cellsX), int(y /
                                                                self.height * self.cellsY)])
