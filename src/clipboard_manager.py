# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

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
