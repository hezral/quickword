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
from gi.repository import GLib
from nltk import data, downloader



#------------------CLASS-SEPARATOR------------------#
DATA_IDS = ('wordnet', 'omw', 'cmudict')


class DataUpdater():
    def __init__(self, application_id=None, *args, **kwargs):

        application_id = "com.github.hezral.quickword"

        self.nltk_data_path = os.path.join(GLib.get_user_data_dir(), application_id, 'nltk_data')

        # setup paths
        data.path = [self.nltk_data_path]
        downloader.download_dir = self.nltk_data_path
        
        # check if data dir exist
        if not os.path.exists(self.nltk_data_path):
            os.makedirs(self.nltk_data_path)
        # else:
        #     print('nltk_data_path:', self.nltk_data_path)

    def download_data(self):    
        # download data if not installed
        for id in DATA_IDS:
            if not downloader.Downloader().is_installed(id, self.nltk_data_path):
                downloader.Downloader().download(id)
                return (id + ': installed')
            else:
                return (id + ': installed')

    def update_data(self):
        # check if any data is stale and update it
        stale = 0
        for id in DATA_IDS:
            if downloader.Downloader().is_stale(id, self.nltk_data_path):
                stale += 1
                print(id, ': stale')
            else:
                print(id, ': up-to-date')
        if stale > 0:
            print('There are', stale, 'data. Updating..')
            downloader.Downloader().update(quiet=False, prefix=self.nltk_data_path)
        else:
            print('All data up-to-date')


updater = DataUpdater()


import threading
from threading import Thread
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


def app_main():
    win = Gtk.Window(default_height=50, default_width=300)
    win.connect("destroy", Gtk.main_quit)

    progress = Gtk.ProgressBar(show_text=True)
    win.add(progress)

    def update_progess(i):
        progress.pulse()
        progress.set_text(str(i))
        return False

    def example_target():
        for id in DATA_IDS:
            if not downloader.Downloader().is_installed(id, updater.nltk_data_path):
                downloader.Downloader().download(id)
                GLib.idle_add(update_progess, id + ': already finished')
                time.sleep(0.2)
            else:
                GLib.idle_add(update_progess, id + ': installed')
                time.sleep(0.2)
            update_progess("finished")

            

    win.show_all()

    thread = threading.Thread(target=example_target)
    thread.daemon = True
    thread.start()

class app_thread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


if __name__ == "__main__":
    app_main()
    Gtk.main()
