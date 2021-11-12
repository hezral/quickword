# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class WordView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clipboard_paste = None
        self.lookup_word = None

        self.stack = Gtk.Stack()
        self.stack.props.expand = True
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.props.homogeneous = True
        self.stack_switcher.props.stack = self.stack
        self.stack_switcher.get_style_context().add_class("subview-switcher")

        self.props.name = 'word-view'
        self.get_style_context().add_class(self.props.name)
        self.set_size_request(350, -1)
        self.props.expand = False
        self.attach(self.stack, 0, 0, 2, 1)
        self.attach(self.stack_switcher, 0, 1, 2, 1,)

    def on_wordlookup(self, button=None, data=None):

        self.lookup_word = data[0]
        synsets = data[2]

        stack = self.get_parent()
        window = stack.get_toplevel()
        window.pronounciation_label.props.label = "/ " + data[1] + " /"
        window.word_action_revealer.set_reveal_child(True)

        # delete all stack children if any
        if self.stack.get_children():
            for child in self.stack.get_children():
                self.stack.remove(child)

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
            # subviews[view].show_all()
            self.stack.add_titled(subviews[view], view, view)
        
        # style left and right tabs for stack switcher
        stack_count = len(self.stack_switcher.get_children())

        left_tab = self.stack_switcher.get_children()[0]
        left_tab.get_style_context().add_class("word-types-left")
        right_tab = self.stack_switcher.get_children()[stack_count-1]
        right_tab.get_style_context().add_class("word-types-right")

        for child in self.stack_switcher.get_children():
            child.get_style_context().add_class("word-types")
            child.props.can_focus = False
        
        self.stack.show_all()


#------------------CLASS-SEPARATOR------------------#


class WordSubView(Gtk.Grid):
    def __init__(self, name, word, contents, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = name
        self.props.hexpand = True
        self.props.row_spacing = 15
        self.props.column_spacing = 0

        scrolled_view = Gtk.ScrolledWindow()
        scrolled_view.props.expand = True
        # scrolled_view.connect("edge-reached", self.on_edge_reached)
        # scrolled_view.connect("edge-overshot", self.on_edge_overshot)

        scrolled_view_grid = Gtk.Grid()
        scrolled_view_grid.props.row_spacing = 10
        scrolled_view_grid.props.expand = True
        scrolled_view_grid.props.margin = 10
        scrolled_view_grid.props.margin_left = 20
        scrolled_view_grid.props.margin_right = 20

        i = 1
        for content in contents:
            scrolled_view_grid.attach(WordItems(word, content), 0, i, 1, 1)
            i += 1
        
        scrolled_view.add(scrolled_view_grid)
        self.attach(scrolled_view, 0, 1, 1, 1)

    def on_edge_overshot(self, scrolledwindow, position):
        # print(position.value_name)
        # stack = self.get_parent()
        # word_view = stack.get_parent()
        # print(word_view)
        ...

    def on_edge_reached(self, scrolledwindow, position):
        # print(position.value_name)
        # stack = self.get_parent()
        # word_view = stack.get_parent()
        # print(word_view)
        ...
        # if position.value_name == "GTK_POS_BOTTOM":
        #     self.count_label.props.label = str(self.more_count) + " more results up.."
        # elif position.value_name == "GTK_POS_TOP":
        #     self.count_label.props.label = str(self.more_count) + " more results below.."


#------------------CLASS-SEPARATOR------------------#


class WordItems(Gtk.Grid):
    def __init__(self, word, contents, multi=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # synset item
        synset = contents
        
        #-- word definition -------#
        definition_str = synset.definition()

        word_definition = Gtk.Label(definition_str)
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
        lemmas.sort(key=len)

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
        eventbox_params = (copy_img, copied_label, copied_img, copied_grid, word, word_definition, word_examples, word_box, lemma_box)

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
        app.on_new_word_lookup(button.props.name)

    def generate_separator(self):
        separator = Gtk.Separator()
        separator.props.hexpand = True
        separator.props.valign = Gtk.Align.CENTER
        return separator

    def on_enter_content_box(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_grid = widget_list[3]
        word_box = widget_list[7]

        # show widget and set flags to trigger transition effect, see application.css
        copy_img.show()
        copy_img.set_state_flags(Gtk.StateFlags.PRELIGHT, True)

        # set flags to ready state for transition effect, see application.css
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # add styling for hover effect
        word_box.get_children()[0].get_style_context().add_class("word-hover")
        try:
            word_box.get_children()[1].get_style_context().remove_class("word-examples")
            word_box.get_children()[1].get_style_context().add_class("word-examples-hover")
        except:
            pass

    def on_leave_content_box(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_grid = widget_list[3]
        word_box = widget_list[7]

        # reset state flagss to ready state for transition effect, see application.css
        copy_img.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # reset state flags to ready state for transition effect, see application.css
        # grid can stay as show state since only toggle widget hide/shows
        copied_grid.set_state_flags(Gtk.StateFlags.DIR_LTR, True)

        # remove styling for hover effect
        word_box.get_children()[0].get_style_context().remove_class("word-hover")
        try:
            word_box.get_children()[1].get_style_context().remove_class("word-examples-hover")
            word_box.get_children()[1].get_style_context().add_class("word-examples")
        except:
            pass
            
    def on_copy_content_clicked(self, eventbox, event, widget_list):
        copy_img = widget_list[0]
        copied_label = widget_list[1]
        copied_img = widget_list[2]
        copied_grid = widget_list[3]
        word = widget_list[4]
        word_definition = widget_list[5]
        word_example = widget_list[6]
        word_lemmas = widget_list[8]
        word_lemmas_list = []
        if len(word_lemmas.get_children()) > 0:
            for child in word_lemmas.get_children():
                word_lemmas_list.append(child.props.label)

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
        to_copy = to_copy + "Pronounciation: " + self.get_wordview().get_toplevel().pronounciation_label.props.label + "\n"
        to_copy = to_copy + "Definition: " + word_definition.props.label + "\n"
        to_copy = to_copy + "Example: " + word_example.props.label + "\n"
        to_copy = to_copy + "Synonyms/Related: " + ", ".join(word_lemmas_list)
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
