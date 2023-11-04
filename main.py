# To Reduce Errors in production
import os
import sys

import gui


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("_internal/assets/cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()


# This is a the swiss Unihockey Worker from Eintracht Beromünster
# You may change the Id's in the config File. Ids can be found on swissunihockey. Supposedly over the api v-2
# https://api-v2.swissunihockey.ch/api/doc

# Starts the gui and gets ready for all interaction
def start():
    gui.create_gui()


# starts
start()
