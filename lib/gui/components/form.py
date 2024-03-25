import ttkbootstrap as ttk


CALIBRI_FONT = ('Calibri', 10)
SEGOE_UI_FONT = ('Segoe UI', 10)

class Label(ttk.Label):
    """A label that can be used to display text."""

    def __init__(self, parent, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = SEGOE_UI_FONT
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


class SelectionBox(ttk.Combobox):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        default_index = None
        if 'default' in kwargs:
            default_index = kwargs['values'].index(kwargs['default'])
            del kwargs['default']
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         state="readonly", )
        self.values = kwargs['values']
        if default_index is not None:
            self.current(default_index)


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

