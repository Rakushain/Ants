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

        self.speed_value = tk.DoubleVar(value=1)
        self.speed_value.trace_add('write', self.on_modif_speed)
        self.foodOrNest = tk.IntVar(value=FoodOrNest.FOOD)
        self.speciesId = tk.IntVar(value=0)
        self.is_modifying = tk.BooleanVar(value=False)
        # self.is_modifying.trace_add('write', self.on_modif_state_change)

        self.create_frame_top()
        self.create_canvas()
        self.create_frame_bottom()

        self.world = World(
            self,
            self.canvas,
            self.canvasW,
            self.canvasH,
            cellsX,
            cellsY,
            maxFood,
            maxNests)

        self.world.loadWorld("1 espece et 1 ressource.json")

        self.root.mainloop()

    def create_world(self):
        self.world.reset()
        print(sys.getrefcount(self.canvas))

    def handle_canvas_click(self, event):
        print(event.x, event.y)
        if (not self.is_modifying.get()):
            self.world.addWall(event.x, event.y)
            return

        if self.world.started:
            return

        try:
            amount = int(self.foodOrNestAmountInput.get())
        except ValueError:
            return

        if amount <= 0:
            return

        print(amount)

        if self.foodOrNest.get() == FoodOrNest.FOOD and len(
                self.world.food) < self.world.maxFood:
            self.world.addFood(Food(self.canvas, event.x, event.y, amount))
        elif self.foodOrNest.get() == FoodOrNest.NEST and len(self.world.nests) < self.world.maxNests:
            self.world.addNest(
                Nest(self.world, len(self.world.nests), event.x, event.y, self.speciesId.get(), amount))

    def handle_canvas_drag(self, event):
        if self.is_modifying.get():
            return

        self.world.addWall(event.x, event.y)

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
        self.canvas.bind("<Button-1>", self.handle_canvas_click)
        self.canvas.bind('<B1-Motion>', self.handle_canvas_drag)

        frame.pack(fill="both", expand="yes")

    def create_frame_top(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both")

        self.create_size_dropdown(frame)

        self.create_worlds_dropdown(frame)

        self.create_species_select(frame)

        self.create_food_or_nest_select(frame)

        self.create_species_traits(frame)

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
            text='OK' if self.is_modifying.get() else 'Modifier',
            command=self.on_modif_state_change)
        self.modif_button.grid(columnspan=2, sticky=tk.NSEW)

        frame.pack(side=tk.LEFT)

    def create_species_traits(self, parent):
        frame = tk.Frame(parent)

        self.species_traits_entries = []

        self.wrong_value_popup_open = False

        for i, (trait, val) in enumerate(species_defaults.items()):
            x = 2 * int(i / 3)
            y = i % 3

            vcmd = (frame.register(self.validate_species_trait),
                    trait, '%P')

            label = tk.Label(frame, text=trait, anchor=tk.W)
            label.grid(column=x, row=y, sticky=tk.NSEW)

            entry = tk.Entry(frame)
            entry.insert(0, val['value'])
            entry.configure(
                state=tk.DISABLED,
                validate='key',
                validatecommand=vcmd
            )
            entry.grid(column=x + 1, row=y, sticky=tk.NSEW)
            self.species_traits_entries.append(entry)

        frame.pack(side=tk.LEFT)

    def validate_species_trait(self, trait, str_val):
        return True

        # trait_defaults = species_defaults[trait]
        # min_val = trait_defaults['min']
        # max_val = trait_defaults['max']

        # valid = False

        # try:
        #     new_val = float(str_val)
        #     if new_val >= trait_defaults['min'] and new_val <= trait_defaults['max']:
        #         self.world.species[self.speciesId.get()].update_trait(
        #             trait, new_val)
        #         valid = True
        # except ValueError:
        #     pass

        # if not valid:
        #     self.spawn_wrong_value_popup(
        #         trait, min_val, max_val, str_val)

        # return valid

    def on_modif_state_change(self, *_):
        print(self.world.started, ' & ', self.is_modifying.get())
        if self.world.started:
            self.is_modifying.set(False)
        else:
            self.is_modifying.set(
                not self.is_modifying.get())
        print(self.world.started, ' & ', self.is_modifying.get(), '\n')

        self.modif_button.configure(
            text='OK' if self.is_modifying.get() else 'Modifier')

        elements = [
            *self.species_radios,
            *self.species_traits_entries,
            self.foodRadio,
            self.nestRadio,
            self.foodOrNestAmountInput,
            self.opt_world_size
        ]

        for element in elements:
            element.configure(
                state=tk.NORMAL if self.is_modifying.get() else tk.DISABLED)

    def on_modif_speed(self, *_):
        self.world.speed_value = self.speed_value.get()

    def create_worlds_dropdown(self, parent):
        loadWorldOptions = []
        for (_, _, filenames) in walk(WORLDS_FOLDER):
            for filename in filenames:
                if (filename.endswith('.json')):
                    loadWorldOptions.append(filename[:-5])

        if (len(loadWorldOptions) <= 0):
            return

        loadWorldVar = tk.StringVar()
        loadWorldVar.set('Nouveau Monde')

        loadWorldDrop = tk.OptionMenu(
            parent,
            loadWorldVar,
            'Nouveau Monde',
            *loadWorldOptions,
            command=lambda filename: self.world.loadWorld(f"{filename}.json") if filename != 'Nouveau Monde' else self.world.reset())

        loadWorldDrop.pack(side=tk.LEFT)

    def create_size_dropdown(self, parent):
        OptionList = [
            "20",
            "50",
            "75",
            "100",
            "150",
            "200"
        ]
        self.world_size = tk.IntVar(parent)
        self.world_size.set(OptionList[1])
        self.world_size.trace_add('write', self.udpate_world_size)

        self.opt_world_size = tk.OptionMenu(
            parent, self.world_size, *OptionList)
        self.opt_world_size.config(
            width=15, font=(
                "Helvetica", 12), state=tk.DISABLED)
        self.opt_world_size.pack(side=tk.RIGHT)

        label_size = tk.Label(parent, text="Taille monde:")
        label_size.config(width=15, font=("Helvetica", 16))
        label_size.pack(side=tk.RIGHT)

    def udpate_world_size(self, *_):
        world_size = self.world_size.get()
        self.world.reset_grid(world_size, world_size)

    def create_frame_bottom(self):
        frame = tk.Frame(self.root, bg='grey')

        self.button_go = tk.Button(
            frame,
            text="Go =>",
            command=self.start_stop)
        self.button_go.pack(side=tk.LEFT)

        button_start = tk.Button(
            frame,
            text="Pas ->",
            command=self.step)
        button_start.pack(side=tk.LEFT)

        label_speed = tk.Label(frame, text="Vitesse :")
        label_speed.config(width=15, height=1, font=("Helvetica, 14"))
        label_speed.pack(side=tk.LEFT)

        button_speed_minus = tk.Button(
            frame,
            text="-",
            height=0,
            width=25,
            command=self.speed_minus)
        button_speed_minus.pack(side=tk.LEFT)

        label_speed_update = tk.Label(frame, textvariable=self.speed_value)
        label_speed_update.config(width=20)
        label_speed_update.pack(side=tk.LEFT)

        button_speed_add = tk.Button(
            frame,
            text="+",
            height=0,
            width=25,
            command=self.speed_add)
        button_speed_add.pack(side=tk.LEFT)

        self.label_time = tk.Label(frame)
        self.label_time.config(width=8, height=2)
        self.label_time.pack(side=tk.LEFT)

        frame.pack(side="bottom", fill="both", padx=5, pady=5)

    def update_time(self):
        #  Permet de mettre le temps à jour sur le label correspondant
        self.label_time.config(text=int(self.world.time))
        # self.main_gui.button_go["text"] = "Go =>"

    def speed_minus(self):
        if 0.25 < self.speed_value.get() <= 2:
            self.speed_value.set(self.speed_value.get() - 0.25)
        else:
            return

    def speed_add(self):
        if 0.25 <= self.speed_value.get() < 2:
            self.speed_value.set(self.speed_value.get() + 0.25)
        else:
            return

    def start_stop(self):
        if self.world.paused or not self.world.started:
            self.is_modifying.set(False)
            self.world.start()
            self.update_time()
            self.button_go["text"] = "Stop"
        else:
            self.world.pause()
            self.button_go["text"] = "Go =>"

    def step(self):
        self.world.next_frame()
        self.button_go["text"] = "Go =>"

    def spawn_wrong_value_popup(self, trait, min_val, max_val, value):
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
            win, text=f"Veuillez choisir une {trait} comprise entre {min_val} et {max_val}")
        l.grid(column=0, row=0)

        l = tk.Label(
            win, text=f"valeur entrée: {value}")
        l.grid(column=0, row=1)

        b = tk.Button(win, text="Ok", command=close_win)
        b.grid(column=0, row=2)

        # win.geometry(("%dx%d%+d%+d" % (250, 50, 750, 400)))
