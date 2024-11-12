import ttkbootstrap as ttk
import tkinter as tk

from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.helpables import Helpable
from lib.utils import real_size, rreal_size

CALIBRI_FONT = ('Calibri', 10)
SEGOE_UI_FONT = ('Segoe UI', 10)
SEGOE_UI_FONT_BOLD = ('Segoe UI', 10, 'bold')


class Label(tk.Label):
    """A label that can be used to display text."""

    def __init__(self, parent, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = SEGOE_UI_FONT
        if 'size' in kwargs:
            kwargs['font'] = (kwargs['font'][0], kwargs['size'])
            del kwargs['size']
        super().__init__(parent, **kwargs)


class BoldLabel(tk.Label):
    """A label that can be used to display text."""

    def __init__(self, parent, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = SEGOE_UI_FONT_BOLD
        if 'size' in kwargs:
            kwargs['font'] = (
                kwargs['font'][0], kwargs['size'], kwargs['font'][2])
            del kwargs['size']
        super().__init__(parent, **kwargs)


class DataButton(ttk.Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         bootstyle="dark", )


class NavigationButton(ttk.Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 15
        if 'bootstyle' not in kwargs:
            kwargs['bootstyle'] = 'primary'
        super().__init__(parent, **kwargs)


class SelectionBox(Helpable, ttk.Combobox):
    """A button that can be used to navigate to a different page."""

    def __init__(self, master=None, **kwargs):
        default_index = None
        if 'default' in kwargs:
            default_index = kwargs['values'].index(kwargs['default'])
            del kwargs['default']
        if 'width' not in kwargs:
            kwargs['width'] = 10
        kwargs['state'] = 'readonly'
        super().__init__(master=master, **kwargs, )
        self.values = kwargs['values']
        if default_index is not None:
            self.current(default_index)


class SpinBox(Helpable, ttk.Spinbox):
    def __init__(self, master=None, **kwargs):
        default_value = None
        if 'default' in kwargs:
            default_value = kwargs.pop('default')
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(master=master, **kwargs,
                         state="readonly", )
        if default_value is not None:
            self.set(default_value)
class Entry(Helpable, ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)


class TableView(Helpable, EditableTreeView):
    def __init__(self, master=None, root=None, **kwargs):
        super().__init__(master=master, root=root, **kwargs)


def create_labeled_selection_box(master, label_text, values, default,
                                 width=10, label_padx=10, box_pad_x=0, pady=10,
                                 wraplength=500):
    # Delimiter Frame
    frame = ttk.Frame(master)
    frame.pack(fill='x', padx=label_padx, pady=pady)
    # What is the delimiter Entry
    label = Label(frame,
                  text=label_text,
                  wraplength=wraplength)
    label.pack(side=ttk.LEFT)
    selection_box = SelectionBox(
        frame,
        values=values,
        default=default,
        width=width)
    selection_box.pack(side=ttk.RIGHT, padx=box_pad_x)
    return label, selection_box


class BrowseButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        if 'text' not in kwargs:
            kwargs['text'] = 'Browse'
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs, )
