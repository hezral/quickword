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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import GLib, Gtk, Granite, GObject, Gdk

from .settings_view import SettingsView
from .noword_view import NoWordView
from .word_view import WordView
from .updater_view import UpdaterView


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
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.stack.add_named(self.word_view, self.word_view.get_name())
        self.stack.add_named(self.settings_view, self.settings_view.get_name())
        self.stack.add_named(self.noword_view, self.noword_view.get_name())
        self.stack.add_named(self.updater_view, self.updater_view.get_name())
        
        self.headerbar = self.generate_headerbar()

        # self.props.resizable = False #set this and window will expand and retract based on child
        self.title = "QuickWord"
        self.set_keep_above(True)
        self.get_style_context().add_class("rounded")
        self.set_size_request(-1, -1) #set width to -1 to expand and retract based on content
        self.props.window_position = Gtk.WindowPosition.MOUSE
        self.set_titlebar(self.headerbar)
        self.add(self.stack)

        self.connect("key-press-event", self.on_key_press)

        self.show_all()
        self.on_start_settings()
        # hide all other views to enable window to expand and retract based on content
        self.noword_view.hide()
        self.settings_view.hide()
        self.updater_view.hide()

    def on_key_press(self, widget, eventkey):

        if not self.noword_view.entry.props.has_focus:
            if Gdk.keyval_name(eventkey.keyval).lower() == "right":
                self.stack.set_visible_child_name("settings-view")
                self.on_view_visible(view="settings-view")

            if Gdk.keyval_name(eventkey.keyval).lower() == "left":
                self.on_view_visible(view="word-view")

        if Gdk.keyval_name(eventkey.keyval).lower() == "m":
                self.on_manual_lookup()

        if self.stack.get_visible_child_name() == "word-view":
            if Gdk.keyval_name(eventkey.keyval).lower() == "n":
                self.word_view.stack.set_visible_child_name("noun")
            if Gdk.keyval_name(eventkey.keyval).lower() == "a":
                self.word_view.stack.set_visible_child_name("adjective")
            if Gdk.keyval_name(eventkey.keyval).lower() == "d":
                self.word_view.stack.set_visible_child_name("adverb")
            if Gdk.keyval_name(eventkey.keyval).lower() == "v":
                self.word_view.stack.set_visible_child_name("verb")

    def on_start_settings(self):
        self.connect("delete-event", self.on_close_window)

        if self.app.gio_settings.get_value("sticky-mode"):
            self.stick()

        if not self.app.gio_settings.get_value("persistent-mode"):
            self.headerbar.set_show_close_button(False)
            self.word_label.props.margin_left = 10
            if self.app.window_manager is not None:
                self.app.window_manager._run(callback=self.on_persistent_mode)
        else:
            self.headerbar.set_show_close_button(True)
            self.word_label.props.margin_left = 0

    def on_persistent_mode(self, wm_class):
        if wm_class is not None:
            if self.app.props.application_id.split(".")[-1] not in wm_class:
                if self.app.running:
                    self.on_close_window()

    def on_enter_word_label(self, *args):
        self.word_action_revealer.set_reveal_child(False)
        if self.stack.get_visible_child_name() == "word-view":
            self.edit_img_revealer.set_reveal_child(True)

    def on_leave_word_label(self, *args):
        if self.stack.get_visible_child_name() == "settings-view":
            pass
        if self.stack.get_visible_child_name() != "no-word-view" or self.stack.get_visible_child_name() != "updater-view":
            self.word_action_revealer.set_reveal_child(False)
            self.edit_img_revealer.set_reveal_child(False)
        if self.stack.get_visible_child_name() == "word-view":
            self.word_action_revealer.set_reveal_child(True)
            self.edit_img_revealer.set_reveal_child(False)

    def on_new_word_selected(self, window, word_data):
        self.lookup_word = word_data[0]
        self.word_label.props.label = word_data[0]
        self.word_view.on_wordlookup(data=word_data)
        self.word_view.show_all()
        self.stack.set_visible_child(self.word_view)
        self.props.resizable = True

    def on_manual_lookup(self, eventbutton=None, eventbox=None, not_found=False, *args):
        self.word_action_revealer.set_reveal_child(False)

        if self.stack.get_visible_child_name() == "word-view":
            if not_found:
                self.noword_view.message.props.label = "Word not found"
            else:
                self.noword_view.message.props.label = "Lookup a new word"
            
            # need to clear entry text since clipboard_listener will pickup the text as it will be selected on focus and cause a loop back to the word-view
            self.noword_view.entry.props.text = ""

            self.noword_view.show_all()
            self.noword_view.icon_overlay.grab_focus()
            self.stack.set_visible_child_name(name="no-word-view")
            self.word_label.props.label = "QuickWord"
            self.word_view.hide()
            self.settings_view.hide()
            self.props.resizable = False
            # delayed grab focus to avoid hotkey character getting inserted in entry field
            GLib.timeout_add(250, self.noword_view.entry.grab_focus)

    def generate_viewswitch(self):
        self.view_switch = Granite.ModeSwitch.from_icon_name("com.github.hezral.quickword-symbolic", "preferences-system-symbolic")
        self.view_switch.props.valign = Gtk.Align.CENTER
        self.view_switch.props.halign = Gtk.Align.END
        self.view_switch.props.hexpand = True
        self.view_switch.props.margin = 4
        self.view_switch.props.name = "view-switch"
        self.view_switch.get_children()[1].props.can_focus = False
        self.view_switch.connect_after("notify::active", self.on_view_visible)
        return self.view_switch

    def generate_headerbar(self):
        self.word_label = Gtk.Label("QuickWord")
        self.word_label.props.vexpand = True
        self.word_label.get_style_context().add_class("lookup-word-header")

        edit_img = Gtk.Image().new_from_icon_name("insert-text-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        edit_img.props.halign = Gtk.Align.START
        self.edit_img_revealer = Gtk.Revealer()
        self.edit_img_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.edit_img_revealer.add(edit_img)

        self.pronounciation_label = Gtk.Label("")
        self.pronounciation_label.props.name = "pronounciation"
        self.pronounciation_label.props.expand = True
        self.pronounciation_label.props.can_focus = False
        self.pronounciation_label.get_style_context().add_class("pronounciation")

        self.speak_btn = Gtk.Button(image=Gtk.Image().new_from_icon_name("audio-volume-high-symbolic", Gtk.IconSize.SMALL_TOOLBAR))
        self.speak_btn.props.name = "speak"
        self.speak_btn.props.expand = True
        self.speak_btn.props.can_focus = False
        self.speak_btn.get_style_context().add_class("speak")
        self.speak_btn.connect("clicked", self.on_speak_word)

        self.word_actions = Gtk.Grid()
        self.word_actions.props.name = "word-actions"
        self.word_actions.props.column_spacing = 6
        self.word_actions.props.expand = False
        self.word_actions.attach(self.pronounciation_label, 0, 0, 1, 1)
        self.word_actions.attach(self.speak_btn, 1, 0, 1, 1)

        self.word_action_revealer = Gtk.Revealer()
        self.word_action_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.word_action_revealer.add(self.word_actions)

        self.word_box = Gtk.EventBox()
        self.word_box.add(self.word_label)
        self.word_box.connect("button-press-event", self.on_manual_lookup)
        self.word_box.connect("enter-notify-event", self.on_enter_word_label)
        self.word_box.connect("leave-notify-event", self.on_leave_word_label)

        self.word_grid = Gtk.Grid()
        self.word_grid.props.column_spacing = 6
        self.word_grid.props.halign = Gtk.Align.START
        self.word_grid.props.valign = Gtk.Align.CENTER
        self.word_grid.attach(self.word_box, 0, 0, 1, 1)
        self.word_grid.attach(self.word_action_revealer, 1, 0, 1, 1)
        self.word_grid.attach(self.edit_img_revealer, 1, 0, 1, 1)

        titlebar_grid = Gtk.Grid()
        titlebar_grid.props.hexpand = True
        titlebar_grid.attach(self.word_grid, 0, 0, 1, 1)
        titlebar_grid.attach(self.generate_viewswitch(), 1, 0, 1, 1)

        headerbar = Gtk.HeaderBar()
        headerbar.props.custom_title = titlebar_grid
        headerbar.props.decoration_layout = "close:"
        return headerbar

    def on_speak_word(self, button):
        import subprocess
        from shutil import which, Error
        try:
            word = self.word_label.props.label
            subprocess.call(["espeak", word])
            print(word)
        except:
            pass

    def on_view_visible(self, viewswitch=None, gparam=None, view=None):

        def set_word_view():
            if self.app.lookup_word is None:
                self.noword_view.show_all()
                self.word_label.props.label = "Quickword"
                self.stack.set_visible_child(self.noword_view)
                self.word_view.hide()
                self.props.resizable = False
            else:
                self.word_view.show_all()
                self.word_label.props.label = self.lookup_word
                self.stack.set_visible_child(self.word_view)
                self.noword_view.hide()
                self.word_action_revealer.set_reveal_child(True)
                self.props.resizable = True

        def set_settings_view():
            self.word_action_revealer.set_reveal_child(False)
            self.settings_view.show_all()
            self.settings_view.on_totalwords()
            self.stack.set_visible_child(self.settings_view)
            self.word_label.props.label = "Settings"
            self.word_view.hide()
            self.noword_view.hide()
            self.props.resizable = False
                
        # app first-run right
        # first-run >> download data view >> no word view or selected word view

        if self.app.first_run:
            print("first-run")
            self.stack.set_visible_child(self.updater_view)
            self.updater_view.show()

        if not self.app.first_run and view is None:
            print("normal-run")
            if viewswitch is not None:
                if viewswitch.props.active:
                    set_settings_view()
                else:
                    set_word_view()
                    self.settings_view.hide()
            else:
                set_word_view()

        if view is not None:
            self.stack.set_visible_child_name(view)
            if view == "settings-view":
                self.view_switch.props.active = True
            else:
                self.view_switch.props.active = False

    def on_close_window(self, window=None, event=None):
        if self.app.gio_settings.get_value("close-mode"):
            if window is None:
                self.hide()
            else:
                window.hide()
            return True
        else:
            self.destroy()