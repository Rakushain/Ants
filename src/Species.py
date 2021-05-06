import numpy as np

species_defaults = {
    "speed": {"min": 0.1, "max": 1, "value": 0.5},
    "stamina": {"min": 1, "max": 1000, "value": 350},
}


class Species:
    def __init__(self, color, speed, stamina):
        self.color = color
        self.speed = speed
        self.stamina = stamina
    
    def update_trait(self, trait, value):
        print(trait, value)
        if trait == 'speed':
            self.speed = value
        elif trait == 'stamina':
            self.stamina = value
