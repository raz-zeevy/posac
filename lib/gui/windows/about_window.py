from tkinter import ttk

from lib.__version__ import VERSION
from lib.gui.windows.window import Window
from lib.utils import rreal_size


class AboutWindow(Window):
    def setup_window(self, **kwargs):
        """Initialize the window."""
        self.title("About POSAC")
        self.resizable(False, False)  # Make window non-resizable
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

    def create_content(self):
        main_description = (
            """POSAC/LSA Program was developed in Fortran by Samuel Shye, the Hebrew University of Jerusalem, as part of a research project supported in part by the U.S. Army Research Institute for the Behavioral and Social Sciences through its European Research Office."""
        )

        self.main_content_label = ttk.Label(
            self,
            text=main_description,
            wraplength=rreal_size(300),
            justify="center",
        )
        self.main_content_label.pack(padx=rreal_size(20), pady=(rreal_size(10), rreal_size(5)))

        references_description = (
            """Basic References:
Shye, S. (1985). Multiple Scaling: The Theory and Application of Partial Order Scalogram Analysis. Amsterdam: North-Holland. [The mathematical foundation of POSAC and its relationship to SSA of the variables]
Shye, S. & Amar, R. (1985). Partial Order Scalogram Analysis by Base Coordinates and Lattice Mapping of the Items by Their Scalogram Roles. In D. Canter (ed.) Facet Theory: Approaches to Social Research. New York: Springer-Verlag. [An article describing POSAC/LSA procedures and computer program.]"""
        )

        self.references_label = ttk.Label(
            self,
            text=references_description,
            wraplength=rreal_size(300),
            justify="left",
            anchor="w"
        )
        self.references_label.pack(padx=rreal_size(20), pady=(rreal_size(5), rreal_size(10)))

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