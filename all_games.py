from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import requests

# Other modules
import helpers
import project_variables

root = project_variables.root
base_key = project_variables.base_key


# Gets all Games from the club and saves them in xlsx
def get_all_games(club_id, club_name):
    print(club_id)
    print("---")
    save_file_name = asksaveasfilename(parent=root, title="Speicherort auswählen", filetype=[("Excel", "*.xlsx")], initialfile=club_name)

    if save_file_name:
        season = helpers.get_season()

        # Preparation for data requests
        games = pd.DataFrame()
        page = 1

        # gets Title
        try:
            r = requests.get(base_key + f'games?mode=club&club_id={club_id}&season={season}&page=1')
            data = pd.json_normalize(r.json())
            title = data['data.title']
            title = str(title[0])
        except Exception as ex:
            messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem Fehler der Request:{ex}")
            return

        while page < 5000:
            # Url from which Data is fetched
            all_url = base_key + f'games?mode=club&club_id={club_id}&season={season}&page={page}'

            try:
                r = requests.get(all_url)
                error = r.json()
            except Exception as ex:
                messagebox.showerror(title="Fehler", message=f"Die Anfrage resultierte in einem "
                                                             f"Fehler der Request: {ex}")

                return

            # Determines error answer
            if "Error" in str(error['type']):
                print("")
                print(error)
                break
            else:
                print(r.json())
                try:
                    games = create_dataframe(r, games)
                except Exception as ex:
                    messagebox.showerror(title="Fehler",
                                         message=f"Die Anfrage resultierte in einem Fehler in der Umformatierung: {ex}")
                    return

                page += 1

        # checks for games at same day
        get_same_day_games(games)
        # Deletes excessive duplicates, then saves the file and opens in explorer
        games.drop_duplicates(subset=['Datum', 'Liga', 'Ort'], inplace=True, keep='first')
        # Deletes the Heimbezeichnung that was necessary for matching different teams in the same Liga
        games.drop('Heimbezeichnung', axis=1, inplace=True)

        # saves data as excel and then shows where it has been saved
        helpers.save_excel(games, title, save_file_name)
        helpers.open_explorer(save_file_name)

    else:
        print("Fehler", "Sie haben den Erstellungsvorgang abgebrochen")


# Processes requestdata into dataframe
def create_dataframe(data, games):
    data = pd.json_normalize(data.json())
    match_list = pd.json_normalize(data['data.regions'])

    # Normalizes data
    match_list = pd.json_normalize(match_list.iloc[0])
    match_list = pd.json_normalize(match_list['rows'])
    match_list = pd.json_normalize(match_list.iloc[0])
    match_list = pd.json_normalize(match_list['cells'])

    i = 0
    # Fills normalized data into dataframe structure
    for row in match_list.iterrows():
        game = pd.json_normalize(match_list.iloc[i])
        game = game['text']

        print(game)
        # Dict for the list of games. Gets saved in excel at last

        game_dict = {
            "Datum": helpers.split_time(helpers.clean_word(game[0]), False),
            "Abfahrt": "",

            "Liga": helpers.clean_liga(helpers.clean_word(game[2])),
            "Ort": helpers.clean_word(game[1]),
            "Anspielzeit": helpers.split_time(helpers.clean_word(game[0]), True),
            "Gegner": helpers.get_opponent(helpers.clean_word(game[3]), helpers.clean_word(game[4])),
            "Anspielzeit2": "",
            "Gegner2": "",
            "Heimbezeichnung": helpers.get_hometeam(helpers.clean_word(game[3]), helpers.clean_word(game[4])),
        }
        # appends dict to dataframe
        games = games.append(game_dict, ignore_index=True)
        i += 1
    return games


# loops through dataframe and adds matching date and liga to the first one
def get_same_day_games(games):
    for game in games.iterrows():
        for maybe_same_day_game in games.iterrows():

            if game[0] < maybe_same_day_game[0]:

                if str(game[1].Datum) == maybe_same_day_game[1].Datum and game[1].Liga == maybe_same_day_game[1].Liga and game[1].Ort == maybe_same_day_game[1].Ort and game[1].Heimbezeichnung == maybe_same_day_game[1].Heimbezeichnung:
                    game[1].Liga = game[1].Liga + " " + helpers.get_hometeam_endung(game[1].Heimbezeichnung)
                    maybe_same_day_game[1].Liga = maybe_same_day_game[1].Liga + " " + helpers.get_hometeam_endung(maybe_same_day_game[1].Heimbezeichnung)
                    game[1].Gegner2 = maybe_same_day_game[1].Gegner
                    game[1].Anspielzeit2 = maybe_same_day_game[1].Anspielzeit
                    break
