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

            # if selected text contains underscore and maybe other special characters
            # try to remove them and get the first word
            containsSpecialChars = any(not c.isalnum() for c in content)
            if containsSpecialChars:
                content_remove_special_chars = content.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                content = content_remove_special_chars.split(" ")[0]
            
            # avoid returning multi-word selections, just the first word
            if len(content.split(" ")) > 1:
                content = content.split(" ")[0]

            valid = True

            return content
        else:
            content = None
            valid = False



#------------------CLASS-SEPARATOR------------------#


class ClipboardPaste(Clipboard):
    def __init__(self, *args, **kwargs):
        super().__init__(atom_type=Gdk.SELECTION_CLIPBOARD, *args, **kwargs)

    def copy_to_clipboard(self, text_to_copy):
        self.clipboard.set_text(text_to_copy, -1)




# # this line is only for debug
# clips = ClipboardListener()
# clips.clipboard.connect("owner-change", self.copy_selected_text)
# import signal
# from gi.repository import GLib
# GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit) 

# Gtk.main()