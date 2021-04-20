import numpy as np
from Nourriture import Nourriture
from Nid import Nid
from Cellule import Cellule
from math import sqrt
from util import theta

class Monde:
    nids = []
    nourriture = []

    def __init__(self, canvas, width, height, celluleW, celluleH):
        celluleW = width / celluleW
        celluleH = height / celluleH
        self.canvas = canvas
        self.celluleH = celluleH
        self.celluleW = celluleW

        self.grille = np.array(
            [
                [
                    Cellule(canvas, canvas.create_rectangle(x * celluleW, y * celluleH, (x+1) * celluleW, (y+1) * celluleH, fill="black"))
                    for y in range(height)
                ]
                for x in range(width)
            ]
        )

        self.width = width
        self.height = height
        self.time = 0

        self.nids.append(Nid(canvas, 250, 250, 10, 1, 200, np.array([255, 0, 0])))
        # self.nids.append(Nid(canvas, 320, 400, 6, 100, 300, np.array([0, 255, 0])))
        # self.nids.append(Nid(canvas, 250, 200, 8, 120, 50, np.array([0, 0, 255])))
        # self.nids.append(Nid(canvas, 450, 450, 4, 50, 100, np.array([0, 255, 255])))
        
        self.nourriture.append(Nourriture(canvas, 100, 100, 20))
        self.nourriture.append(Nourriture(canvas, 400, 400, 20))
        self.nourriture.append(Nourriture(canvas, 100, 400, 20))
        self.nourriture.append(Nourriture(canvas, 400, 100, 20))

        self.updateNids()
        # self.drawGrille()
    
    def updateNids(self):
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

                # cellulesProches = self.grille[x-1:x+1,y-1:y+1].flatten()
                # direction = np.random.choice(DIR_CHOICES, p=cellulesProches)

                # for gX in range(x - 1, x + 1):
                #     for gY in range(y - 1, y + 1):
                #         if (x == gX and y == gY):
                #             continue

                possibleDirs = []
                poidsDirs = []

                for gX in range(-2, 3):
                    for gY in range(-2, 3):
                        a = np.array([x+gX, y+gY])
                        
                        if (a[0] < 0 or a[0] >= self.width or a[1] < 0 or a[1] >= self.height or (gX == 0 and gY == 0)):
                            continue

                        angle = theta(a, fourmi.direction)
                        # if angle < np.pi / 2 and angle > -np.pi / 2:
                        if angle < np.pi / 2 and angle > -np.pi / 2:
                            possibleDirs.append(np.array([gX, gY]))
                            poidsDirs.append(self.grille[a[0], a[1]].pheromones[0])
                            # self.canvas.itemconfig(self.grille[a[0], a[1]].canvasId, fill="blue")
                            # self.canvas.after(20, lambda: self.canvas.itemconfig(self.grille[a[0], a[1]].canvasId, fill="black"))
                        # else:
                        #     self.canvas.itemconfig(self.grille[a[0], a[1]].canvasId, fill="black")

                # if x > 0:
                #     if theta(np.array([-1, 0]), np.array([fourmi.x, fourmi.y])) < np.pi / 2:
                #         possibleDirs.append(np.array([-1, 0]))
                #         poidsDirs.append(self.grille[x-1, y].pheromones[0])
                # if x < self.width:
                #     if theta(np.array([1, 0]), np.array([fourmi.x, fourmi.y])) < np.pi / 2:
                #         possibleDirs.append(np.array([1, 0]))
                #         poidsDirs.append(self.grille[x+1, y].pheromones[0])
                # if y > 0:
                #     if theta(np.array([0, 1]), np.array([fourmi.x, fourmi.y])) < np.pi / 2:
                #         possibleDirs.append(np.array([0, 1]))
                #         poidsDirs.append(self.grille[x, y-1].pheromones[0])
                # if y > self.height:
                #     if theta(np.array([0, -1]), np.array([fourmi.x, fourmi.y])) < np.pi / 2:
                #         possibleDirs.append(np.array([0, -1]))
                #         poidsDirs.append(self.grille[x, y+1].pheromones[0])
                
                fourmi.update(self.time, possibleDirs, np.array(poidsDirs))
        self.time += 1
        self.canvas.after(20, self.updateNids)
    
    # def drawGrille(self):
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             self.grille[x, y].addPheromones(np.array([-0.25, -0.25, -0.25]))
                        
    #     self.canvas.after(1000, self.drawGrille)
    #     pass

    def worldToGrid(self, x, y):
        return int(x / self.celluleW * self.width), int(y / self.celluleH * self.height)

    def addPheromones(self, x, y, color):
        # TODO: fourmi qui sort du canvas = not implemented
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.grille[x, y].addPheromones(color / 255) # TODO: Color

        # if decreaseLater:
            # self.canvas.after(20, lambda: self.decreasePheromones(x, y, color * 0.95))
            # print(np.sum(self.grille[x, y].pheromones)>0)
            # self.addPheromones(x, y, -color * 0.5 / 255, np.sum(self.grille[x, y].pheromones) > 0) # TODO: Color

    # def decreasePheromones(self, x, y, color):
    #     self.grille[x, y].addPheromones(-color / 255) # TODO: Color
        # self.canvas.itemconfig(self.grille[x, y].canvasId, fill=rgbtohex(self.grille[x, y].pheromones * 255))

