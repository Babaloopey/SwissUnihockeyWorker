# To Reduce Errors in production
import sys, os


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

# This is a the swiss Unihockey Worker from Eintracht Beromünster
# You may change the Id's in the config File. Ids can be found on swissunihockey. Supposedly over the api v-2
# https://api-v2.swissunihockey.ch/api/doc

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import tkinter as tk
import os

import datetime

import requests
import pandas as pd

from openpyxl import load_workbook
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import configurationScript
import math

base_key = 'https://api-v2.swissunihockey.ch/api/'
configFile = 'config.json'

teams = pd.read_json(configFile)
clubname = teams.iloc[0]
print(clubname)
for team in teams.iterrows():
    print(team[1].description)
    print(team[1].id)

root = tk.Tk()
root.title("Spielplanerstellung")
root.iconbitmap("ball.ico")

def linesInGui():
    buttonheight = 50
    print(math.ceil(len(teams)/3))
    return (math.ceil(len(teams)/3)*buttonheight)

def createGui():
    canvas = tk.Canvas(root, height=(50+linesInGui()), width=650)
    canvas.pack()

    titelFrame = tk.Frame(root)
    titelFrame.place(relwidth=0.8, height=40, relx=0.00, rely=0.05)
    configFrame = tk.Frame(root)
    configFrame.place(relwidth=0.2, height=40, relx=0.8, rely=0.05)

    # columns for a grid in the gui
    column1 = tk.Frame(root)
    column1.place(relwidth=0.25, relheight=0.75, relx=0.05, y=60)

    column2 = tk.Frame(root)
    column2.place(relwidth=0.25, relheight=0.75, relx=0.375, y=60)

    column3 = tk.Frame(root)
    column3.place(relwidth=0.25, relheight=0.75, relx=0.7, y=60)

    greeting = tk.Label(titelFrame, text=clubname[0], font=("Arial", 25))
    greeting.pack()

    btn_configuration = tk.Button(configFrame, text="Konfiguration", fg="black", command=lambda: configurationScript.showWindow()).pack()

    # Team-Ids from swissunihockey. Are used with the buttons
    # team-Ids

    for widget in column1.winfo_children():
        widget.destroy()
    for widget in column2.winfo_children():
        widget.destroy()
    for widget in column3.winfo_children():
        widget.destroy()

    for team in teams.iterrows():
        if (team[0]+1 <= (len(teams) / 3)):
            tk.Button(column1, text=team[1].description, padx=10, pady=10, fg="white", bg="#000000", width=50,
                      command=lambda c=team: print(c)).pack()
        elif (team[0]+1 <= (len(teams) / 3 * 2)):
            tk.Button(column2, text=team[1].description, padx=10, pady=10, fg="white", bg="#000000", width=50,
                      command=lambda c=team: print(c)).pack()
        elif (team[0]+1 <= (len(teams) / 3 * 3)):
            tk.Button(column3, text=team[1].description, padx=10, pady=10, fg="white", bg="#000000", width=50,
                      command=lambda c=team: print(c)).pack()

    # Buttons for the gui

    root.mainloop()


# Function which gets called when a team-button is pressed
def getTeamGames(team_id):
    print(team_id)
    print("---")
    if ('None' not in team_id):
        saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])

        if (saveFileName):
            messagebox.showinfo("In Bearbeitung",
                                "Das Erstellen der Liste dauert einen Moment. Wenn es fertig ist, wird der Dateimanager geöffnet")
            saison = getSaison()

            # gets Title for Excel
            r = requests.get(base_key + f'games?mode=team&team_id={team_id}&season={saison}&page=1')
            data = pd.json_normalize(r.json())
            title = data['data.title']
            title = str(title[0])

            # prepares everything for requests
            page = 1
            games = pd.DataFrame()

            # Loop that calls requests until all games were fetched. Has an upper limit to not accidentally spam the api
            while (page < 10):

                # Link where data gets requested. team id, saison and page are dynamic
                teamUrl = base_key + f'games?mode=team&team_id={team_id}&season={saison}&page={page}'

                r = requests.get(teamUrl)
                error = r.json()

                # Determines error answer
                if ("Error" in str(error['type'])):
                    break
                else:
                    print(r.json())
                    games = createDataframeMatch(r, games)
                    page += 1

            getSameDayGameswithoutLiga(games)
            # deletes all excessive duplicates, then saves the data in an excel and then opens the explorer to show the file
            games.drop_duplicates(subset=['Datum', 'Ort'], inplace=True, keep='first')

            saveExcel(games, title, saveFileName)

            openExplorer(saveFileName)

        # Falls kein Speicherort ausgewählt wird
        else:
            messagebox.showinfo("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")
    else:
        messagebox.showerror("Fehler", "Keine ID hinterlegt. Korrigieren sie diese im config File", )


# Processes data from match requests
def createDataframeMatch(data, games):
    data = pd.json_normalize(data.json())
    matchList = pd.json_normalize(data['data.regions'])

    # normalizes data
    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['rows'])
    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['cells'])

    i = 0
    # Fills normalized data into dataframe structure. Different dict than in function above
    for row in matchList.iterrows():
        game = pd.json_normalize(matchList.iloc[i])
        game = game['text']

        # Dataframe for the list of games. Gets saved in excel at last
        gamedict = {
            "Datum": splitTime(cleanWord(game[0]), False),
            "Abfahrt": "",
            "Ort": cleanWord(game[1]),
            "Anspielzeit": splitTime(cleanWord(game[0]), True),
            "Gegner": getOpponent(cleanWord(game[2]), cleanWord(game[3])),
            "Anspielzeit2": "",
            "Gegner2": ""

        }

        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1

    return games


def getSameDayGameswithoutLiga(games):
    for game in games.iterrows():
        for maybeSameDayGame in games.iterrows():

            if (game[0] < maybeSameDayGame[0]):

                if str(game[1].Datum) == maybeSameDayGame[1].Datum:
                    game[1].Gegner2 = maybeSameDayGame[1].Gegner
                    game[1].Anspielzeit2 = maybeSameDayGame[1].Anspielzeit
                    break


# Gets all Games from the club and saves them in xlsx
def getAllGames(club_id):
    print(club_id)
    print("---")
    saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])

    if (saveFileName):
        messagebox.showinfo("In Bearbeitung",
                            "Das Erstellen der Liste dauert einen Moment. Wenn es fertig ist, wird der Dateimanager geöffnet")

        saison = getSaison()

        # Preparation for data requests
        games = pd.DataFrame()
        page = 1

        # gets Title
        r = requests.get(base_key + f'games?mode=club&club_id={club_id}&season={saison}&page=1')
        data = pd.json_normalize(r.json())
        title = data['data.title']
        title = str(title[0])

        while (page < 30):
            # Url from which Data is fetched
            allUrl = base_key + f'games?mode=club&club_id={club_id}&season={saison}&page={page}'

            r = requests.get(allUrl)
            error = r.json()

            # Determines error answer
            if ("Error" in str(error['type'])):
                break
            else:
                print(r.json())
                games = createDataframe(r, games)
                page += 1

        # Deletes excessive duplicates, then saves the file and opens in explorer

        getSameDayGames(games)

        games.drop_duplicates(subset=['Datum', 'Liga', 'Ort'], inplace=True, keep='first')

        saveExcel(games, title, saveFileName)

        openExplorer(saveFileName)

    else:
        messagebox.showinfo("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")


# Processes requestdata into dataframe
def createDataframe(data, games):
    data = pd.json_normalize(data.json())
    matchList = pd.json_normalize(data['data.regions'])

    # Normalizes data
    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['rows'])
    matchList = pd.json_normalize(matchList.iloc[0])
    matchList = pd.json_normalize(matchList['cells'])

    i = 0
    # Fills normalized data into dataframe structure
    for row in matchList.iterrows():
        game = pd.json_normalize(matchList.iloc[i])
        game = game['text']
        # Dict for the list of games. Gets saved in excel at last

        gamedict = {
            "Datum": splitTime(cleanWord(game[0]), False),
            "Abfahrt": "",

            "Liga": cleanLiga(cleanWord(game[2])),
            "Ort": cleanWord(game[1]),
            "Anspielzeit": splitTime(cleanWord(game[0]), True),
            "Gegner": getOpponent(cleanWord(game[3]), cleanWord(game[4])),
            "Anspielzeit2": "",
            "Gegner2": "",

        }
        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1
    return games


def getSameDayGames(games):
    for game in games.iterrows():
        for maybeSameDayGame in games.iterrows():

            if (game[0] < maybeSameDayGame[0]):

                if str(game[1].Datum) == maybeSameDayGame[1].Datum and game[1].Liga == maybeSameDayGame[1].Liga:
                    game[1].Gegner2 = maybeSameDayGame[1].Gegner
                    game[1].Anspielzeit2 = maybeSameDayGame[1].Anspielzeit
                    break


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


# Compares teamnames with "Eintracht Beromünster" and determines which one the opponent is
def getOpponent(team1, team2):
    if "Eintracht Beromünster" not in team1:
        return team1
    elif "Eintracht Beromünster" not in team2:
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


def getId(searchTerm):
    print(searchTerm)


# Press the green button in the gutter to run the script.
createGui()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
