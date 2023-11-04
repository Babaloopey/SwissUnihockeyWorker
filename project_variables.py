import tkinter as tk
import os as os
import pandas as pd

# Includes all globally callable variables

base_key = 'https://api-v2.swissunihockey.ch/api/'
config_file = 'config.json'

button_colour = "#265143"

root = tk.Tk()
root.title("Spielplanerstellung")


def update_teams():
    if os.path.exists(config_file):
        teams = pd.read_json(config_file)
    else:
        # Create a default teams DataFrame or load some initial data
        teams = create_default_teams()

    return teams


def create_default_teams():
    # Create a default DataFrame or load initial data
    # You can customize this part according to your requirements
    data = [
        {"description": "Eintracht Berom\u00fcnster", "id": 417058},
        {"description": "Herren KF 3. Liga", "id": 428216}, {"description": "Herren KF 4. Liga II", "id": 428649},
        {"description": "Junioren A", "id": 428055}, {"description": "Junioren B", "id": 428960},
        {"description": "Junioren C", "id": 428603}, {"description": "Damen KF 2. Liga", "id": 428361},
        {"description": "Damen KF 3. Liga II", "id": 432100}, {"description": "Juniorinnen B", "id": 430452}
    ]

    default_teams = pd.DataFrame(data)

    # Save the default teams DataFrame to the config_file
    default_teams.to_json(config_file, orient='records')

    return default_teams
