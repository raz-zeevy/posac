import tkinter as tk
import ttkbootstrap as ttk
class ZeroOptionTab(tk.Frame):
    DEFAULT_VALUES = dict(zero_option=True)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()
        self.set_default()

    ###########
    #   GUI   #
    ###########

    def _create_widgets(self):
        tk.label = tk.Label(self, text="Is zero(0) the missing value, "
                                       "and the only missing value, for all "
                                       "variables?",
                            font=("Segoe UI", 13),
                            wraplength=500,
                            justify='left')
        tk.label.pack(fill='x', padx=(0,0), pady=(25,0))
        self._zero_option_combo = ttk.Combobox(self, values=["Yes", "No"],
                                         width=5,
                                               font=("Segoe UI", 11))
        self._zero_option_combo.pack(padx=10, pady=(25,0))

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

    def set_default(self):
        self.set(**self.DEFAULT_VALUES)

