from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import requests

import helpers
import projectVariables

root = projectVariables.root
base_key = projectVariables.base_key


# Function which gets called when a team-button is pressed
def getTeamGames(team_id):
    print(team_id)
    print("---")
    if (team_id):
        saveFileName = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")])

        if (saveFileName):
            saison = helpers.getSaison()

            # gets Title for Excel
            try:
                r = requests.get(base_key + f'games?mode=team&team_id={team_id}&season={saison}&page=1')
                data = pd.json_normalize(r.json())
                title = data['data.title']
                title = str(title[0])
            except:
                messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem Fehler der Request")
                return

            # prepares everything for requests
            page = 1
            games = pd.DataFrame()

            # Loop that calls requests until all games were fetched. Has an upper limit to not accidentally spam the api
            while (page < 1000):

                # Link where data gets requested. team id, saison and page are dynamic
                teamUrl = base_key + f'games?mode=team&team_id={team_id}&season={saison}&page={page}'

                try:
                    r = requests.get(teamUrl)
                    error = r.json()
                except:
                    messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem Fehler der Request")
                    return

                # Determines error answer
                if ("Error" in str(error['type'])):
                    break
                else:
                    print(r.json())
                    try:
                        games = createDataframeMatch(r, games)
                    except:
                        messagebox.showerror(title="Fehler",
                                             message=f"Die Anfrage resultierte in einem Fehler in der Umformatierung")
                        return

                    page += 1

            getSameDayGameswithoutLiga(games)
            # deletes all excessive duplicates, then saves the data in an excel and then opens the explorer to show the file
            games.drop_duplicates(subset=['Datum', 'Ort'], inplace=True, keep='first')

            helpers.saveExcel(games, title, saveFileName)

            helpers.openExplorer(saveFileName)

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
            "Datum": helpers.splitTime(helpers.cleanWord(game[0]), False),
            "Abfahrt": "",
            "Ort": helpers.cleanWord(game[1]),
            "Anspielzeit": helpers.splitTime(helpers.cleanWord(game[0]), True),
            "Gegner": helpers.getOpponent(helpers.cleanWord(game[2]), helpers.cleanWord(game[3])),
            "Anspielzeit2": "",
            "Gegner2": ""

        }

        # appends dict to dataframe
        games = games.append(gamedict, ignore_index=True)
        i += 1

    return games

#puts games at the same day together
def getSameDayGameswithoutLiga(games):
    for game in games.iterrows():
        for maybeSameDayGame in games.iterrows():

            if (game[0] < maybeSameDayGame[0]):

                if str(game[1].Datum) == maybeSameDayGame[1].Datum:
                    game[1].Gegner2 = maybeSameDayGame[1].Gegner
                    game[1].Anspielzeit2 = maybeSameDayGame[1].Anspielzeit
                    break
