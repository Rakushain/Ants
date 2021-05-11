import numpy as np

species_defaults = {
    "speed": {"min": 0.1, "max": 1, "value": 0.5},
    "stamina": {"min": 1, "max": 1000, "value": 350},
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
        if trait == 'speed':
            self.speed = value
        elif trait == 'stamina':
            self.stamina = value