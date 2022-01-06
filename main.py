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

    canvas = tk.Canvas(root, height=300, width=650)
    canvas.pack()

    titelFrame = tk.Frame(root)
    titelFrame.place(relwidth=1, relheight=0.1, relx=0.00, rely=0.05)

    column1 = tk.Frame(root)
    column1.place(relwidth=0.25, relheight=0.75, relx=0.05, rely=0.25)

    column2 = tk.Frame(root)
    column2.place(relwidth=0.25, relheight=0.75, relx=0.375, rely=0.25)

    column3 = tk.Frame(root)
    column3.place(relwidth=0.25, relheight=0.75, relx=0.7, rely=0.25)

    greeting = tk.Label(titelFrame, text="Spielplanerstellung Eintracht Beromünster", font=("Arial", 25))
    greeting.pack()

    btn_AJun = tk.Button(column1, text="A Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=getAllGames).pack()
    btn_BJun = tk.Button(column1, text="B Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=getAllGames).pack()
    btn_CJun = tk.Button(column1, text="C Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=getAllGames).pack()
    btn_Djun = tk.Button(column1, text="D Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=getAllGames).pack()

    btn_AJuniorinnen = tk.Button(column2, text="A Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=getAllGames).pack()
    btn_BJuniorinnen = tk.Button(column2, text="B Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=getAllGames).pack()
    btn_CJuniorinnen = tk.Button(column2, text="C Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=getAllGames).pack()
    btn_DJuniorinnen = tk.Button(column2, text="D Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=getAllGames).pack()

    btn_allGames = tk.Button(column3, text="Alle Spiele", padx=10, pady=10, fg="white", bg="#000000", width=50,
                             command=getAllGames).pack()
    btn_Herren1 = tk.Button(column3, text="Herren 1", padx=10, pady=10, fg="white", bg="#000000", width=50,
                            command=getAllGames).pack()
    btn_Herren2 = tk.Button(column3, text="Herren 2", padx=10, pady=10, fg="white", bg="#000000", width=50,
                            command=getAllGames).pack()
    btn_Damen = tk.Button(column3, text="Damen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                          command=getAllGames).pack()

    root.mainloop()


def getAllGames():
    club_id = 417058
    season = 2021
    url = base_key + f'games?mode=club&club_id={club_id}&season={season}'
    print(url)
    r = requests.get(url)


    data = pd.json_normalize(r.json())

    matchList = pd.json_normalize(data['data.regions'])

    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['rows'])
    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['cells'])

    # muss für jede Zeile von cells gemacht werden

    # Textinfors für Match
    i=0
    games = pd.DataFrame()

    for row in matchList.iterrows():
        game = pd.json_normalize(matchList.iloc[i])
        game = game['text']
        # Dataframe for the list of games. Gets saved in excel at last


        gamedict = {
            "Datum": splitTime(cleanWord(game[0]), False),
            "Abfahrt": "",

            "Liga": cleanWord(game[2]),
            "Ort": cleanWord(game[1]),
            "Anspielzeit": splitTime(cleanWord(game[0]), True),
            "Gegner": getOpponent(cleanWord(game[3]), cleanWord(game[4])),
            "Anspielzeit 2" : getSameDayMatch(game[0],game[2],matchList,i, "time"),
            "Gegner 2" : getSameDayMatch(game[0],game[2],matchList, i, "opponent")

        }

        games = games.append(gamedict, ignore_index=True)
        i+=1


    # Headers als Textinfo
    # header = pd.json_normalize(data['data.headers'])
    # header = pd.json_normalize(header.iloc[0])
    # header = header['text']

    # Set destination directory to save excel.
    xlsFilepath = r'C:\\Users\\Florin Rüedi\\OneDrive\\Standardordner\\Spielliste.xlsx'
    writer = pd.ExcelWriter(xlsFilepath, engine='xlsxwriter')

    # Write excel to file using pandas to_excel
    games.to_excel(writer, startrow=1, sheet_name='Sheet1', index=False)
    # Indicate workbook and worksheet for formatting
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    for i, col in enumerate(games.columns):
        # find length of column i
        column_len = games[col].astype(str).str.len().max()
        # Setting the length if the column header is larger
        # than the max column value length
        column_len = max(column_len, len(col)) + 2
        # set the column length
        worksheet.set_column(i, i, column_len)
    writer.save()

def saveExcel():
    return

def getSameDayMatch(date, liga, matchliste, rowCount, type):
    i=0
    print(i)
    print(rowCount)
    for row in matchliste.iterrows():
        if i != rowCount:
            game = pd.json_normalize(matchliste.iloc[i])
            game = game['text']

            print(date + liga)
            print(game[0] + game[2])

            if splitTime(game[0], False) == splitTime(date, False) and game[2] == liga and type == "time":

                return cleanWord(splitTime(game[0], True))

            if splitTime(game[0], False) == splitTime(date, False) and game[2] == liga and type == "opponent":
                return getOpponent(cleanWord(game[3]), cleanWord(game[4]))

        i+=1
    return "-"


def getOpponent(team1, team2):
    if team1 != "Eintracht Beromünster":
        return team1
    else:
        return team2


def cleanWord(word):
    unwantedCharacters = "[]'"

    word = str(word)

    for character in unwantedCharacters:
        word = word.replace(character, "")

    return word


def splitTime(datetime, type):
    datetime = str(datetime)

    if type == False:
        try:
            array = datetime.split(',');
            return array[0];
        except:
            return "-"


    else:
        try:
            array = datetime.split(',');
            return array[1];
        except:
            return "-"


# Press the green button in the gutter to run the script.
getAllGames()
createGui()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
