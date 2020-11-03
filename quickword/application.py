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


import sys, os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject, Pango

from datetime import datetime

print("python_run", datetime.now())

# QuickWord imports
from main_window import QuickWordWindow
from clipboard import ClipboardListener, ClipboardPaste
from lookup import WordLookup
from updater import DataUpdater

#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set application properties
        self.props.application_id = "com.github.hezral.quickword"

        provider = Gtk.CssProvider()
        provider.load_from_path("/home/adi/Work/quickword/data/application.css")
        # # provider.load_from_resource ("com/github/hezral/quickword/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # initialize any objects
        self.window = None

        first_run = True
        if first_run:
            from updater import DataUpdater
            data_updater = DataUpdater()
            print("updater initiated", datetime.now())
        
        # initialize clipboard listener and get current selected text if any
        clipboard_listener = ClipboardListener()
        lookup_word = clipboard_listener.copy_selected_text()
        
        # setup listener for new text selection
        clipboard_listener.clipboard.connect("owner-change", clipboard_listener.copy_selected_text)

        # initialize clipboard paster
        clipboard_paste = ClipboardPaste()

        print("init", datetime.now())

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # setup quiting app using Escape, Ctrl+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])
        
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = QuickWordWindow(application=self)
            self.add_window(self.window)
            self.window.show_all()
            
        print("startup", datetime.now())

    def do_activate(self):
        print("activate", datetime.now())


        
        # run updater in background
        import io
        from updater import DataUpdater
        data_updater = DataUpdater()

        # redirect sys.stdout to a buffer
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        while data_updater.update_data():
            print("updating:", sys.stdout.getvalue())
        
        # get output and restore sys.stdout
        #output = sys.stdout.getvalue()
        sys.stdout = stdout

        #print("output:", output)

        print("background updater initiated", datetime.now())



    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

#------------------CLASS-SEPARATOR------------------#

if __name__ == "__main__":
    app = QuickWordApp()
    app.run(sys.argv)


