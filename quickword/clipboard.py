#!/usr/bin/env python3

'''
    Copyright 2018 Adi Hezral (hezral@gmail.com)

    This file is part of QuickWord.

    QuickWord is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    QuickWord is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with QuickWord.  If not, see <http://www.gnu.org/licenses/>.
'''


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import signal

class Clipboard():
    def __init__(self):
        # create clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        # target type to listen for
        self.text_target = Gdk.Atom.intern('text/plain', False)

        # this line is only for debug
        self.clipboard.connect("owner-change", self.clipboard_changed)
        # this line is only for debug
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit) 

class ClipboardListener(Clipboard):

    def clipboard_changed(self, clipboard=None, event=None):
        if self.clipboard.wait_is_target_available(self.text_target):
            content = self.clipboard.wait_for_text()
            # avoid returning multi-word selections
            if len(content.split(" ")) > 1:
                valid = False
            else:
                valid = True
        else:
            content = None
            valid = False
        # this line is only for debug
        print(content, valid)
        return content, valid

class ClipboardCopy(Clipboard):
    
    def copied(self, clipboard=None, event=None):
        print('copy')

# this line is only for debug
clips = ClipboardListener()
Gtk.main()