#!/usr/bin/env python3

# Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)
#
# This file is part of QuickWord ("Application").
#
# The Application is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The Application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Application.  If not, see <http://www.gnu.org/licenses/>.

import sys, os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

from .main_window import QuickWordWindow
from .clipboard_manager import ClipboardListener, ClipboardPaste
from .word_lookup import WordLookup
from .utils import HelperUtils

#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):

    clipboard_listener = ClipboardListener()
    clipboard_paste = ClipboardPaste()
    utils = HelperUtils()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.application_id = "com.github.hezral.quickword"

        self.window = None
        self.word_data = None

        self.gio_settings = Gio.Settings(schema_id=self.props.application_id)
        self.gtk_settings = Gtk.Settings().get_default()
        self.first_run = self.gio_settings.get_value("first-run")

        # initialize word lookup
        self._word_lookup = WordLookup(application_id=self.props.application_id)
        if self.first_run:
            self.generate_data_manager()
        else:
            self._word_lookup.get_synsets("a") # hack to load wordnet faster
            self.total_words = self._word_lookup.get_totalwords() # get total words in Wordnet
        
        # get current selected text
        self.lookup_word = self.clipboard_listener.copy_selected_text()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # setup quiting app using Escape, Ctrl+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        # set CSS provider
        provider = Gtk.CssProvider()
        provider.load_from_path(os.path.join(os.path.dirname(__file__), "data", "application.css"))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # prepend custom path for icon theme
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path(os.path.join(os.path.dirname(__file__), "data", "icons"))        

    def do_activate(self):
        # Only allow a single window and raise any existing ones
        if self.window is None:
            self.window = QuickWordWindow(application=self)
            self.window.word_view.clipboard_paste = self.clipboard_paste
            self.add_window(self.window)
            self.window.show_all()
            self.window.present()

        if self.lookup_word is None:
            self.lookup_word = "QuickWord"
        else:
            self.word_data = self._word_lookup.get_synsets(self.lookup_word)
            if self.word_data is not None:
                self.on_new_word_lookup(self.word_data)

        # setup listener for new text selection
        self.clipboard_listener.clipboard.connect("owner-change", self.on_new_word_selected)

    def generate_data_manager(self):
        from .data_manager import DataManager
        self._data_manager = DataManager(application_id=self.props.application_id)
        return True

    def on_new_word_selected(self, clipboard, event):
        new_word = self.clipboard_listener.copy_selected_text()
        self.on_new_word_lookup(new_word)

    def on_new_word_lookup(self, word_data):
        # check if data is string from new word selected or data from background lookup
        if isinstance(word_data, str):
            new_word = word_data
            word_data = self._word_lookup.get_synsets(new_word)

        if word_data is not None:
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


def main(version):
    app = QuickWordApp()
    return app.run(sys.argv)