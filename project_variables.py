import tkinter as tk

import pandas as pd

# Includes all globally callable variables

base_key = 'https://api-v2.swissunihockey.ch/api/'
config_file = 'config.json'

button_colour = "#265143"

root = tk.Tk()
root.title("Spielplanerstellung")


def update_teams():
    teams = pd.read_json(config_file)
    return teams
