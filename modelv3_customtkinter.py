import pandas as pd
import numpy as np
import customtkinter as ctk
from PIL import ImageTk, Image

pokedex = pd.read_csv("pokedata.csv", index_col=0)

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

def select_pokemon(move=None):
    try:
        if move == 'forward':
            pokemon_search_box.set(pokemon_search_box.get()[pokemon_search_box.current() + 1])
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

    pokemon_name_label.configure(text="\n".join(selected.split(" - ")))

    pokedex_entry_string = ". ".join(pokedex[pokedex.name == \
                              selected]["pokedex_entry"].values[0].split(". ")[:4])
    if pokedex_entry_string[-1] != "." and pokedex_entry_string[-1] != "!":
        pokedex_entry_string += "."
    pokedex_entry.configure(text=pokedex_entry_string)

    height_label.configure(text="Height:\n" + str(pokedex[pokedex.name == \
                                             selected]["height"].values[0]) + " m")
    weight_label.configure(text="Weight:\n" + str(pokedex[pokedex.name == \
                                             selected]["weight"].values[0]) + " kg")

    if pokedex[pokedex.name == selected]["catch_rate"].isna().all():
        catch_rate_label.configure(text="Catch Rate:\nNo known data")
    else:
        catch_rate_label.configure(text="Catch Rate:\n" + str(pokedex[pokedex.name == \
                                                selected]["catch_rate"].values[0]) \
                                                + "%\nwith Pokeball")

    label_image = ImageTk.PhotoImage(file = \
                 f"Pokemon Pictures/{pokedex[pokedex.name == selected].index[0] + 1}.png")
    picture_label.configure(image=label_image)
    picture_label.image = label_image

    type_one_label.configure(image=type_dict[pokedex[pokedex.name == selected]["type1"].values[0]])

    if pokedex[pokedex.name == selected]["type2"].values[0] == "none":
        type2label.grid_remove()
    else:
        type2label.configure(image=type_dict[pokedex[pokedex.name == selected]["type2"].values[0]])
        type2label.grid(row=0, column=1)

    for widget in stat_frame.winfo_children():
        widget.destroy()

    draw_box = ctk.CTkCanvas(stat_frame, height=100, width=275, bg="white", 
                     borderwidth=0, highlightthickness=0)
    draw_box.grid(row=0, rowspan=6, column=2, sticky="nsew")

    start_x1 = 0
    start_y1 = 7
    start_x2 = 250
    start_y2 = 27
    bar_height = 20
    bar_step = 13

    for row, stat in enumerate(stat_labels):
        stat_value = pokedex[pokedex.name == selected][stat_list[row]].values[0]
        text_box = ctk.CTkLabel(stat_frame, 
                            text=stat + f" {stat_value}",
                            font=ctk.CTkFont(size=12, family="Futura"),
                            anchor="w",
                            fg_color="transparent",
                            justify="left")
        text_box.grid(row=row, column=0, sticky="nsw")

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
                                  fill=fill)

        start_y1 = start_y2 + bar_step
        start_y2 = start_y1 + bar_height

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Pokedex")
window.geometry("1200x700")

window.grid_rowconfigure(0, weight=0, pad=20)
window.grid_rowconfigure([i for i in range(1,4)], weight=1)
window.grid_columnconfigure([i for i in range(3)], minsize=50, weight=1)

name_frame = ctk.CTkFrame(window, corner_radius=10)
pokemon_name_label = ctk.CTkLabel(name_frame, 
                      height=40,
                      text="Pokemon Name Here", 
                      text_color="yellow",
                      font=ctk.CTkFont(size=16, weight="bold", family="Futura"))
pokemon_name_label.pack(padx=10, pady=10)
name_frame.grid(row=0, column=0, padx=10, sticky="ew")

picture_frame = ctk.CTkFrame(window, corner_radius=10)
picture_frame.grid_rowconfigure(0, weight=1)
picture_frame.grid_columnconfigure(0, weight=1)

picture_label = ctk.CTkLabel(picture_frame, text="")
picture_label.grid(row=0, column=0, sticky="nsew")

picture_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10)
picture_frame.grid_propagate(False)

type_frame = ctk.CTkFrame(window, corner_radius=10)
type_one_label = ctk.CTkLabel(type_frame, text="Type 1 Here", font=ctk.CTkFont(size=16))
type_one_label.grid(row=0, column=0)
type2label = ctk.CTkLabel(type_frame, text="Type 2 Here", font=ctk.CTkFont(size=16))
type2label.grid(row=0, column=1)
type_frame.grid(row=3, column=0, pady=10)

info_frame = ctk.CTkFrame(window, corner_radius=10)
info_frame.grid_rowconfigure([0,1,2], weight=2, minsize=200)
info_frame.grid_columnconfigure([0,1], weight=1, minsize=300)

pokedex_entry = ctk.CTkLabel(info_frame, text="Pokedex Entry", font=ctk.CTkFont(size=16),
                         wraplength=700, anchor="w", fg_color="black", text_color="light blue",
                         justify="left")
pokedex_entry.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

height_label = ctk.CTkLabel(info_frame, text="Height", font=ctk.CTkFont(size=16), corner_radius=5,
                       fg_color="white", text_color="black")
height_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

weight_label = ctk.CTkLabel(info_frame, text="Weight", font=ctk.CTkFont(size=16), corner_radius=5,
                       fg_color="white", text_color="black")
weight_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

catch_rate_label = ctk.CTkLabel(info_frame, text="Catch Rate", font=ctk.CTkFont(size=16), corner_radius=5,
                      fg_color="white", text_color="black")
catch_rate_label.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

stat_frame = ctk.CTkFrame(info_frame, corner_radius=5, fg_color="white")

stat_frame.grid_rowconfigure([i for i in range(6)], weight=1)
stat_frame.grid_columnconfigure(1, weight=1)

stat_labels = ["HP:", "ATK:", "DEF:", "SPA:", "SPD:", "SPE:"]

draw_box = ctk.CTkCanvas(stat_frame, height=100, width=275, bg="white", 
                     borderwidth=0, highlightthickness=0)

draw_box.grid(row=0, rowspan=6, column=2, sticky="nsew")

start_x1 = 0
start_y1 = 7
start_x2 = 250
start_y2 = 27
bar_height = 20
bar_step = 13

for row, stat in enumerate(stat_labels):
    text_box = ctk.CTkLabel(stat_frame, 
                        text=stat,
                        font=ctk.CTkFont(size=12),
                        anchor="w",
                        fg_color="white",
                        justify="left")
    text_box.grid(row=row, column=0, sticky="nsw")

    draw_box.create_rectangle(start_x1, start_y1, start_x2, start_y2, fill="green")
    start_y1 = start_y2 + bar_step
    start_y2 = start_y1 + bar_height

stat_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

info_frame.grid(row=1, rowspan=3, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
info_frame.grid_propagate(False)

search_frame = ctk.CTkFrame(window, corner_radius=10)
search_frame.grid_columnconfigure([0,1,2,3,4], weight=1)
search_frame.grid_rowconfigure(0, weight=1, minsize=55)

left_button = ctk.CTkButton(search_frame, text="Previous", font=ctk.CTkFont(size=16), 
                        command=lambda: select_pokemon(move="backward"))
left_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

submit_button = ctk.CTkButton(search_frame, text="Search!", font=ctk.CTkFont(size=14), 
                          command=select_pokemon)
submit_button.grid(row=0, column=3, padx=5, pady=5)

right_button = ctk.CTkButton(search_frame, text="Next", font=ctk.CTkFont(size=16),
                         command=lambda: select_pokemon(move="forward"))
right_button.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

def search_pokemon():
    current_text = pokemon_search_box.get()
    if current_text == "" or current_text in pokedex.name.tolist():
        pokemon_search_box.configure(values=pokedex.name.tolist())
    else:
        values = []
        for name in pokedex.name.tolist():
            if current_text.lower() in name.lower():
                values.append(name)
        pokemon_search_box.configure(values=values)

pokemon_search_box = ctk.CTkComboBox(search_frame, 
                          values=pokedex.name.tolist(),
                          font=ctk.CTkFont(size=16), 
                          command=lambda x: select_pokemon(),
                          height=40)
pokemon_search_box.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=5, padx=10)

search_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

window.mainloop()
