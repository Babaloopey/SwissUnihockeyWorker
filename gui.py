import tkinter as tk
import configurationScript
import math
import projectVariables
import allGames
import teamGames

root = projectVariables.root


# calculates how big the gui has to be
def linesInGui(teams):
    buttonheight = 50
    print(math.ceil(len(teams) / 3))
    return (math.ceil(len(teams) / 3) * buttonheight)


def createGui():
    for widget in root.winfo_children():
        widget.destroy()

    teams = projectVariables.updateTeams()
    clubname = teams.iloc[0]

    canvas = tk.Canvas(root, height=(70 + linesInGui(teams)), width=650)
    canvas.pack()

    titelFrame = tk.Frame(root)
    titelFrame.place(relwidth=0.8, height=40, relx=0.00, rely=0.05)
    configFrame = tk.Frame(root)
    configFrame.place(relwidth=0.2, height=40, relx=0.8, rely=0.05)

    # columns for a grid in the gui
    column1 = tk.Frame(root)
    column1.place(relwidth=0.25, relheight=0.75, relx=0.05, y=70)

    column2 = tk.Frame(root)
    column2.place(relwidth=0.25, relheight=0.75, relx=0.375, y=70)

    column3 = tk.Frame(root)
    column3.place(relwidth=0.25, relheight=0.75, relx=0.7, y=70)

    greeting = tk.Label(titelFrame, text=clubname[0], font=("Calibri", 25))
    greeting.pack()

    btn_configuration = tk.Button(configFrame, text="Konfiguration", fg="black", bg="#eddcd9",
                                  command=lambda: configurationScript.showWindow()).pack()

    # Team-Ids from swissunihockey. Are used with the buttons.
    # Dynamically created buttons from the config.json. makes sure the buttons are evenly distributed
    for team in teams.iterrows():
        if (team[0] < (len(teams) / 3)):
            tk.Button(column1, text=team[1].description, padx=10, pady=10, fg="white", bg=projectVariables.buttoncolour,
                      width=50,
                      command=lambda c=team: callDistributor(c, clubname)).pack()
        elif (team[0] < (len(teams) / 3 * 2)):
            tk.Button(column2, text=team[1].description, padx=10, pady=10, fg="white", bg=projectVariables.buttoncolour,
                      width=50,
                      command=lambda c=team: callDistributor(c, clubname)).pack()
        elif (team[0] < (len(teams) / 3 * 3)):
            tk.Button(column3, text=team[1].description, padx=10, pady=10, fg="white", bg=projectVariables.buttoncolour,
                      width=50,
                      command=lambda c=team: callDistributor(c, clubname)).pack()

    # Buttons for the gui

    root.mainloop()


# Looks whether allGames must be called or TeamGames since it cannot be defined in the buttons themself
def callDistributor(team, clubname):
    print(clubname[0])
    if str(clubname[0]) == str(team[1].description):
        allGames.getAllGames(team[1].id)
    else:
        teamGames.getTeamGames(team[1].id)
