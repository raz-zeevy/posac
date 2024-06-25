import tkinter as tk
from tkinter import *
from tkinter import messagebox
from abc import ABC, abstractmethod

#todo:
    # there is the bbox method that is used in the editable_tree_view to get
    # the position of the cell to place the entry widget. This method can be
    # used in the helpables to place the help text in the right place.
class HelpMixin(ABC):
    """
    HelpMixin class is an abstract class that provides a help text when the
    user presses the F1 key. The help text is shown in a messagebox.
    """
    def __init__(self, help_title="Help", help_text="No help available",
                 **kwargs):
        self.help_title = help_title
        self.help_text = help_text
        super().__init__(**kwargs)
        self.bind("<FocusIn>", self._bind_help)
        self.bind("<FocusOut>", self._unbind_help)

    def _bind_help(self, event=None):
        self.bind("<F1>", self._show_help)

    def _unbind_help(self, event=None):
        self.unbind("<F1>")

    def _show_help(self, event=None):
        messagebox.showinfo(self.help_title, self.help_text)


class HelpableEntry(HelpMixin, tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
