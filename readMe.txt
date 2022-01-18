This is an unofficial Spielplanerstellungs- application from "STV Eintracht Beromünster" other Clubs can be selected as well
Created with the official API of swissunihockey v 2.32.2
https://api-v2.swissunihockey.ch/api/doc

Installation Guide:
	Download the whole registry.
	Edit the config File to your liking.
	Start main.exe in /main

	Maybe you have to install python in advance: https://www.python.org/downloads/

You may adjust the Ids in the config.json located in this directory. The application builds the gui based on this file

This is v1.1 at the time of 12.01.2022

Update Log:
Bugfix +0.01
Major Update + 0.1
Rework +1

Version	Date		Action
--------------------------------------
1.0/ 11.01.22	Application first published
1.1/ 12.01.22   Configuration Window and dynamic gui implemented
1.11 18.01.22   Bug fixed when determining opponent after reconfiguring




Do not use for commercial use. This is a free project. You may distribute and share it.
created by Florin Rüedi, Basislehrjahr 2022

Documentation:
    main.exe -> Starts the application
    gui.py -> Manages the whole gui
    projecctVariables.py -> Manages global project-variables
    allGames.py -> Manages how the data for allGames is handled
    teamGames.py -> Manages how the data for a Team is handled
    helpers.py -> Functions which are used from more than 1 module, such as data-formating functions
    configurationScript.py -> Manages the whole configuration window and how things get saved in the config.json
    config.json -> holds the data for the gui. Can be changed manually or through the "Konfigurieren" button













