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
from gi.repository import Gtk, Pango

# for espeak
import subprocess
from shutil import which, Error

#------------------CLASS-SEPARATOR------------------#


class WordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # copy to clipboard
        self.clipboard_paste = None
        self.lookup_word = None

        #-- pronounciation --------#
        pronounciation_label = Gtk.Label()
        pronounciation_label.props.name = "pronounciation-label"
        pronounciation_label.props.halign = Gtk.Align.START
        pronounciation_label.props.hexpand = True
        pronounciation_label.get_style_context().add_class(pronounciation_label.props.name)

        #-- speak button --------#
        speak_btn = Gtk.Button(image=Gtk.Image().new_from_icon_name("audio-volume-high-symbolic", Gtk.IconSize.SMALL_TOOLBAR))
        speak_btn.props.halign = Gtk.Align.START
        speak_btn.props.hexpand = False
        speak_btn.props.margin_right = 5
        speak_btn.props.name = "speak-btn"
        speak_btn.connect("clicked", self.on_speak_word)
        speak_btn.set_size_request(30, 24)

        #-- stack construct --------#
        stack = Gtk.Stack()
        stack.props.expand = True
        stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        
        # info stack switcher contruct
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.stack = stack
        stack_switcher.props.margin_top = 4
        stack_switcher.get_style_context().add_class("subview-switcher")       

         #-- WordView construct--------#
        self.props.name = 'word-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = False
        self.props.margin = 20
        self.props.margin_top = 0
        self.props.row_spacing = 6       
        self.attach(speak_btn, 0, 1, 1, 1)
        self.attach(pronounciation_label, 1, 1, 1, 1)
        self.attach(stack, 0, 2, 2, 1)
        self.attach(stack_switcher, 0, 3, 2, 1,)

    def on_speak_word(self, button):
        try:
            subprocess.call(["espeak", self.lookup_word])
        except:
            pass

    def on_wordlookup(self, button=None, data=None):
        view = self
        pronounciation_label = [child for child in view.get_children() if child.get_name() == "pronounciation-label"][0]
        speak_btn = [child for child in view.get_children() if child.get_name() == "speak-btn"][0]
        stack = [child for child in view.get_children() if isinstance(child, Gtk.Stack)][0]
        stack_switcher = [child for child in view.get_children() if isinstance(child, Gtk.StackSwitcher)][0]

        self.lookup_word = data[0]
        synsets = data[2]

        # set pronounciation label
        pronounciation = data[1]
        pronounciation_label.props.label = "/ " + pronounciation + " /"
        
        # delete all stack children if any
        if stack.get_children():
            for child in stack.get_children():
                stack.remove(child)

        # create list for each type of word
        noun_data = []
        adjective_data = []
        adverb_data = []
        ver_data = []

        # add data to each word list
        for synset in synsets:
            if synset.pos() == "n":
                noun_data.append(synset)
            if synset.pos() == "a" or synset.pos() == "s":
                adjective_data.append(synset)
            if synset.pos() == "r":
                adverb_data.append(synset)
            if synset.pos() == "v":
                ver_data.append(synset)

        # add word lists to dict
        word_list_dict = {}
        word_list_dict["noun"] = noun_data
        word_list_dict["adjective"] = adjective_data
        word_list_dict["adverb"] = adverb_data
        word_list_dict["verb"] = ver_data

        subviews = {}
        for type in word_list_dict:
            if len(word_list_dict[type]) > 0:
                subviews["{0}".format(type)] = WordSubView(name=type, word=self.lookup_word, contents=word_list_dict[type])
                
        # add views to stack
        for view in subviews:
            stack.add_titled(subviews[view], view, view)
        
        # # style left and right tabs for stack switcher
        stack_count = len(stack_switcher.get_children())
        left_tab = stack_switcher.get_children()[0]
        left_tab.get_style_context().add_class("word-types-left")
        right_tab = stack_switcher.get_children()[stack_count-1]
        right_tab.get_style_context().add_class("word-types-right")
        
        stack.show_all()


#------------------CLASS-SEPARATOR------------------#


class WordSubView(Gtk.Grid):
    def __init__(self, name, word, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- WordSubView construct -----#
        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 6
        self.props.column_spacing = 0

        if len(self.get_children()) > 0:
            print("children:", self.get_children())

        scrolled_view = Gtk.ScrolledWindow()
        scrolled_view.props.vexpand = True
        scrolled_view.set_size_request(-1, 500)
        scrolled_view_grid = Gtk.Grid()

        i = 1
        for content in contents:
            if len(contents) > 10:
                scrolled_view_grid.attach(WordItems(word, content), 0, i, 1, 1)
            else:
                self.attach(WordItems(word, content), 0, i, 1, 1)
            i += 1
        
        if len(scrolled_view_grid.get_children()) > 10:
            scrolled_view.add(scrolled_view_grid)
            self.attach(scrolled_view, 0, 1, 1, 1)

            more_count = len(scrolled_view_grid.get_children()) - 10
            label = Gtk.Label(str(more_count) + " more results below..")
            label.get_style_context().add_class("more-results")
            self.attach(label, 0, 2, 1, 1)

#------------------CLASS-SEPARATOR------------------#


class WordItems(Gtk.Grid):
    def __init__(self, word, contents, multi=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # synset item
        synset = contents
        
        #-- word definition -------#
        definition_str = synset.definition()

        word_definition = Gtk.Label(definition_str)
        word_definition.props.max_width_chars = 50
        word_definition.props.wrap = True
        word_definition.props.hexpand = True
        word_definition.props.wrap_mode = Pango.WrapMode.WORD
        word_definition.props.justify = Gtk.Justification.FILL
        word_definition.props.halign = Gtk.Align.START
        word_definition.props.valign = Gtk.Align.CENTER
        word_definition.get_style_context().add_class("word-definition")

        #-- word examples -------#
        examples = synset.examples()

        if len(examples) > 0:
            examples_str = '"' + examples[0] + '"'
        else:
            examples_str = ""

        word_examples = Gtk.Label(examples_str)
        word_examples.props.max_width_chars = 50
        word_examples.props.wrap = True
        word_examples.props.hexpand = True
        word_examples.props.wrap_mode = Pango.WrapMode.WORD
        word_examples.props.justify = Gtk.Justification.FILL
        word_examples.props.halign = Gtk.Align.START
        word_examples.props.valign = Gtk.Align.START
        word_examples.get_style_context().add_class("word-examples")

        # box for definition and examples
        word_box = Gtk.VBox()
        word_box.props.hexpand = True
        word_box.set_size_request(-1, 24)
        word_box.add(word_definition)
        if not examples_str == "":
            word_definition.props.valign = Gtk.Align.START
            word_box.add(word_examples)

        #-- lemmas (similar words) -------#
        lemmas = synset.lemma_names()
        # print(lemmas)

        lemmas.sort(key=len)

        # print(lemmas)

        # remove lemma that is same with lookup word
        for lemma in lemmas:
            if lemma.lower() == word.lower():
                lemmas.remove(lemma)
 
        # grid to hold lemma till 5th item
        lemma_box = Gtk.Grid()
        lemma_box.props.column_spacing = 2
        lemma_box.props.row_spacing = 2
        lemma_box.props.hexpand = True
        lemma_box.props.halign = Gtk.Align.START

        # grid to hold lemma for 6th item onwards
        lemma_more_box = Gtk.Grid()
        lemma_more_box.props.margin_top = 10
        lemma_more_box.props.hexpand = False
        lemma_more_box.props.halign = Gtk.Align.START
        lemma_more_box.props.column_spacing = 2
        lemma_more_box.props.row_spacing = 4
        # encased into expander
        lemma_more_expander = Gtk.Expander()
        lemma_more_expander.props.margin_top = 3        
        lemma_more_expander.add(lemma_more_box)
        
        # iterate through lemmas list
        i = j = k = 0
        charslen = 0
        charslenmore = 0
        if len(lemmas) > 1:
            for lemma in lemmas:
                # if text contains underscore and maybe other special characters
                # use lemma_label for cleaned string
                # use lemma_name for original string
                containsSpecialChars = any(not c.isalnum() for c in lemma)
                if containsSpecialChars:
                    lemma_name = lemma.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                else:
                    lemma_name = lemma

                charslen = len(lemma) + charslen
                if i < 6:
                    if charslen <= 70:
                        lemma_box.attach(self.generate_lemma_buttons(lemma_label=lemma_name, lemma_name=lemmas[i]), i, 1, 1, 1)
                    else:
                        charslenmore = len(lemma) + charslenmore
                        if charslenmore <= 70:
                            lemma_more_box.attach(self.generate_lemma_buttons(lemma_label=lemma_name, lemma_name=lemmas[i]), j, 1, 1, 1)
                            j += 1
                        else:
                            lemma_more_box.attach(self.generate_lemma_buttons(lemma_label=lemma_name, lemma_name=lemmas[i]), k, 2, 1, 1) #need to recalculate i from zero and offset
                            k += 1
                i += 1

        # add margin if lemma_more_box is present
        if len(lemma_more_box.get_children()) >= 1:
            lemma_box.props.margin_left = 16

        #-- copy action -------#
        copy_img = Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        copy_img.props.no_show_all = True
        copy_img.props.hexpand = True
        copy_img.props.halign = Gtk.Align.END
        copy_img.props.valign = Gtk.Align.END
        copy_img.get_style_context().add_class("transition-on")
        copy_img.get_style_context().add_class("copy-img")
        
        # copied notification
        copied_img = Gtk.Image().new_from_icon_name("emblem-default", Gtk.IconSize.SMALL_TOOLBAR)
        copied_img.props.no_show_all = True
        copied_label = Gtk.Label("Copied to clipboard")
        copied_label.props.no_show_all = True
        
        copied_grid = Gtk.Grid()
        copied_grid.props.column_spacing = 4
        copied_grid.props.halign = Gtk.Align.END
        copied_grid.props.valign = Gtk.Align.END
        copied_grid.props.hexpand = True
        copied_grid.get_style_context().add_class("transition-on")
        copied_grid.get_style_context().add_class("copied-content")
        copied_grid.attach(copied_img, 0, 1, 1, 1)
        copied_grid.attach(copied_label, 1, 1, 1, 1)
       
        # workaround to avoid weird issue with enter and notify events after adding to the eventbox
        # put all in a grid, then put in eventbox. overlay didn't work
        content_grid = Gtk.Grid()
        content_grid.props.row_spacing = 0
        content_grid.props.hexpand = True
        content_grid.attach(copy_img, 0, 1, 1, 2)
        content_grid.attach(copied_grid, 0, 1, 1, 2)
        content_grid.attach(word_box, 0, 1, 1, 1)

        #-- eventbox -------#
        content_eventbox = Gtk.EventBox()
        content_eventbox.add(content_grid)
        
        # list items to pass to eventbox events
        eventbox_params = (copy_img, copied_label, copied_img, copied_grid, word, word_definition, word_examples)

        content_eventbox.connect("enter-notify-event", self.on_enter_content_box, eventbox_params)
        content_eventbox.connect("leave-notify-event", self.on_leave_content_box, eventbox_params)
        content_eventbox.connect("button-press-event", self.on_copy_content_clicked, eventbox_params)

        #-- WordItems construct--------#
        # self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 2
        self.props.column_spacing = 0        
        self.attach(content_eventbox, 0, 1, 5, 1)

        if len(lemma_more_box) >= 1:
            self.attach(lemma_more_expander, 0, 2, 5, 1)
            self.attach(lemma_box, 1, 2, 1, 1)
        else:
            self.attach(lemma_box, 0, 2, 1, 1)


    def generate_lemma_buttons(self, lemma_label, lemma_name):
        button = Gtk.Button(label=lemma_label)
        button.props.name = lemma_name
        button.props.expand = False
        button.get_style_context().add_class("word-lemmas")
        button.connect("clicked", self.on_lemma_clicked)
        return button
    
    def on_lemma_clicked(self, button):
        wordview = self.get_wordview()
        stack = wordview.get_parent()
        window = stack.get_parent()
        app = window.props.application
        # callback to WordLookup
        lookup = app.emit("on-new-word-lookup", button.props.name)
        # check if word lookup succeeded or not
        if lookup is False:
            pass

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
        copy_img.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

        # set flags to ready state for transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

    def on_leave_content_box(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_grid = widget_list[3]

        # reset state flagss to ready state for transition effect, see application.css
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # reset state flags to ready state for transition effect, see application.css
        # grid can stay as show state since only toggle widget hide/shows
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

    def on_copy_content_clicked(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_label = widget_list[1]
        copied_img = widget_list[2]
        copied_grid = widget_list[3]
        word = widget_list[4]
        word_definition = widget_list[5]
        word_example = widget_list[6]

        # reset state flagss to ready state for transition effect, see application.css
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # show widgets
        copied_label.show()
        copied_img.show()

        # set flags to trigger transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

        # callback to copy content to clipboard
        clipboard_paste = self.get_wordview().clipboard_paste
        to_copy = "Word: " + word + "\n"
        to_copy = to_copy + "Definition: " + word_definition.props.label + "\n"
        to_copy = to_copy + "Example: " + word_example.props.label
        clipboard_paste.copy_to_clipboard(to_copy)

    def get_wordview(self):        
        worditem = self
        # if not in scrolled view
        if isinstance(worditem.get_parent(), WordSubView):
            wordsubview = worditem.get_parent() #WordSubView
            stack = wordsubview.get_parent() #GtkStack
            wordview = stack.get_parent() #WordView
        # in scrolled view
        else:
            worditemgrid = worditem.get_parent() #GtkGrid
            viewport = worditemgrid.get_parent() #GtkViewport
            scrolledwindow = viewport.get_parent() #GtkScrolledWindow
            wordsubview = scrolledwindow.get_parent() #WordSubView
            stack = wordsubview.get_parent() #GtkStack
            wordview = stack.get_parent() #WordView
        return wordview
