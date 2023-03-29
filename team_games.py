from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import requests

import helpers
import project_variables

root = project_variables.root
base_key = project_variables.base_key


# Function which gets called when a team-button is pressed
def get_team_games(team_id, team_name):
    print(team_id)
    print("---")
    if team_id:
        save_file_name = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")], initialfile=team_name)

        if save_file_name:
            saison = helpers.get_season()

            # gets Title for Excel
            try:
                r = requests.get(base_key + f'games?mode=team&team_id={team_id}&season={saison}&page=1')
                data = pd.json_normalize(r.json())
                title = data['data.title']
                title = str(title[0])
            except Exception as ex:
                messagebox.showerror(title="Fehler",
                                     message=f"Die Anfrage resultierte in einem Fehler der Request:  {ex}")
                return

            # prepares everything for requests
            page = 1
            games = pd.DataFrame()

            # Loop that calls requests until all games were fetched. Has an upper limit to not accidentally spam the api
            while page < 1000:

                # Link where data gets requested. team id, season and page are dynamic
                team_url = base_key + f'games?mode=team&team_id={team_id}&season={saison}&page={page}'

                try:
                    r = requests.get(team_url)
                    error = r.json()
                except Exception as ex:
                    messagebox.showerror(title="Fehler",
                                         message=f"Die Anfrage resultierte in einem Fehler der Request: {ex}")
                    return

                # Determines error answer
                if "Error" in str(error['type']):
                    break
                else:
                    print(r.json())
                    try:
                        games = create_dataframe_match(r, games)
                    except Exception as ex:
                        messagebox.showerror(title="Fehler",
                                             message=f"Die Anfrage resultierte in einem Fehler in der "
                                                     f"Umformatierung:{ex}")
                        return

                    page += 1

            get_same_day_games_without_liga(games)
            # deletes all excessive duplicates, then saves the data in an excel and then opens
            # the explorer to show the file

            games.drop_duplicates(subset=['Datum', 'Ort'], inplace=True, keep='first')

            helpers.save_excel(games, title, save_file_name)

            helpers.open_explorer(save_file_name)

        # Falls kein Speicherort ausgewählt wird
        else:
            print("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")
    else:
        messagebox.showerror("Fehler", "Keine ID hinterlegt. Korrigieren sie diese im config File", )


# Processes data from match requests
def create_dataframe_match(data, games):
    data = pd.json_normalize(data.json())
    match_list = pd.json_normalize(data['data.regions'])

    # normalizes data
    match_list = pd.json_normalize(match_list.iloc[0])
    match_list = pd.json_normalize(match_list['rows'])
    match_list = pd.json_normalize(match_list.iloc[0])
    match_list = pd.json_normalize(match_list['cells'])

    i = 0
    # Fills normalized data into dataframe structure. Different dict than in function above
    for row in match_list.iterrows():
        game = pd.json_normalize(match_list.iloc[i])
        game = game['text']

        # Dataframe for the list of games. Gets saved in excel at last
        game_dict = {
            "Datum": helpers.split_time(helpers.clean_word(game[0]), False),
            "Abfahrt": "",
            "Ort": helpers.clean_word(game[1]),
            "Anspielzeit": helpers.split_time(helpers.clean_word(game[0]), True),
            "Gegner": helpers.get_opponent(helpers.clean_word(game[2]), helpers.clean_word(game[3])),
            "Anspielzeit2": "",
            "Gegner2": ""

        }

        # appends dict to dataframe
        games = games.append(game_dict, ignore_index=True)
        i += 1

    return games


# puts games at the same day together
def get_same_day_games_without_liga(games):
    for game in games.iterrows():
        for maybe_same_day_game in games.iterrows():

            if game[0] < maybe_same_day_game[0]:

                if str(game[1].Datum) == maybe_same_day_game[1].Datum:
                    game[1].Gegner2 = maybe_same_day_game[1].Gegner
                    game[1].Anspielzeit2 = maybe_same_day_game[1].Anspielzeit
                    break
