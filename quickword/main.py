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
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject, Pango

#------------------CLASS-SEPARATOR------------------#

class QuickWordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        #-- constants --------#
        self.LOOKUP_WORD = "QuickWord"

        #-- view --------#
        word = WordView()
        settings = SettingsView()
        settings.connect("notify::visible", self.on_settings_view_visible)

        #-- stack --------#
        stack = Gtk.Stack()
        stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        stack.add_named(word, word.get_name())
        stack.add_named(settings, settings.get_name())

        #-- header --------#
        #------ lookup word label ----#
        word_label = Gtk.Label(self.LOOKUP_WORD)
        word_label.props.selectable = True
        word_label.props.halign = Gtk.Align.START
        word_label.props.valign = Gtk.Align.CENTER
        word_label.get_style_context().add_class("lookup-word-header")

        #------ view switch ----#
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path('data/icons')
        view_switch = Granite.ModeSwitch.from_icon_name("com.github.hezral.quickwork-symbolic", "preferences-system-symbolic")
        view_switch.props.primary_icon_tooltip_text = "Word Lookup"
        view_switch.props.secondary_icon_tooltip_text = "Settings"
        view_switch.props.valign = Gtk.Align.CENTER
        view_switch.bind_property("active", settings, "visible", GObject.BindingFlags.BIDIRECTIONAL)


        #-- header construct--------#
        headerbar = Gtk.HeaderBar()
        headerbar.pack_start(word_label)
        headerbar.pack_end(view_switch)
        headerbar.props.show_close_button = False
        headerbar.props.decoration_layout = "close:maximize"
        headerbar.get_style_context().add_class("default-decoration")
        headerbar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

        #-- objects --------#
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")


        #-- window construct--------#
        self.props.resizable = True
        # self.props.skip_taskbar_hint = True
        self.title = "QuickWord"
        # self.props.width_request = 200
        # self.props.height_request = 80
        #self.props.default_height = 500
        #self.props.default_width = 500
        self.set_keep_above(True)
        #self.props.border_width = 20
        self.get_style_context().add_class("rounded")
        self.set_size_request(500, 500)
        self.props.window_position = Gtk.WindowPosition.MOUSE
        self.set_titlebar(headerbar)
        self.add(stack)
        self.state_flags_changed_count = 0
        if gio_settings.get_value("close-on-focus-out"):
            self.state_flags_on = self.connect("state-flags-changed", self.on_focus_out)
            print('state-flags-on')
        

    def on_settings_view_visible(self, widget, gparam):
        # get window children
        window_children = self.get_children()
        # loop through and find Gtk.Stack
        for child in window_children:
            if isinstance(child, Gtk.Stack):
                stack = child
                # toggle settings_view visiblility based on visible property
                if widget.is_visible():
                    widget.show_all()
                    stack.set_visible_child_full(name='settings_view', transition=Gtk.StackTransitionType.CROSSFADE)
                    stack.get_style_context().add_class("stack-settings")
                else:
                    widget.hide()
                    stack.set_visible_child_full(name='word_view', transition=Gtk.StackTransitionType.CROSSFADE)
                    stack.get_style_context().remove_class("stack-settings")
            if isinstance(child, Gtk.HeaderBar):
                headerbar = child
                for child in headerbar.get_children():
                    if isinstance(child, Gtk.Label):
                        if child.get_label() == "Settings":
                            child.props.label = self.LOOKUP_WORD
                            headerbar.get_style_context().remove_class("headerbar-settings")
                        else:
                            child.props.label = "Settings"
                            headerbar.get_style_context().add_class("headerbar-settings")


    def on_focus_out(self, widget, event):
        # state flags for window active state
        active_state_flags = ['GTK_STATE_FLAG_NORMAL', 'GTK_STATE_FLAG_DIR_LTR']
        state_flags = self.get_state_flags().value_names
        if not state_flags == active_state_flags and self.state_flags_changed_count > 1:
            self.destroy()
        else:
            self.state_flags_changed_count += 1
            print('state-flags-changed', self.state_flags_changed_count)



#------------------CLASS-SEPARATOR------------------#

class WordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- view construct--------#
        self.props.name = 'word_view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        self.props.row_spacing = 12
        self.props.column_spacing = 6

        definition = WordSection(name="definition", contents="This is a contents block of text with lots of texts")
        other = WordSection(name="other", contents="This is a contents block of text with lots of texts")

        self.attach(definition, 0, 1, 1, 1)
        self.attach(other, 0, 2, 1, 1)


class WordSection(Gtk.Grid):
    def __init__(self, name, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 6
        self.props.column_spacing = 6

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
        content.props.max_width_chars = 60
        content.props.selectable = True
        content.props.wrap = True
        content.props.wrap_mode = Pango.WrapMode.WORD_CHAR
        content.props.halign = Gtk.Align.START
        content.props.valign = Gtk.Align.START
        content.get_style_context().add_class("section-content")

        #-- separator -------#
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER

        self.attach(header, 0, 1, 1, 1)
        self.attach(self.generate_separator(), 1, 1, 4, 1)
        self.attach(sub_header, 0, 2, 1, 1)
        self.attach(content, 0, 3, 5, 1)

    def generate_separator(self):
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER
        return separator

        

#------------------CLASS-SEPARATOR------------------#

class SettingsView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        #-- theme switch ----#
        theme_label = Gtk.Label("Switch between Light/Dark theme")
        theme_label.props.halign = Gtk.Align.START
        theme_switch = Gtk.Switch()
        theme_switch.props.name = "theme-switch"
        theme_switch.props.halign = Gtk.Align.END
        theme_switch.props.hexpand = True
        theme_switch.connect("notify::active", self.on_switch_activated)
        theme_switch.bind_property ("active", Gtk.Settings().get_default(), "gtk_application_prefer_dark_theme", GObject.BindingFlags.INVERT_BOOLEAN)

        #-- close on focus out ----#
        close_on_focus_out_label = Gtk.Label("Close QuickWord if out of focus")
        close_on_focus_out_label.props.halign = Gtk.Align.START
        close_on_focus_out_switch = Gtk.Switch()
        close_on_focus_out_switch.props.name = "close-on-focus-out"
        close_on_focus_out_switch.props.halign = Gtk.Align.END
        close_on_focus_out_switch.props.hexpand = True
        close_on_focus_out_switch.connect("notify::active", self.on_switch_activated)
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
        gio_settings.bind ("close-on-focus-out", close_on_focus_out_switch, "active", Gio.SettingsBindFlags.DEFAULT)

        grid = Gtk.Grid()
        grid.props.margin = 8
        grid.props.hexpand = True
        grid.props.row_spacing = 8
        grid.props.column_spacing = 6
        grid.attach(theme_label, 0, 1, 1, 1)
        grid.attach(theme_switch, 1, 1, 1, 1)
        grid.attach(self.generate_separator(), 0, 2, 2, 1)
        grid.attach(close_on_focus_out_label, 0, 3, 1, 1)
        grid.attach(close_on_focus_out_switch, 1, 3, 1, 1)


        frame = Gtk.Frame()
        frame.get_style_context().add_class("settings-frame")
        frame.add(grid)


        #-- view construct--------#
        self.props.name = "settings_view"
        self.get_style_context().add_class(self.props.name)
        # self.props.visible = False
        # self.props.no_show_all = True
        self.props.expand = True
        self.props.margin = 20
        self.props.row_spacing = 6
        self.props.column_spacing = 6
        self.attach(frame, 0, 1, 1, 1)

    def generate_separator(self):
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER
        return separator


    def on_switch_activated(self, switch, gparam):
        name = switch.get_name()
        # stack = self.get_parent()
        # window = stack.get_parent()
        print(self)

        if self.is_visible():
            print('visible')
            print(self.get_parent())
            print(self.get_parent().get_parent())

        # gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")

        # if name == "close-on-focus-out" and gio_settings.get_value("close-on-focus-out") == "true":
        #     window.state_flags_on = self.connect("state-flags-changed", window.on_focus_out)
        # else:
        #     window.disconnect(window.state_flags_on)

#------------------CLASS-SEPARATOR------------------#

class QuickWordApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set application properties
        self.props.application_id = "com.github.hezral.quickword"

        provider = Gtk.CssProvider()
        provider.load_from_path("/home/adi/Work/quickword/data/application.css")
        # # provider.load_from_resource ("com/github/hezral/quickword/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # initialize any objects
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        # Support quiting app using Super+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])



    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = QuickWordWindow(application=self)
            self.add_window(self.window)
            self.window.show_all()

    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

#------------------CLASS-SEPARATOR------------------#

if __name__ == "__main__":
    app = QuickWordApp()
    app.run(sys.argv)



