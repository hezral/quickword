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

from re import sub
import sys, os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject, Pango

# QuickWord imports
from settings_view import SettingsView
from noword_view import NoWordView

#------------------CLASS-SEPARATOR------------------#

class QuickWordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- constants --------#
        self.lookup_word = "QuickWord"

        #-- view --------#
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
        
        #-- header --------#
        #------ lookup word label ----#
        word_label = Gtk.Label(self.lookup_word)
        word_label.props.selectable = True
        word_label.props.halign = Gtk.Align.START
        word_label.props.valign = Gtk.Align.CENTER
        word_label.get_style_context().add_class("lookup-word-header")

        #------ view switch ----#
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path("data/icons")
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

        

        #-- window construct--------#
        self.props.resizable = True
        # self.props.skip_taskbar_hint = True
        self.title = "QuickWord"
        self.set_keep_above(True)
        self.get_style_context().add_class("rounded")
        self.set_size_request(600, 500)
        self.props.window_position = Gtk.WindowPosition.MOUSE
        self.set_titlebar(headerbar)
        self.add(stack)

        
        
        #-- window settings--------#
        self.state_flags_changed_count = 0
        self.active_state_flags = ['GTK_STATE_FLAG_NORMAL', 'GTK_STATE_FLAG_DIR_LTR']
        
        gio_settings = Gio.Settings(schema_id="com.github.hezral.quickword")
        
        if not gio_settings.get_value("persistent-mode"):
            self.state_flags_on = self.connect("state-flags-changed", self.on_persistent_mode)
            # print('state-flags-on')
        if not gio_settings.get_value("sticky-mode"):
            self.stick()
        
        

    def on_view_visible(self, view, gparam=None, runlookup=None, word=None):
        # get window children
        window = self
        window_children = window.get_children()
        stack = [child for child in window_children if isinstance(child, Gtk.Stack)][0]
        headerbar = [child for child in window_children if isinstance(child, Gtk.HeaderBar)][0]
        word_label = [child for child in headerbar.get_children() if isinstance(child, Gtk.Label)][0]

        if word is not None:
            self.lookup_word = word.capitalize()

        # toggle settings-view visibility based on visible property
        if view.props.name == "settings-view" and view.is_visible():
            view.show_all()
            stack.set_visible_child_full(name="settings-view", transition=Gtk.StackTransitionType.CROSSFADE)
            stack.get_style_context().add_class("stack-settings")
            word_label.props.label = "Settings"
            headerbar.get_style_context().add_class("headerbar-settings")
        elif view.props.name == "no-word-view" and runlookup:
            view.hide()
            stack.set_visible_child_full(name="word-view", transition=Gtk.StackTransitionType.CROSSFADE)
            word_label.props.label = self.lookup_word
            headerbar.get_style_context().remove_class("headerbar-settings")
        elif self.lookup_word == "QuickWord":
            view.hide()
            word_label.props.label = self.lookup_word
            stack.get_style_context().remove_class("stack-settings")
            stack.set_visible_child_full(name="no-word-view", transition=Gtk.StackTransitionType.CROSSFADE)
            headerbar.get_style_context().remove_class("headerbar-settings")
        else:
            view.hide()
            word_label.props.label = self.lookup_word
            stack.get_style_context().remove_class("stack-settings")
            stack.set_visible_child_full(name="word-view", transition=Gtk.StackTransitionType.CROSSFADE)
            headerbar.get_style_context().remove_class("headerbar-settings")

        # # toggle settings_view visiblility based on visible property
        # if view.is_visible():
        #     view.show_all()
        #     stack.set_visible_child_full(name="settings-view", transition=Gtk.StackTransitionType.CROSSFADE)
        #     stack.get_style_context().add_class("stack-settings")
        # else:
        #     view.hide()
        #     stack.get_style_context().remove_class("stack-settings")
        #     if self.lookup_word == "QuickWord":
        #         stack.set_visible_child_full(name="no-word-view", transition=Gtk.StackTransitionType.CROSSFADE)
        #     else:
        #         stack.set_visible_child_full(name="word-view", transition=Gtk.StackTransitionType.CROSSFADE)

        # if word_label.get_label() == "Settings":
        #     word_label.props.label = self.lookup_word
        #     headerbar.get_style_context().remove_class("headerbar-settings")
        # else:
        #     word_label.props.label = "Settings"
        #     headerbar.get_style_context().add_class("headerbar-settings")



    def on_persistent_mode(self, widget, event):
        # state flags for window active state
        self.state_flags = self.get_state_flags().value_names
        # print(self.state_flags)
        if not self.state_flags == self.active_state_flags and self.state_flags_changed_count > 1:
            self.destroy()
        else:
            self.state_flags_changed_count += 1
            # print('state-flags-changed', self.state_flags_changed_count)


#------------------CLASS-SEPARATOR------------------#




#------------------CLASS-SEPARATOR------------------#

class WordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- view construct--------#
        self.props.name = 'word-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 12
        self.props.column_spacing = 6

        #-- view contents--------#
        definition = WordSection(name="definition", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        other = WordSection(name="other", contents="This is a contents block of text with lots of texts lots of texts lots of texts lots of texts")
        
        self.attach(definition, 0, 1, 1, 1)
        self.attach(other, 0, 2, 1, 1)





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
        copy_img.props.valign = Gtk.Align.END
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



