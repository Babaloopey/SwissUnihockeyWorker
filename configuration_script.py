import json
import tkinter as tk
from tkinter import messagebox

import pandas as pd
import requests

import gui
import helpers
import project_variables

base_key = 'https://api-v2.swissunihockey.ch/api/'
config_file = 'config.json'
global global_search_term

# creates the whole gui at the start and then hides id
root = tk.Tk()
root.title("Konfigurationsabfrage")
root.resizable(False, False)

canvas = tk.Canvas(root, height=700, width=650)
canvas.pack()

# Layout of Window
titel_frame = tk.Frame(root)
titel_frame.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.05)

search_column1 = tk.Frame(root)
search_column1.place(relwidth=0.25, relheight=0.07, relx=0.15, rely=0.13)

search_column2 = tk.Frame(root)
search_column2.place(relwidth=0.25, relheight=0.07, relx=0.375, rely=0.13)

search_column3 = tk.Frame(root)
search_column3.place(relwidth=0.25, relheight=0.07, relx=0.65, rely=0.123)

text_frame1 = tk.Frame(root)
text_frame1.place(relwidth=0.35, relheight=0.78, relx=0.1, rely=0.22)

text_frame2 = tk.Frame(root)
text_frame2.place(relwidth=0.3, relheight=0.78, relx=0.4, rely=0.22)

text_frame3 = tk.Frame(root)
text_frame3.place(relwidth=0.2, relheight=0.78, relx=0.7, rely=0.22)

# searchbar in configWindow
input_label = tk.Label(search_column1, text="Clubsuche:", width=50, fg="black", font=("Arial", 10))
input_label.pack()
input_entry = tk.Entry(search_column2, fg="black", bg="white", width=50, font=("Arial", 10))
input_entry.pack()
submit_btn = tk.Button(search_column3, text="Suchen", fg="white", bg=project_variables.button_colour, width=50,
                       font=("Arial", 10),
                       command=lambda: get_all_clubs(input_entry.get()))
submit_btn.pack()

root.withdraw()


# shows configWindow
def show_window():
    root.deiconify()
    clear_config_window()

    greeting = tk.Label(titel_frame, text="Konfiguration der Ids", font=("Arial", 25))
    greeting.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def on_closing():
    root.withdraw()


# gets all Clubs and show the matching ones with a button on the side
def get_all_clubs(search_term):
    clubs = []
    global global_search_term
    global_search_term = search_term
    print(global_search_term)

    clear_config_window()

    greeting = tk.Label(titel_frame, text="Konfiguration der Ids", font=("Arial", 25))
    greeting.pack()

    # request for clubs
    try:
        r = requests.get(base_key + f'clubs')
        data = r.json()
        entries = pd.json_normalize(data['entries'])
    except Exception as ex:
        messagebox.showerror(title="Fehler", message=f'Fehler bei der Request: {ex}')
        return

    # checks whether entry matches with search_term
    for entry in entries.iterrows():
        if search_term.upper() in str(entry[1].iloc[0]).upper():
            clubs.append(entry[1])
    # legend for clubtable
    description_label = tk.Label(text_frame1, text="Bezeichnung", width=50, fg="black", font='Arial 10 bold').pack()
    id_label = tk.Label(text_frame2, text="ID", width=50, fg="black", font='Arial 10 bold').pack()
    button_label = tk.Label(text_frame3, text="    ", width=50, fg="black", font='Arial 10 bold').pack()

    # Creation of Labels and buttons for matching entries
    i = 0
    for club in clubs:
        name_label = tk.Label(text_frame1, text=str(club[0]), width=50, fg="black", height=1, pady="2.75",
                              font=("Arial", 10)).pack()
        id_label = tk.Label(text_frame2, text=str(club[3]), width=50, fg="black", height=1, pady="2.75",
                            font=("Arial", 10)).pack()
        team_btn = tk.Button(text_frame3, text="Teams", width=50, fg="white", height=1,
                             bg=project_variables.button_colour,
                             command=lambda c=club: get_all_teams_from_club(c)).pack()
        i += 1


# gets all teams from club
def get_all_teams_from_club(club):
    saison = helpers.get_season()
    club_id = club[3]
    # request
    try:
        r = requests.get(base_key + f'teams?mode=by_club&club_id={club_id}&season={saison}')
        data = r.json()
        teams_from_club = pd.json_normalize(data['entries'])
    except Exception as ex:
        messagebox.showerror(title="Fehler", message=f'Fehler bei der Request: {ex}')
        return

    clear_config_window()

    # puts clubname on top and creates submit and cancel button
    greeting = tk.Label(titel_frame, text=club[0], font=("Arial", 25))
    greeting.pack()
    # sends the teams to a function which saves them in the json and updates the gui
    save_btn = tk.Button(text_frame3, text="Speichern", width=50, fg="white", height=1,
                         bg=project_variables.button_colour,
                         command=lambda c=club: submit_teams(teams_from_club, club)).pack()
    # jumps back to the overview of the clubs
    cancel_btn = tk.Button(text_frame3, text="Abbrechen", width=50, fg="white", height=1,
                           bg=project_variables.button_colour,
                           command=lambda c=club: get_all_clubs(global_search_term)).pack()

    description_label = tk.Label(text_frame1, text="Bezeichnung", width=50, fg="black", font='Arial 10 bold').pack()
    id_label = tk.Label(text_frame2, text="ID", width=50, fg="black", font='Arial 10 bold').pack()

    # Labels for teamname and id
    for team_from_club in teams_from_club.iterrows():
        name_label = tk.Label(text_frame1, text=str(team_from_club[1].iloc[0]), width=50, fg="black", height=1,
                              pady="2.75",
                              font=("Arial", 10)).pack()
        id_label = tk.Label(text_frame2, text=str(team_from_club[1].iloc[3]), width=50, fg="black", height=1,
                            pady="2.75",
                            font=("Arial", 10)).pack()


# saves teams in dicts and fills them into config.json. Then hides the window and updates the main gui
def submit_teams(teams, club):
    print(club)
    team_dicts = []
    club_dict = {
        "description": club[0],
        "id": club[3]
    }
    team_dicts.append(club_dict)

    for team in teams.iterrows():
        team_dict = {
            "description": str(team[1].iloc[0]),
            "id": team[1].iloc[3]
        }
        team_dicts.append(team_dict)

    with open(config_file, 'w') as file:
        json.dump(team_dicts, file)

    root.withdraw()

    gui.create_gui()


# clears grid from configWindow to update data later
def clear_config_window():
    for widget in text_frame1.winfo_children():
        widget.destroy()

    for widget in text_frame2.winfo_children():
        widget.destroy()

    for widget in text_frame3.winfo_children():
        widget.destroy()
    for widget in titel_frame.winfo_children():
        widget.destroy()
