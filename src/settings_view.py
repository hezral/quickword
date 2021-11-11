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
from gi.repository import Gtk, Gio, Gdk, GObject, Pango, Granite


class SettingsView(Gtk.Grid):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.app = app

        theme_switch = SubSettings(type="switch", name="theme-switch", label="Switch between Dark/Light theme", sublabel=None, separator=False)
        theme_optin = SubSettings(type="checkbutton", name="theme-optin", label=None, sublabel=None, separator=True, params=("Follow system appearance style",))

        theme_switch.switch.bind_property("active", self.app.gtk_settings, "gtk-application-prefer-dark-theme", GObject.BindingFlags.SYNC_CREATE)

        self.app.granite_settings.connect("notify::prefers-color-scheme", self.on_appearance_style_change, theme_switch)
        theme_switch.switch.connect_after("notify::active", self.on_switch_activated)
        theme_optin.checkbutton.connect_after("notify::active", self.on_checkbutton_activated, theme_switch)
        
        self.app.gio_settings.bind("prefer-dark-style", theme_switch.switch, "active", Gio.SettingsBindFlags.DEFAULT)
        self.app.gio_settings.bind("theme-optin", theme_optin.checkbutton, "active", Gio.SettingsBindFlags.DEFAULT)

        close_button = SubSettings(type="switch", name="close-button", label="Show close button", sublabel="Always show close button",separator=True)
        close_button.switch.connect_after("notify::active", self.on_switch_activated)
        self.app.gio_settings.bind("close-button", close_button.switch, "active", Gio.SettingsBindFlags.DEFAULT)

        persistent_mode = SubSettings(type="switch", name="persistent-mode", label="Persistent mode", sublabel="Stays open and updates as text changes",separator=True)
        persistent_mode.switch.connect_after("notify::active", self.on_switch_activated, close_button)
        self.app.gio_settings.bind("persistent-mode", persistent_mode.switch, "active", Gio.SettingsBindFlags.DEFAULT)

        close_mode = SubSettings(type="switch", name="close-mode", label="Background mode", sublabel="Close window and run-in-background",separator=True)
        close_mode.switch.connect_after("notify::active", self.on_switch_activated)
        self.app.gio_settings.bind("close-mode", close_mode.switch, "active", Gio.SettingsBindFlags.DEFAULT)
        
        sticky_mode = SubSettings(type="switch", name="sticky-mode", label="Sticky mode", sublabel="Window is displayed on all workspaces",separator=False)
        sticky_mode.switch.connect_after("notify::active", self.on_switch_activated)
        self.app.gio_settings.bind("sticky-mode", sticky_mode.switch, "active", Gio.SettingsBindFlags.DEFAULT)

        display_behaviour = SettingsGroup("Display & Behaviour", (theme_switch, theme_optin, persistent_mode, close_button, close_mode, sticky_mode))

        buyme_coffee = SubSettings(type="button", name="buy-me-coffee", label="Show Support", sublabel="Thanks for supporting me!", separator=False, params=("Coffee Time", Gtk.Image().new_from_icon_name("com.github.hezral.quickword-coffee", Gtk.IconSize.LARGE_TOOLBAR), ))
        buyme_coffee.button.connect("clicked", self.on_button_clicked)

        check_updates = SubSettings(type="button", name="check-updates", label="NA", sublabel=None, separator=True, params=("Check Updates", Gtk.Image().new_from_icon_name("software-update-available", Gtk.IconSize.LARGE_TOOLBAR), ))
        check_updates.button.connect("clicked", self.on_button_clicked)

        others = SettingsGroup("Others", (check_updates, buyme_coffee, ))

        self.props.name = "settings-view"
        self.get_style_context().add_class(self.props.name)
        self.props.expand = True
        self.props.margin = 20
        self.props.margin_top = 10
        self.props.row_spacing = 10
        self.props.column_spacing = 6
        self.attach(display_behaviour, 0, 0, 1, 1)
        self.attach(others, 0, 1, 1, 1)

    def on_button_clicked(self, button, params=None):
        name = button.get_name()
        if name == "check-updates":
            self.on_check_update()
        if name == "buy-me-coffee":
            Gtk.show_uri_on_window(None, "https://www.buymeacoffee.com/hezral", Gdk.CURRENT_TIME)

    def on_check_update(self):
        stack = self.get_parent()
        window = stack.get_parent()

        window.updater_view.show_all()
        window.stack.set_visible_child_name("updater-view")
        window.word_label.props.label = "Updater"
        window.settings_view.hide()

    def on_totalwords(self):
        stack = self.get_parent()
        window = stack.get_parent()
        app = window.props.application
        others_settinggroup = [child for child in self.get_children() if child.get_name() == "Others"][0]
        others_settinggroup_frame = [child for child in others_settinggroup.get_children() if isinstance(child, Gtk.Frame)][0]
        check_updates_subsetting = [child for child in others_settinggroup_frame.get_children()[0].get_children() if child.get_name() == "check-updates"][0]
        # print(check_updates_subsetting.get_children())

        if check_updates_subsetting.label_text.props.label == "NA":
            check_updates_subsetting.label_text.props.label = "Total words available: " + str(app._word_lookup.get_totalwords())

    def generate_separator(self):
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER
        return separator

    def on_switch_activated(self, switch, gparam, widget=None):
        name = switch.get_name()
        main_window = self.get_toplevel()

        if self.is_visible():
            # stack = self.get_parent()
            # window = stack.get_parent()
            if name == "persistent-mode":
                close_button = widget
                if switch.get_active():
                    self.app.window_manager._stop()
                    main_window.set_keep_above(True) # manually trigger a window manager event to stop the thread
                    main_window.headerbar.set_show_close_button(True)
                    main_window.word_label.props.margin_left = 0
                    # if self.app.gio_settings.get_value("close-button"):
                        # close_button.props.sensitive = True
                else:
                    self.app.window_manager._run(callback=main_window.on_persistent_mode)
                    if not self.app.gio_settings.get_value("close-button"):
                        main_window.headerbar.set_show_close_button(False)
                        main_window.word_label.props.margin_left = 10

                main_window.headerbar.hide()
                main_window.headerbar.show_all()

            if name == "sticky-mode":
                if switch.get_active():
                    main_window.stick()
                else:
                    main_window.unstick()

            if name == "close-button":
                if switch.get_active():
                    main_window.word_label.props.margin_left = 0
                    main_window.headerbar.set_show_close_button(True)
                else:
                    main_window.word_label.props.margin_left = 10
                    main_window.headerbar.set_show_close_button(False)
                main_window.headerbar.hide()
                main_window.headerbar.show_all()
                        

            

    def on_checkbutton_activated(self, checkbutton, gparam, widget):
        name = checkbutton.get_name()
        theme_switch = widget
        if name == "theme-optin":
            if self.app.gio_settings.get_value("theme-optin"):
                prefers_color_scheme = self.app.granite_settings.get_prefers_color_scheme()
                sensitive = False
            else:
                prefers_color_scheme = Granite.SettingsColorScheme.NO_PREFERENCE
                theme_switch.switch.props.active = self.app.gio_settings.get_value("prefer-dark-style")
                sensitive = True

            self.app.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
            self.app.granite_settings.connect("notify::prefers-color-scheme", self.app.on_prefers_color_scheme)

            if "DARK" in prefers_color_scheme.value_name:
                active = True
            else:
                active = False

            theme_switch.switch.props.active = active
            theme_switch.props.sensitive = sensitive

    def on_appearance_style_change(self, granite_settings, gparam, widget):
        theme_switch = widget
        if theme_switch.switch.props.active:
            theme_switch.switch.props.active = False
        else:
            theme_switch.switch.props.active = True


class SettingsGroup(Gtk.Grid):
    def __init__(self, group_label, subsettings_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grid = Gtk.Grid()
        grid.props.margin = 8
        grid.props.hexpand = True
        grid.props.row_spacing = 8
        grid.props.column_spacing = 10

        i = 0
        for subsetting in subsettings_list:
            grid.attach(subsetting, 0, i, 1, 1)
            i += 1

        frame = Gtk.Frame()
        frame.props.name = "settings-group-frame"
        frame.props.hexpand = True
        frame.add(grid)

        label = Gtk.Label(group_label)
        label.props.name = "settings-group-label"
        label.props.halign = Gtk.Align.START
        label.props.margin_left = 4

        self.props.name = group_label
        self.props.halign = Gtk.Align.FILL
        self.props.hexpand = True
        self.props.row_spacing = 4
        self.props.can_focus = False
        self.attach(label, 0, 0, 1, 1)
        self.attach(frame, 0, 1, 1, 1)


class SubSettings(Gtk.Grid):
    def __init__(self, type=None, name=None, label=None, sublabel=None, separator=True, params=None, utils=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = type

        # box---
        box = Gtk.VBox()
        box.props.spacing = 2
        box.props.hexpand = True

        # label---
        if label is not None:
            self.label_text = Gtk.Label(label)
            self.label_text.props.halign = Gtk.Align.START
            box.add(self.label_text)
        
        # sublabel---
        if sublabel is not None:
            self.sublabel_text = Gtk.Label(sublabel)
            self.sublabel_text.props.halign = Gtk.Align.START
            self.sublabel_text.props.wrap_mode = Pango.WrapMode.WORD
            self.sublabel_text.props.max_width_chars = 30
            self.sublabel_text.props.justify = Gtk.Justification.LEFT
            #self.sublabel_text.props.wrap = True
            self.sublabel_text.get_style_context().add_class("settings-sub-label")
            box.add(self.sublabel_text)

        if type == "switch":
            self.switch = Gtk.Switch()
            self.switch.props.name = name
            self.switch.props.halign = Gtk.Align.END
            self.switch.props.valign = Gtk.Align.CENTER
            self.switch.props.hexpand = False
            self.attach(self.switch, 1, 0, 1, 2)

        if type == "spinbutton":
            self.spinbutton = Gtk.SpinButton().new_with_range(min=params[0], max=params[1], step=params[2])
            self.spinbutton.props.name = name
            self.attach(self.spinbutton, 1, 0, 1, 2)

        if type == "button":
            if len(params) == 1:
                self.button = Gtk.Button(label=params[0])
            else:
                self.button = Gtk.Button(label=params[0], image=params[1])
            self.button.props.name = name
            self.button.props.hexpand = False
            self.button.props.always_show_image = True
            self.button.set_size_request(90, -1)
            if len(params) >1:
                label = [child for child in self.button.get_children()[0].get_child() if isinstance(child, Gtk.Label)][0]
                label.props.valign = Gtk.Align.CENTER
            self.attach(self.button, 1, 0, 1, 2)

        if type == "checkbutton":
            self.checkbutton = Gtk.CheckButton().new_with_label(params[0])
            self.checkbutton.props.name = name
            self.attach(self.checkbutton, 0, 0, 1, 2)

        # separator ---
        if separator:
            row_separator = Gtk.Separator()
            row_separator.props.hexpand = True
            row_separator.props.valign = Gtk.Align.CENTER
            if type == None:
                self.attach(row_separator, 0, 0, 1, 1)
            else:
                self.attach(row_separator, 0, 2, 2, 1)
        
        # SubSettings construct---
        self.props.name = name
        self.props.hexpand = True
        if type == None:
            self.attach(box, 0, 0, 1, 1)
        else:
            self.props.row_spacing = 8
            self.props.column_spacing = 10
            self.attach(box, 0, 0, 1, 2)