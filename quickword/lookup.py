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
import os
from datetime import datetime
import gi
from gi.repository import GLib

from nltk import data, downloader
from nltk.corpus import wordnet as wn


APPLICATION_ID = "com.github.hezral.quickword"



class WordLookup():
    def __init__(self, *args, **kwargs):

        nltk_data_path = os.path.join(GLib.get_user_data_dir(), APPLICATION_ID, 'nltk_data')
        
        data.path = [nltk_data_path]
        downloader.download_dir = nltk_data_path
        data_downloader = downloader.Downloader()

        # check if data dir exist
        if not os.path.exists(nltk_data_path):
            os.makedirs(nltk_data_path)

        # check if wordnet data is installed
        if not data_downloader.is_installed('wordnet', nltk_data_path):
            data_downloader.download('wordnet')

        # check if omw data is installed for language support
        if not data_downloader.is_installed('omw', nltk_data_path):
            data_downloader.download('omw')

        # check if any data is stale and update it
        if data_downloader.is_stale('wordnet', nltk_data_path) and data_downloader.is_stale('omw', nltk_data_path):
            data_downloader.update(quiet=False, prefix=nltk_data_path)
    
    def get_synsets(self, word):
        synsets = wn.synsets(word)
        return synsets

wd = WordLookup()


print(wd.lookup('dog'))