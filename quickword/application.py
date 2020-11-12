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

# gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject

# thread import
from threading import Thread
from datetime import datetime

# print(datetime.now(), "python_run", )

# QuickWord imports
from main_window import QuickWordWindow
from clipboard_manager import ClipboardListener, ClipboardPaste
from word_lookup import WordLookup
from data_manager import DataUpdater
from custom_shortcut_settings import CustomShortcutSettings

#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom signals for callback from manual word lookup in no-word-view
        # GObject.signal_new(signal_name, type, flags, return_type, param_types)
        # param_types is a list example [GObject.TYPE_PYOBJECT, GObject.TYPE_STRING]
        GObject.signal_new("on-new-word-lookup", Gtk.Application, GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, [GObject.TYPE_PYOBJECT])

        # set application properties
        self.props.application_id = "com.github.hezral.quickword"
        # Gdk.set_program_class("com.github.hezral.quickword")

        # setup path
        self.modulepath = os.path.dirname(__file__)


        # initialize objects
        self.window = None
        self.word_data = None

        # initialize word lookup
        self._word_lookup = WordLookup(application_id=self.props.application_id)
        # print(datetime.now(), "word lookup background init ")

        # create data manager if first run
        if self.first_run:
            self.generate_data_manager()
        
        # initialize clipboard listener and clipboard paster
        self.clipboard_listener = ClipboardListener()
        self.clipboard_paste = ClipboardPaste()

        # get current selected text if any
        self.lookup_word = self.clipboard_listener.copy_selected_text()
        # print(datetime.now(), "self.lookup_word", self.lookup_word)

        # first run
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
        self.first_run = gio_settings.get_value("first-run")
        # print(datetime.now(), "first_run", self.first_run)
        
        # setup signal for new word lookup
        self.connect("on-new-word-lookup", self.on_new_word_lookup)

        # setup clipboard listener and paster after app activation
        self.connect_after("activate", self.after_activate)

        # Set shortcut
        SHORTCUT = "<Super><Control>d"
        ID = "gtk-launch" + " " + self.props.application_id
        _custom_shortcut_settings = CustomShortcutSettings()

        has_shortcut = False
        for shortcut in _custom_shortcut_settings.list_custom_shortcuts():
            if shortcut[1] == ID:
                has_shortcut = True

        if has_shortcut is False:
            shortcut = _custom_shortcut_settings.create_shortcut()
            if shortcut is not None:
                _custom_shortcut_settings.edit_shortcut(shortcut, SHORTCUT)
                _custom_shortcut_settings.edit_command(shortcut, ID)

 
        # print(datetime.now(), "app init")

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # setup quiting app using Escape, Ctrl+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        # set CSS provider
        provider = Gtk.CssProvider()
        provider.load_from_path(os.path.join(self.modulepath, "data/application.css"))
        # # provider.load_from_resource ("com/github/hezral/quickword/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # print(datetime.now(), "startup")

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = QuickWordWindow(application=self)
            self.add_window(self.window)
            self.window.show_all()

        # print(datetime.now(), "activate")

    def after_activate(self, app):
        # setup listener for new text selection
        self.clipboard_listener.clipboard.connect("owner-change", self.on_new_word_selected)
        # print(datetime.now(), "cliboard listener initiated")

        # setup paster for copying texts in word-view
        stack = self.window.get_window_child_widgets()[1]
        word_view = stack.get_child_by_name("word-view")
        word_view.clipboard_paste = self.clipboard_paste

        # get total words in Wordnet
        if not self.first_run:
            self.total_words = self._word_lookup.get_totalwords()

            # default if no word found or selected
            # start background lookup if word selected
            if self.lookup_word is None:
                self.lookup_word = "QuickWord"
                #self._run_background_lookup = None
            else:
                # self._run_background_lookup = RunInBackground(target=self._word_lookup.get_synsets, args=(self.lookup_word,))
                # self._run_background_lookup.start()
                # # print(datetime.now(), "lookup background init")

                # self.word_data = app._run_background_lookup.join()
                # # print(datetime.now(), "background lookup retrieved")
                self.word_data = self._word_lookup.get_synsets(self.lookup_word)

            if self.word_data is not None:
                app.emit("on-new-word-lookup", self.word_data)
                # print(datetime.now(), "emit word lookup")
            else:
                self.lookup_word = "QuickWord"

        # setup background updater
        # print(datetime.now(), "background updater initiated")

        # print(datetime.now(), "post-activate")

    def generate_data_manager(self):
        self._data_manager = DataUpdater(application_id=self.props.application_id)
        # print(datetime.now(), "updater initiated")
        return True

    def on_word_lookup_load(self, application_id):
        _word_lookup = WordLookup(application_id=application_id)
        return _word_lookup

    def on_new_word_selected(self, clipboard, event):
        # get selected word from clipboard
        new_word = self.clipboard_listener.copy_selected_text()
        # trigger new word lookup
        self.on_new_word_lookup(self, new_word)

    def on_new_word_lookup(self, app, word_data):
        # check if data is string from new word selected or data from background lookup
        if isinstance(word_data, str):
            new_word = word_data
            word_data = self._word_lookup.get_synsets(new_word)

        if word_data is not None:
            #print(word_data)
            # emit the signal to trigger content update callback
            self.window.emit("on-new-word-selected", word_data)
            # print(datetime.now(), "emit on-new-word-selected")
            return True
        else:
            # go back to no-word-view
            self.window.on_manual_lookup(not_found=True)
            return False


    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

class RunInBackground(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs)

    def join(self, *args):
        Thread.join(self, *args) 
        return self._return

#------------------CLASS-SEPARATOR------------------#

# if __name__ == "__main__":
#     app = QuickWordApp()
#     app.run(sys.argv)


