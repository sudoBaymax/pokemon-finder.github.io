import pandas as pd
import numpy as np
import tkinter as tkint
from tkinter import ttk

pokedata = pd.read_csv("pokedata.csv", index_col = 0)

stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defence', 'speed']

def scale_statistic(x):
    start_x1 = 250
    start_x2 = 1

    min_x = 20
    max_x = 150

    min_x = 20
    max_x = 150

    if x < min_x:
        x = min_x
    elif x > max_x:
        x = max_x
    
    return round((start_x1 - start_x2)*((x - min_x) / (max_x - min_x)) + start_x2)