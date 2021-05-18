import numpy as np
from util import create_circle, random_inside_circle, distance, rotate


class Ant:
    """
    Classe représentant une Fourmi
    Attributs:
        world:          Référence au monde.
        nest:           Nid auquel appartient la fourmi.
        ant_id:         Identifiant de la fourmi.
        color:          Couleur de l espece.
    """

    has_food = False
    food_amount = 0
    food_target = None
    view_angle = 120
    # distance par rapport au centre du nid pour déposer la nourriture
    food_disposal_distance = 4

    def __init__(self, world, nest, ant_id, color):

        self.world = world
        self.nest_pos = nest.pos
        self.nest_id = nest.nest_id
        self.species_id = nest.species_id

        # fait apparaitre la fourmi autour du nid lors de l initialisation
        random_pos = random_inside_circle() * 30
        self.pos = nest.pos + random_pos

        # donne une direction a la fourmi
        self.direction = random_inside_circle()

        self.steer_strength = 0.25  # virage serre
        self.wander_strength = 10  # definit la déviation de la trajectoire actuelle

        species = self.world.species[self.species_id]
        # parametres des fourmis, que l utiisateur peut mofifier
        self.speed = species.speed
        self.base_stamina = species.stamina
        self.stamina = species.stamina
        self.color = color
        self.wander_chance = species.wander_chance
        self.comeback = species.comeback
        self.view_distance = species.view_distance

        # velocite de la fourmi (vitesse a un instant donne)
        self.velocity = self.direction * self.speed * self.world.speed_value

        # chaine de caractere formate
        self.ant_id = f"ANT_{nest.nest_id}_{ant_id}"

        # senseurs de la fourmi => a proximite d une ressource ou de pheromones, la fourmi capte leur presence
        # 1 a gauche, 1 a droite et 1 devant
        self.sensor_circles = [
            create_circle(
                self.world.canvas,
                -10,
                -10,
                1,
                "", outline="") for i in range(3)]
        # vision de la fourmi
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
        # representation de la fourmi
        self.ant_circle = create_circle(
            self.world.canvas,
            self.pos[0],
            self.pos[1],
            2,
            self.color, tags=self.ant_id)

    def update(self):
        """
        Fonction qui permet de mettre a jour la Fourmi.
        """
        grid_x, grid_y = self.world.world_to_grid(self.pos)

        # Test si fourmi est dans la grille
        if grid_x >= 0 and grid_x < self.world.cellsX and grid_y >= 0 and grid_y < self.world.cellsY:
            if self.has_food:
                self.world.grid[grid_x, grid_y].add_pheromones(
                    self.species_id, self.pos)
        # on verifie si la fourmi est dans le nid
        self.check_nest()

        self.sense_pheromones()

        self.handle_food()

        # vitesse que la fourmi veut avoir, afin de ne pas depasser la vitesse maximale
        # on garde en memoire la velocite de la frame precedente (self.velocity),
        # on calcule donc la nouvelle velocite (desired_velocity)

        desired_velocity = self.direction * self.speed * self.world.speed_value

        # en effectuant la difference entre les 2 velocites, on obtient l acceleration de la fourmi
        # par laquelle on multiplie par l'intensite du virage. Si elle devie trop,
        # la norme de la velocite va devenir trop grande et accelerer plus que
        # la vitesse maximale de l espece
        acceleration = (desired_velocity - self.velocity) * self.steer_strength
        acceleration_magnitude = np.linalg.norm(acceleration)
        if acceleration_magnitude > self.steer_strength:
            # si l acceleration est trop grande, on la reduit pour que la
            # fourmi ne depasse jamais sa vitesse maximale
            acceleration = acceleration / acceleration_magnitude * self.steer_strength

        # on effectue la meme verification avec la velocite
        self.velocity = self.velocity + acceleration
        velocity_magnitude = np.linalg.norm(self.velocity)
        if velocity_magnitude > (self.speed * self.world.speed_value):
            self.velocity = self.velocity / velocity_magnitude * \
                self.speed * self.world.speed_value

        self.sense_wall()
        # on met a jour la position avec la nouvelle velocite
        self.pos += self.velocity
        # et on bouge la fourmi sur le canvas
        self.world.canvas.move(self.ant_id, self.velocity[0], self.velocity[1])

        self.world.canvas.itemconfigure(
            self.ant_circle,
            fill="gray" if self.stamina <= 0 else self.color)
        # tourner l angle de vue en fonction de sa rotation
        self.update_angle()

    def wander(self):
        """
        Fonction qui permet a une fourmi d explorer le canvas
        """
        # direction aleatoire
        self.direction = (
            self.direction +
            random_inside_circle() *
            self.wander_strength)

        self.stamina -= self.world.speed_value

    def handle_food(self):
        """
        Fonction qui permet de detecter ou de prendre de la nourriture
        """
        # si la fourmi a trouve une ressource ou est fatiguee, elle rentre au nid
        # direction fourmi - nid represente par un vecteur que l on normalise
        if self.has_food or self.stamina <= 0:
            self.direction = (self.nest_pos - self.pos)
            self.direction = self.direction / np.linalg.norm(self.direction)
        # si la fourmi ne voit pas de nourriture, alors elle en cherche
        elif not self.food_target:
            # distance minimale d une nourriture, qu on initialise a l infini
            min_dist = np.Infinity
            for food in self.world.food:
                if food.amount <= 0:
                    continue

                dist = distance(self.pos, food.pos)
                # on regarde si la distance est inferieure a la portee de la fourmi,
                #  auquel cas elle a trouve de la nourriture
                if dist < (self.view_distance +
                           food.scale) and dist < min_dist:
                    min_dist = dist
                    self.food_target = food
        else:
            if self.food_target.amount <= 0:
                self.food_target = None
                return
            # si elle a de la nourriture en vue, elle se rapproche de la
            # ressource et va la prendre
            food_dir = (self.food_target.pos - self.pos)
            dist = np.linalg.norm(self.direction)

            if dist < max(self.food_target.scale, 20):
                self.has_food = True
                self.food_target.decrease()
                self.food_amount += 1
            else:
                self.direction = food_dir / dist

    def check_nest(self):
        """
        Fonction qui verifie si la fourmi est dans le nid
        """
        dist = np.linalg.norm(self.nest_pos - self.pos)
        # si la fourmi est dans le nid, on reinitialise l endurance de la
        # fourmi
        if dist < self.food_disposal_distance:
            self.stamina = self.base_stamina
            if self.has_food:
                self.world.nests[self.nest_id].add_food(self.food_amount)
                self.has_food = False
                self.food_target = None
                self.direction = random_inside_circle()

    def update_angle(self):
        """
        Fonction qui met a jour l angle de vue
        """
        # angle du vecteur par rapport a l axe des abscisses
        self.angle = np.rad2deg(
            np.arctan2(
                self.velocity[1],
                self.velocity[0]))

        if self.has_food or self.stamina <= 0:
            self.world.canvas.itemconfigure(self.view_arc, outline="")
        else:
            self.world.canvas.itemconfig(
                self.view_arc,
                start=-self.angle - self.view_angle / 2,
                extent=self.view_angle,
                outline=self.color
            )

    def sense_pheromones(self):
        """
        Fonction qui permet a la fourmi de sentir les pheromones
        """
        # initialisation des capteurs
        sensor_fwd = self.view_distance * \
            self.velocity / np.linalg.norm(self.velocity)
        sensor_left = rotate(sensor_fwd,
                             np.deg2rad(self.view_angle / 2))
        sensor_right = rotate(
            sensor_fwd, np.deg2rad(
                -self.view_angle / 2))

        self.sensors = [sensor_fwd, sensor_left, sensor_right]
        # cercles representant les capteurs (transparents actuellement)
        sensor_fwd_circle, sensor_left_circle, sensor_right_circle = self.sensor_circles
        # mise a jour des coordonnees des 3 senseurs
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

        # for sensor in self.sensor_circles:
        #     self.world.canvas.itemconfig(sensor, fill='blue')

        # nombre de pheromones que les 3 senseurs detectent,
        # avec self.wander_chance qui choisit si la fourmi suit un senseur ou
        # explore
        pheromones_amount = [0, 0, 0, self.wander_chance]
        for i, sensor in enumerate(self.sensors):
            # position sur la grille du senseur
            grid_x, grid_y = self.world.world_to_grid(sensor + self.pos)
            # rectangle qui définit toutes les cases de la grille que le
            # senseur voit
            top_left = np.array([grid_x - 1, grid_y - 1])
            btm_right = np.array([grid_x + 2, grid_y + 2])

            # on cree ensuite une sous grille pour que le senseur puisse capter les pheromones environnantes
            # en forme de cercle
            subgrid = self.world.grid[max(0, top_left[0]):min(self.world.cellsX, btm_right[0]),
                                      max(0, top_left[1]):min(self.world.cellsX, btm_right[1]), ]
            # on fait la somme des pheromones de la sous grille
            for row in subgrid:
                for cell in row:
                    pheromones_amount[i] = cell.get_pheromones(self.species_id)

        sum_pheromones = np.sum(pheromones_amount)
        if sum_pheromones == 0:
            return
        # on fait un choix avec un poids : plus il y a de pheromones, plus la
        # fourmi est susceptible de suivre cette direction
        choice = np.random.choice(
            [0, 1, 2, 4], p=pheromones_amount / sum_pheromones)
        # si le choix = 4, la fourmi explore
        if choice == 4:
            self.wander()
            return

        self.direction = self.sensors[choice]

        # self.world.canvas.itemconfig(
        #     self.sensor_circles[choice], fill='yellow')

    def resetStamina(self):
        """
        Réinitialise l'endurance de la fourmi.
        """

        self.stamina = self.base_stamina

    def sense_wall(self):
        """
        Fonction qui permet a une fourmi de detecter un mur
        """
        new_pos = self.pos + self.velocity
        new_grid_x, new_grid_y = self.world.world_to_grid(new_pos)

        check_walls = True
        # on verifie si la fourmi est bien dans le canvas
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

        grid_x, grid_y = self.world.world_to_grid(self.pos)
        # on verifie si un mur est sur le chemin de la fourmi
        if self.world.wall[new_grid_x, new_grid_y]:
            if new_grid_x < grid_x:
                self.velocity[0] = -1
                self.direction[0] = -1
            else:
                self.velocity[0] = 1
                self.direction[0] = 1

            if new_grid_y < grid_y:
                self.velocity[1] = -1
                self.direction[1] = -1
            else:
                self.velocity[1] = 1
                self.direction[1] = 1

            self.velocity = self.velocity * -1
