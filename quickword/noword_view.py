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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango


#------------------CLASS-SEPARATOR------------------#


class NoWordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- quickword logo --------#
        left_icon = Gtk.Image().new_from_file("data/icons/134.svg")
        #left_icon.get_style_context().add_class("quickword-icon-left")
        right_icon = Gtk.Image().new_from_file("data/icons/133.svg")
        right_icon.get_style_context().add_class("quickword-icon-right")
        icon_overlay = Gtk.Overlay()
        icon_overlay.add(left_icon)
        icon_overlay.add_overlay(right_icon)
        icon_overlay.props.can_focus = True
        icon_overlay.props.focus_on_click = True
        icon_overlay.grab_focus()
        
        #-- message header --------#
        message = Gtk.Label("No word detected")
        message.props.name = "message"
        message.props.margin_bottom = 5
        message.props.hexpand = True
        message.props.halign = Gtk.Align.CENTER
        message.props.valign = Gtk.Align.CENTER
        message.props.max_width_chars = 30
        message.props.wrap = True
        message.props.wrap_mode = Pango.WrapMode.WORD
        message.props.justify = Gtk.Justification.CENTER
        message.get_style_context().add_class("h3")

        #-- message header --------#
        sub_message = Gtk.Label("Select a word in any application or document\nor type a word below to get a quick word lookup")
        sub_message.props.margin_bottom = 10
        sub_message.props.hexpand = True
        sub_message.props.halign = Gtk.Align.CENTER
        sub_message.props.valign = Gtk.Align.CENTER
        sub_message.props.max_width_chars = 40
        sub_message.props.wrap = True
        sub_message.props.wrap_mode = Pango.WrapMode.WORD
        sub_message.props.justify = Gtk.Justification.CENTER

        #-- word entry --------#
        entry = Gtk.Entry()
        entry.set_size_request(-1, 40)
        entry.props.expand = False
        entry.props.margin = 10
        entry.props.margin_bottom = 0
        entry.props.focus_on_click = True
        entry.props.placeholder_text = "type a word like 'quick' and press enter"
        entry.props.xalign = 0.5
        entry.get_style_context().add_class("entry-word")
        entry.connect("key-press-event", self.on_entry_start)
        entry.connect("button-press-event", self.on_entry_start)
        entry.connect("activate", self.on_entry_activate)
        entry.connect("icon_press", self.on_backspace)

        #-- NoWordView construct--------#
        self.props.name = 'no-word-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 12
        self.props.column_spacing = 6
        self.props.valign = Gtk.Align.CENTER
        self.attach(icon_overlay, 0, 1, 1, 1)
        self.attach(message, 0, 2, 1, 1)
        self.attach(sub_message, 0, 3, 1, 1)
        self.attach(entry, 0, 4, 1, 1)


    def on_entry_start(self, entry, eventkey):
        entry.props.secondary_icon_name = "edit-clear-symbolic"

    def on_backspace(self, entry, entry_icon, eventbutton):
        entry.props.text = ""

    def on_entry_activate(self, entry):
        view = self
        stack = self.get_parent()
        window = stack.get_parent()
        app = window.props.application
        icon_overlay = [child for child in self.get_children() if isinstance(child, Gtk.Overlay)][0]
        message = [child for child in self.get_children() if child.props.name == "message"][0]
        entry.props.secondary_icon_name = None

        if entry.props.text == "":
            # need to reset text, bug maybe?
            entry.props.text = ""
            entry.props.placeholder_text = "need a word here 😀️"
            icon_overlay.grab_focus()
        else:
            # callback to WordLookup
            lookup = app.emit("on-new-word-lookup", entry.props.text)
            # check if word lookup succeeded or not
            if lookup is False:
                message.props.label = "Word not found"
                entry.props.text = ""
                entry.props.placeholder_text = "please type a valid ssssword 🧐️"
                icon_overlay.grab_focus()
