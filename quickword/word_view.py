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


#------------------CLASS-SEPARATOR------------------#


class WordView(Gtk.Grid):
    def __init__(self, word_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # copy to clipboard
        self.clipboard_paste = None

        #-- pronounciation --------#
        pronounciation_label = Gtk.Label()
        pronounciation_label.props.name = "pronounciation_label"
        pronounciation_label.props.halign = Gtk.Align.START
        pronounciation_label.props.expand = False
        pronounciation_label.get_style_context().add_class("pronounciation-label")

        #-- stack construct --------#
        stack = Gtk.Stack()
        stack.props.expand = True
        stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        
        # info stack switcher contruct
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.stack = stack
        stack_switcher.get_style_context().add_class("subview-switcher")

        button = Gtk.Button(label="remove")
        button.connect("clicked", self.on_wordlookup)

         #-- WordView construct--------#
        self.props.name = 'word-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = False
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 12
        self.props.column_spacing = 6
        self.attach(pronounciation_label, 0, 1, 1, 1)
        self.attach(stack, 0, 2, 1, 1)
        self.attach(stack_switcher, 0, 3, 1, 1,)

    def on_wordlookup(self, button=None, data=None):
        view = self
        pronounciation_label = [child for child in view.get_children() if child.get_name() == "pronounciation_label"][0]
        stack = [child for child in view.get_children() if isinstance(child, Gtk.Stack)][0]
        stack_switcher = [child for child in view.get_children() if isinstance(child, Gtk.StackSwitcher)][0]

        word = data[1]
        synsets = data[2]

        # if len(pronounciation) > 1:
        #     for i in pronounciation:
        #         pronounciation = pronounciation + "," + "/" + i + "/"
        # else:
        #     pronounciation = "/" + data[1] + "/"
        # pronounciation_label.props.label = '-'.join(pronounciation)

        pronounciation = data[1]
        # pronounciation_str = ""
        # if len(pronounciation) > 1:
        #     for item in pronounciation:
        #         if pronounciation_str == "":
        #             pronounciation_str = "," + item
        #         else:
        #             pronounciation_str = pronounciation_str + ", " + item
        # elif len(pronounciation) == 0:
        #     pronounciation_str = ""
        # else:
        #     pronounciation_str = pronounciation[0]

        #print(pronounciation_str)

        #pronounciation_label.props.label = "/ " + '-'.join(pronounciation_str) + " /"

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
                subviews["{0}".format(type)] = WordSubView(name=type, contents=word_list_dict[type])
                
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
    def __init__(self, name, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- WordSubView construct -----#
        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 6
        self.props.column_spacing = 0

        if len(self.get_children()) > 0:
            print("children:", self.get_children())

        i = 1
        for content in contents:
            self.attach(WordItems(content), 0, i, 1, 1)
            i += 1
        

#------------------CLASS-SEPARATOR------------------#


class WordItems(Gtk.Grid):
    def __init__(self, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #print("content", dir(contents))
        synset = contents

        lemmas = synset.lemma_names()

        # if text contains underscore and maybe other special characters
        # try to remove them and get the first word
        for lemma in lemmas:
            containsSpecialChars = any(not c.isalnum() for c in lemma)
            if containsSpecialChars:
                new_lemma = lemma.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                lemmas.append(new_lemma)
                lemmas.remove(lemma)

        lemmas_str = ""
        if len(lemmas) > 1:
            for i in range(0, len(lemmas), 6):
                if i < 6:
                    lemmas_str += ", ".join(lemmas[i:i+6])
                else:
                    lemmas_str += "\n" + ", ".join(lemmas[i:i+6])
        else:
            lemmas_str = lemmas[0]
        
        definition_str = synset.definition()

        examples = synset.examples()
        examples_str = ""
        if len(examples) > 1:
            for example in examples:
                if examples_str == "":
                    examples_str = "- " + example
                else:
                    examples_str = examples_str + "\n" + "- " + example
        elif len(examples) == 0:
            examples_str = ""
        else:
            examples_str = "- " + examples[0]

        
        #-- header -------#
        lemma_names = Gtk.Label(lemmas_str)
        lemma_names.props.max_width_chars = 50
        lemma_names.props.wrap = True
        lemma_names.props.wrap_mode = Pango.WrapMode.CHAR
        lemma_names.props.halign = Gtk.Align.START
        lemma_names.props.valign = Gtk.Align.CENTER
        lemma_names.get_style_context().add_class("section-header")

        #-- word definition -------#
        word_definition = Gtk.Label(definition_str)
        # word_definition.props.margin_bottom = 4
        #word_definition.props.margin_left = 4
        word_definition.props.max_width_chars = 50
        word_definition.props.wrap = True
        word_definition.props.hexpand = True
        word_definition.props.wrap_mode = Pango.WrapMode.WORD
        word_definition.props.justify = Gtk.Justification.FILL
        word_definition.props.halign = Gtk.Align.START
        word_definition.props.valign = Gtk.Align.START
        word_definition.set_size_request(-1, 30)
        word_definition.get_style_context().add_class("word-definition")

        #-- word examples -------#
        word_examples = Gtk.Label(examples_str)
        word_examples.props.max_width_chars = 50
        word_examples.props.wrap = True
        word_examples.props.hexpand = True
        word_examples.props.wrap_mode = Pango.WrapMode.WORD
        word_examples.props.justify = Gtk.Justification.FILL
        word_examples.props.halign = Gtk.Align.START
        word_examples.props.valign = Gtk.Align.START
        word_examples.get_style_context().add_class("section-content")

        word_examples_expander = Gtk.Expander()
        word_examples_expander.props.label = "Examples (" + str(len(examples)) + ")"
        word_examples_expander.add(word_examples)

        #-- copy action -------#
        copy_img = Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        copy_img.props.no_show_all = True
        copy_img.props.hexpand = True
        copy_img.props.halign = Gtk.Align.END
        copy_img.props.valign = Gtk.Align.START
        copy_img.get_style_context().add_class("transition-on")
        copy_img.get_style_context().add_class("copy-img")
        

        copied_img = Gtk.Image().new_from_icon_name("emblem-default", Gtk.IconSize.SMALL_TOOLBAR)
        copied_img.props.no_show_all = True

        copied_label = Gtk.Label("Copied to clipboard")
        copied_label.props.no_show_all = True
        
        copied_grid = Gtk.Grid()
        copied_grid.props.column_spacing = 4
        copied_grid.props.halign = Gtk.Align.END
        copied_grid.props.valign = Gtk.Align.START
        copied_grid.props.hexpand = True
        copied_grid.get_style_context().add_class("transition-on")
        copied_grid.get_style_context().add_class("copied-content")
        copied_grid.attach(copied_img, 0, 1, 1, 1)
        copied_grid.attach(copied_label, 1, 1, 1, 1)

        hidden_widget = (copy_img, copied_label, copied_img, copied_grid, synset)

        # workaround to avoid weird issue with enter and notify events after adding to the eventbox
        # put all in a grid, then put in eventbox. overlay didn't work
        content_grid = Gtk.Grid()
        content_grid.props.hexpand = True
        content_grid.attach(copy_img, 0, 1, 1, 3)
        content_grid.attach(copied_grid, 0, 1, 1, 3)
        content_grid.attach(word_definition, 0, 1, 1, 1)

        # if not examples_str == "":
        #     content_grid.attach(word_examples_expander, 0, 2, 1, 1)

        #-- eventbox -------#
        content_eventbox = Gtk.EventBox()
        content_eventbox.add(content_grid)
        content_eventbox.connect("enter-notify-event", self.on_enter_content_box, hidden_widget)
        content_eventbox.connect("leave-notify-event", self.on_leave_content_box, hidden_widget)
        content_eventbox.connect("button-press-event", self.on_copy_content_clicked, hidden_widget)

        #-- WordItems construct--------#
        # self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 3
        self.props.column_spacing = 0

        self.attach(lemma_names, 0, 1, 1, 1)
        self.attach(self.generate_separator(), 1, 1, 4, 1)
        self.attach(content_eventbox, 0, 2, 5, 1)
        if len(examples) >= 1:
            self.attach(word_examples_expander, 0, 3, 1, 1)

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
        content = widget_list[4]

        # reset state flagss to ready state for transition effect, see application.css
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # show widgets
        copied_label.show()
        copied_img.show()

        # set flags to trigger transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

        # callback to copy content to clipboard
        clipboard_paste = self.get_clipboard_paste()
        
        print(clipboard_paste)
        clipboard_paste.copy_to_clipboard("test")

        print("Callback to copy to clipbpard:")

    def get_clipboard_paste(self):
        subview = self.get_parent()
        wordview_stack = subview.get_parent()
        wordview = wordview_stack.get_parent()
        clipboard_paste = wordview.clipboard_paste
        return clipboard_paste