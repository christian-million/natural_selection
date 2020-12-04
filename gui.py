import tkinter as tk
import keyring
import requests

WEBHOOK_URL = keyring.get_password("NSBOT", "webhook")


def send():
    content = f"N Agents: {var_n_agents.get()}\nN Food: {var_n_food.get()}\nN Days: {var_n_days.get()}\nN Steps: {var_n_steps.get()}"
    data = {"username": "Christian Million",
            "content": content}
    requests.post(WEBHOOK_URL, data=data)


window = tk.Tk()
window.geometry("720x720")
window.resizable(False, False)
window.title("Natural Selection Simulator")
icon = tk.PhotoImage(file='images/logo.png')
window.iconphoto(True, icon)


# n_agents, n_food, n_days, n_steps
var_n_agents = tk.StringVar()
lbl_n_agents = tk.Label(window, text="N Agents:")
txt_n_agents = tk.Entry(window, textvariable=var_n_agents)
lbl_n_agents.pack()
txt_n_agents.pack()

var_n_food = tk.StringVar()
lbl_n_food = tk.Label(window, text="N Food:")
txt_n_food = tk.Entry(window, textvariable=var_n_food)
lbl_n_food.pack()
txt_n_food.pack()

var_n_days = tk.StringVar()
lbl_n_days = tk.Label(window, text="N Days:")
txt_n_days = tk.Entry(window, textvariable=var_n_days)
lbl_n_days.pack()
txt_n_days.pack()

var_n_steps = tk.StringVar()
lbl_n_steps = tk.Label(window, text="N Steps:")
txt_n_steps = tk.Entry(window, textvariable=var_n_steps)
lbl_n_steps.pack()
txt_n_steps.pack()

btn = tk.Button(window, text="Run Simulation", command=send)
btn.pack()

window.mainloop()
