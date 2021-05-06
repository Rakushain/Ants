import numpy as np
from util import create_circle, vectRot, random_inside_circle, distance


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

    has_food = False
    food_target = None
    view_distance = 10
    # TODO: cringe
    food_disposal_distance = 4

    def __init__(self, world, nestX, nestY, speed, stamina, color):
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

        self.world = world
        self.nest_pos = np.array([nestX, nestY])

        random_pos = random_inside_circle() * 30
        self.pos = np.array([nestX, nestY]) + random_pos

        self.speed = 4  # speed
        self.base_stamina = stamina
        self.stamina = stamina
        self.color = color
        self.id = create_circle(
            self.world.canvas,
            self.pos[0],
            self.pos[1],
            2,
            color)
        self.direction = random_inside_circle()

        self.steer_strength = 2
        self.wander_strength = 1
        self.velocity = 0

    def update(self, time):
        """
            Mise a jour de la Fourmi.

            Args:
                time:           Temps actuelle de la simulation.
                possibleDirs:   Directions que la fourmi peut prendre.
                dirWeights:     Poids de chaque direction (poids plus élevé -> fourmi a plus de chance d'aller dans cette direction).

            Returns:
                None
        """

        self.check_nest()

        self.wander()
        self.handle_food()

        desired_velocity = self.direction * self.speed

        acceleration = (desired_velocity - self.velocity) * self.steer_strength
        acceleration_magnitude = np.linalg.norm(acceleration)
        if acceleration_magnitude > self.steer_strength:
            acceleration = acceleration / acceleration_magnitude * self.steer_strength

        self.velocity = self.velocity + acceleration
        velocity_magnitude = np.linalg.norm(self.velocity)
        if velocity_magnitude > self.speed:
            self.velocity = self.velocity / velocity_magnitude * self.speed

        self.pos += self.velocity
        self.world.canvas.move(self.id, self.velocity[0], self.velocity[1])
    
    def wander(self):
        self.direction = (
            self.direction +
            random_inside_circle() *
            self.wander_strength)

        self.stamina -= 1
            

    def handle_food(self):
        if self.has_food or self.stamina <= 0:
            self.direction = (self.nest_pos - self.pos)
            self.direction = self.direction / np.linalg.norm(self.direction)
        elif not self.food_target:
            # TODO: Select rdm food
            min_dist = np.Infinity
            for food in self.world.food:
                dist = distance(self.pos, food.pos)

                if dist < (self.view_distance +
                           food.scale) and dist < min_dist:
                    min_dist = dist
                    self.food_target = food

        else:
            food_dir = (self.food_target.pos - self.pos)
            dist = np.linalg.norm(self.direction)
            
            if dist < self.food_target.scale:
                self.has_food = True
                self.food_target.decrease()
            else:
                self.direction = food_dir / dist
    
    def check_nest(self):
        dist = np.linalg.norm(self.nest_pos - self.pos)
        if dist < self.food_disposal_distance:
            self.has_food = False
            self.food_target = None
            self.direction = random_inside_circle()
            self.stamina = self.base_stamina

    def resetStamina(self):
        """
        Réinitialise l'endurance de la fourmi.
        """

        self.stamina = self.base_stamina
