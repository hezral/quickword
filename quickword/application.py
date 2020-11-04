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

# base imports
import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject

from datetime import datetime

print(datetime.now(), "python_run", )

# QuickWord imports
from main_window import QuickWordWindow
from clipboard_manager import ClipboardListener, ClipboardPaste
from word_lookup import WordLookup


#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set application properties
        self.props.application_id = "com.github.hezral.quickword"

        # initialize any objects
        self.window = None

        # first run
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
        first_run = False
        if first_run:
            from data_manager import DataUpdater
            data_updater = DataUpdater(application_id=self.props.application_id)
            print(datetime.now(), "updater initiated")

        # initialize word lookup
        _word_lookup = WordLookup(application_id=self.props.application_id)
        print(datetime.now(), "word lookup init")
        
        # initialize clipboard listener and get current selected text if any
        clipboard_listener = ClipboardListener()
        self.lookup_word = clipboard_listener.copy_selected_text()
        
        # default if no word found or selected
        if self.lookup_word is None or self.lookup_word == "" or self.lookup_word == " ":
            self.lookup_word = "QuickWord"
        else:
            word_data = _word_lookup.get_synsets(self.lookup_word)
        
        # initialize clipboard paster
        clipboard_paste = ClipboardPaste()

        # setup clipboard listener and paster after app activation
        self.connect_after("activate", self.on_activate, clipboard_listener, clipboard_paste, _word_lookup)
        
        # set CSS provider
        provider = Gtk.CssProvider()
        provider.load_from_path("data/application.css")
        # # provider.load_from_resource ("com/github/hezral/quickword/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Add custom signals for callback from manual word lookup in no-word-view
        # GObject.signal_new(signal_name, type, flags, return_type, param_types)
        GObject.signal_new("on-new-word-entered", Gtk.Application, GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, [GObject.TYPE_STRING])
        self.connect("on-new-word-entered", self.on_new_word_lookup, _word_lookup)

        print(datetime.now(), "app init")

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
            self.window = QuickWordWindow(application=self, lookup_word=self.lookup_word, lookup_data=None)
            self.add_window(self.window)
            self.window.show_all()

        print(datetime.now(), "startup")

    def do_activate(self):
        print(datetime.now(), "activate")

    def on_activate(self, app, clipboard_listener, clipboard_paste, _word_lookup):
        # setup listener for new text selection
        clipboard_listener.clipboard.connect("owner-change", self.on_new_word_selected, clipboard_listener, _word_lookup)
        print(datetime.now(), "cliboard listener initiated")

        # setup background updater
        print(datetime.now(), "background updater initiated")

        # setup paster for copying texts in word-view
        stack = self.window.get_window_child_widgets()[1]
        word_view = stack.get_child_by_name("word-view")
        word_view.clipboard_paste = clipboard_paste

        print(datetime.now(), "post-activate")

    def on_new_word_selected(self, clipboard, event, clipboard_listener, _word_lookup):
        # get selected word from clipboard
        new_word = clipboard_listener.copy_selected_text()

        # trigger new word lookup
        self.on_new_word_lookup(self, new_word, _word_lookup)

    def on_new_word_lookup(self, app, new_word, _word_lookup):
        
        word_data = _word_lookup.get_synsets(new_word)

        print(word_data)
        if word_data is not None:
            # emit the signal to trigger content update callback
            self.window.emit("on-new-word-selected", new_word)



    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

#------------------CLASS-SEPARATOR------------------#

if __name__ == "__main__":
    app = QuickWordApp()
    app.run(sys.argv)


