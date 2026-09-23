import tkinter as tk
from tkinter import ttk

from lib.__version__ import VERSION
from lib.gui.windows.window import Window
from lib.help.help_window.markup_parser import MarkupParser
from lib.help.posac_help import PosacHelp
from lib.utils import rreal_size

ABOUT_SECTION = "Welcome to the Posac program"


class AboutWindow(Window):
    def setup_window(self, **kwargs):
        """Initialize the window."""
        self.title("About POSAC")
        self.geometry(f"{rreal_size(620)}x{rreal_size(640)}")
        self.resizable(True, True)  # The description is too long for a fixed height
        self.create_widgets()
        self.update_idletasks()  # Ensure all elements are rendered before centering
        self.center_window()

    def create_widgets(self):
        self.create_title()
        self.create_content()
        # self.create_credit()
        self.create_version()
        self.create_developer_info()

    def create_title(self):
        self.title_label = ttk.Label(
            self, text="POSAC Analysis Tool", font=("Helvetica", rreal_size(16), "bold")
        )
        self.title_label.pack(pady=(rreal_size(20), rreal_size(10)))

    @staticmethod
    def get_description():
        """The description shared with the 'What is Posac' help screen."""
        markup = PosacHelp.get(ABOUT_SECTION, return_dict=False)
        return MarkupParser().strip_markup(markup).replace("<f1_br>", "").strip()

    def create_content(self):
        content_frame = ttk.Frame(self)
        content_frame.pack(
            fill="both",
            expand=True,
            padx=rreal_size(20),
            pady=(rreal_size(10), rreal_size(5)),
        )

        scrollbar = ttk.Scrollbar(content_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.description = tk.Text(
            content_frame,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
            font=("Helvetica", rreal_size(9)),
            yscrollcommand=scrollbar.set,
            background=self.cget("background"),
        )
        self.description.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.description.yview)

        self.description.insert("1.0", self.get_description())
        self.description.config(state="disabled")

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
            version_frame, text=f"Version: {VERSION}", font=("Helvetica", rreal_size(9))
        )
        version_label.pack()

    def create_developer_info(self):
        dev_frame = ttk.Frame(self)
        dev_frame.pack(pady=(rreal_size(0), rreal_size(20)))

        dev_label = ttk.Label(
            dev_frame,
            text="Program Interface Developed by Raz Zeevy\nraz3zeevy@gmail.com",
            font=("Helvetica", rreal_size(9)),
            justify="center"
        )
        dev_label.pack()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    about_window = AboutWindow(root)
    root.mainloop()