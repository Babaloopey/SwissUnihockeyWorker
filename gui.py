import math
import tkinter as tk

import all_games
import configuration_script
import project_variables
import team_games

root = project_variables.root


# calculates how big the gui has to be
def lines_in_gui(teams):
    button_height = 50
    print(math.ceil(len(teams) / 3))
    return math.ceil(len(teams) / 3) * button_height


def create_gui():
    for widget in root.winfo_children():
        widget.destroy()

    teams = project_variables.update_teams()
    club_name = teams.iloc[0]

    canvas = tk.Canvas(root, height=(70 + lines_in_gui(teams)), width=650)
    canvas.pack()

    title_frame = tk.Frame(root)
    title_frame.place(relwidth=0.8, height=40, relx=0.00, rely=0.05)
    config_frame = tk.Frame(root)
    config_frame.place(relwidth=0.2, height=40, relx=0.8, rely=0.05)

    # columns for a grid in the gui
    column1 = tk.Frame(root)
    column1.place(relwidth=0.25, relheight=0.75, relx=0.05, y=70)

    column2 = tk.Frame(root)
    column2.place(relwidth=0.25, relheight=0.75, relx=0.375, y=70)

    column3 = tk.Frame(root)
    column3.place(relwidth=0.25, relheight=0.75, relx=0.7, y=70)

    greeting = tk.Label(title_frame, text=club_name[0], font=("Calibri", 25))
    greeting.pack()

    btn_configuration = tk.Button(config_frame, text="Konfiguration", fg="black", bg="#eddcd9",
                                  command=lambda: configuration_script.show_window()).pack()

    # Team-Ids from Swissunihockey. Are used with the buttons.
    # Dynamically created buttons from the config.json. makes sure the buttons are evenly distributed
    for team in teams.iterrows():
        if team[0] < (len(teams) / 3):
            tk.Button(column1, text=team[1].description, padx=10, pady=10, fg="white",
                      bg=project_variables.button_colour,
                      width=50,
                      command=lambda c=team: call_distributor(c, club_name)).pack()
        elif team[0] < (len(teams) / 3 * 2):
            tk.Button(column2, text=team[1].description, padx=10, pady=10, fg="white",
                      bg=project_variables.button_colour,
                      width=50,
                      command=lambda c=team: call_distributor(c, club_name)).pack()
        elif team[0] < (len(teams) / 3 * 3):
            tk.Button(column3, text=team[1].description, padx=10, pady=10, fg="white",
                      bg=project_variables.button_colour,
                      width=50,
                      command=lambda c=team: call_distributor(c, club_name)).pack()

    # Buttons for the gui

    root.protocol("WM_DELETE_WINDOW", end_application)
    root.mainloop()


# Looks whether allGames must be called or TeamGames since it cannot be defined in the buttons themself
def call_distributor(team, club_name):
    print(club_name[0])
    wait_animation()
    if str(club_name[0]) == str(team[1].description):
        all_games.get_all_games(team[1].id)
    else:
        team_games.get_team_games(team[1].id)

    create_gui()


def wait_animation():
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, height=(70 + lines_in_gui(project_variables.update_teams())), width=650)
    canvas.pack()

    loading_frame = tk.Frame(root)
    loading_frame.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.4)

    loading_label = tk.Label(loading_frame, text="Spielplan wird erstellt...", font=("Calibri", 30))
    loading_label.pack()


def end_application():
    configuration_script.root.destroy()
    root.destroy()
