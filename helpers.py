import os

import datetime

import pandas as pd

from openpyxl import load_workbook
from tkinter.filedialog import askopenfile

import project_variables

# takes Global variables
root = project_variables.root
teams = project_variables.update_teams()
clubname = teams.iloc[0]


# Compares teamnames with "Eintracht Beromünster" and determines which one the opponent is
def get_opponent(team1, team2):
    if clubname[0] not in team1:
        return team1
    elif clubname[0] not in team2:
        return team2
    else:
        return "Undefiniert"


# Deletes excessive words from Liga
def clean_liga(word):
    word = word.replace("Regional", "")
    new_word = word.replace("Aktive", "")

    description = new_word.split(',')
    return description[0]


# Cleans the word from unwanted characters
def clean_word(word):
    unwanted_characters = "[]'"

    word = str(word)

    for character in unwanted_characters:
        word = word.replace(character, "")

    return word


# Splits time so date and time are separately stored. Takes bool as input to determine which has to be returned
def split_time(date_time, time_asked):
    date_time = str(date_time)

    if not time_asked:
        try:
            array = date_time.split(',')
            return array[0]
        except Exception as ex:
            print(ex)
            return "-"

    else:
        try:
            array = date_time.split(',')
            return array[1]
        except Exception as ex:
            print(ex)
            return "-"


# Opens Explorer with inputted directory. Used to show the saved file at the end
def open_explorer(save_file_name):
    save_file_name = make_initial_dir(save_file_name)
    file = askopenfile(parent=root, title="Erfolgreich gespeichert", initialdir=save_file_name, mode="r",
                       filetype=[("Excel", "*.xlsx")])
    if file:
        selected_file = file.name
        os.startfile(selected_file)


# Gets the path without the filename for openExplorer function
def make_initial_dir(path):
    array = path.split('/')
    path = path.replace(array[len(array) - 1], "")

    return path


# Function to determine game-season. Changes on the month of april
def get_season():
    now = datetime.datetime.now()
    if now.month > 3:
        season = now.year
    else:
        season = now.year - 1

    return season


# saves the dataframe into an excel and adjusts layout
def save_excel(games, title, filename):
    # Set destination directory to save excel.
    if ".xlsx" not in filename:
        filename = filename + '.xlsx'

    xls_filepath = filename
    writer = pd.ExcelWriter(xls_filepath, engine='xlsxwriter')

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
    workbook = load_workbook(filename=xls_filepath)
    # open workbook
    sheet = workbook.active
    # modify the desired cell
    sheet["A1"] = title
    # save the file
    workbook.save(filename=xls_filepath)

    return
