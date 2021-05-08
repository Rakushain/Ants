import numpy as np
from util import create_circle, vectRot, random_inside_circle, distance, rotate


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
    food_amount = 0
    food_target = None
    view_distance = 40
    view_angle = 120
    # TODO: cringe
    food_disposal_distance = 4

    def __init__(self, world, nest, ant_id, speed, stamina, color):
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
        self.nest_pos = nest.pos
        self.nest_id = nest.nest_id
        self.species_id = nest.species_id

        random_pos = random_inside_circle() * 30
        self.pos = nest.pos + random_pos

        self.direction = random_inside_circle()

        self.steer_strength = 0.25
        self.wander_strength = 10
        self.speed = 4  # speed
        self.velocity = self.direction * self.speed * self.world.speed_value

        self.base_stamina = stamina
        self.stamina = stamina
        self.color = color

        self.ant_id = f"ANT_{nest.nest_id}_{ant_id}"

        self.sensors = [
            create_circle(
                self.world.canvas,
                -10,
                -10,
                1,
                "gray") for i in range(3)]  # TODO: Remove cringe

        self.view_arc = self.world.canvas.create_arc(
            self.pos[0] -
            self.view_distance,
            self.pos[1] -
            self.view_distance,
            self.pos[0] +
            self.view_distance,
            self.pos[1] +
            self.view_distance,
            fill="",
            tags=self.ant_id)

        self.update_angle()

        self.ant_circle = create_circle(
            self.world.canvas,
            self.pos[0],
            self.pos[1],
            2,
            color, tags=self.ant_id)

    def update(self):
        """
            Mise a jour de la Fourmi.

            Args:
                time:           Temps actuelle de la simulation.
                possibleDirs:   Directions que la fourmi peut prendre.
                dirWeights:     Poids de chaque direction (poids plus élevé -> fourmi a plus de chance d'aller dans cette direction).

            Returns:
                None
        """
        grid_x, grid_y = self.world.worldToGrid(self.pos)

        # Test si fourmi est dans la grille
        if grid_x >= 0 and grid_x < self.world.cellsX and grid_y >= 0 and grid_y < self.world.cellsY:
            if self.has_food:
                # TODO: variable amount
                self.world.grid[grid_x, grid_y].addPheromones(
                    self.species_id, self.pos)  # TODO: Color

        self.check_nest()

        self.sense_pheromones()

        self.wander()
        self.handle_food()

        desired_velocity = self.direction * self.speed * self.world.speed_value

        acceleration = (desired_velocity - self.velocity) * self.steer_strength
        acceleration_magnitude = np.linalg.norm(acceleration)
        if acceleration_magnitude > self.steer_strength:
            acceleration = acceleration / acceleration_magnitude * self.steer_strength

        self.velocity = self.velocity + acceleration
        velocity_magnitude = np.linalg.norm(self.velocity)
        if velocity_magnitude > (self.speed * self.world.speed_value):
            self.velocity = self.velocity / velocity_magnitude * \
                self.speed * self.world.speed_value

        self.pos += self.velocity
        self.world.canvas.move(self.ant_id, self.velocity[0], self.velocity[1])

        self.world.canvas.itemconfigure(
            self.ant_circle,
            fill="gray" if self.stamina <= 0 else self.color)

        self.update_angle()

    def wander(self):
        self.direction = (
            self.direction +
            random_inside_circle() *
            self.wander_strength)

        self.stamina -= self.world.speed_value

    def handle_food(self):
        if self.has_food or self.stamina <= 0:
            self.direction = (self.nest_pos - self.pos)
            self.direction = self.direction / np.linalg.norm(self.direction)
        elif not self.food_target:
            # TODO: Select rdm food
            min_dist = np.Infinity
            for food in self.world.food:
                if food.amount <= 0:
                    continue

                dist = distance(self.pos, food.pos)

                if dist < (self.view_distance +
                           food.scale) and dist < min_dist:
                    min_dist = dist
                    self.food_target = food
        else:
            if self.food_target.amount <= 0:
                self.food_target = None
                return

            food_dir = (self.food_target.pos - self.pos)
            dist = np.linalg.norm(self.direction)

            if dist < max(self.food_target.scale, 4):
                self.has_food = True
                self.food_target.decrease()
                self.food_amount += 1
            else:
                self.direction = food_dir / dist

    def check_nest(self):
        dist = np.linalg.norm(self.nest_pos - self.pos)
        if dist < self.food_disposal_distance:
            self.stamina = self.base_stamina
            if self.has_food:
                self.world.nests[self.nest_id].addFood(self.food_amount)
                self.has_food = False
                self.food_target = None
                self.direction = random_inside_circle()

    def update_angle(self):
        self.angle = np.rad2deg(
            np.arctan2(
                self.velocity[1],
                self.velocity[0]))

        if self.has_food or self.stamina <= 0:
            self.world.canvas.itemconfigure(self.view_arc, outline="")
        else:
            self.world.canvas.itemconfigure(
                self.view_arc,
                start=-self.angle - self.view_angle / 2,
                extent=self.view_angle,
                outline=self.color
            )

    def sense_pheromones(self):
        sensor_fwd = self.view_distance * \
            self.velocity / np.linalg.norm(self.velocity)
        sensor_left = rotate(sensor_fwd,
                             np.deg2rad(-self.view_angle / 2)) + self.pos
        sensor_right = rotate(
            sensor_fwd, np.deg2rad(
                self.view_angle / 2)) + self.pos
        sensor_fwd += self.pos

        #TODO: cringe
        # sensor_fwd_circle, sensor_left_circle, sensor_right_circle = self.sensors
        # self.world.canvas.coords(
        #     sensor_fwd_circle,
        #     sensor_fwd[0] - self.world.cellW,
        #     sensor_fwd[1] - self.world.cellH,
        #     sensor_fwd[0] + self.world.cellW,
        #     sensor_fwd[1] + self.world.cellH)

        # self.world.canvas.coords(
        #     sensor_left_circle,
        #     sensor_left[0] - self.world.cellW,
        #     sensor_left[1] - self.world.cellH,
        #     sensor_left[0] + self.world.cellW,
        #     sensor_left[1] + self.world.cellH)

        # self.world.canvas.coords(
        #     sensor_right_circle,
        #     sensor_right[0] - self.world.cellW,
        #     sensor_right[1] - self.world.cellH,
        #     sensor_right[0] + self.world.cellW,
        #     sensor_right[1] + self.world.cellH)

        pheromones = [0, 0, 0]
        for i, sensor in enumerate([sensor_fwd, sensor_left, sensor_right]):
            grid_x, grid_y = self.world.worldToGrid(sensor)

            top_left = np.array([grid_x - 1, grid_y - 1])
            btm_right = np.array([grid_x + 2, grid_y + 2])

            subgrid = self.world.grid[max(0, top_left[0]):min(self.world.cellsX, btm_right[0]),
                                      max(0, top_left[1]):min(self.world.cellsX, btm_right[1]), ]

            for row in subgrid:
                for cell in row:
                    for pheromone in cell.pheromones[self.species_id]:
                        lifetime = self.world.time - pheromone.creation_time
                        evaporation = max(1, lifetime / 1000)
                        pheromones[i] += 1 - evaporation

        if np.sum(pheromones) == 0:
            return

        value_fwd, value_left, value_right = pheromones

        if value_fwd > max(value_left, value_right):
            self.direction = sensor_fwd
        elif value_left > value_right:
            self.direction = sensor_left
        else:
            self.direction = sensor_right

    def resetStamina(self):
        """
        Réinitialise l'endurance de la fourmi.
        """

        self.stamina = self.base_stamina


class Sensor:
    def __init__(self):
        pass

    def sense_pheromones(self, position, velocity, angle):
        pass
