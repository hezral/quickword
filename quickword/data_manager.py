#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of QuickWord ("Application").

    The Application is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The Application is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this Application.  If not, see <http://www.gnu.org/licenses/>.
'''

import os


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

import threading
import time

from nltk import data, downloader

DATA_IDS = ('wordnet',)


#------------------CLASS-SEPARATOR------------------#


class DataUpdater():
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

# #------------------CLASS-SEPARATOR------------------#


class UpdateWindow(Gtk.Dialog):
    def __init__(self, parent_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- UpdateDialog construct--------#
        self.props.name = "QuickWord Data Manager"
        self.props.transient_for = parent_window
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.modal = True

        

# updater = DataUpdater()

# try:
#     updater.update_data()
# except:
#     print("update failed")



# def app_main():
#     win = Gtk.Window(default_height=50, default_width=300)
#     win.connect("destroy", Gtk.main_quit)

#     progress = Gtk.ProgressBar(show_text=True)
#     spinner = Gtk.Spinner()
#     label = Gtk.Label()
#     label.props.expand = True

#     grid = Gtk.Grid()
#     grid.props.expand = True
#     grid.attach(spinner, 0, 1, 1, 1)
#     grid.attach(label, 0, 2, 1, 1)
#     grid.attach(progress, 0, 3, 1, 1)


#     win.add(grid)

#     def update_progess(i, fraction):
#         progress.pulse()
#         progress.set_text(str(i))
#         if fraction == 1:
#             progress.set_fraction(fraction)
#         else:
#             progress.set_pulse_step(fraction)
#         return False

#     def example_target():
#         spinner.start()
#         fraction = 1 / len(DATA_IDS)
#         for id in DATA_IDS:
            
#             if not downloader.Downloader().is_installed(id, updater.nltk_data_path):
#                 downloader.Downloader().download(id)
#                 GLib.idle_add(update_progess, id + ': installed', fraction)
#                 #time.sleep(0.5)
#                 label.set_label(id + ': already finished')
#             else:
#                 GLib.idle_add(update_progess, id + ': installed', fraction)
#                 label.set_label(id + ': already installed')
#             time.sleep(0.5)
#             fraction = fraction + 0.3
#         spinner.stop()
#         label.set_label('finished')
#         update_progess("finished", 1)

#     win.show_all()

#     thread = threading.Thread(target=example_target)
#     thread.daemon = True
#     thread.start()

# # if __name__ == "__main__":
# #     app_main()
# #     Gtk.main()


