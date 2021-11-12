# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import os


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

import threading
import time

from nltk import data, downloader

DATA_IDS = ('wordnet',)


#------------------CLASS-SEPARATOR------------------#


class DataManager():
    def __init__(self, application_id="com.github.hezral.quickword", *args, **kwargs):

        self.nltk_data_path = os.path.join(GLib.get_user_data_dir(), application_id, 'nltk_data')

        # setup paths
        data.path = [self.nltk_data_path]
        downloader.download_dir = self.nltk_data_path
        
        # check if data dir exist
        if not os.path.exists(self.nltk_data_path):
            os.makedirs(self.nltk_data_path)

    def update_data(self, callback=None):
        # check if any data is stale and update it
        stale = 0
        for id in DATA_IDS:
            if downloader.Downloader().is_stale(id, self.nltk_data_path):
                stale += 1
                GLib.idle_add(callback, "Updating", id + " has an update")
                time.sleep(0.5)
            else:
                GLib.idle_add(callback, "No Updates", id + " is up-to-date")
        if stale > 0:
            GLib.idle_add(callback, "Updates Available", "There are " + str(stale) + "data updates available for download")
            time.sleep(0.5)
            downloader.Downloader().update(quiet=False, prefix=self.nltk_data_path)
            time.sleep(0.5)
            GLib.idle_add(callback, "Completed", "All data has been updated.")
        else:
            time.sleep(0.5)
            GLib.idle_add(callback, "No Updates", "All data is up-to-date.")

    def download_data(self, callback=None):   
        # download data if not installed
        for id in DATA_IDS:
            if not downloader.Downloader().is_installed(id, self.nltk_data_path):
                GLib.idle_add(callback, "Downloading...", "Downloading " + id)
                time.sleep(0.5)
                downloader.Downloader().download(id)
                time.sleep(0.5)
                GLib.idle_add(callback, "Downloading", id + " data has been downloaded.")
                time.sleep(0.5)
                GLib.idle_add(callback, "Completed", "All data has been downloaded.")
            else:
                time.sleep(0.5)
                GLib.idle_add(callback, "Downloaded", "All data has already been downloaded.")
        


    def run_func(self, runname=None, callback=None):
        if runname == "download":
            target = self.download_data
        else:
            target = self.update_data
        thread = threading.Thread(target=target, args=(callback,))
        thread.daemon = True
        thread.start()


