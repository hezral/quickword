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
    def __init__(self, word_data=None, clipboardcopy=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- process the data --------#
        # Wordnet POS 
        # ADJ: 'a'
        # ADJ_SAT: 's'
        # ADV: 'r'
        # NOUN: 'n'
        # VERB: 'v'



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

         #-- view construct--------#
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
        self.attach(button, 0, 4, 1, 1)

        self.on_wordlookup()


    



    def on_wordlookup(self, button=None, data=None):
        view = self
        pronounciation_label = [child for child in view.get_children() if child.get_name() == "pronounciation_label"][0]
        stack = [child for child in view.get_children() if isinstance(child, Gtk.Stack)][0]
        stack_switcher = [child for child in view.get_children() if isinstance(child, Gtk.StackSwitcher)][0]

        pronounciation = "/" + "pronounciation" + "/"
        pronounciation_label.props.label = pronounciation

        # delete all stack children if any
        if stack.get_children():
            for child in stack.get_children():
                stack.remove(child)

        import random
        import string

        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))

        data = ("n", result_str + "-1", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data1 = ("r", result_str + "-1", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data2 = ("a", result_str + "-2", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data3 = ("v", result_str + "-3", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data4 = ("s", result_str + "-4", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data5 = ("n", result_str + "-5", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")
        data6 = ("s", result_str + "-6", "a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds", "the dog barked all night")

        synsets = (data, data1, data2, data3, data4, data5, data6)

        # create list for each type of word
        noun_data = []
        adjective_data = []
        adverb_data = []
        ver_data = []

        # add data to each word list
        for synset in synsets:
            if synset[0] == "n":
                noun_data.append(synset)
            if synset[0] == "a" or synset[0] == "s":
                adjective_data.append(synset)
            if synset[0] == "r":
                adverb_data.append(synset)
            if synset[0] == "v":
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

        #-- view construct -----#
        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 4
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
        
        #-- header -------#
        lemma_names = Gtk.Label(contents[1])
        lemma_names.props.halign = Gtk.Align.START
        lemma_names.props.valign = Gtk.Align.CENTER
        lemma_names.get_style_context().add_class("section-header")

        #-- word definition -------#
        word_definition = Gtk.Label(contents[2])
        word_definition.props.margin_bottom = 8
        word_definition.props.margin_left = 4
        word_definition.props.max_width_chars = 50
        word_definition.props.wrap = True
        word_definition.props.hexpand = True
        word_definition.props.wrap_mode = Pango.WrapMode.WORD
        word_definition.props.justify = Gtk.Justification.FILL
        word_definition.props.halign = Gtk.Align.START
        word_definition.props.valign = Gtk.Align.START
        word_definition.get_style_context().add_class("section-content")

        #-- word examples -------#
        word_examples = Gtk.Label("Examples: " + contents[3])
        word_examples.props.margin_bottom = 15
        word_examples.props.max_width_chars = 50
        word_examples.props.wrap = True
        word_examples.props.hexpand = True
        word_examples.props.wrap_mode = Pango.WrapMode.WORD
        word_examples.props.justify = Gtk.Justification.FILL
        word_examples.props.halign = Gtk.Align.START
        word_examples.props.valign = Gtk.Align.START
        word_examples.get_style_context().add_class("section-content")

        #-- copy action -------#
        copy_img = Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        copy_img.props.no_show_all = True
        copy_img.props.hexpand = True
        copy_img.props.halign = Gtk.Align.END
        copy_img.props.valign = Gtk.Align.END
        copy_img.get_style_context().add_class("transition-on")

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

        # contents = (lemma_names, word_definition)
        hidden_widget = (copy_img, copied_label, copied_img, copied_grid, contents)

        # workaround to avoid weird issue with enter and notify events after adding to the eventbox
        # put all in a grid, then put in eventbox. overlay didn't work
        content_grid = Gtk.Grid()
        content_grid.props.hexpand = True
        content_grid.attach(word_definition, 0, 1, 1, 1)
        content_grid.attach(copy_img, 0, 1, 1, 3)
        content_grid.attach(copied_grid, 0, 1, 1, 3)
        content_grid.attach(word_examples, 0, 2, 1, 1)


        content_eventbox = Gtk.EventBox()
        content_eventbox.add(content_grid)
        content_eventbox.connect("enter-notify-event", self.on_enter_content_box, hidden_widget)
        content_eventbox.connect("leave-notify-event", self.on_leave_content_box, hidden_widget)
        content_eventbox.connect("button-press-event", self.on_copy_content_clicked, hidden_widget)

        # self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 3
        self.props.column_spacing = 0

        self.attach(lemma_names, 0, 1, 1, 1)
        self.attach(self.generate_separator(), 1, 1, 4, 1)
        self.attach(content_eventbox, 0, 2, 5, 1)

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
        print("Callback to copy to clipbpard:", content)