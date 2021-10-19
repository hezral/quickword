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
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango


class NoWordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- quickword logo --------#
        left_icon = Gtk.Image().new_from_icon_name("com.github.hezral.quickword-left", Gtk.IconSize.DIALOG)
        right_icon = Gtk.Image().new_from_icon_name("com.github.hezral.quickword-right", Gtk.IconSize.DIALOG)

        left_icon.set_pixel_size(96)
        right_icon.set_pixel_size(96)

        right_icon.get_style_context().add_class("quickword-icon-right")
        
        self.icon_overlay = Gtk.Overlay()
        self.icon_overlay.add(left_icon)
        self.icon_overlay.add_overlay(right_icon)
        self.icon_overlay.props.can_focus = True
        self.icon_overlay.props.focus_on_click = True
        # self.icon_overlay.grab_focus()
        
        #-- message header --------#
        self.message = Gtk.Label("No word detected")
        self.message.props.name = "message"
        self.message.props.margin_bottom = 5
        self.message.props.hexpand = True
        self.message.props.halign = Gtk.Align.CENTER
        self.message.props.valign = Gtk.Align.CENTER
        self.message.props.max_width_chars = 30
        self.message.props.wrap = True
        self.message.props.wrap_mode = Pango.WrapMode.WORD
        self.message.props.justify = Gtk.Justification.CENTER
        self.message.get_style_context().add_class("h3")

        #-- message header --------#
        self.sub_message = Gtk.Label("Select a word in any application or document\nor type a word below to get a quick word lookup")
        self.sub_message.props.margin_bottom = 10
        self.sub_message.props.hexpand = True
        self.sub_message.props.halign = Gtk.Align.CENTER
        self.sub_message.props.valign = Gtk.Align.CENTER
        self.sub_message.props.max_width_chars = 40
        self.sub_message.props.wrap = True
        self.sub_message.props.wrap_mode = Pango.WrapMode.WORD
        self.sub_message.props.justify = Gtk.Justification.CENTER

        #-- word entry --------#
        self.entry = Gtk.Entry()
        self.entry.set_size_request(-1, 40)
        self.entry.props.expand = False
        self.entry.props.focus_on_click = True
        self.entry.props.placeholder_text = "type a word like 'quick' and press enter"
        self.entry.props.xalign = 0.5
        self.entry.get_style_context().add_class("entry-word")
        self.entry.connect("key-press-event", self.on_entry_start)
        self.entry.connect("button-press-event", self.on_entry_start)
        self.entry.connect("activate", self.on_entry_activate)
        self.entry.connect("icon_press", self.on_backspace)


        self.props.name = 'no-word-view'
        self.get_style_context().add_class(self.props.name)
        self.set_size_request(350, -1)
        self.props.margin = 20
        self.props.margin_left = 20
        self.props.margin_right = 20
        self.props.expand = True
        self.props.row_spacing = 12
        self.props.column_spacing = 6
        self.props.valign = Gtk.Align.CENTER
        self.attach(self.icon_overlay, 0, 1, 1, 1)
        self.attach(self.message, 0, 2, 1, 1)
        self.attach(self.sub_message, 0, 3, 1, 1)
        self.attach(self.entry, 0, 4, 1, 1)


    def on_entry_start(self, entry, eventkey):
        entry.props.secondary_icon_name = "edit-clear-symbolic"

    def on_backspace(self, entry, entry_icon, eventbutton):
        entry.props.text = ""

    def on_entry_activate(self, entry):
        self.entry.props.secondary_icon_name = None
        window = self.get_toplevel()

        if self.entry.props.text == "":
            # need to reset text, bug maybe?
            self.entry.props.text = ""
            self.entry.props.placeholder_text = "need a word here 😀️"
            self.icon_overlay.grab_focus()
        else:
            # callback to WordLookup
            lookup = window.props.application.on_new_word_lookup(entry.props.text)
            # check if word lookup succeeded or not
            if lookup is False:
                self.message.props.label = "Word not found"
                self.entry.props.text = ""
                self.entry.props.placeholder_text = "please type a valid word 🧐️"
                self.icon_overlay.grab_focus()
            else:
                self.hide()
