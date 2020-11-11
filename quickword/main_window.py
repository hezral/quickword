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


import sys, os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject, Pango

# QuickWord imports
from settings_view import SettingsView
from noword_view import NoWordView
from word_view import WordView
from updater_view import UpdaterView


#------------------CLASS-SEPARATOR------------------#


class QuickWordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom signals to detec new word selected
        # GObject.signal_new(signal_name, type, flags, return_type, param_types)
        # param_types is a list example [GObject.TYPE_PYOBJECT, GObject.TYPE_STRING]
        GObject.signal_new("on-new-word-selected", Gtk.ApplicationWindow, GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, [GObject.TYPE_PYOBJECT])
        self.connect("on-new-word-selected", self.on_new_word_selected)

        #-- variables --------#
        # self.lookup_word = "QuickWord"
        app = self.props.application

        # setup path
        self.modulepath = os.path.dirname(__file__)


        #-- view --------#
        updater = UpdaterView()
        noword = NoWordView()
        word = WordView()
        settings = SettingsView()
        settings.connect("notify::visible", self.on_view_visible)
        
        #-- stack --------#
        stack = Gtk.Stack()
        stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        stack.add_named(word, word.get_name())
        stack.add_named(settings, settings.get_name())
        stack.add_named(noword, noword.get_name())
        stack.add_named(updater, updater.get_name())
        
        #-- header --------#
        headerbar = self.generate_headerbar(settings_view=settings)

        #-- QuickWordWindow construct--------#
        self.props.resizable = False #set this and window will expand and retract based on child
        # self.props.skip_taskbar_hint = True
        # self.set_icon_name("com.github.hezral.quickword")
        self.title = "QuickWord"
        self.set_keep_above(True)
        self.get_style_context().add_class("rounded")
        self.set_size_request(600, -1) #set width to -1 to expand and retract based on content
        self.props.window_position = Gtk.WindowPosition.MOUSE
        self.set_titlebar(headerbar)
        self.add(stack)
        
        #-- QuickWordWindow variables--------#

        # this is for tracking window state flags for persistent mode
        self.state_flags_changed_count = 0
        self.active_state_flags = ['GTK_STATE_FLAG_NORMAL', 'GTK_STATE_FLAG_DIR_LTR']
        
        self.on_start_settings()
        

        # set active views based on app launch conditions
        # initial view is noword-view for manual lookup
        self.active_view = None
        self.current_view = None
        if app.first_run:
            self.active_view = updater
            self.current_view = "updater-view"
        
        elif app.lookup_word is None:
            self.active_view = noword
            self.current_view = "no-word-view"

        elif app.lookup_word is not None or app.lookup_word == "QuickWord":
            self.active_view = noword
            self.current_view = "no-word-view"

        elif app.lookup_word is not None and not app.lookup_word == "QuickWord":
            self.active_view = word
            self.current_view = "word-view"
        
        

    def on_start_settings(self):
        # read user saved settings
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
        if not gio_settings.get_value("persistent-mode"):
            self.state_flags_on = self.connect("state-flags-changed", self.on_persistent_mode)
            # print('state-flags-on')
        if gio_settings.get_value("sticky-mode"):
            self.stick()

    def generate_headerbar(self, settings_view):
        word_label = Gtk.Label("QuickWord")
        word_label.props.vexpand = True
        word_label.get_style_context().add_class("lookup-word-header")

        edit_img = Gtk.Image().new_from_icon_name("insert-text-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        edit_img.props.no_show_all = True
        edit_img.get_style_context().add_class("transition-on")

        word_grid = Gtk.Grid()
        word_grid.props.column_spacing = 4
        word_grid.props.halign = Gtk.Align.START
        word_grid.props.valign = Gtk.Align.CENTER
        word_grid.attach(word_label, 0, 1, 1, 1)
        word_grid.attach(edit_img, 1, 1, 1, 1)

        word_box = Gtk.EventBox()
        word_box.add(word_grid)
        word_box.connect("button-press-event", self.on_manual_lookup)
        word_box.connect("enter-notify-event", self.on_enter_word_label)
        word_box.connect("leave-notify-event", self.on_leave_word_label)

        #------ view switch ----#
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path(os.path.join(self.modulepath, "data/icons"))
        view_switch = Granite.ModeSwitch.from_icon_name("com.github.hezral.quickword-symbolic", "preferences-system-symbolic")
        view_switch.props.primary_icon_tooltip_text = "Word Lookup"
        view_switch.props.secondary_icon_tooltip_text = "Settings"
        view_switch.props.valign = Gtk.Align.CENTER
        view_switch.bind_property("active", settings_view, "visible", GObject.BindingFlags.BIDIRECTIONAL)
        #.connect("activate", self.on_view_visible)

        #-- header construct--------#
        headerbar = Gtk.HeaderBar()
        headerbar.pack_start(word_box)
        headerbar.pack_end(view_switch)
        headerbar.props.show_close_button = False
        headerbar.props.decoration_layout = "close:maximize"
        headerbar.get_style_context().add_class("default-decoration")
        headerbar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        return headerbar

    def get_window_child_widgets(self):
        window = self
        window_children = window.get_children()
        headerbar = [child for child in window_children if isinstance(child, Gtk.HeaderBar)][0]
        stack = [child for child in window_children if isinstance(child, Gtk.Stack)][0]
        word_box = [child for child in headerbar.get_children() if isinstance(child, Gtk.EventBox)][0]
        word_grid = word_box.get_child()
        return headerbar, stack, word_grid

    def get_window_child(self, class_obj):
        widget = [child for child in self.get_children() if isinstance(child, class_obj)][0]
        return widget

    def on_new_word_selected(self, window, word_data):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        word_label = [child for child in word_grid.get_children() if isinstance(child, Gtk.Label)][0]
        word_label.props.label = word_data[0]
        word_view = stack.get_child_by_name("word-view")
        stack.set_visible_child(word_view)
        word_view.on_wordlookup(data=word_data)
        # reset active_view and lookup_word
        self.active_view = word_view
        self.current_view = "word-view"

    def on_enter_word_label(self, *args):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        edit_img = [child for child in word_grid.get_children() if isinstance(child, Gtk.Image)][0]
        # show widget and set flags to trigger transition effect, see application.css
        if stack.get_visible_child_name() == "word-view":
            edit_img.show()
            edit_img.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

    def on_leave_word_label(self, *args):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        edit_img = [child for child in word_grid.get_children() if isinstance(child, Gtk.Image)][0]
        # hide and reset state flagss to ready state for transition effect, see application.css
        if stack.get_visible_child_name() == "settings-view":
            pass
        else:
            edit_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

    def on_manual_lookup(self, eventbutton=None, eventbox=None, not_found=False, *args):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        word_label = [child for child in word_grid.get_children() if isinstance(child, Gtk.Label)][0]
        noword_view = stack.get_child_by_name("no-word-view")
        message = [child for child in noword_view.get_children() if child.get_name() == "message"][0]

        if stack.get_visible_child_name() == "word-view":
            if not_found:
                message.props.label = "Word not found"
            else:
                message.props.label = "Lookup a new word"
            
            # need to clear entry text since clipboard_listener will pickup the text as it will be selected on focus and cause a loop back to the word-view
            entry = [child for child in noword_view.get_children() if isinstance(child, Gtk.Entry)][0]
            entry.props.text = ""
            #need to show since it was hiddden in on_view_visible
            noword_view.show() 
            stack.set_visible_child_name(name="no-word-view")
            word_label.props.label = "QuickWord"
            self.active_view = noword_view
            self.current_view = "no-word-view"

    def on_view_visible(self, view, gparam=None, runlookup=None, word=None):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        word_label = [child for child in word_grid.get_children() if isinstance(child, Gtk.Label)][0]
        updater_view = stack.get_child_by_name("updater-view")
        word_view = stack.get_child_by_name("word-view")
        noword_view = stack.get_child_by_name("no-word-view")
        settings_view = stack.get_child_by_name("settings-view")
        app = self.props.application

        if word is not None:
            self.lookup_word = word.capitalize()
        
        # toggle settings-view visibility based on visible property
        # intial view is always settings-view since connected to its visible signal
        current_stack_child = {}
        current_stack_child["current"] = stack.get_visible_child()

        #print(current_stack_child["current"])

        if view.is_visible():
            word_label.props.label = "Settings"
            self.current_view = "settings-view"
            settings_view.on_totalwords()
            #print("on:settings")

        elif app.first_run is True:
            view.hide()
            word_label.props.label = "QuickWord"
            self.current_view = "updater-view"
            #print("updater")

        elif self.active_view == noword_view:
            view.hide()
            word_label.props.label = "QuickWord"
            self.current_view = "no-word-view"
            #print("noword-view")

        elif self.active_view == word_view and not app.lookup_word == "QuickWord":
            view.hide()
            word_label.props.label = word_view.lookup_word
            self.current_view = "word-view"
            #print("on:word-view")

        # elif self.active_view == word_view and app.lookup_word == "QuickWord":
        #     view.hide()
        #     word_label.props.label = "QuickWord"
        #     self.current_view = "no-word-view"
        #     print("on:word-view > no-word-view")

        elif self.active_view == updater_view:
            view.hide()
            word_label.props.label = "QuickWord"
            self.current_view = "updater-view"
            #print("on:updater-view")

        elif current_stack_child["current"] == word_view:
            view.hide()
            word_label.props.label = word_view.lookup_word
            self.current_view = "word-view"
            #print("on:settings-view > word-view")

        elif current_stack_child["current"] == noword_view:
            view.hide()
            word_label.props.label = "QuickWord"
            self.current_view = "no-word-view"
            #print("noword-view")

        elif current_stack_child["current"] == updater_view:
            view.hide()
            word_label.props.label = "QuickWord"
            self.current_view = "updater-view"
            #print("updater-view")

        #print(app.lookup_word)

        # toggle css styling
        if self.current_view == "settings-view":
            stack.get_style_context().add_class("stack-settings")
            headerbar.get_style_context().add_class("headerbar-settings")
        else:
            stack.get_style_context().remove_class("stack-settings")
            headerbar.get_style_context().remove_class("headerbar-settings")

        # finally set visible stack
        # print("active", self.active_view)
        # print("triggered", view)

        stack.set_visible_child_name(self.current_view)


    def on_persistent_mode(self, widget, event):
        # state flags for window active state
        self.state_flags = self.get_state_flags().value_names
        # print(self.state_flags)
        if not self.state_flags == self.active_state_flags and self.state_flags_changed_count > 1:
            self.destroy()
        else:
            self.state_flags_changed_count += 1
            # print('state-flags-changed', self.state_flags_changed_count)

