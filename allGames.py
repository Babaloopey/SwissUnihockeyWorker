import requests
import pandas as pd

from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox

# Other modules
import projectVariables
import helpers

root = projectVariables.root
base_key = projectVariables.base_key


# Gets all Games from the club and saves them in xlsx
def getAllGames(club_id):
    print(club_id)
    print("---")
    saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])

    if (saveFileName):
        messagebox.showinfo("In Bearbeitung",
                            "Das Erstellen der Liste dauert einen Moment. Wenn es fertig ist, wird der Dateimanager geöffnet")

        saison = helpers.getSaison()

        # Preparation for data requests
        games = pd.DataFrame()
        page = 1

        # gets Title
        try:
            r = requests.get(base_key + f'games?mode=club&club_id={club_id}&season={saison}&page=1')
            data = pd.json_normalize(r.json())
            title = data['data.title']
            title = str(title[0])
        except:
            messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem Fehler der Request")
            return

        while (page < 5000):
            # Url from which Data is fetched
            allUrl = base_key + f'games?mode=club&club_id={club_id}&season={saison}&page={page}'

            try:
                r = requests.get(allUrl)
                error = r.json()
            except:
                messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem Fehler der Request")
                return

            # Determines error answer
            if "Error" in str(error['type']):
                print("")
                print(error)
                break
            else:
                print(r.json())
                try:
                    games = createDataframe(r, games)
                except:
                    messagebox.showerror(title="Fehler",
                                         message=f"Die Anfrage resultierte in einem Fehler in der Umformatierung")
                    return

                page += 1

        # checks for games at same day
        getSameDayGames(games)
        # Deletes excessive duplicates, then saves the file and opens in explorer
        games.drop_duplicates(subset=['Datum', 'Liga', 'Ort'], inplace=True, keep='first')

        # saves data as excel and then shows where it has been saved
        helpers.saveExcel(games, title, saveFileName)
        helpers.openExplorer(saveFileName)

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
            "Datum": helpers.splitTime(helpers.cleanWord(game[0]), False),
            "Abfahrt": "",

            "Liga": helpers.cleanLiga(helpers.cleanWord(game[2])),
            "Ort": helpers.cleanWord(game[1]),
            "Anspielzeit": helpers.splitTime(helpers.cleanWord(game[0]), True),
            "Gegner": helpers.getOpponent(helpers.cleanWord(game[3]), helpers.cleanWord(game[4])),
            "Anspielzeit2": "",
            "Gegner2": "",

        }
        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1
    return games


# loops through dataframe and adds matching dates and ligas to the first one
def getSameDayGames(games):
    for game in games.iterrows():
        for maybeSameDayGame in games.iterrows():

            if (game[0] < maybeSameDayGame[0]):

                if str(game[1].Datum) == maybeSameDayGame[1].Datum and game[1].Liga == maybeSameDayGame[1].Liga:
                    game[1].Gegner2 = maybeSameDayGame[1].Gegner
                    game[1].Anspielzeit2 = maybeSameDayGame[1].Anspielzeit
                    break
