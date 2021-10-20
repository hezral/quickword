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
from gi.repository import Gtk, Gdk


#------------------CLASS-SEPARATOR------------------#


class Clipboard():
    def __init__(self, atom_type):
        
        # create clipboard
        self.clipboard = Gtk.Clipboard.get(atom_type)

        # target type to listen for
        self.text_target = Gdk.Atom.intern('text/plain', False)


#------------------CLASS-SEPARATOR------------------#


class ClipboardListener(Clipboard):
    def __init__(self, *args, **kwargs):
        super().__init__(atom_type=Gdk.SELECTION_PRIMARY, *args, **kwargs)
        
    def copy_selected_text(self, clipboard=None, event=None):
        if self.clipboard.wait_is_target_available(self.text_target):
            content = self.clipboard.wait_for_text()

            # remove multiple lines and only return first line
            if "\n" in content:
                content = content.split("\n")[0]
                
            # lowercase the word
            content = content.lower()

            # remove spaces in front and back
            content = content.strip()

            # remove special characters in front of word
            if len(content) > 0:
                FirstContainsSpecialChars = any(not c.isalnum() for c in content[0])
                LastContainsSpecialChars = any(not c.isalnum() for c in content[len(content)-1])

                if FirstContainsSpecialChars:
                    content = content[1:]
                if LastContainsSpecialChars:
                    content = content[0:-1]

            # don't return empty lines
            if len(content) > 0:
                valid = True
                return content
        else:
            content = None
            valid = False
            return content


#------------------CLASS-SEPARATOR------------------#


class ClipboardPaste(Clipboard):
    def __init__(self, *args, **kwargs):
        super().__init__(atom_type=Gdk.SELECTION_CLIPBOARD, *args, **kwargs)

    def copy_to_clipboard(self, text_to_copy):
        self.clipboard.set_text(text_to_copy, -1)
