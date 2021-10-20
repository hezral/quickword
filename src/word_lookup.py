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

import os
import gi
from gi.repository import GLib

# nltk imports
from nltk import data
from nltk.corpus import wordnet as wn

# for ipa output of words by espeak
import subprocess
from shutil import which, Error

class WordLookup():
    def __init__(self, application_id="com.github.hezral.quickword", *args, **kwargs):

        # setup nltk data path
        nltk_data_path = os.path.join(GLib.get_user_data_dir(), application_id, 'nltk_data')
        data.path = [nltk_data_path]

        #check if espeak is installed
        try:
            self.espeak = which("espeak")
        except Error as error:
            print("espeak not installed") 
        
    def get_synsets(self, word):

        # create list to store data to return
        # structure = word, pronounciation, synsets
        data_tuple = []

        # lowercase the word
        word = word.lower()

        # remove spaces in front and back
        word = word.strip()

        # remove special characters in front of word
        FirstContainsSpecialChars = any(not c.isalnum() for c in word[0])
        LastContainsSpecialChars = any(not c.isalnum() for c in word[len(word)-1])

        if FirstContainsSpecialChars:
             word = word[1:]
        if LastContainsSpecialChars:
             word = word[0:-1]

        # get synsets for word
        # wordnet lookup can only contain letters, numbers, spaces, hyphens, periods, slashes, and/or apostrophes.
        # check if safe chars and try to get synsets first
        containsSafeChar = set(" -./'_")
        if any((c in containsSafeChar) for c in word):

            synsets = wn.synsets(word)
            # if none returns
            if len(synsets) == 0:
                word = word.translate({ord(c): " " for c in " -./'_"}).split(" ")[0] #replace safe chars with space and only get for first word

                synsets = wn.synsets(word)
        else:
            synsets = wn.synsets(word)
        
        # clean up word for display, remove any special characters
        containsSpecialChars = any(not c.isalnum() for c in word)
        if containsSpecialChars:
            _word = word.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            data_tuple.append(_word.title())
        else:
            data_tuple.append(word.capitalize())

        # get pronounciation
        try:
            run_espeak = subprocess.Popen([self.espeak, word, "-q", "--ipa"], stdout=subprocess.PIPE)
            stdout, stderr = run_espeak.communicate()
            pronounce = stdout.decode("utf-8").split("\n")[0].strip()
        except:
            pronounce = ["NA"]
        # add pronounciation to data list

        data_tuple.append(pronounce)

        # add to data list if there is any synset found
        if len(synsets) > 0:
            data_tuple.append(synsets)

            return data_tuple

    def get_totalwords(self):
        return len(wn._lemma_pos_offset_map)


# wl = WordLookup()

# print(type(wl))

# wl.get_synsets("test")

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
