#To Reduce Errors in production
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

base_key = 'https://api-v2.swissunihockey.ch/api/'
configFile = 'config.txt'

with open(configFile) as f:
    ids = f.readlines()

root = tk.Tk()
root.title("Spielplanerstellung")
root.iconbitmap("ball.ico")



def createGui():
    canvas = tk.Canvas(root, height=300, width=650)
    canvas.pack()

    titelFrame = tk.Frame(root)
    titelFrame.place(relwidth=1, relheight=0.2, relx=0.00, rely=0.05)

    # columns for a grid in the gui
    column1 = tk.Frame(root)
    column1.place(relwidth=0.25, relheight=0.75, relx=0.05, rely=0.25)

    column2 = tk.Frame(root)
    column2.place(relwidth=0.25, relheight=0.75, relx=0.375, rely=0.25)

    column3 = tk.Frame(root)
    column3.place(relwidth=0.25, relheight=0.75, relx=0.7, rely=0.25)

    greeting = tk.Label(titelFrame, text="Spielplanerstellung Eintracht Beromünster", font=("Arial", 25))
    greeting.pack()

    # Team-Ids from swissunihockey. Are used with the buttons
    # team-Ids
    id_aJun = getId("id_aJun")
    id_bJun = getId("id_bJun")
    id_cJun = getId("id_cJun")
    id_dJun = getId("id_dJun")
    id_aInnen = getId("id_aInnen")
    id_bInnen = getId("id_bInnen")
    id_cInnen = getId("id_cInnen")
    id_dInnen = getId("id_dInnen")
    id_damen = getId("id_damen")
    id_herren1 = getId("id_herren1")
    id_herren2 = getId("id_herren2")

    print(id_aJun)

    # Buttons for the gui
    btn_AJun = tk.Button(column1, text="A Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=lambda: getTeamGames(id_aJun)).pack()
    btn_BJun = tk.Button(column1, text="B Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=lambda: getTeamGames(id_bJun)).pack()
    btn_CJun = tk.Button(column1, text="C Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=lambda: getTeamGames(id_cJun)).pack()
    btn_Djun = tk.Button(column1, text="D Junioren", padx=10, pady=10, fg="white", bg="#000000", width=50,
                         command=lambda: getTeamGames(id_dJun)).pack()

    btn_AJuniorinnen = tk.Button(column2, text="A Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=lambda: getTeamGames(id_aInnen)).pack()
    btn_BJuniorinnen = tk.Button(column2, text="B Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=lambda: getTeamGames(id_bInnen)).pack()
    btn_CJuniorinnen = tk.Button(column2, text="C Juniorinnen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                                 command=lambda: getTeamGames(id_cInnen)).pack()
    btn_DJuniorinnen = tk.Button(column2, text="D Juniorinnen", padx=10, pady=10, fg="white", bg="#000000",
                                 width=50, command=lambda: getTeamGames(id_dInnen)).pack()

    btn_allGames = tk.Button(column3, text="Alle Spiele", padx=10, pady=10, fg="white", bg="#000000", width=50,
                             command=getAllGames).pack()
    btn_Herren1 = tk.Button(column3, text="Herren 1", padx=10, pady=10, fg="white", bg="#000000", width=50,
                            command=lambda: getTeamGames(id_herren1)).pack()
    btn_Herren2 = tk.Button(column3, text="Herren 2", padx=10, pady=10, fg="white", bg="#000000", width=50,
                            command=lambda: getTeamGames(id_herren2)).pack()
    btn_Damen = tk.Button(column3, text="Damen", padx=10, pady=10, fg="white", bg="#000000", width=50,
                          command=lambda: getTeamGames(id_damen)).pack()

    root.mainloop()


# Function which gets called when a team-button is pressed
def getTeamGames(team_id):
    print(team_id)
    print("---")
    if ('None' not in team_id):
        saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])
        if (saveFileName):

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

            # deletes all excessive duplicates, then saves the data in an excel and then opens the explorer to show the file
            games.drop_duplicates(subset=['Datum', 'Ort'], inplace=True)

            saveExcel(games, title, saveFileName)

            openExplorer(saveFileName)

        # Falls kein Speicherort ausgewählt wird
        else:
            messagebox.showerror("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")
    else:
        messagebox.showerror("Fehler", "Keine ID hinterlegt. Korrigieren sie diese im config File", )


# Gets all Games from the club and saves them in xlsx
def getAllGames():
    saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])

    if (saveFileName):
        club_id = getId("club_id")

        saison = getSaison()

        # Preparation for data requests
        games = pd.DataFrame()
        page = 1

        # gets Title
        r = requests.get(base_key + f'games?mode=club&club_id={club_id}&season={saison}&page=1')
        data = pd.json_normalize(r.json())
        title = data['data.title']
        title = str(title[0])

        while (page < 25):
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
        games.drop_duplicates(subset=['Datum', 'Liga', 'Ort'], inplace=True)

        saveExcel(games, title, saveFileName)

        openExplorer(saveFileName)

    else:
        messagebox.showerror("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")


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
            "Anspielzeit 2": getSameDayMatch(game[0], game[2], matchList, i, "time"),
            "Gegner 2": getSameDayMatch(game[0], game[2], matchList, i, "opponent"),

        }
        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1
    return games


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
            "Anspielzeit 2": getSameDayMatchwithoutLiga(game[0], matchList, i, "time"),
            "Gegner 2": getSameDayMatchwithoutLiga(game[0], matchList, i, "opponent")

        }

        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1

    return games


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


# compares games from a list to find matching Date Location used for Teams
def getSameDayMatchwithoutLiga(date, matchliste, rowCount, type):
    i = 0
    for row in matchliste.iterrows():
        if i != rowCount:
            game = pd.json_normalize(matchliste.iloc[i])
            game = game['text']

            if splitTime(game[0], False) == splitTime(date, False) and type == "time":
                return cleanWord(splitTime(game[0], True))

            if splitTime(game[0], False) == splitTime(date, False) and type == "opponent":
                return getOpponent(cleanWord(game[2]), cleanWord(game[3]))

        i += 1
    return "-"


# compares games from a list to find matching Date Location and Liga. Used for allGames
def getSameDayMatch(date, liga, matchliste, rowCount, type):
    i = 0
    for row in matchliste.iterrows():
        if i != rowCount:
            game = pd.json_normalize(matchliste.iloc[i])
            game = game['text']

            if splitTime(game[0], False) == splitTime(date, False) and game[2] == liga and type == "time":
                return cleanWord(splitTime(game[0], True))

            if splitTime(game[0], False) == splitTime(date, False) and game[2] == liga and type == "opponent":
                return getOpponent(cleanWord(game[3]), cleanWord(game[4]))

        i += 1
    return "-"


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
    file = file.name
    if (file):
        os.startfile(file)


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
    for id in ids:
        if searchTerm in id:
            number = id.split('$')
            print(searchTerm)
            print(number[1])
            return number[1]


# Press the green button in the gutter to run the script.
createGui()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
