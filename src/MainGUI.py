import tkinter as tk
import numpy as np
from World import World
from Food import Food
from Nest import Nest
import sys
from os import walk
from Species import species_defaults


class FoodOrNest:
    """
    Classe qui attribue une valeur a food et nest
    """
    FOOD = 0
    NEST = 1


BG_COLOR = "#F1F1F1"
WORLDS_FOLDER = "worlds"


class MainGUI:
    """
    Classe représentant le Monde
    Attributs:
        canvasW:        Largeur du canvas en pixels
        canvasH:        Hauteur du canvas en pixels
        cellsX:         Nombre de cellules de la grille en horizontal
        cellsY:         Nombre de cellules de la grille en vertical
        maxFood:        Nombre maximum de nourriture sur le canvas
        maxNests:       Nombre maximum de nids sur le canvas
    """

    def __init__(self, canvasW, canvasH, cellsX, cellsY, maxFood, maxNests):
        # Fenetre principale
        self.root = tk.Tk()
        self.root.configure(bg=BG_COLOR)
        self.root.title("Ants")

        self.canvasW = canvasW
        self.canvasH = canvasH

        # Liste des variables de tkinter pour mettre a jour les differents
        # widgets
        self.speed_value = tk.DoubleVar(value=1)
        self.speed_value.trace_add('write', self.on_modif_speed)
        self.species_food = tk.StringVar()
        self.foodOrNest = tk.IntVar(value=FoodOrNest.FOOD)
        self.speciesId = tk.IntVar(value=0)
        self.previous_species_id = tk.IntVar(value=0)
        self.is_modifying = tk.BooleanVar(value=False)

        self.new_world = 0

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

        self.speciesId.trace_add('write', self.on_species_select)
        # par defaut, on charge le monde avec un nid et une ressource
        self.world.loadWorld("1 espece et 1 ressource.json")

        self.root.mainloop()

    def handle_canvas_click(self, event):
        """
        Fonction qui permet de detecter un clic sur le canvas
        """
        # par defaut, on ajoute un mur avec un clic gauche
        if (not self.is_modifying.get()):
            grid_x, grid_y = self.world.world_to_grid(
                np.array([event.x, event.y]))
            self.world.add_wall(grid_x, grid_y)
            return
        # si le monde est lance, on ne peux plus rien ajouter sauf des murs
        if self.world.started:
            return
        try:
            amount = int(self.foodOrNestAmountInput.get())
        except ValueError:
            self.spawn_wrong_value_popup("notint", 0, 0, 0)
            return
        # on regarde si l utilisateur a selectionne de la nourriture ou un nid a placer
        # et on fait apparaitre un popup si la valeur n'est pas comprise dans
        # l'intervalle
        if self.foodOrNest.get() == FoodOrNest.FOOD and len(
                self.world.food) < self.world.maxFood:
            if 0 < amount <= 30:
                self.world.add_food(
                    Food(
                        self.canvas,
                        event.x,
                        event.y,
                        amount))
            else:
                self.spawn_wrong_value_popup("nourriture", 1, 30, amount)
        elif self.foodOrNest.get() == FoodOrNest.NEST and len(self.world.nests) < self.world.maxNests:
            if 0 < amount <= 100:
                self.world.add_nest(
                    Nest(self.world, len(self.world.nests), event.x, event.y, self.speciesId.get(), amount))
            else:
                self.spawn_wrong_value_popup(
                    "population de nid", 1, 100, amount)
        self.opt_world_size.configure(state=tk.DISABLED)

    def handle_canvas_drag(self, event):
        """
        Fonction qui permet de detecter le clic maintenu
        """
        if self.is_modifying.get():
            return

        grid_x, grid_y = self.world.world_to_grid(np.array([event.x, event.y]))
        self.world.add_wall(grid_x, grid_y)

    def create_canvas(self):
        """
        Creation du canvas
        """
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
        """
        Creation de la frame supérieure
        """
        frame = tk.Frame(self.root)
        frame.pack(fill="both")

        self.create_worlds_dropdown(frame)

        self.create_species_select(frame)

        self.create_food_or_nest_select(frame)

        self.create_species_traits(frame)

        self.create_sun_check(frame)

        self.create_size_dropdown(frame)

        frame.pack(fill="both", padx=5, pady=5)

    def create_food_or_nest_select(self, parent):
        """
        Fonction qui crée les boutons pour placer de la nourriture ou un nid
        ainsi qu'une entry pour sélectionner la quantité
        """
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
        """
        Fonction qui permet de choisir l'espèce a modifier
        et crée un bouton modifier / Ok
        """
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
            radio.grid(column=i % 2, row=int(i / 2))

            self.species_radios.append(radio)

        self.modif_button = tk.Button(
            frame,
            text='OK' if self.is_modifying.get() else 'Modifier',
            command=self.on_modif_state_change)
        self.modif_button.grid(columnspan=2, sticky=tk.NSEW)

        frame.pack(side=tk.LEFT)

    def on_species_select(self, *_):
        """
        Fonction de garder en mémoire les valeurs des caractéristiques des fourmis
        lorsque l'on change d'espèce
        """
        self.root.focus()
        previous_species = self.world.species[self.previous_species_id.get()]
        species = self.world.species[self.speciesId.get()]

        for trait, entry in self.species_traits_entries.items():
            previous_species.update_trait(trait, entry.get())
            entry.delete(0, tk.END)
            entry.insert(0, species[trait])

        self.previous_species_id.set(self.speciesId.get())

    def update_species_entry(self, trait, value):
        """
        Fonction qui permet de mettre à jour les entries lors du chargement d'un monde
        """
        entry = self.species_traits_entries[trait]
        entry.delete(0, tk.END)
        entry.insert(0, value)
        # impossibilite de changer les valeurs sur les entries
        # print(entry.value())
        # print(entry.get())

    def create_species_traits(self, parent):
        """
        Fonction qui crée toutes les entries pour les paramètres des fourmis
        """
        frame = tk.Frame(parent)

        self.species_traits_entries = {}

        self.wrong_value_popup_open = False

        for i, (trait, val) in enumerate(species_defaults.items()):
            x = 2 * int(i / 3)
            y = i % 3

            vcmd = (frame.register(self.validate_species_trait),
                    trait, '%P')

            label = tk.Label(frame, text=val['name'], anchor=tk.W)
            label.grid(column=x, row=y, sticky=tk.NSEW)

            entry = tk.Entry(frame)
            entry.insert(0, val['value'])
            entry.configure(
                state=tk.DISABLED,
                validate='focusout',
                validatecommand=vcmd
            )
            entry.grid(column=x + 1, row=y, sticky=tk.NSEW)
            self.species_traits_entries[trait] = entry

        frame.pack(side=tk.LEFT)

    def validate_species_trait(self, trait, str_val):
        """
        Fonction qui vérifie si les valeurs entrées sont conformes
        """
        trait_defaults = species_defaults[trait]
        min_val = trait_defaults['min']
        max_val = trait_defaults['max']

        try:
            new_val = float(str_val)
            if new_val >= min_val and new_val <= max_val:
                self.world.species[self.speciesId.get()].update_trait(
                    trait, new_val)
            else:
                raise ValueError
        except ValueError:
            self.spawn_wrong_value_popup(
                trait, min_val, max_val, str_val)

        return True

    def on_modif_state_change(self, *_):
        """
        Fonction qui permet d'activer ou de désactiver les widgets en fonction de l'état du bouton Modifier / Ok
        """
        self.root.focus()
        if self.world.started:
            self.is_modifying.set(False)
        else:
            self.is_modifying.set(
                not self.is_modifying.get())

        self.modif_button.configure(
            text='OK' if self.is_modifying.get() else 'Modifier')

        elements = [
            *self.species_radios,
            *[entry for _, entry in self.species_traits_entries.items()],
            self.foodRadio,
            self.nestRadio,
            self.foodOrNestAmountInput,
            self.sun_check
        ]
        self.opt_world_size.configure(state=tk.NORMAL if self.is_modifying.get(
        ) and self.new_world == 1 else tk.DISABLED)
        self.new_world = 0

        for element in elements:
            element.configure(
                state=tk.NORMAL if self.is_modifying.get() else tk.DISABLED)

    def on_modif_speed(self, *_):
        """
        Fonction qui récupère la vitesse du monde
        """
        self.world.speed_value = self.speed_value.get()

    def create_worlds_dropdown(self, parent):
        """
        Fonction qui permet de créer un menu d'options contenant les mondes prédéfinis
        """
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
            command=lambda filename: self.world.loadWorld(f"{filename}.json") if filename != 'Nouveau Monde' else [self.world.reset(), self.update_new_world_value()])

        loadWorldDrop.pack(side=tk.LEFT)

        button_save = tk.Button(
            parent,
            text="Sauvegarder",
            command=lambda: self.world.save_world())
        button_save.pack(side=tk.LEFT)

    def create_size_dropdown(self, parent):
        """
        Fonction qui permet de créer un menu d'options contenant les tailles du monde (non fonctionnel)
        """
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
        self.world_size.trace_add('write', self.update_world_size)

        label_size = tk.Label(parent, text="Taille monde:")
        label_size.config(width=15, font=("Helvetica", 16))
        label_size.pack(side=tk.LEFT, anchor=tk.NW)

        self.opt_world_size = tk.OptionMenu(
            parent, self.world_size, *OptionList)
        self.opt_world_size.config(
            width=15, font=(
                "Helvetica", 12), state=tk.DISABLED)
        self.opt_world_size.pack(side=tk.LEFT, anchor=tk.NW)

    def create_sun_check(self, parent):
        """
        Fonction qui permet de créer une checkbox pour le mode Soleil (non fonctionnel)
        """
        frame = tk.Frame(parent)
        self.sun_check = tk.Checkbutton(frame)
        self.sun_check.config(text="Mode Soleil", width=15, font=(
            "Helvetica", 12), state=tk.DISABLED)
        self.sun_check.pack(side=tk.LEFT)
        frame.pack(side=tk.BOTTOM, anchor=tk.SW)

    def update_world_size(self, *_):
        """
        Fonction qui permet de mettre à jour la taille du monde (non fonctionnelle)
        """
        # si le canvas est vide, on change la taille du monde
        if len(self.canvas.find_all()) == 2560:
            world_size = self.world_size.get()
            self.world.reset_grid(world_size, world_size)

    def create_frame_bottom(self):
        """
        Fonction qui crée la frame inférieure
        """
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

        button_about = tk.Button(frame, text="A propos", command=self.about)
        button_about.pack(side=tk.RIGHT)

        button_speed_add = tk.Button(
            frame,
            text="+",
            height=0,
            width=25,
            command=self.speed_add)
        button_speed_add.pack(side=tk.RIGHT)

        label_speed_update = tk.Label(frame, textvariable=self.speed_value)
        label_speed_update.config(width=20)
        label_speed_update.pack(side=tk.RIGHT)

        button_speed_minus = tk.Button(
            frame,
            text="-",
            height=0,
            width=25,
            command=self.speed_minus)
        button_speed_minus.pack(side=tk.RIGHT)

        label_speed = tk.Label(frame, text="Vitesse :")
        label_speed.config(width=15, height=1, font=("Helvetica, 14"))
        label_speed.pack(side=tk.RIGHT)

        self.label_time = tk.Label(frame)
        self.label_time.config(width=8, height=2)
        self.label_time.pack(side=tk.RIGHT)

        self.label_species_food = tk.Label(
            frame, textvariable=self.species_food)
        self.label_species_food.config(width=8, height=2)
        self.label_species_food.pack(side=tk.RIGHT)

        frame.pack(side="bottom", fill="both", padx=5, pady=5)

    def update_time(self):
        """
        Fonction permettant de mettre le temps à jour sur le label correspondant
        """
        self.label_time.config(text=int(self.world.time))

    def update_new_world_value(self):
        """
        Fonction qui vérifie si un nouveau monde a été créé
        """
        self.new_world = 1

    def update_species_food(self):
        """
        Fonction qui crée un label permettant de voir l'évolution de la répartition de la nourriture entre espèces
        """
        l = [species for species in self.world.species if species.active == True]
        res = ""
        for species in l:
            res += str(species.species_id + 1) + "-" + str(species.food) + " "
        self.species_food.set(res)

    def speed_minus(self):
        """
        Diminue la vitesse du monde
        """
        if 0.25 < self.speed_value.get() <= 2:
            self.speed_value.set(self.speed_value.get() - 0.25)
        else:
            return

    def speed_add(self):
        """
        Augmente la vitesse du monde
        """
        if 0.25 <= self.speed_value.get() < 2:
            self.speed_value.set(self.speed_value.get() + 0.25)
        else:
            return

    def start_stop(self):
        """
        Fonction qui lance ou stoppe le monde avec les widgets nécessaires
        """
        if self.world.paused or not self.world.started:
            self.is_modifying.set(False)
            self.world.start()
            self.update_time()
            self.on_modif_state_change()
            self.update_species_food()
            self.button_go["text"] = "Stop"
        else:
            self.world.pause()
            self.button_go["text"] = "Go =>"

    def step(self):
        """
        Fonction qui permet de regarder l'évolution frame par frame
        """
        self.world.next_frame()
        self.button_go["text"] = "Go =>"

    def spawn_wrong_value_popup(self, trait, min_val, max_val, value):
        """
        Cree un popup quand la taille d une ressource n est pas comprise entre sa valeur minimale et maximale
        """
        if self.wrong_value_popup_open:
            return

        self.wrong_value_popup_open = True

        win = tk.Toplevel()
        win.wm_title("Attention !")

        def close_win():
            win.destroy()
            self.wrong_value_popup_open = False

        if trait == "notint":
            l = tk.Label(
                win, text=f"Veuillez choisir une valeur entière")
            l.grid(column=0, row=0)
            b = tk.Button(win, text="Ok", command=close_win)
            b.grid(column=0, row=1)
            return

        l = tk.Label(
            win, text=f"Veuillez choisir une {trait} comprise entre {min_val} et {max_val}")
        l.grid(column=0, row=0)

        l = tk.Label(
            win, text=f"valeur entrée: {value}")
        l.grid(column=0, row=1)

        b = tk.Button(win, text="Ok", command=close_win)
        b.grid(column=0, row=2)

    def about(self):
        """
        Cree un popup qui decrit les possibilites de l application
        """
        win = tk.Toplevel()
        win.wm_title("***** A propos *****")
        liste = ["Bienvenue sur Ants Viewer !",
                 "",
                 " - Au lancement de l'application, vous pouvez charger un monde prédéfini à l'aide du",
                 "menu déroulant en haut à gauche. Vous pouvez également créer votre monde en modifiant ",
                 "le monde chargé au lancement ou en appuyant sur Nouveau Monde.",
                 "- Vous pouvez modifier la quantité de nourriture présente dans une ressource, la population",
                 "des nids, et vous pourrez également modifier les caractéristiques des fourmis de",
                 "l'espèce séléctionnée.",
                 "- Cependant, le nombre maximum de nids et de ressources est limité à 4",
                 "- Vous avez la possibilité de sauvegarder votre monde.",
                 "- Vous avez également la possibilité de poser des murs à l'aide du clic gauche de votre",
                 "souris, ce qui obligera les fourmis à trouver un chemin alternatif.",
                 "-Dans le menu en bas de la fenêtre, vous pouvez lancer la simulation ou la stopper lorsque",
                 "celle-ci a déjà été lancée. Un mode pas à pas est également disponible.",
                 "-La vitesse de la simulation peut etre modifiée, allant de x 0.25 à x 2.0",
                 "- Vous pouvez changer les différentes statistiques des fourmis",
                 "",
                 "! Certaines valeurs ne seront pas prises en compte :",
                 "! Retour, Suivi phero., Dépot Phéro., Freq. alea. .",
                 "! Il n'est pas encore possible de changer la taille de votre monde.",
                 "! Le mode Soleil n'est pas encore disponible."
                 ]
        for i in range(len(liste)):
            tk.Label(win, text=liste[i]).pack(side=tk.TOP, anchor=tk.W)

        b = tk.Button(win, text="Ok", command=win.destroy)
        b.pack(side=tk.BOTTOM)

        win.geometry(("%dx%d%+d%+d" % (500, 500, 750, 400)))
