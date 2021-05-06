import tkinter as tk
import numpy as np
from World import World
from Food import Food
from Nest import Nest
import sys
from os import walk
from Species import species_defaults


class FoodOrNest:
    FOOD = 0
    NEST = 1


BG_COLOR = "#F1F1F1"
WORLDS_FOLDER = "worlds"


class MainGUI:
    def __init__(self, canvasW, canvasH, cellsX, cellsY, maxFood, maxNests):
        self.root = tk.Tk()
        self.root.configure(bg=BG_COLOR)
        self.root.title("Ants")

        self.canvasW = canvasW
        self.canvasH = canvasH

        self.foodOrNest = tk.IntVar(value=FoodOrNest.FOOD)
        self.speciesId = tk.IntVar(value=0)
        self.isModifying = tk.BooleanVar(value=False)
        self.isModifying.trace_add('write', self.on_modif_state_change)

        self.create_frame_top()
        self.create_canvas()
        self.create_frame_bottom()

        self.world = World(
            self.canvas,
            self.canvasW,
            self.canvasH,
            cellsX,
            cellsY,
            maxFood,
            maxNests)

        self.root.mainloop()

    def create_world(self):
        self.world.reset()
        print(sys.getrefcount(self.canvas))

    def handleCanvasClick(self, event):
        print(event.x, event.y)
        if (not self.isModifying.get()) or self.world.started:
            return

        try:
            amount = int(self.foodOrNestAmountInput.get())
        except ValueError:
            return

        if amount <= 0:
            return

        print(amount)

        if self.foodOrNest.get() == FoodOrNest.FOOD:
            self.world.addFood(Food(self.canvas, event.x, event.y, amount))
        elif self.foodOrNest.get() == FoodOrNest.NEST:
            self.world.addNest(
                Nest(self.world, event.x, event.y, self.speciesId.get(), amount))

    def create_canvas(self):
        frame = tk.Frame(self.root)

        self.canvas = tk.Canvas(
            frame,
            width=self.canvasW,
            height=self.canvasH,
            bd=0,
            bg=BG_COLOR,
            highlightthickness=0)
        self.canvas.pack(expand="yes")
        self.canvas.bind("<Button-1>", self.handleCanvasClick)

        frame.pack(fill="both", expand="yes")

    def create_frame_top(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both")

        self.create_worlds_dropdown(frame)

        self.create_species_select(frame)

        self.create_food_or_nest_select(frame)

        self.create_species_characteristics(frame)

        frame.pack(fill="both", padx=5, pady=5)

    def create_food_or_nest_select(self, parent):
        frame = tk.Frame(parent)

        self.foodRadio = tk.Radiobutton(
            frame,
            text="Nourriture",
            variable=self.foodOrNest,
            value=FoodOrNest.FOOD,
            state=tk.DISABLED
        )
        self.foodRadio.pack(side=tk.TOP, anchor=tk.NW)
        self.nestRadio = tk.Radiobutton(
            frame,
            text="Nid",
            variable=self.foodOrNest,
            value=FoodOrNest.NEST,
            state=tk.DISABLED
        )
        self.nestRadio.pack(side=tk.TOP, anchor=tk.NW)

        self.foodOrNestAmountInput = tk.Entry(frame)
        self.foodOrNestAmountInput.insert(0, "20")
        self.foodOrNestAmountInput.configure(state=tk.DISABLED)
        self.foodOrNestAmountInput.pack(side=tk.LEFT, anchor=tk.NW)

        frame.pack(side=tk.LEFT)

    def create_species_select(self, parent):
        frame = tk.Frame(parent)

        self.species_radios = []

        for i in range(4):
            radio = tk.Radiobutton(
                frame,
                text=f"Espece {i + 1}",
                variable=self.speciesId,
                value=i,
                state=tk.DISABLED
            )
            # radio.pack(side=tk.LEFT)
            radio.grid(column=i % 2, row=int(i / 2))

            self.species_radios.append(radio)

        self.modif_button = tk.Button(
            frame,
            text='OK' if self.isModifying.get() else 'Modifier',
            command=lambda: self.isModifying.set(
                not self.isModifying.get()))
        self.modif_button.grid(columnspan=2, sticky=tk.NSEW)

        frame.pack(side=tk.LEFT)

    def create_species_characteristics(self, parent):
        frame = tk.Frame(parent)

        self.species_characteristics_entries = []

        self.wrong_value_popup_open = False

        for i, (characteristic, val) in enumerate(species_defaults.items()):
            x = 2 * int(i / 3)
            y = i % 3

            vcmd = (frame.register(self.validate_species_characteristic),
                    characteristic, '%P')

            label = tk.Label(frame, text=characteristic, anchor=tk.W)
            label.grid(column=x, row=y, sticky=tk.NSEW)

            entry = tk.Entry(frame)
            entry.insert(0, val['value'])
            entry.configure(
                state=tk.DISABLED,
                validate='key',
                validatecommand=vcmd
            )
            entry.grid(column=x + 1, row=y, sticky=tk.NSEW)
            self.species_characteristics_entries.append(entry)

        frame.pack(side=tk.LEFT)

    def validate_species_characteristic(self, characteristic, str_val):
        print('val', str_val)
        characteristic_defaults = species_defaults[characteristic]
        min_val = characteristic_defaults['min']
        max_val = characteristic_defaults['max']

        valid = False

        try:
            print(str_val)
            new_val = float(str_val)
            if new_val >= characteristic_defaults['min'] and new_val <= characteristic_defaults['max']:
                valid = True
        except ValueError:
            pass

        if not valid:
            self.spawn_wrong_value_popup(
                characteristic, min_val, max_val, str_val)

        return valid

    def on_modif_state_change(self, *_):
        self.modif_button.configure(
            text='OK' if self.isModifying.get() else 'Modifier')

        elements = [
            *self.species_radios,
            *self.species_characteristics_entries,
            self.foodRadio,
            self.nestRadio,
            self.foodOrNestAmountInput
        ]

        for element in elements:
            element.configure(
                state=tk.NORMAL if self.isModifying.get() else tk.DISABLED)

    def create_worlds_dropdown(self, parent):
        loadWorldOptions = []
        for (_, _, filenames) in walk(WORLDS_FOLDER):
            for filename in filenames:
                if (filename.endswith('.json')):
                    loadWorldOptions.append(filename)

        if (len(loadWorldOptions) <= 0):
            return

        loadWorldVar = tk.StringVar()
        loadWorldVar.set('Nouveau Monde')

        loadWorldDrop = tk.OptionMenu(
            parent,
            loadWorldVar,
            'Nouveau Monde',
            *loadWorldOptions,
            command=lambda filename: self.world.loadWorld(filename) if filename != 'Nouveau Monde' else self.world.reset())

        loadWorldDrop.pack(side=tk.LEFT)

    def create_frame_bottom(self):
        frame = tk.Frame(self.root, bg='grey')

        button_start = tk.Button(
            frame,
            text="GO =>",
            command=lambda: self.world.start())
        button_start.pack(side=tk.LEFT)

        button_start = tk.Button(
            frame,
            text="Pas ->",
            command=lambda: self.world.next_frame())
        button_start.pack(side=tk.LEFT)

        frame.pack(side="bottom", fill="both", padx=5, pady=5)

    def spawn_wrong_value_popup(self, characteristic, min_val, max_val, value):
        """
        Cree un popup quand la taille d une ressource n est pas comprise entre 1 et 30
        """
        print('xd', self.wrong_value_popup_open)
        if self.wrong_value_popup_open:
            return

        self.wrong_value_popup_open = True

        win = tk.Toplevel()
        win.wm_title("Attention !")

        def close_win():
            win.destroy()
            self.wrong_value_popup_open = False

        l = tk.Label(
            win, text=f"Veuillez choisir une {characteristic} comprise entre {min_val} et {max_val}")
        l.grid(column=0, row=0)

        l = tk.Label(
            win, text=f"valeur entrée: {value}")
        l.grid(column=0, row=1)

        b = tk.Button(win, text="Ok", command=close_win)
        b.grid(column=0, row=2)

        # win.geometry(("%dx%d%+d%+d" % (250, 50, 750, 400)))
