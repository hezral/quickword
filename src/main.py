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
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite

from .main_window import QuickWordWindow
from .clipboard_manager import ClipboardListener, ClipboardPaste
from .word_lookup import WordLookup
from .active_window_manager import ActiveWindowManager
from .utils import HelperUtils

from datetime import datetime

#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):

    app_id = "com.github.hezral.quickword"
    gtk_settings = Gtk.Settings().get_default()
    gio_settings = Gio.Settings(schema_id=app_id)
    granite_settings = Granite.Settings.get_default()
    clipboard_listener = ClipboardListener()
    clipboard_paste = ClipboardPaste()
    utils = HelperUtils()
    window_manager = None
    window = None
    lookup_word = None
    word_data = None
    running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.application_id = self.app_id
        self.window_manager = ActiveWindowManager(gtk_application=self)
        self.first_run = self.gio_settings.get_value("first-run")

        # initialize word lookup
        self._word_lookup = WordLookup(application_id=self.props.application_id)
        if self.first_run:
            self.generate_data_manager()
        else:
            self._word_lookup.get_synsets("a") # hack to load wordnet faster maybe
            # self.total_words = self._word_lookup.get_totalwords() # get total words in Wordnet
            ...

        if self.gio_settings.get_value("theme-optin"):
            prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
            self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
            self.granite_settings.connect("notify::prefers-color-scheme", self.on_prefers_color_scheme)

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

        if self.window is None:
            self.window = QuickWordWindow(application=self)
            self.window.word_view.clipboard_paste = self.clipboard_paste
            self.add_window(self.window)
            self.window.present_with_time(Gdk.CURRENT_TIME)

        # get current selected text and lookup
        self.on_new_word_selected()

        self.running = True

        # setup listener for new text selection
        self.clipboard_listener.clipboard.connect("owner-change", self.on_new_word_selected)

    def generate_data_manager(self):
        from .data_manager import DataManager
        self._data_manager = DataManager(application_id=self.props.application_id)
        return True 

    def on_new_word_selected(self, clipboard=None, event=None):
        self.on_new_word_lookup(self.clipboard_listener.copy_selected_text())

    def on_new_word_lookup(self, word):
        self.lookup_word = word
        word_data = None
        if word is not None:
            word_data = self._word_lookup.get_synsets(word)

        if word_data is not None:
            # emit the signal to trigger content update callback
            self.window.emit("on-new-word-selected", word_data)
            return True
        else:
            # go back to no-word-view
            self.lookup_word = None
            self.window.on_manual_lookup(not_found=True)
            return False

    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

    def on_prefers_color_scheme(self, *args):
        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)

def main(version):
    app = QuickWordApp()
    return app.run(sys.argv)