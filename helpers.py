import tkinter as tk
import os

import datetime

import pandas as pd

from openpyxl import load_workbook
from tkinter.filedialog import askopenfile

import projectVariables

# takes Global variables
root = projectVariables.root
teams = projectVariables.updateTeams()
clubname = teams.iloc[0]


# Compares teamnames with "Eintracht Beromünster" and determines which one the opponent is
def getOpponent(team1, team2):
    if clubname[0] not in team1:
        print(clubname[0])
        return team1
    elif clubname[0] not in team2:
        return team2
    else:
        return "Undefiniert"


# Deletes excessive words from Liga
def cleanLiga(word):
    word = word.replace("Regional", "")
    new_word = word.replace("Aktive", "")

    description = new_word.split(',')
    return description[0]


# Cleans the word from unwanted characters
def cleanWord(word):
    unwantedCharacters = "[]'"

    word = str(word)

    for character in unwantedCharacters:
        word = word.replace(character, "")

    return word


# Splits time so date and time are seperately storable. Takes bool as input to determine which has to be returned
def splitTime(datetime, type):
    datetime = str(datetime)

    if type == False:
        try:
            array = datetime.split(',')
            return array[0]
        except:
            return "-"

    else:
        try:
            array = datetime.split(',')
            return array[1]
        except:
            return "-"


# Opens Explorer with inputted directory. Used to show the saved file at the end
def openExplorer(saveFileName):
    saveFileName = makeInitialDir(saveFileName)
    file = askopenfile(parent=root, title="Erfolgreich gespeichert", initialdir=saveFileName, mode="r",
                       filetype=[("Excel", "*.xlsx")])
    if (file):
        selectedFile = file.name
        os.startfile(selectedFile)


# Gets the path without the filenam for openExplorer function
def makeInitialDir(path):
    array = path.split('/')
    path = path.replace(array[len(array) - 1], "")

    return path


# Function to determine game-saison. Changes on the month of april
def getSaison():
    now = datetime.datetime.now()
    if (now.month > 3):
        saison = now.year
    else:
        saison = now.year - 1

    return saison


# saves the datafram into an excel and adjusts layout
def saveExcel(games, title, filename):
    # Set destination directory to save excel.
    if ".xlsx" not in filename:
        filename = filename + '.xlsx'

    xlsFilepath = filename
    writer = pd.ExcelWriter(xlsFilepath, engine='xlsxwriter')

    # Write excel to file using pandas to_excel
    games.to_excel(writer, startrow=1, sheet_name='Sheet1', index=False)
    # Indicate workbook and worksheet for formatting
    worksheet = writer.sheets['Sheet1']

    # adjusts column-layout
    for i, col in enumerate(games.columns):
        # find length of column i
        column_len = games[col].astype(str).str.len().max()
        # Setting the length if the column header is larger
        # than the max column value length
        column_len = max(column_len, len(col)) + 2
        # set the column length
        worksheet.set_column(i, i, column_len)
    writer.save()

    # Adds the title to the existing File
    # load excel file
    workbook = load_workbook(filename=xlsFilepath)
    # open workbook
    sheet = workbook.active
    # modify the desired cell
    sheet["A1"] = title
    # save the file
    workbook.save(filename=xlsFilepath)

    return
