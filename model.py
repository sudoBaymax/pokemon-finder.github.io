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

