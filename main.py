# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import tkinter as tk
from tkinter import filedialog, Text
import os

import requests
import pandas as pd
import json
from openpyxl import workbook

import arff
import numpy as np
import json

base_key = 'https://api-v2.swissunihockey.ch/api/'

def createGui():
    root = tk.Tk()


    canvas = tk.Canvas(root, height = 300, width = 650)
    canvas.pack()

    titelFrame = tk.Frame(root)
    titelFrame.place(relwidth = 1, relheight = 0.1, relx =0.00, rely =0.05)

    column1= tk.Frame(root)
    column1.place(relwidth = 0.25, relheight =0.75, relx =0.05, rely=0.25)

    column2= tk.Frame(root)
    column2.place(relwidth = 0.25, relheight =0.75, relx =0.375, rely=0.25)

    column3= tk.Frame(root)
    column3.place(relwidth = 0.25, relheight =0.75, relx =0.7, rely=0.25)

    greeting = tk.Label(titelFrame, text ="Spielplanerstellung Eintracht Beromünster", font=("Arial", 25))
    greeting.pack()

    btn_AJun = tk.Button(column1 , text ="A Junioren", padx = 10, pady =10, fg ="white", bg ="#000000", width =50, command =getAllGames ).pack()
    btn_BJun = tk.Button(column1 ,text ="B Junioren", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_CJun = tk.Button(column1 , text ="C Junioren", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_Djun = tk.Button(column1 ,text ="D Junioren", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()


    btn_AJuniorinnen = tk.Button(column2 ,text ="A Juniorinnen", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_BJuniorinnen = tk.Button(column2 ,text ="B Juniorinnen", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_CJuniorinnen = tk.Button(column2 ,text ="C Juniorinnen", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_DJuniorinnen = tk.Button(column2 ,text ="D Juniorinnen", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()

    btn_allGames = tk.Button(column3 , text ="Alle Spiele", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_Herren1 = tk.Button(column3 , text ="Herren 1", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_Herren2 = tk.Button(column3 , text ="Herren 2", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()
    btn_Damen = tk.Button(column3 , text ="Damen", padx = 10, pady =10, fg ="white", bg ="#000000", width =50,command =getAllGames).pack()

    root.mainloop()


def getAllGames():
    club_id = 417058
    season = 2021
    url = base_key + f'games?mode=club&club_id={club_id}&season={season}'
    print(url)
    r = requests.get(url)

    matchliste = r.json()


    data=pd.json_normalize(r.json())


    print(data['data.regions'])

    answer = data['data.regions']
    header = data['data.headers']
    title = data['data.title']



    print(header)
    print(title)

    answer = pd.json_normalize(answer)


    answer.to_excel('C:\\Users\\Florin Rüedi\\OneDrive\\Standardordner\\Spielliste4.xlsx')





# Press the green button in the gutter to run the script.
getAllGames()
createGui()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
