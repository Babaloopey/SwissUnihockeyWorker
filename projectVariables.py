import tkinter as tk
import pandas as pd

#Includes all globally callable variables

base_key = 'https://api-v2.swissunihockey.ch/api/'
configFile = 'config.json'

buttoncolour = "#265143"

root = tk.Tk()
root.title("Spielplanerstellung")
root.iconbitmap("ball.ico")

def updateTeams():
    global teams
    teams = pd.read_json(configFile)
    return teams
