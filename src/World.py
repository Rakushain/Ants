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
        Species(0, np.array([255, 0, 0])),
        Species(1, np.array([0, 255, 0])),
        Species(2, np.array([0, 0, 255])),
        Species(3, np.array([255, 255, 0])),
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
        for nest in self.nests:
            species = self.species[nest.species_id + 1]
            for ant in nest.ants:
                ant.speed = species.speed
                ant.stamina = species.stamina
                ant.base_stamina = species.stamina
                ant.view_distance = species.view_distance
                ant.wander_chance = species.wander_chance
                ant.comeback = 1 - ant.wander_chance

        self.started = True
        self.paused = False
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

        self.main_gui.button_go.configure(text="Go =>")
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
        if self.charged > 0 and self.main_gui.is_modifying.get() == True:
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
        
                for i, species in enumerate(world_data["species"]):
                    for trait, value in species.items():
                        self.species[i].update_trait(trait,value)
                        self.main_gui.update_species_entry(trait, value)
                        

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
        all_traits = []
        #  sauvegarde des caracteristiques des fourmis
        for i in range(4):
            all_traits += [{"speed": self.species[i].speed,
                                "stamina": self.species[i].stamina,
                                "evaporation": self.species[i].evaporation,
                                "view_distance": self.species[i].view_distance,
                                "exploration": self.species[i].exploration,
                                "comeback": self.species[i].comeback,
                                "wander_chance": self.species[i].speed,
                                "deposit": self.species[i].deposit,
                                "random_move": self.species[i].random_move}]
        data["species"] = all_traits
        

        files = [('JSON File', '*.json')]
        filepos = asksaveasfile(filetypes=files, defaultextension=".json")
        if filepos is not None:
            self.write_to_json(filepos, data)
        else:
            return

    def reset_grid(self, size_x, size_y):
        self.cellsX = size_x
        self.cellsY = size_y
        self.cellW = self.width / self.cellsX
        self.cellH = self.height / self.cellsY

        for row in self.grid:
            for cell in row:
                cell.reset()

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
        self.canvas.after(20, self.update)

    def world_to_grid(self, pos):
        x, y = pos
        return np.array([int(x / self.width * self.cellsX), int(y /
                                                                self.height * self.cellsY)])
