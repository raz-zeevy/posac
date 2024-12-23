import tkinter as tk

from lib.gui.components.form import SelectionBox
from lib.help.posac_help import Help

class ZeroOptionTab(tk.Frame):
    DEFAULT_VALUES = dict(zero_option=True)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()
        self.reset_default()

    ###########
    #   GUI   #
    ###########

    def _create_widgets(self):
        label = tk.Label(self, text="Is zero(0) the missing value, "
                                       "and the only missing value, for all "
                                       "variables?",
                            font=("Segoe UI", 13),
                            wraplength=500,
                            justify='left')
        label.pack(fill='x', padx=(0,0), pady=(25,0))
        self._zero_option_combo = SelectionBox(self, values=["Yes", "No"],
                                               font=("Segoe UI", 11),
                                               help=Help.MISSING_VALUE)
        self._zero_option_combo.bind("<<ComboboxSelected>>",
                                     lambda e: self._on_change())
        self._zero_option_combo.pack(padx=10, pady=(25,0))

    def _on_change(self):
        pass

    #################
    #   Get & Set   #
    #################

    def get_zero_option(self):
        return self._zero_option_combo.get() == self._zero_option_combo['values'][0]

    def set_zero_option(self, value):
        self._zero_option_combo.set(self._zero_option_combo['values'][0] if value else self._zero_option_combo['values'][1])

    def get_all(self):
        return dict(zero_option=self.get_zero_option())

    def set(self, **kwargs):
        if 'zero_option' in kwargs:
            self.set_zero_option(kwargs['zero_option'])
        self._on_change()

    def reset_default(self):
        self.set(**self.DEFAULT_VALUES)

