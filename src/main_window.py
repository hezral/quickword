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
from gi.repository import Gtk, Gio, Granite, GObject, GLib

from .settings_view import SettingsView
from .noword_view import NoWordView
from .word_view import WordView
from .updater_view import UpdaterView

#------------------CLASS-SEPARATOR------------------#


class QuickWordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom signals to detect new word selected
        # GObject.signal_new(signal_name, type, flags, return_type, param_types)
        # param_types is a list example [GObject.TYPE_PYOBJECT, GObject.TYPE_STRING]
        GObject.signal_new("on-new-word-selected", Gtk.ApplicationWindow, GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, [GObject.TYPE_PYOBJECT])
        self.connect("on-new-word-selected", self.on_new_word_selected)

        self.lookup_word = "QuickWord"
        self.app = self.props.application

        self.updater_view = UpdaterView()
        self.noword_view = NoWordView()
        self.word_view = WordView()
        self.settings_view = SettingsView(app=self.app)
        
        self.stack = Gtk.Stack()
        self.stack.props.margin = 20
        self.stack.props.margin_top = 0
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.stack.add_named(self.word_view, self.word_view.get_name())
        self.stack.add_named(self.settings_view, self.settings_view.get_name())
        self.stack.add_named(self.noword_view, self.noword_view.get_name())
        self.stack.add_named(self.updater_view, self.updater_view.get_name())
        
        self.headerbar = self.generate_headerbar()

        self.props.resizable = False #set this and window will expand and retract based on child
        self.title = "QuickWord"
        self.set_keep_above(True)
        self.get_style_context().add_class("rounded")
        self.set_size_request(600, -1) #set width to -1 to expand and retract based on content
        self.props.window_position = Gtk.WindowPosition.MOUSE
        # self.props.border_width = 20
        self.set_titlebar(self.headerbar)
        self.add(self.stack)
        self.show_all()

        self.on_start_settings()

        self.on_view_visible()

    def on_start_settings(self):
        if self.app.gio_settings.get_value("sticky-mode"):
            self.stick()
        if not self.app.gio_settings.get_value("persistent-mode"):
            if self.app.window_manager is not None:
                self.app.window_manager._run(callback=self.on_persistent_mode)

    def on_persistent_mode(self, wm_class):
        if wm_class is not None:
            if self.app.props.application_id.split(".")[-1] not in wm_class:
                if self.app.running:
                    print("destroy")
                    self.destroy()

    def on_enter_word_label(self, *args):
        word_grid = self.word_box.get_child()
        edit_img = [child for child in word_grid.get_children() if isinstance(child, Gtk.Image)][0]
        # show widget and set flags to trigger transition effect, see application.css
        if self.stack.get_visible_child_name() == "word-view":
            edit_img.show()
            edit_img.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

    def on_leave_word_label(self, *args):
        word_grid = self.word_box.get_child()
        edit_img = [child for child in word_grid.get_children() if isinstance(child, Gtk.Image)][0]
        # hide and reset state flagss to ready state for transition effect, see application.css
        if self.stack.get_visible_child_name() == "settings-view":
            pass
        else:
            edit_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

    def on_new_word_selected(self, window, word_data):
        self.lookup_word = word_data[0]
        self.word_label.props.label = word_data[0]
        self.stack.set_visible_child(self.word_view)
        self.word_view.on_wordlookup(data=word_data)

    def on_manual_lookup(self, eventbutton=None, eventbox=None, not_found=False, *args):
        message = [child for child in self.noword_view.get_children() if child.get_name() == "message"][0]

        if self.stack.get_visible_child_name() == "word-view":
            if not_found:
                message.props.label = "Word not found"
            else:
                message.props.label = "Lookup a new word"
            
            # need to clear entry text since clipboard_listener will pickup the text as it will be selected on focus and cause a loop back to the word-view
            entry = [child for child in self.noword_view.get_children() if isinstance(child, Gtk.Entry)][0]
            entry.props.text = ""
            #need to show since it was hiddden in on_view_visible
            self.noword_view.show()
            self.stack.set_visible_child_name(name="no-word-view")
            self.word_label.props.label = "QuickWord"
            self.active_view = self.noword_view
            self.current_view = "no-word-view"

    def generate_viewswitch(self):
        self.view_switch = Granite.ModeSwitch.from_icon_name("com.github.hezral.quickword-symbolic", "preferences-system-symbolic")
        self.view_switch.props.valign = Gtk.Align.CENTER
        self.view_switch.props.halign = Gtk.Align.END
        self.view_switch.props.hexpand = True
        self.view_switch.props.margin = 4
        self.view_switch.props.name = "view-switch"
        self.view_switch.connect_after("notify::active", self.on_view_visible)
        return self.view_switch

    def generate_headerbar(self):
        self.word_label = Gtk.Label("QuickWord")
        self.word_label.props.vexpand = True
        self.word_label.get_style_context().add_class("lookup-word-header")

        edit_img = Gtk.Image().new_from_icon_name("insert-text-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        edit_img.props.no_show_all = True
        edit_img.get_style_context().add_class("transition-on")

        word_grid = Gtk.Grid()
        word_grid.props.column_spacing = 4
        word_grid.props.halign = Gtk.Align.START
        word_grid.props.valign = Gtk.Align.CENTER
        word_grid.attach(self.word_label, 0, 0, 1, 1)
        word_grid.attach(edit_img, 1, 0, 1, 1)

        self.word_box = Gtk.EventBox()
        self.word_box.add(word_grid)
        self.word_box.connect("button-press-event", self.on_manual_lookup)
        self.word_box.connect("enter-notify-event", self.on_enter_word_label)
        self.word_box.connect("leave-notify-event", self.on_leave_word_label)

        titlebar_grid = Gtk.Grid()
        titlebar_grid.props.hexpand = True
        titlebar_grid.attach(self.word_box, 0, 0, 1, 1)
        titlebar_grid.attach(self.generate_viewswitch(), 1, 0, 1, 1)

        headerbar = Gtk.HeaderBar()
        headerbar.props.custom_title = titlebar_grid
        headerbar.props.show_close_button = False
        headerbar.props.decoration_layout = "close:"
        headerbar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        return headerbar

    def on_view_visible(self, viewswitch=None, gparam=None):

        def set_word_view():
            if self.app.lookup_word is None:
                print("noword_view")
                # self.noword_view.set_visible(True)
                self.word_label.props.label = "Quickword"
                self.stack.set_visible_child(self.noword_view)
                # GLib.timeout_add(1000, self.stack.set_visible_child, self.noword_view)
            else:
                print("word_view")
                self.word_label.props.label = self.lookup_word
                self.stack.set_visible_child(self.word_view)
                # GLib.timeout_add(1000, self.stack.set_visible_child, self.word_view)

        # app first-run
        # first-run >> download data view >> no word view or selected word view

        if self.app.first_run:
            print("first-run")
            self.stack.set_visible_child(self.updater_view)

        if not self.app.first_run:
            print("normal-run")
            if viewswitch is not None:
                if viewswitch.props.active:
                    self.settings_view.on_totalwords()
                    self.stack.set_visible_child(self.settings_view)
                    self.word_label.props.label = "Settings"
                else:
                    set_word_view()
            else:
                set_word_view()

        # app normal-run >> no word view or selected word view

        # app running
        # no word view >> settings view
        # settings view >> no word view
        # settings view >>> selected word view
        # settings view >> updater view
        # updater view >> no word view
        # updater view >> selected word view