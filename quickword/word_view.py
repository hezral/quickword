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

class WordView(Gtk.Grid):
    def __init__(self, word_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- view construct--------#
        self.props.name = 'word-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = False
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 12
        self.props.column_spacing = 6

        #-- view contents--------#
        definition = WordSection(name="definition", contents="This is a contents block of text ")
        other = WordSection(name="other", contents="This is a contents block of text")
        
        definition2 = WordSection(name="definition2", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        other2 = WordSection(name="other2", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        
        definition3 = WordSection(name="definition3", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        other3 = WordSection(name="other3", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        
        self.attach(definition, 0, 1, 1, 1)
        self.attach(other, 0, 2, 1, 1)
        self.attach(definition2, 0, 3, 1, 1)
        self.attach(other2, 0, 4, 1, 1)
        self.attach(definition3, 0, 5, 1, 1)
        self.attach(other3, 0, 6, 1, 1)





#------------------CLASS-SEPARATOR------------------#

class WordSection(Gtk.Grid):
    def __init__(self, name, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #-- header -------#
        header = Gtk.Label(name.capitalize())
        header.props.halign = Gtk.Align.START
        header.props.valign = Gtk.Align.CENTER
        header.get_style_context().add_class("section-header")

        #-- sub_header -------#
        sub_header = Gtk.Label("noun")
        sub_header.props.halign = Gtk.Align.START
        sub_header.props.valign = Gtk.Align.CENTER
        sub_header.get_style_context().add_class("section-sub-header")

        #-- content -------#
        content = Gtk.Label(contents)
        content.props.margin_bottom = 10
        content.props.max_width_chars = 50
        content.props.wrap = True
        content.props.hexpand = True
        content.props.wrap_mode = Pango.WrapMode.WORD
        content.props.halign = Gtk.Align.START
        content.props.valign = Gtk.Align.START
        content.get_style_context().add_class("section-content")

        copy_img = Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        copy_img.props.no_show_all = True
        copy_img.props.hexpand = True
        copy_img.props.halign = Gtk.Align.END
        copy_img.props.valign = Gtk.Align.START
        copy_img.get_style_context().add_class("copy-content")

        copied_img = Gtk.Image().new_from_icon_name("emblem-default", Gtk.IconSize.SMALL_TOOLBAR)
        copied_img.props.no_show_all = True

        copied_label = Gtk.Label("Copied to clipboard")
        copied_label.props.no_show_all = True
        
        copied_grid = Gtk.Grid()
        copied_grid.props.column_spacing = 4
        copied_grid.props.halign = Gtk.Align.END
        copied_grid.props.valign = Gtk.Align.END
        copied_grid.props.hexpand = True
        copied_grid.get_style_context().add_class("copied-content")
        copied_grid.attach(copied_img, 0, 1, 1, 1)
        copied_grid.attach(copied_label, 1, 1, 1, 1)

        hidden_widget = (copy_img, copied_label, copied_img, copied_grid)

        # workaround to avoid weird issue with enter and notify events after adding to the eventbox
        # put all in a grid, then put in eventbox. overlay didn't work
        content_grid = Gtk.Grid()
        content_grid.props.hexpand = True
        content_grid.attach(content, 0, 1, 1, 1)
        content_grid.attach(copy_img, 0, 1, 1, 1)
        content_grid.attach(copied_grid, 0, 1, 1, 1)

        content_eventbox = Gtk.EventBox()
        content_eventbox.add(content_grid)
        content_eventbox.connect("enter-notify-event", self.on_enter_content_box, hidden_widget)
        content_eventbox.connect("leave-notify-event", self.on_leave_content_box, hidden_widget)
        content_eventbox.connect("button-press-event", self.on_copy_content_clicked, hidden_widget)

        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 6
        self.props.column_spacing = 0

        self.attach(header, 0, 1, 1, 1)
        self.attach(self.generate_separator(), 1, 1, 4, 1)
        self.attach(sub_header, 0, 2, 1, 1)
        self.attach(content_eventbox, 0, 3, 5, 1)

    def generate_separator(self):
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER
        return separator

    def on_enter_content_box(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_grid = widget_list[3]

        # show widget and set flags to trigger transition effect, see application.css
        copy_img.show()
        copy_img.set_state_flags(Gtk.StateFlags.BACKDROP, True)

        # set flags to ready state for transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)


    def on_leave_content_box(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_label = widget_list[1]
        copied_img = widget_list[2]
        copied_grid = widget_list[3]

        # hide and reset state flagss to ready state for transition effect, see application.css
        copy_img.hide()
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # hide widgets
        copied_label.hide()
        copied_img.hide()

        # reset state flags to ready state for transition effect, see application.css
        # grid can stay as show state since only toggle widget hide/shows
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)


    def on_copy_content_clicked(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_label = widget_list[1]
        copied_img = widget_list[2]
        copied_grid = widget_list[3]

        # hide and reset state flagss to ready state for transition effect, see application.css
        copy_img.hide()
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # show widgets
        copied_label.show()
        copied_img.show()

        # set flags to trigger transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.BACKDROP, True)

