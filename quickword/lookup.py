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

from nltk import data
from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict as cm


class WordLookup():
    def __init__(self, application_id=None, *args, **kwargs):

        application_id = "com.github.hezral.quickword"

        nltk_data_path = os.path.join(GLib.get_user_data_dir(), application_id, 'nltk_data')

        data.path = [nltk_data_path]

        self.dictionary = cm.dict()

    def get_synsets(self, word):

        print('Word:', word)

        try:
            pronounce = self.dictionary[word]
            print(pronounce)
        except:
            pass

        synsets = wn.synsets(word)

        if len(synsets) > 0:
            print(len(synsets))
            print('Synonyms:', synsets)

            for synset in synsets:

                name = synset.name().split('.')[0]

                # sometimes synset contains underscore and maybe other special characters
                # need to remove them
                containsSpecialChars = any(not c.isalnum() for c in name)
                if containsSpecialChars:
                    name_removeSpecialChars = name.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                    print('Words:', name_removeSpecialChars)
                else:
                    print('Words:',name)

                definition = synset.definition()
                print('Definition:', definition)

                examples = synset.examples()
                print('Examples:', examples)

            return synsets

# Wordnet POS
# ADJ: 'a'
# ADJ_SAT: 's'
# ADV: 'r'
# NOUN: 'n'
# VERB: 'v'


# the lines is only for debug
# def lookup(clipboard=None, event=None, wd=None):
#     content, valid = clipboard_listener.copy_selected_text(clipboard)
#     if content and valid:
#         results = wd.get_synsets(content)
#         #print(results)
# from clipboard import ClipboardListener
# wd = WordLookup()
# clipboard_listener = ClipboardListener()
# clipboard_listener.copy_selected_text()

# the lines is only for debug
# clipboard_listener.clipboard.connect("owner-change", lookup, wd)
# import gi, signal
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, GLib
# GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)
# Gtk.main()
