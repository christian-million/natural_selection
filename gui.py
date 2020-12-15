import tkinter as tk
import keyring
import requests
from model import Model
from json import load, dumps
from csv import writer
import subprocess
from imgurpython import ImgurClient
import time

WEBHOOK_URL = keyring.get_password("NSBOT", "webhook")
IMG_CLIENT_ID = keyring.get_password("NSBOT", "imgur")
IMG_SECRET = keyring.get_password("NSBOT", "imgur_secret")


class Settings(tk.LabelFrame):
    '''Container to hold the main settings.'''
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # N Agents
        lbl_n_agent = tk.Label(self, text="# of Starting Agents")
        lbl_n_agent.grid(row=0, column=0, sticky='w')
        self.n_agent = tk.Scale(self, from_=1, to=50, orient=tk.HORIZONTAL)
        self.n_agent.grid(row=1, column=0, sticky='w')

        # N Food
        lbl_n_food = tk.Label(self, text="Daily Food")
        lbl_n_food.grid(row=0, column=1, sticky='w')
        self.n_food = tk.Scale(self, from_=1, to=200, orient=tk.HORIZONTAL)
        self.n_food.grid(row=1, column=1, sticky='w')

        # N Days
        lbl_n_days = tk.Label(self, text="# of Days")
        lbl_n_days.grid(row=0, column=2, sticky='w')
        self.n_days = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        self.n_days.grid(row=1, column=2, sticky='w')

        # N Steps
        lbl_day_steps = tk.Label(self, text="# Steps per Day")
        lbl_day_steps.grid(row=0, column=3, sticky='w')
        self.day_steps = tk.Scale(self, from_=50, to=150, orient=tk.HORIZONTAL)
        self.day_steps.grid(row=1, column=3, sticky='w')

        self.reset()

    def get(self):
        '''Captures the current state of all widgets'''
        self.parent.params["N_AGENTS"] = self.n_agent.get()
        self.parent.params["N_FOOD"] = self.n_food.get()
        self.parent.params["N_DAYS"] = self.n_days.get()
        self.parent.params["DAILY_STEPS"] = self.day_steps.get()

    def reset(self):
        '''Resets the value of each widget to default paramters'''
        self.n_agent.set(self.parent.defaults["N_AGENTS"])
        self.n_food.set(self.parent.defaults["N_FOOD"])
        self.n_days.set(self.parent.defaults["N_DAYS"])
        self.day_steps.set(self.parent.defaults["DAILY_STEPS"])


class Mutations(tk.LabelFrame):
    '''Mutation related widgets'''
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initial Attribute Value Column
        lbl_init = tk.Label(self, text="Starting Value")
        lbl_init.grid(row=0, column=0)

        self.init_speed = tk.Scale(self, from_=1, to=3, orient=tk.HORIZONTAL)
        self.init_speed.grid(row=1, column=0, sticky='w')

        self.init_size = tk.Scale(self, from_=1, to=3, orient=tk.HORIZONTAL)
        self.init_size.grid(row=2, column=0, sticky='w')

        self.init_sense = tk.Scale(self, from_=3, to=7, orient=tk.HORIZONTAL)
        self.init_sense.grid(row=3, column=0, sticky='w')

        # Allow Mutations Column
        lbl_allow = tk.Label(self, text="Allow Mutations")
        lbl_allow.grid(row=0, column=1, sticky='w')

        self.var_chk_speed_allow = tk.BooleanVar(self)
        self.chk_speed_allow = tk.Checkbutton(self, text="Speed", variable=self.var_chk_speed_allow)
        self.chk_speed_allow.grid(row=1, column=1, sticky='w')

        self.var_chk_size_allow = tk.BooleanVar(self)
        self.chk_size_allow = tk.Checkbutton(self, text="Size", variable=self.var_chk_size_allow)
        self.chk_size_allow.grid(row=2, column=1, sticky='w')

        self.var_chk_sense_allow = tk.BooleanVar(self)
        self.chk_sense_allow = tk.Checkbutton(self, text="Sense", variable=self.var_chk_sense_allow)
        self.chk_sense_allow.grid(row=3, column=1, sticky='w')

        # Attribute Modifier Column
        lbl_mod = tk.Label(self, text="Attribute Modifier (%)")
        lbl_mod.grid(row=0, column=2)

        self.speed_mod = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.speed_mod.grid(row=1, column=2, sticky='w')

        self.size_mod = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.size_mod.grid(row=2, column=2, sticky='w')

        self.sense_mod = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.sense_mod.grid(row=3, column=2, sticky='w')

        # Mutation Rate
        lbl_mutate_rate = tk.Label(self, text="Chance of Mutation (%)")
        lbl_mutate_rate.grid(row=4, column=0)

        self.mutate_rate = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.mutate_rate.grid(row=4, column=1, columnspan=2, sticky='w')

        # Reproduction Modifier
        lbl_rep_mod = tk.Label(self, text="Reproduction Mod (%)")
        lbl_rep_mod.grid(row=5, column=0)

        self.rep_mod = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.rep_mod.grid(row=5, column=1, columnspan=2, sticky='w')

        # Set Defaults
        self.reset()

    def get(self):
        '''Captures the current state of all widgets'''
        self.parent.params["SPEED"] = self.init_speed.get()
        self.parent.params["SIZE"] = self.init_size.get()
        self.parent.params["SENSE"] = self.init_sense.get()
        self.parent.params["SPEED_ALLOW"] = self.var_chk_speed_allow.get()
        self.parent.params["SIZE_ALLOW"] = self.var_chk_size_allow.get()
        self.parent.params["SENSE_ALLOW"] = self.var_chk_sense_allow.get()
        self.parent.params["SPEED_MOD"] = self.speed_mod.get() / 100
        self.parent.params["SIZE_MOD"] = self.size_mod.get() / 100
        self.parent.params["SENSE_MOD"] = self.sense_mod.get() / 100
        self.parent.params["MUTATION_RATE"] = self.mutate_rate.get() / 100
        self.parent.params["REPRODUCTION_MOD"] = self.rep_mod.get() / 100

    def reset(self):
        '''Resets the value of each widget to default paramters'''
        self.init_speed.set(self.parent.defaults["SPEED"])
        self.init_size.set(self.parent.defaults["SIZE"])
        self.init_sense.set(self.parent.defaults["SENSE"])
        self.var_chk_speed_allow.set(self.parent.defaults["SPEED_ALLOW"])
        self.var_chk_size_allow.set(self.parent.defaults["SIZE_ALLOW"])
        self.var_chk_sense_allow.set(self.parent.defaults["SENSE_ALLOW"])
        self.speed_mod.set(self.parent.defaults["SPEED_MOD"]*100)
        self.size_mod.set(self.parent.defaults["SIZE_MOD"]*100)
        self.sense_mod.set(self.parent.defaults["SENSE_MOD"]*100)
        self.mutate_rate.set(self.parent.defaults["MUTATION_RATE"]*100)
        self.rep_mod.set(self.parent.defaults["REPRODUCTION_MOD"]*100)


class Env(tk.LabelFrame):
    '''Environment Attributes'''
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # PREDATOR RATIO
        lbl_pred_ratio = tk.Label(self, text="Predator Ratio (%)")
        lbl_pred_ratio.grid(row=0, column=0, sticky='w')
        self.pred_ratio = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.pred_ratio.grid(row=0, column=1, sticky='w')

        # FOOD SIZE
        lbl_food_size = tk.Label(self, text="Food Size")
        lbl_food_size.grid(row=1, column=0, sticky='w')
        self.food_size = tk.Scale(self, from_=1, to=3, orient=tk.HORIZONTAL)
        self.food_size.grid(row=1, column=1, sticky='w')

        # FOOD VALUE
        lbl_food_value = tk.Label(self, text="Food Value")
        lbl_food_value.grid(row=2, column=0, sticky='w')
        self.food_value = tk.Scale(self, from_=500, to=1500, orient=tk.HORIZONTAL)
        self.food_value.grid(row=2, column=1, sticky='w')

        # EAT DISTANCE
        lbl_eat_dist = tk.Label(self, text="Eat Distance")
        lbl_eat_dist.grid(row=3, column=0, sticky='w')
        self.eat_dist = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL)
        self.eat_dist.grid(row=3, column=1, sticky='w')

        # ENVIRONMENT HEIGHT
        lbl_height = tk.Label(self, text="Env. Length")
        lbl_height.grid(row=4, column=0, sticky='w')
        self.height = tk.Scale(self, from_=50, to=150, orient=tk.HORIZONTAL)
        self.height.grid(row=4, column=1, sticky='w')

        # ENVIRONMENT WIDTH
        lbl_width = tk.Label(self, text="Env. Width")
        lbl_width.grid(row=5, column=0, sticky='w')
        self.width = tk.Scale(self, from_=50, to=150, orient=tk.HORIZONTAL)
        self.width.grid(row=5, column=1, sticky='w')

        # HEADING MOD
        lbl_head_mod = tk.Label(self, text="Heading Modifier")
        lbl_head_mod.grid(row=6, column=0, sticky='w')
        self.head_mod = tk.Scale(self, from_=15, to=60, orient=tk.HORIZONTAL)
        self.head_mod.grid(row=6, column=1, sticky='w')

        # STEP BUFFER
        lbl_step = tk.Label(self, text="Step Buffer")
        lbl_step.grid(row=7, column=0, sticky='w')
        self.step = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL)
        self.step.grid(row=7, column=1, sticky='w')

        # Set Defaults
        self.reset()

    def get(self):
        '''Captures the current state of all widgets'''
        self.parent.params["PREDATOR_RATIO"] = self.pred_ratio.get()/100
        self.parent.params["FOOD_SIZE"] = self.food_size.get()
        self.parent.params["FOOD_VALUE"] = self.food_value.get()
        self.parent.params["EAT_DIST"] = self.eat_dist.get()
        self.parent.params["HEIGHT"] = self.height.get()
        self.parent.params["WIDTH"] = self.width.get()
        self.parent.params["HEADING_MOD"] = self.head_mod.get()
        self.parent.params["STEP_BUFFER"] = self.step.get()

    def reset(self):
        '''Resets the value of each widget to default paramters'''
        self.pred_ratio.set(self.parent.defaults["PREDATOR_RATIO"]*100)
        self.food_size.set(self.parent.defaults["FOOD_SIZE"])
        self.food_value.set(self.parent.defaults["FOOD_VALUE"])
        self.eat_dist.set(self.parent.defaults["EAT_DIST"])
        self.height.set(self.parent.defaults["HEIGHT"])
        self.width.set(self.parent.defaults["WIDTH"])
        self.head_mod.set(self.parent.defaults["HEADING_MOD"])
        self.step.set(self.parent.defaults["STEP_BUFFER"])


class Application(tk.Tk):
    '''Main Tkinter Window Controller'''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        with open('defaults.json') as f:
            defaults = load(f)
            self.defaults = {key: value.get("value") for key, value in defaults.items()}

        self.params = self.defaults.copy()

        btn_submit = tk.Button(self, text="Run Model", command=self.run_model)
        btn_submit.pack(side=tk.TOP)

        btn_reset = tk.Button(self, text="Reset Parameters", command=self.reset_params)
        btn_reset.pack(side=tk.TOP)

        self.settings = Settings(self, text="Model Settings")
        self.settings.pack(side=tk.TOP, fill=tk.BOTH)

        self.env = Env(self, text="Environment")
        self.env.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.mutations = Mutations(self, text="Mutations / Attributes")
        self.mutations.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def get_params(self):
        self.settings.get()
        self.env.get()
        self.mutations.get()

        print(self.params)

    def reset_params(self):
        '''Sets all parameters to default values'''
        self.params = self.defaults.copy()
        self.settings.reset()
        self.env.reset()
        self.mutations.reset()

    def run_model(self):
        '''Runs the Natural Selection Simulator'''
        self.get_params()
        self.model = Model(self.params)

        # Run and Time the Model
        start_time = time.time()
        self.model.run()
        print(f"Model took {(time.time() - start_time)} seconds.")

        with open("pop.csv", 'w', newline='') as f:
            r = writer(f)
            r.writerows(self.model.pop_sum)

        # Run the Rscript that populates the graph
        subprocess.run(["C:/Program Files/R/R-3.5.3/bin/Rscript.exe", 'show_pop.R'])

        link = self.upload_img("images/model_results.png")

        self.send(link)

    def upload_img(self, path):
        '''Uploads image anonymously to imgur and returns the resulting weblink'''
        client = ImgurClient(IMG_CLIENT_ID, IMG_SECRET)
        resp = client.upload_from_path(path)

        return resp["link"]

    def send(self, link):
        '''Sends an embedded link to Natural Selection Discord Channel'''
        data = {"username": "Natural Simulation Results",
                "content": "Results",
                "embeds": [{"image": {"url": link}}]}

        requests.post(WEBHOOK_URL, data=dumps(data), headers={"Content-Type": "application/json"})


if __name__ == '__main__':

    app = Application()
    app.geometry("600x500")
    app.resizable(False, False)
    app.title("Natural Selection Simulator")
    icon = tk.PhotoImage(file='images/logo.png')
    app.iconphoto(True, icon)
    app.mainloop()
