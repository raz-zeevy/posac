from tkinter import ttk

from lib.gui.windows.window import Window


class AboutWindow(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("About")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.create_title()
        self.create_content()

    def create_title(self):
        self.title_label = ttk.Label(self, text="About", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

    def create_content(self):
        self.content_label = ttk.Label(self, text="This is a test application")
        self.content_label.pack(pady=10)