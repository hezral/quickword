#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_events.py
#
#  Copyright 2017 John Coppens <john*at*jcoppens*dot*com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class EventsTest(Gtk.Grid):
    def __init__(self):
        super(EventsTest, self).__init__()

        btn = Gtk.Button("Top right")
        btn.connect("clicked", lambda x: print("Button clicked"))

        self.attach(Gtk.Label("Top left"), 0, 0, 1, 1)
        self.attach(btn, 1, 0, 1, 1)
        self.attach(Gtk.SpinButton(), 0, 1, 1, 1)
        self.show_all()


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.connect("button-press-event", self.on_button_pressed)
        self.connect("event-after", self.on_event_after)

        evtest = EventsTest()

        self.add(evtest)
        # self.show_all()

    def on_button_pressed(self, btn, event):
        print("Main window button pressed")
        print(event)
        return True

    def on_event_after(self, wdg, event):
        print("Event after")

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))