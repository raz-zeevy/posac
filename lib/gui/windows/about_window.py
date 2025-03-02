from tkinter import ttk
from lib.__version__ import VERSION
from lib.gui.windows.window import Window
from lib.utils import rreal_size

class AboutWindow(Window):
    def setup_window(self, **kwargs):
        self.title("About POSAC")
        self.resizable(False, False)  # Make window non-resizable
        self.create_widgets()

    def create_widgets(self):
        self.create_title()
        self.create_content()
        self.create_credit()
        self.create_version()
        self.create_developer_info()

    def create_title(self):
        self.title_label = ttk.Label(
            self, 
            text="POSAC Analysis Tool",
            font=("Helvetica", rreal_size(16), "bold")
        )
        self.title_label.pack(pady=(rreal_size(20), rreal_size(10)))

    def create_content(self):
        description = (
            "POSAC (Partial Order Scalogram Analysis with Base Coordinates) "
            "is a mathematical scaling procedure that analyzes multivariate "
            "data by representing profiles as points in a geometric space "
            "while preserving their partial order relationships."
        )
        
        self.content_label = ttk.Label(
            self,
            text=description,
            wraplength=rreal_size(300),  # Wrap text at 300 pixels
            justify="center"
        )
        self.content_label.pack(padx=rreal_size(20), pady=rreal_size(10))

    def create_credit(self):
        credit_frame = ttk.Frame(self)
        credit_frame.pack(pady=(rreal_size(5), rreal_size(10)))
        
        credit_label = ttk.Label(
            credit_frame,
            text="Theory and Original Program by\nProf. Shmuel Shay",
            font=("Helvetica", rreal_size(10)),
            justify="center"
        )
        credit_label.pack()

    def create_version(self):
        version_frame = ttk.Frame(self)
        version_frame.pack(pady=(rreal_size(10), rreal_size(5)))  # Reduced bottom padding
        
        version_label = ttk.Label(
            version_frame,
            text=f"Version: {VERSION}",
            font=("Helvetica", rreal_size(9))
        )
        version_label.pack()

    def create_developer_info(self):
        dev_frame = ttk.Frame(self)
        dev_frame.pack(pady=(rreal_size(0), rreal_size(20)))
        
        dev_label = ttk.Label(
            dev_frame,
            text="Developed by Raz Zeevy\nraz3zeevy@gmail.com",
            font=("Helvetica", rreal_size(9)),
            justify="center"
        )
        dev_label.pack()