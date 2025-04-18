import pandas as pd
import numpy as np
import tkinter as tkint
from tkinter import ttk
from PIL import ImageTk

pokedata = pd.read_csv("pokedata.csv", index_col = 0)

stat_list = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defence', 'speed']

def scale_statistic(x):
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
    
    pokedata_entry_string = ". ".join(pokedata[pokedata.name == selected]["pokedata_entry"].values[0].split(". ")[:4])
    
    if pokedata_entry_string[-1] != "." and pokedata_entry_string[-1] != "!":
        pokedata_entry_string += "."
    
    pokedata_entry["text"] = pokedata_entry_string
    
    height_label["text"] = "Height:\n" + str(pokedata[pokedata.name == selected]["height"].values[0]) + " m"
    weight_label["text"] = "Weight:\n" + str(pokedata[pokedata.name == selected]["weight"].values[0]) + " kg"

    if pokedata[pokedata.name == selected]["catch_rate"].isna().all():
        catch_rate_label["text"] = "Catch Rate:\nNo known data"
    else:
        catch_rate_label["text"] = "Catch Rate:\n" + str(pokedata[pokedata.name == selected]["catch_rate"].values[0]) + "%\nwith Pokeball"
    label_image = ImageTk.PhotoImage(file = f"Pokemon Pictures/{pokedata[pokedata.name == selected].index[0] + 1}.png")
    label_image = ImageTk.PhotoImage(file = f"Pokemon Pictures/{pokedata[pokedata.name == selected].index[0] + 1}.png")
    picture_label.config(image = label_image)
    picture_label.image = label_image
    
    type_one_label["image"] = type_dict[pokedata[pokedata.name == selected]["type1"].values[0]]
    
    if pokedata[pokedata.name == selected]["type2"].values[0] == "none":
        type_two_label.grid_forget()
    else:
        type_two_label["image"] = type_dict[pokedata[pokedata.name == selected]["type2"].values[0]]
        type_two_label.grid(row = 0, column = 1)
        
    for widget in stat_frame.winfo_children():
        widget.destroy()
    
    stat_canvas = tkint.Canvas(stat_frame, height = 100, width = 275, bg = "white", borderwidth = 0, highlightthickness = 0)
    stat_canvas.grid(row = 0, rowspan = 6, column = 2, sticky = "nsew")
    
    start_x1 = 0
    start_y1 = 7
    start_x2 = 250
    start_y2 = 27
    bar_height = 20
    bar_step = 13

    for row, stat in enumerate(stat_list):
        stat_value = pokedata[pokedata.name == selected][stat_list[row]].values[0]
        
        text_box = tkint.Label(stat_frame, text = stat + f" {stat_value}", font = ("Futura", 12), anchor = "w", bg = "white", justify = tkint.LEFT, borderwidth = 0)
        text_box.grid(row = row, column = 0, sticky = "nsw")
        
        if stat_value <= 50:
            fill = "red"
        elif 51 <= stat_value < 70:
            fill = "orange"
        elif 70 <= stat_value < 90:
            fill = "yellow"
        else:
            fill = "green"
        
        stat_canvas.create_rectangle(start_x1, start_y1, scale_statistic(stat_value), start_y2, fill = fill)
        
        start_y1 = start_y2 + bar_step
        start_y2 = start_y1 + bar_height

window = tkint.Tk()

window.title("Pokedex")
window.geometry("1200x700")
window.configure(background = "crimson")

type_list = ['grass', 'fire', 'water', 'bug', 'normal', 'dark', 'poison',
       'electric', 'ground', 'ice', 'fairy', 'steel', 'fighting',
       'psychic', 'rock', 'ghost', 'dragon', 'flying']

type_dict = {i: tkint.PhotoImage(file = f"Type Pictures/{i.capitalize()}.png") for i in type_list}

window.rowconfigure(0, weight = 0, pad = 20)
window.rowconfigure([i for i in range(1,4)], weight = 1)
window.columnconfigure([i for i in range(3)], minsize = 50, weight = 1)

name_frame = tkint.Frame(window, relief = tkint.RAISED, borderwidth = 4, bg = "blue1")
pokemon_name_label = tkint.Label(name_frame, 
                      height = 2,
                      text = "Pokemon Name Here", 
                      fg = "yellow",
                      bg = "blue1",
                      font = ("Futura", 16, "bold"))
pokemon_name_label.pack()
name_frame.grid(row = 0, column = 0, padx = 10, sticky = "ew")

picture_frame = tkint.Frame(window, 
                         relief = tkint.SUNKEN, 
                         borderwidth = 2, 
                         height = 400,
                         width = 400,
                         bg = "white")

picture_frame.rowconfigure(0, weight = 1)
picture_frame.columnconfigure(0, weight = 1)

picture_label = tkint.Label(picture_frame, bg = "white")
picture_label.grid(row = 0, column = 0, sticky = "nsew")

picture_frame.grid(row = 1, column = 0, rowspan = 2, sticky = "nsew", padx = 10)
picture_frame.grid_propagate(False)

type_frame = tkint.Frame(window, relief = tkint.RAISED, borderwidth = 2)
type_one_label = tkint.Label(type_frame, text = "Type 1 Here", font = ("Futura", 16))
type_one_label.grid(row = 0, column = 0)
type_two_label = tkint.Label(type_frame, text = "Type 2 Here", font = ("Futura", 16))
type_two_label.grid(row = 0, column = 1)
type_frame.grid(row = 3, column = 0)

info_frame = tkint.Frame(window, relief = tkint.SUNKEN, borderwidth = 4)

info_frame.rowconfigure([0,1,2], weight = 2, minsize = 200)
info_frame.columnconfigure([0,1], weight = 1, minsize = 300)

pokedex_entry = tkint.Label(info_frame, text = "Pokedex Entry", font = ("Futura", 16),
                         wraplength = 700, anchor = "w", bg = "black", fg = "light blue",
                         justify=tkint.LEFT)
pokedex_entry.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")

pokedata_entry = tkint.Label(info_frame, text = "", font = ("Futura", 16),
                         wraplength = 700, anchor = "w", bg = "white", fg = "black",
                         justify=tkint.LEFT)
pokedata_entry.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")

height_label = tkint.Label(info_frame, text = "Height", font = ("Futura", 16), borderwidth = 2,
                       relief = tkint.RIDGE, bg = "white")
height_label.grid(row = 1, column = 0, sticky = "nsew")

weight_label = tkint.Label(info_frame, text = "Weight", font = ("Futura", 16), borderwidth = 2,
                       relief = tkint.RIDGE, bg = "white")
weight_label.grid(row = 1, column = 1, sticky = "nsew")

catch_rate_label = tkint.Label(info_frame, text = "Catch Rate", font = ("Futura", 16), borderwidth = 2,
                      relief = tkint.RIDGE, bg = "white")
catch_rate_label.grid(row = 2, column = 1, sticky = "nsew")

stat_frame = tkint.Frame(info_frame, borderwidth = 2, relief = tkint.RIDGE, bg = "white")

stat_frame.rowconfigure([i for i in range(6)], weight = 1)
stat_frame.columnconfigure(1, weight = 1)

stat_labels = ["HP:", "ATK:", "DEF:", "SPA:", "SPD:", "SPE:"]

stat_canvas = tkint.Canvas(stat_frame, height = 100, width = 275, bg = "white", 
                     borderwidth = 0, highlightthickness = 0)

stat_canvas.grid(row = 0, rowspan = 6, column = 2, sticky = "nsew")

start_x1 = 0
start_y1 = 7
start_x2 = 250
start_y2 = 27
bar_height = 20
bar_step = 13

for row, stat in enumerate(stat_labels):
    text_box = tkint.Label(stat_frame, 
                        text = stat,
                        font = ("Futura", 12),
                        anchor = "w",
                        bg = "white",
                        justify = tkint.LEFT,
                        borderwidth = 0)
    text_box.grid(row = row, column = 0, sticky = "nsw")

    stat_canvas.create_rectangle(start_x1, start_y1, start_x2, start_y2, fill = "green")
    
    start_y1 = start_y2 + bar_step
    start_y2 = start_y1 + bar_height
    
stat_frame.grid(row = 2, column = 0, sticky = "nsew")

info_frame.grid(row = 1, rowspan = 3, column = 1, columnspan = 2, sticky = "nsew")

info_frame.grid_propagate(False)

search_frame = tkint.Frame(window, relief = tkint.RAISED, borderwidth = 3, bg = "light blue")

search_frame.columnconfigure([0,1,2,3,4], weight = 1)
search_frame.rowconfigure(0, weight = 1, minsize = 55)

left_button = tkint.Button(search_frame, text = "Previous", font = ("Futura", 16), 
                        command = lambda: select_pokemon(move = "backward"))
left_button.grid(row = 0, column = 0, sticky = "ew")

submit_button = tkint.Button(search_frame, text = "Search!", font = ("Futura", 14), 
                          command = select_pokemon)
submit_button.grid(row = 0, column = 3)

right_button = tkint.Button(search_frame, text = "  Next  ", font = ("Futura", 16),
                         command = lambda: select_pokemon(move = "forward"))
right_button.grid(row = 0, column = 4, sticky = "ew")

def search_pokemon():
    current_text = pokemon_search_box.get()
    if current_text == "" or current_text in pokedata.name.tolist():
        pokemon_search_box.config(values = pokedata.name.tolist())
    else:
        values = []
        for name in pokedata.name.tolist():
            if current_text.lower() in name.lower():
                values.append(name)
        pokemon_search_box.config(values = values)
    
