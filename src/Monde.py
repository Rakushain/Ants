import numpy as np
from Nourriture import Nourriture
from Nid import Nid
from Cellule import Cellule
from math import sqrt
from util import theta

class Monde:
    nids = []
    nourriture = []
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
                    Cellule(canvas, canvas.create_rectangle(x * self.cellW, y * self.cellH, (x+1) * self.cellW, (y+1) * self.cellH, outline=""))
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
        self.updateNids()
        
    def stop(self):
        self.started = False
        self.paused = True
        
    def next_frame(self):
        self.started = True
        self.paused = True
        self.updateNids()

    def reset(self):
        self.stop()

        for nid in self.nids:
            for fourmi in nid.fourmis:
                del fourmi
            del nid
        
        for food in self.nourriture:
            del food
        
        self.nids = []
        self.nourriture = []
        
        self.time = 0

        self.nids.append(Nid(self.canvas, 250, 250, 10, 1, 200, np.array([255, 0, 0])))
        # self.nids.append(Nid(canvas, 320, 400, 6, 100, 300, np.array([0, 255, 0])))
        # self.nids.append(Nid(canvas, 250, 200, 8, 120, 50, np.array([0, 0, 255])))
        # self.nids.append(Nid(canvas, 450, 450, 4, 50, 100, np.array([0, 255, 255])))
        
        self.nourriture.append(Nourriture(self.canvas, 100, 100, 20))
        # self.nourriture.append(Nourriture(self.canvas, 400, 400, 20))
        # self.nourriture.append(Nourriture(self.canvas, 100, 400, 20))
        # self.nourriture.append(Nourriture(self.canvas, 400, 100, 20))
    
    def addFood(self, food):
        self.nourriture.append(food)

    def addNid(self, nid):
        self.nids.append(nid)
    
    def updateNids(self):
        if not self.started:
            return
        
        for nid in self.nids:
            for fourmi in nid.fourmis:
                x, y = self.worldToGrid(fourmi.x, fourmi.y)
                
                if fourmi.hasFood:                    
                    self.addPheromones(x, y, nid.color / 20)
                else:
                    for nourriture in self.nourriture:
                        if sqrt((fourmi.x - nourriture.x)**2 + (fourmi.y - nourriture.y)**2) <= nourriture.maxAmount and nourriture.amount > 0:
                            nourriture.decrease(1)
                            fourmi.hasFood = True
                
                if sqrt((fourmi.x - nid.x)**2 + (fourmi.y - nid.y)**2) <= nid.taille:
                    fourmi.hasFood = False
                    fourmi.resetEndurance()

                possibleDirs = []
                poidsDirs = []

                for gX in range(-2, 3):
                    for gY in range(-2, 3):
                        a = np.array([x+gX, y+gY])
                        
                        if (a[0] < 0 or a[0] >= self.width or a[1] < 0 or a[1] >= self.height or (gX == 0 and gY == 0)):
                            continue

                        angle = theta(a, fourmi.direction)
                        if angle < np.pi / 2 and angle > -np.pi / 2:
                            possibleDirs.append(np.array([gX, gY]))
                            poidsDirs.append(self.grille[a[0], a[1]].pheromones[0])
                
                fourmi.update(self.time, possibleDirs, np.array(poidsDirs))

        
        if self.paused:
            return
        
        self.time += 1
        self.canvas.after(20, self.updateNids)

    def worldToGrid(self, x, y):
        return int(x / self.cellW * self.width), int(y / self.cellH * self.height)

    def addPheromones(self, x, y, color):
        # TODO: fourmi qui sort du canvas = not implemented
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.grille[x, y].addPheromones(color / 255) # TODO: Color