import numpy as np

species_defaults = {
    "speed": {"name": "Vitesse", "min": 1, "max": 10, "value": 4, "fn": int},
    "stamina": {"name": "Endurance", "min": 1, "max": 1000, "value": 350, "fn": int},
    "evaporation": {"name": "Temps Evaporation", "min": 1, "max": 1000, "value": 500, "fn": float},
    "view_distance": {"name": "Portee", "min": 10, "max": 100, "value": 40, "fn": int},
    "exploration": {"name": "Exploration", "min": 0.1, "max": 0.9, "value": 0.1, "fn": float},
    "comeback": {"name": "Retour", "min": 0.1, "max": 0.9, "value": 0.9, "fn": float},
    "wander_chance": {"name": "Suivi phero.", "min": 0, "max": 0, "value": 0, "fn": int},
    "deposit": {"name": "Depot phero.", "min": 0, "max": 0, "value": 0, "fn": int},
    "random_move": {"name": "Freq. alea.", "min": 0, "max": 0, "value": 0, "fn": int},
}


class Species:
    def __init__(self, species_id, color):
        self.species_id = species_id
        self.color = color
        self.inv_color = np.array([255 - val for val in self.color])
        for trait, value in species_defaults.items():
            setattr(self, trait, value['fn'](value['value']))

        self.reset()

    def __getitem__(self, key):
        if key in species_defaults.keys():
            value = species_defaults[key]
            return (getattr(self, key, value['value']))
        return getattr(self, key)

    def reset(self):
        self.food = 0
        self.active = False

    def set_active(self):
        self.active = True

    def add_food(self, amount):
        self.food += amount

    def update_trait(self, trait, value):
        setattr(self, trait, species_defaults[trait]['fn'](value))
