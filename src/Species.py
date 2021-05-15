import numpy as np

species_defaults = {
    "Vitesse": {"min": 1, "max": 10, "value": 4},
    "Endurance": {"min": 1, "max": 1000, "value": 350},
    "Evaporation": {"min": 1, "max": 1000, "value": 1000},
    "Portee": {"min": 1, "max": 20, "value": 10},
    "Exploration": {"min": 0.1, "max": 0.9, "value": 0.1},
    "Retour": {"min": 0, "max": 0, "value": 0},
    "Suivi phero.": {"min": 0, "max": 0, "value": 0},
    "Depot phero.": {"min": 0, "max": 0, "value": 0},
    "Freq. alea.": {"min": 0, "max": 0, "value": 0},
}


class Species:
    def __init__(self, species_id, color, speed, stamina):
        self.species_id = species_id
        self.color = color
        self.speed = speed
        self.stamina = stamina
        self.reset()

    def reset(self):
        self.food = 0
        self.active = False

    def set_active(self):
        self.active = True

    def add_food(self, amount):
        self.food += amount

    def update_trait(self, trait, value):
        print(trait, value)
        if trait == 'Vitesse':
            self.speed = value
        elif trait == 'Endurance':
            self.stamina = value
