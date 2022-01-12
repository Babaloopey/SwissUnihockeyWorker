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



def showWindow():
    root = tk.Tk()
    root.title("Konfigurationsabfrage")
    root.iconbitmap("ball.ico")
    root.resizable(False, False)

    canvas = tk.Canvas(root, height=700, width=650)
    canvas.pack()

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

    greeting = tk.Label(titelFrame, text="Konfiguration der Ids", font=("Arial", 25))
    greeting.pack()

    inputLabel = tk.Label(searchcolumn1, text="Clubsuche:", width=50, fg="black", font=("Arial", 10))
    inputLabel.pack()
    input = tk.Entry(searchcolumn2, fg="black", bg="white", width=50, font=("Arial", 10))
    input.pack()
    submitBtn = tk.Button(searchcolumn3, text="Suchen", fg="white", bg="#000000", width=50, font=("Arial", 10),
                          command=lambda: getAllClubs(input.get(), textFrame1, textFrame2, textFrame3))
    submitBtn.pack()

    root.mainloop()


def getAllClubs(searchTerm, textFrame1, textFrame2, textFrame3):
    clubs = []
    global globalSearchTerm
    globalSearchTerm = searchTerm
    print(globalSearchTerm)
    for widget in textFrame1.winfo_children():
        widget.destroy()

    for widget in textFrame2.winfo_children():
        widget.destroy()

    for widget in textFrame3.winfo_children():
        widget.destroy()

    r = requests.get(base_key + f'clubs')
    data = r.json()
    entries = pd.json_normalize(data['entries'])

    for entry in entries.iterrows():
        if searchTerm.upper() in str(entry[1].iloc[0]).upper():
            clubs.append(entry[1])
    descriptionLabel = tk.Label(textFrame1, text="Bezeichnung", width=50, fg="black", font=('Arial 10 bold')).pack()
    idLabel = tk.Label(textFrame2, text="ID", width=50, fg="black", font=('Arial 10 bold')).pack()
    buttonLabel = tk.Label(textFrame3, text="    ", width=50, fg="black", font=('Arial 10 bold')).pack()
    i = 0

    for club in clubs:
        nameLabel = tk.Label(textFrame1, text=str(club[0]), width=50, fg="black", height=1, pady="2.75",
                             font=("Arial", 10)).pack()
        idLabel = tk.Label(textFrame2, text=str(club[3]), width=50, fg="black", height=1, pady="2.75",
                           font=("Arial", 10)).pack()
        teamButton = tk.Button(textFrame3, text="Teams", width=50, fg="white", height=1, bg='black',
                               command=lambda c=club: getAllTeams(c, textFrame1, textFrame2, textFrame3)).pack()
        i += 1


def getAllTeams(club, textFrame1, textFrame2, textFrame3):
    saison = getSaison()
    club_id = club[3]
    r = requests.get(base_key + f'teams?mode=by_club&club_id={club_id}&season={saison}')
    data = r.json()
    teamsFromClub = pd.json_normalize(data['entries'])

    for widget in textFrame1.winfo_children():
        widget.destroy()

    for widget in textFrame2.winfo_children():
        widget.destroy()

    for widget in textFrame3.winfo_children():
        widget.destroy()

    print()
    submitButton = tk.Button(textFrame3, text="Speichern", width=50, fg="white", height=1, bg='black',
                             command=lambda c=club: submitTeams(teamsFromClub)).pack()
    cancelButton = tk.Button(textFrame3, text="Abbrechen", width=50, fg="white", height=1, bg='black',
                             command=lambda c=club: getAllClubs(globalSearchTerm, textFrame1, textFrame2, textFrame3)).pack()

    descriptionLabel = tk.Label(textFrame1, text="Bezeichnung", width=50, fg="black", font=('Arial 10 bold')).pack()
    idLabel = tk.Label(textFrame2, text="ID", width=50, fg="black", font=('Arial 10 bold')).pack()

    for teamFromClub in teamsFromClub.iterrows():
        nameLabel = tk.Label(textFrame1, text=str(teamFromClub[1].iloc[0]), width=50, fg="black", height=1, pady="2.75",
                             font=("Arial", 10)).pack()
        idLabel = tk.Label(textFrame2, text=str(teamFromClub[1].iloc[3]), width=50, fg="black", height=1, pady="2.75",
                           font=("Arial", 10)).pack()


def getSaison():
    now = datetime.datetime.now()
    if (now.month > 3):
        saison = now.year
    else:
        saison = now.year - 1

    return saison


def submitTeams(teams):
    print(teams)
