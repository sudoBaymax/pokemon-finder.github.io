import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image

pokedex = pd.read_csv("pokedata.csv", index_col = 0)

stat_list = ['hp', 'attack', 'defence', 'sp_attack', 'sp_defence', 'speed']

def scale_stat(x):
    start_x1 = 250
    start_x2 = 1
    min_x = 20
    max_x = 150
    if x < min_x:
        x = min_x
    elif x > max_x:
        x = max_x
    return round((start_x1 - start_x2)*((x - min_x) / (max_x - min_x)) + start_x2)

def select_pokemon(move = None):
    try:
        if move == 'forward':
            pokemon_search_box.current(pokemon_search_box.current() + 1)
            selected = pokemon_search_box.get()
        elif move == 'backward':
            pokemon_search_box.current(pokemon_search_box.current() - 1)
            selected = pokemon_search_box.get()
        else:
            selected = pokemon_search_box.get()
    except Exception as e:
        print(e)
        selected = pokemon_search_box.get()

    pokemon_name_label["text"] = "\n".join(selected.split(" - "))

    pokedex_entry_string = ". ".join(pokedex[pokedex.name == \
                              selected]["pokedex_entry"].values[0].split(". ")[:4])
    if pokedex_entry_string[-1] != "." and pokedex_entry_string[-1] != "!":
        pokedex_entry_string += "."
    pokedex_entry["text"] = pokedex_entry_string

    height_label["text"] = "Height:\n" + str(pokedex[pokedex.name == \
                                             selected]["height"].values[0]) + " m"
    weight_label["text"] = "Weight:\n" + str(pokedex[pokedex.name == \
                                             selected]["weight"].values[0]) + " kg"

    if pokedex[pokedex.name == selected]["catch_rate"].isna().all():
        catch_rate_label["text"] = "Catch Rate:\nNo known data"
    else:
        catch_rate_label["text"] = "Catch Rate:\n" + str(pokedex[pokedex.name == \
                                                selected]["catch_rate"].values[0]) \
                                                + "%\nwith Pokeball"

    label_image = ImageTk.PhotoImage(file = \
                 f"Pokemon Pictures/{pokedex[pokedex.name == selected].index[0] + 1}.png")
    picture_label.config(image = label_image)
    picture_label.image = label_image

    type_one_label["image"] = type_dict[pokedex[pokedex.name == selected]["type1"].values[0]]

    if pokedex[pokedex.name == selected]["type2"].values[0] == "none":
        type2label.grid_forget()
    else:
        type2label["image"] = type_dict[pokedex[pokedex.name == selected]["type2"].values[0]]
        type2label.grid(row = 0, column = 1)

    for widget in stat_frame.winfo_children():
        widget.destroy()

    draw_box = tk.Canvas(stat_frame, height = 100, width = 275, bg = "white", 
                     borderwidth = 0, highlightthickness = 0)
    draw_box.grid(row = 0, rowspan = 6, column = 2, sticky = "nsew")

    start_x1 = 0
    start_y1 = 7
    start_x2 = 250
    start_y2 = 27
    bar_height = 20
    bar_step = 13

    for row, stat in enumerate(stat_labels):
        stat_value = pokedex[pokedex.name == selected][stat_list[row]].values[0]
        text_box = tk.Label(stat_frame, 
                            text = stat + f" {stat_value}",
                            font = ("Futura", 12),
                            anchor = "w",
                            bg = "white",
                            justify = tk.LEFT,
                            borderwidth = 0)
        text_box.grid(row = row, column = 0, sticky = "nsw")

        if stat_value <= 50:
            fill = "red"
        elif 51 <= stat_value < 70:
            fill = "orange"
        elif 70 <= stat_value < 90:
            fill = "yellow"
        else:
            fill = "green"

        draw_box.create_rectangle(start_x1, 
                                  start_y1, 
                                  scale_stat(stat_value),
                                  start_y2, 
                                  fill = fill)

        start_y1 = start_y2 + bar_step
        start_y2 = start_y1 + bar_height

window = tk.Tk()
window.title("Pokedex")
window.geometry("1200x700")
window.configure(background = "crimson")

type_list = ['grass', 'fire', 'water', 'bug', 'normal', 'dark', 'poison',
       'electric', 'ground', 'ice', 'fairy', 'steel', 'fighting',
       'psychic', 'rock', 'ghost', 'dragon', 'flying']
type_dict = {i: ImageTk.PhotoImage(file = f"Type Pictures/{i.capitalize()}.png") for i in type_list}

window.rowconfigure(0, weight = 0, pad = 20)
window.rowconfigure([i for i in range(1,4)], weight = 1)
window.columnconfigure([i for i in range(3)], minsize = 50, weight = 1)

name_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 4, bg = "blue1")
pokemon_name_label = tk.Label(name_frame, 
                      height = 2,
                      text = "Pokemon Name Here", 
                      fg = "yellow",
                      bg = "blue1",
                      font = ("Futura", 16, "bold"))
pokemon_name_label.pack()
name_frame.grid(row = 0, column = 0, padx = 10, sticky = "ew")

picture_frame = tk.Frame(window, 
                         relief = tk.SUNKEN, 
                         borderwidth = 2, 
                         height = 400,
                         width = 400,
                         bg = "white")

picture_frame.rowconfigure(0, weight = 1)
picture_frame.columnconfigure(0, weight = 1)

picture_label = tk.Label(picture_frame, bg = "white")
picture_label.grid(row = 0, column = 0, sticky = "nsew")

picture_frame.grid(row = 1, column = 0, rowspan = 2, sticky = "nsew", padx = 10)
picture_frame.grid_propagate(False)

type_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 2)
type_one_label = tk.Label(type_frame, text = "Type 1 Here", font = ("Futura", 16))
type_one_label.grid(row = 0, column = 0)
type2label = tk.Label(type_frame, text = "Type 2 Here", font = ("Futura", 16))
type2label.grid(row = 0, column = 1)
type_frame.grid(row = 3, column = 0)

info_frame = tk.Frame(window, relief = tk.SUNKEN, borderwidth = 4)
info_frame.rowconfigure([0,1,2], weight = 2, minsize = 200)
info_frame.columnconfigure([0,1], weight = 1, minsize = 300)

pokedex_entry = tk.Label(info_frame, text = "Pokedex Entry", font = ("Futura", 16),
                         wraplength = 700, anchor = "w", bg = "black", fg = "light blue",
                         justify=tk.LEFT)
pokedex_entry.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")

height_label = tk.Label(info_frame, text = "Height", font = ("Futura", 16), borderwidth = 2,
                       relief = tk.RIDGE, bg = "white")
height_label.grid(row = 1, column = 0, sticky = "nsew")

weight_label = tk.Label(info_frame, text = "Weight", font = ("Futura", 16), borderwidth = 2,
                       relief = tk.RIDGE, bg = "white")
weight_label.grid(row = 1, column = 1, sticky = "nsew")

catch_rate_label = tk.Label(info_frame, text = "Catch Rate", font = ("Futura", 16), borderwidth = 2,
                      relief = tk.RIDGE, bg = "white")
catch_rate_label.grid(row = 2, column = 1, sticky = "nsew")

stat_frame = tk.Frame(info_frame, borderwidth = 2, relief = tk.RIDGE, bg = "white")

stat_frame.rowconfigure([i for i in range(6)], weight = 1)
stat_frame.columnconfigure(1, weight = 1)

stat_labels = ["HP:", "ATK:", "DEF:", "SPA:", "SPD:", "SPE:"]

draw_box = tk.Canvas(stat_frame, height = 100, width = 275, bg = "white", 
                     borderwidth = 0, highlightthickness = 0)

draw_box.grid(row = 0, rowspan = 6, column = 2, sticky = "nsew")

start_x1 = 0
start_y1 = 7
start_x2 = 250
start_y2 = 27
bar_height = 20
bar_step = 13

for row, stat in enumerate(stat_labels):
    text_box = tk.Label(stat_frame, 
                        text = stat,
                        font = ("Futura", 12),
                        anchor = "w",
                        bg = "white",
                        justify = tk.LEFT,
                        borderwidth = 0)
    text_box.grid(row = row, column = 0, sticky = "nsw")

    draw_box.create_rectangle(start_x1, start_y1, start_x2, start_y2, fill = "green")
    start_y1 = start_y2 + bar_step
    start_y2 = start_y1 + bar_height

stat_frame.grid(row = 2, column = 0, sticky = "nsew")

info_frame.grid(row = 1, rowspan = 3, column = 1, columnspan = 2, sticky = "nsew")
info_frame.grid_propagate(False)

search_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 3, bg = "light blue")
search_frame.columnconfigure([0,1,2,3,4], weight = 1)
search_frame.rowconfigure(0, weight = 1, minsize = 55)

left_button = tk.Button(search_frame, text = "Previous", font = ("Futura", 16), 
                        command = lambda: select_pokemon(move = "backward"))
left_button.grid(row = 0, column = 0, sticky = "ew")

submit_button = tk.Button(search_frame, text = "Search!", font = ("Futura", 14), 
                          command = select_pokemon)
submit_button.grid(row = 0, column = 3)

right_button = tk.Button(search_frame, text = "  Next  ", font = ("Futura", 16),
                         command = lambda: select_pokemon(move = "forward"))
right_button.grid(row = 0, column = 4, sticky = "ew")

def search_pokemon():
    current_text = pokemon_search_box.get()
    if current_text == "" or current_text in pokedex.name.tolist():
        pokemon_search_box.config(values = pokedex.name.tolist())
    else:
        values = []
        for name in pokedex.name.tolist():
            if current_text.lower() in name.lower():
                values.append(name)
        pokemon_search_box.config(values = values)

pokemon_search_box = ttk.Combobox(search_frame, 
                          values = pokedex.name.tolist(),
                          font = ("Futura", 16), 
                          postcommand = search_pokemon)
pokemon_search_box.grid(row = 0, column = 1, columnspan = 2, sticky = "nsew", pady = 5, padx = 10)

search_frame.grid(row = 0, column = 1, columnspan = 2, sticky = "ew")

window.mainloop()