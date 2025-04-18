import pandas as pd
import numpy as np
import tkinter as tkint
from tkinter import ttk

pokedata = pd.read_csv("pokedata.csv", index_col = 0)

stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defence', 'speed']

