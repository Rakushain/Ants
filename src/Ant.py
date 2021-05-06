import numpy as np
from util import create_circle, vectRot


class Ant:
    """
    Classe représentant une Fourmi

    Attributes:
        canvas:         Référence au canvas.
        id:             Identifiant de la fourmi sur le canvas.
        nestX:          Position du nid en X.
        nestY:          Position du nid en Y.
        x:              Position de la fourmi en X.
        y:              Position de la fourmi en Y.
        baseStamina:    Endurance max de la fourmi.
        stamina:        Endurance actuelle de la fourmi.
        color:          Couleur de la fourmi.
        direction:      Direction de la fourmi.
    """

    hasFood = False

    def __init__(self, canvas, nestX, nestY, speed, stamina, color):
        """
            Initialisation de la Fourmi.

            Args:
                canvas:     Référence au canvas.
                nestX:      Position du nid en X.
                nestY:      Position du nid en Y.
                stamina:    Endurance max de la fourmi.
                color:      Couleur de la fourmi.

            Returns:
                Une nouvelle instance de Fourmi.
        """

        self.canvas = canvas
        self.nestX = nestX
        self.nestY = nestY
        self.x = nestX
        self.y = nestY
        self.speed = speed
        self.baseStamina = stamina
        self.stamina = stamina
        self.color = color
        self.id = create_circle(self.canvas, self.x, self.y, 2, color)
        self.direction = np.random.uniform(-1.0, 1.0, (2))

    def update(self, time, possibleDirs, dirWeights):
        """
            Mise a jour de la Fourmi.

            Args:
                time:           Temps actuelle de la simulation.
                possibleDirs:   Directions que la fourmi peut prendre.
                dirWeights:     Poids de chaque direction (poids plus élevé -> fourmi a plus de chance d'aller dans cette direction).

            Returns:
                None
        """

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
        """
        Réinitialise l'endurance de la fourmi.
        """

        self.stamina = self.baseStamina
