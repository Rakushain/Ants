import numpy as np
from util import create_circle, vect_rot, random_inside_circle, distance, rotate


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
    # distance par rapport au centre du nid pour déposer la nourriture
    food_disposal_distance = 4
    # Chance que la fourmi parte dans une direction aléatoire
    wander_chance = 0.1

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

        self.steer_strength = 0.25  # virage serre
        self.wander_strength = 10  # definit la déviation de la trajectoire actuelle
        self.speed = speed  # speed
        self.velocity = self.direction * self.speed * self.world.speed_value

        self.base_stamina = stamina
        self.stamina = stamina
        self.color = color

        self.ant_id = f"ANT_{nest.nest_id}_{ant_id}"

        self.sensor_circles = [
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
        grid_x, grid_y = self.world.world_to_grid(self.pos)

        # Test si fourmi est dans la grille
        if grid_x >= 0 and grid_x < self.world.cellsX and grid_y >= 0 and grid_y < self.world.cellsY:
            if self.has_food:
                # TODO: variable amount
                self.world.grid[grid_x, grid_y].add_pheromones(
                    self.species_id, self.pos)  # TODO: Color

        self.check_nest()

        self.sense_pheromones()

        # self.wander()
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

        self.sense_wall()

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

            if dist < max(self.food_target.scale, 20):
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
                self.world.nests[self.nest_id].add_food(self.food_amount)
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
        # normaliser le vec -> toujours de longueur 1 -> multiplier par la vitesse
        # si on normalise pas le vecteur ,la fourmi ira plus vite en diagonale
        # que dans les directions classiques
        sensor_fwd = self.view_distance * \
            self.velocity / np.linalg.norm(self.velocity)
        sensor_left = rotate(sensor_fwd,
                             np.deg2rad(self.view_angle / 2))
        sensor_right = rotate(
            sensor_fwd, np.deg2rad(
                -self.view_angle / 2))

        self.sensors = [sensor_fwd, sensor_left, sensor_right]

        #TODO: cringe
        sensor_fwd_circle, sensor_left_circle, sensor_right_circle = self.sensor_circles
        self.world.canvas.coords(
            sensor_fwd_circle,
            sensor_fwd[0] - self.world.cellW + self.pos[0],
            sensor_fwd[1] - self.world.cellH + self.pos[1],
            sensor_fwd[0] + self.world.cellW + self.pos[0],
            sensor_fwd[1] + self.world.cellH + self.pos[1])

        self.world.canvas.coords(
            sensor_left_circle,
            sensor_left[0] - self.world.cellW + self.pos[0],
            sensor_left[1] - self.world.cellH + self.pos[1],
            sensor_left[0] + self.world.cellW + self.pos[0],
            sensor_left[1] + self.world.cellH + self.pos[1])

        self.world.canvas.coords(
            sensor_right_circle,
            sensor_right[0] - self.world.cellW + self.pos[0],
            sensor_right[1] - self.world.cellH + self.pos[1],
            sensor_right[0] + self.world.cellW + self.pos[0],
            sensor_right[1] + self.world.cellH + self.pos[1])

        for sensor in self.sensor_circles:
            self.world.canvas.itemconfig(sensor, fill='blue')

        pheromones = [0, 0, 0, self.wander_chance]
        for i, sensor in enumerate(self.sensors):
            grid_x, grid_y = self.world.world_to_grid(sensor + self.pos)

            top_left = np.array([grid_x - 1, grid_y - 1])
            btm_right = np.array([grid_x + 2, grid_y + 2])

            subgrid = self.world.grid[max(0, top_left[0]):min(self.world.cellsX, btm_right[0]),
                                      max(0, top_left[1]):min(self.world.cellsX, btm_right[1]), ]

            for row in subgrid:
                for cell in row:
                    pheromones[i] = cell.get_pheromones(self.species_id)

        sum_pheromones = np.sum(pheromones)
        if sum_pheromones == 0:
            return

        choice = np.random.choice([0, 1, 2, 4], p=pheromones / sum_pheromones)

        if choice == 4:
            self.wander()
            return

        self.direction = self.sensor_circles[choice]
        self.world.canvas.itemconfig(
            self.sensor_circles[choice], fill='yellow')

        # if value_fwd > max(value_left, value_right):
        #     self.direction = sensor_fwd
        #     # TODO: cringe
        #     self.world.canvas.itemconfig(sensor_fwd_circle, fill='yellow')
        # elif value_left > value_right:
        #     self.direction = sensor_left
        #     # TODO: cringe
        #     self.world.canvas.itemconfig(sensor_left_circle, fill='yellow')
        # else:
        #     self.direction = sensor_right
        #     # TODO: cringe
        #     self.world.canvas.itemconfig(sensor_right_circle, fill='yellow')

    def resetStamina(self):
        """
        Réinitialise l'endurance de la fourmi.
        """

        self.stamina = self.base_stamina

    def sense_wall(self):
        new_pos = self.pos + self.velocity
        new_grid_x, new_grid_y = self.world.world_to_grid(new_pos)

        check_walls = True

        if new_pos[0] < 0:
            self.velocity[0] = 1
            self.direction[0] = 1
            check_walls = False

        if new_pos[0] > self.world.width:
            self.velocity[0] = -1
            self.direction[0] = -1
            check_walls = False

        if new_pos[1] < 0:
            self.velocity[1] = 1
            self.direction[1] = 1
            check_walls = False

        if new_pos[1] > self.world.height:
            self.velocity[1] = -1
            self.direction[1] = -1
            check_walls = False

        if not check_walls:
            return

        if self.world.wall[new_grid_x, new_grid_y]:
            if new_pos[0] < self.pos[0]:
                self.velocity[0] = -1
                self.direction[0] = -1
            else:
                self.velocity[0] = 1
                self.direction[0] = 1

            if new_pos[1] < self.pos[1]:
                self.velocity[1] = -1
                self.direction[1] = -1
            else:
                self.velocity[1] = 1
                self.direction[1] = 1

            self.velocity = self.velocity * -1

        # if self.world.wall
