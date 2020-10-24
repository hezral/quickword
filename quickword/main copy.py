#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of QuickWord.

    QuickWord is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    QuickWord is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Movens.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk

#------------------CLASS-SEPARATOR------------------#

export_json_button = Gtk.Button(label="Export to JSON", image=Gtk.Image.new_from_icon_name("text-css", Gtk.IconSize.LARGE_TOOLBAR))
export_json_button.set_always_show_image(True)
export_json_button.props.halign = Gtk.Align.FILL
export_json_button.props.xalign = 0.0

export_csv_button = Gtk.Button(label="Export to CSV ", image=Gtk.Image.new_from_icon_name("application-vnd.ms-excel", Gtk.IconSize.LARGE_TOOLBAR))
export_csv_button.set_always_show_image(True)
export_csv_button.props.halign = Gtk.Align.FILL
export_csv_button.props.xalign = 0.0

export_txt_button = Gtk.Button(label="Export to TXT ", image=Gtk.Image.new_from_icon_name("text-x-generic", Gtk.IconSize.LARGE_TOOLBAR))
export_txt_button.set_always_show_image(True)
export_txt_button.props.halign = Gtk.Align.FILL
export_txt_button.props.xalign = 0.0

popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
popover_box.pack_start(export_json_button, True, True, 0)
popover_box.pack_start(export_csv_button, True, True, 0)
popover_box.pack_start(export_txt_button, True, True, 0)
popover_box.props.expand = True

popover = Gtk.Popover()
popover.props.constrain_to = Gtk.PopoverConstraint.NONE

popover.props.modal = True
popover.add(popover_box)
popover.get_style_context().add_class("pop")
popover.show_all()

Gtk.main()
