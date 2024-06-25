import tkinter as tk


class MainPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()

    def _create_widgets(self):
        self._create_general_settings_frame()

    def _create_general_settings_frame(self):
        self.general_settings_frame = tk.LabelFrame(self, text='General Settings')
        self.general_settings_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)