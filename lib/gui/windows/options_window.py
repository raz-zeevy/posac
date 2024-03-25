from tkinter import ttk

from lib.gui.windows.window import Window


class OptionsWindow(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Options")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.create_notebook()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.create_general_tab()
        self.create_theme_tab()

    def create_general_tab(self):
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")

    def create_theme_tab(self):
        self.theme_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theme_tab, text="Theme")
