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
import gi
from gi.repository import GLib
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gio


#------------------CLASS-SEPARATOR------------------#


class UpdaterView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- quickword logo --------#
        download_icon = Gtk.Image().new_from_icon_name("emblem-downloads", Gtk.IconSize.DIALOG)
        download_icon.props.halign = Gtk.Align.END
        download_icon.props.valign = Gtk.Align.START
        download_icon.props.expand = False
        download_icon.props.name = "download-icon"
        download_icon.get_style_context().add_class("quickword-icon-right")
        
        left_icon = Gtk.Image().new_from_icon_name("com.github.hezral.quickword-left", Gtk.IconSize.DIALOG)
        right_icon = Gtk.Image().new_from_icon_name("com.github.hezral.quickword-right", Gtk.IconSize.DIALOG)

        left_icon.set_pixel_size(96)
        right_icon.set_pixel_size(96)

        left_icon.props.expand = False
        right_icon.props.expand = False

        icon_overlay = Gtk.Overlay()
        icon_overlay.add(left_icon)
        icon_overlay.add_overlay(right_icon)
        icon_overlay.add_overlay(download_icon)
        icon_overlay.props.halign = Gtk.Align.CENTER
        icon_overlay.props.can_focus = True
        icon_overlay.props.focus_on_click = True
        icon_overlay.grab_focus()

        #-- message header --------#

        message = Gtk.Label()
        message.props.name = "message"
        message.props.margin_bottom = 5
        message.props.hexpand = True
        message.props.halign = Gtk.Align.CENTER
        message.props.valign = Gtk.Align.CENTER
        message.props.max_width_chars = 30
        message.props.wrap = True
        message.props.wrap_mode = Pango.WrapMode.WORD
        message.props.justify = Gtk.Justification.CENTER
        message.get_style_context().add_class("h2")

        sub_message = Gtk.Label()
        sub_message.props.name = "sub-message"
        sub_message.props.margin_bottom = 10
        sub_message.props.hexpand = True
        sub_message.props.halign = Gtk.Align.CENTER
        sub_message.props.valign = Gtk.Align.CENTER
        sub_message.props.max_width_chars = 50
        sub_message.props.wrap = True
        sub_message.props.wrap_mode = Pango.WrapMode.WORD
        sub_message.props.justify = Gtk.Justification.CENTER

        #-- proceed button --------#
        proceed_btn = Gtk.Button(label="Proceed")
        proceed_btn.props.name = "proceed-btn"
        proceed_btn.get_style_context().add_class("h3")
        proceed_btn.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        proceed_btn.set_size_request(-1, 32)
        proceed_btn.connect("clicked", self.on_proceed_update)

        #-- start button --------#
        start_btn = Gtk.Button(label="Start Using Quickword")
        start_btn.props.name = "start-btn"
        start_btn.get_style_context().add_class("h3")
        start_btn.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        start_btn.set_size_request(-1, 32)
        start_btn.connect("clicked", self.on_start)

        #-- UpdaterView construct--------#
        self.props.name = 'updater-view'
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
        self.attach(proceed_btn, 0, 4, 1, 1)
        self.attach(start_btn, 0, 4, 1, 1)
        self.connect_after("realize", self.generate_message_str)

    def generate_message_str(self, view):

        stack = self.get_parent()
        window = stack.get_parent()
        app = window.props.application

        if app.first_run:
            message_str ="Hello!"
            sub_message_str = "Before QuickWord can work, it needs to download dictionary data."
            sub_message_str = sub_message_str + "\n" + "Please ensure internet connectivity, before proceeding."
            sub_message_str = sub_message_str + "\n" + "This usually takes less than a minute."
        else:
            message_str = "Check for Updates"
            sub_message_str = "Check for any updates to dictionary data"
        message = [child for child in self.get_children() if child.props.name == "message"][0]
        sub_message = [child for child in self.get_children() if child.props.name == "sub-message"][0]

        message.props.label = message_str
        sub_message.props.label = sub_message_str
        
    def on_start(self, button):
        stack = self.get_parent()
        window = stack.get_parent()
        app = window.props.application

        lookup = app.emit("on-new-word-lookup", app.lookup_word)

        if lookup is False:
            stack.set_visible_child_name("no-word-view")
            self.current_view = "no-word-view"

    def on_proceed_update(self, button):
        stack = self.get_parent()
        window = stack.get_parent()
        app = window.props.application
        icon_overlay = [child for child in self.get_children() if isinstance(child, Gtk.Overlay)][0]
        download_icon = [child for child in icon_overlay.get_children() if child.props.name == "download-icon"][0]

        download_icon.get_style_context().remove_class("quickword-icon-right")
        download_icon.get_style_context().add_class("download-icon-start")

        if app.first_run:
            app._data_manager.run_func(runname="download", callback=self.on_update_progress)
            gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
            gio_settings.set_boolean("first-run", False)
        else:
            run = app.generate_data_manager()
            while run is False:
                GLib.idle_add(self.on_update_progress, "One moment..", "Waiting for data manager")
            app._data_manager.run_func(runname="update", callback=self.on_update_progress)

    def on_update_progress(self, message_str, sub_message_str):
        message = [child for child in self.get_children() if child.props.name == "message"][0]
        sub_message = [child for child in self.get_children() if child.props.name == "sub-message"][0]
        
        if message_str == "Completed" or message_str == "Downloaded" or message_str == "No Updates":
            start_btn = [child for child in self.get_children() if child.props.name == "start-btn"][0]
            self.remove_row(4)
            self.attach(start_btn, 0, 4, 1, 1)
        else:
            proceed_btn = [child for child in self.get_children() if child.props.name == "proceed-btn"][0]
            proceed_btn.props.label = "Please wait.."

        message.props.label = message_str
        sub_message.props.label = sub_message_str
        

