import tkinter as tk

import json

import requests
import pandas as pd
import helpers
import gui
import projectVariables

base_key = 'https://api-v2.swissunihockey.ch/api/'
configFile = 'config.json'

# creates the whole gui at the start and then hides id
root = tk.Tk()
root.title("Konfigurationsabfrage")
root.iconbitmap("ball.ico")
root.resizable(False, False)

canvas = tk.Canvas(root, height=700, width=650)
canvas.pack()

# Layout of Window
titelFrame = tk.Frame(root)
titelFrame.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.05)

searchcolumn1 = tk.Frame(root)
searchcolumn1.place(relwidth=0.25, relheight=0.07, relx=0.15, rely=0.13)

searchcolumn2 = tk.Frame(root)
searchcolumn2.place(relwidth=0.25, relheight=0.07, relx=0.375, rely=0.13)

searchcolumn3 = tk.Frame(root)
searchcolumn3.place(relwidth=0.25, relheight=0.07, relx=0.65, rely=0.123)

textFrame1 = tk.Frame(root)
textFrame1.place(relwidth=0.35, relheight=0.78, relx=0.1, rely=0.22)

textFrame2 = tk.Frame(root)
textFrame2.place(relwidth=0.3, relheight=0.78, relx=0.4, rely=0.22)

textFrame3 = tk.Frame(root)
textFrame3.place(relwidth=0.2, relheight=0.78, relx=0.7, rely=0.22)

# searchbar in configWindow
inputLabel = tk.Label(searchcolumn1, text="Clubsuche:", width=50, fg="black", font=("Arial", 10))
inputLabel.pack()
input = tk.Entry(searchcolumn2, fg="black", bg="white", width=50, font=("Arial", 10))
input.pack()
submitBtn = tk.Button(searchcolumn3, text="Suchen", fg="white", bg=projectVariables.buttoncolour, width=50,
                      font=("Arial", 10),
                      command=lambda: getAllClubs(input.get()))
submitBtn.pack()

root.withdraw()



# shows configWindow
def showWindow():
    root.deiconify()
    clearConfigWindow()

    greeting = tk.Label(titelFrame, text="Konfiguration der Ids", font=("Arial", 25))
    greeting.pack()

    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()

def onClosing():
    root.withdraw()

# gets all Clubs and show the matching ones with a button on the side
def getAllClubs(searchTerm):
    clubs = []
    global globalSearchTerm
    globalSearchTerm = searchTerm
    print(globalSearchTerm)

    clearConfigWindow()

    greeting = tk.Label(titelFrame, text="Konfiguration der Ids", font=("Arial", 25))
    greeting.pack()

    # request for clubs
    r = requests.get(base_key + f'clubs')
    data = r.json()
    entries = pd.json_normalize(data['entries'])

    # checks whether entry matches with searchTerm
    for entry in entries.iterrows():
        if searchTerm.upper() in str(entry[1].iloc[0]).upper():
            clubs.append(entry[1])
    # legend for clubtable
    descriptionLabel = tk.Label(textFrame1, text="Bezeichnung", width=50, fg="black", font=('Arial 10 bold')).pack()
    idLabel = tk.Label(textFrame2, text="ID", width=50, fg="black", font=('Arial 10 bold')).pack()
    buttonLabel = tk.Label(textFrame3, text="    ", width=50, fg="black", font=('Arial 10 bold')).pack()

    # Creation of Labels and buttons for matching entries
    i = 0
    for club in clubs:
        nameLabel = tk.Label(textFrame1, text=str(club[0]), width=50, fg="black", height=1, pady="2.75",
                             font=("Arial", 10)).pack()
        idLabel = tk.Label(textFrame2, text=str(club[3]), width=50, fg="black", height=1, pady="2.75",
                           font=("Arial", 10)).pack()
        teamButton = tk.Button(textFrame3, text="Teams", width=50, fg="white", height=1,
                               bg=projectVariables.buttoncolour,
                               command=lambda c=club: getAllTeamsFromClub(c)).pack()
        i += 1


# gets all teams from club
def getAllTeamsFromClub(club):
    saison = helpers.getSaison()
    club_id = club[3]
    # request
    r = requests.get(base_key + f'teams?mode=by_club&club_id={club_id}&season={saison}')
    data = r.json()
    teamsFromClub = pd.json_normalize(data['entries'])

    clearConfigWindow()

    # puts clubname on top and creates submit and cancel button
    greeting = tk.Label(titelFrame, text=club[0], font=("Arial", 25))
    greeting.pack()
    # sends the teams to a function which saves them in the json and updates the gui
    submitButton = tk.Button(textFrame3, text="Speichern", width=50, fg="white", height=1,
                             bg=projectVariables.buttoncolour,
                             command=lambda c=club: submitTeams(teamsFromClub, club)).pack()
    # jumps back to the overview of the clubs
    cancelButton = tk.Button(textFrame3, text="Abbrechen", width=50, fg="white", height=1,
                             bg=projectVariables.buttoncolour,
                             command=lambda c=club: getAllClubs(globalSearchTerm)).pack()

    descriptionLabel = tk.Label(textFrame1, text="Bezeichnung", width=50, fg="black", font=('Arial 10 bold')).pack()
    idLabel = tk.Label(textFrame2, text="ID", width=50, fg="black", font=('Arial 10 bold')).pack()

    # Labels for teamname and id
    for teamFromClub in teamsFromClub.iterrows():
        nameLabel = tk.Label(textFrame1, text=str(teamFromClub[1].iloc[0]), width=50, fg="black", height=1, pady="2.75",
                             font=("Arial", 10)).pack()
        idLabel = tk.Label(textFrame2, text=str(teamFromClub[1].iloc[3]), width=50, fg="black", height=1, pady="2.75",
                           font=("Arial", 10)).pack()


# saves teams in dicts and fills them into config.json. Then hides the window and updates the main gui
def submitTeams(teams, club):
    print(club)
    teamDicts = []
    clubdict = {
        "description": club[0],
        "id": club[3]
    }
    teamDicts.append(clubdict)

    for team in teams.iterrows():
        teamdict = {
            "description": str(team[1].iloc[0]),
            "id": team[1].iloc[3]
        }
        teamDicts.append(teamdict)

    with open(configFile, 'w') as file:
        json.dump(teamDicts, file)

    root.withdraw()

    gui.createGui()


# clears grid from configWindow to update data later
def clearConfigWindow():
    for widget in textFrame1.winfo_children():
        widget.destroy()

    for widget in textFrame2.winfo_children():
        widget.destroy()

    for widget in textFrame3.winfo_children():
        widget.destroy()
    for widget in titelFrame.winfo_children():
        widget.destroy()
