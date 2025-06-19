import tkinter as tk
import ttkbootstrap as ttk
class HelpBar(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        status_bar = ttk.Label(self, text="For Help manual press 'Alt+F1' or press 'F1' on "
                                          "the data fields",
                               relief=ttk.SUNKEN, anchor='w',
                               background='#F0F0F0', padding=(0, 2))
        # pack the status bar at the bottom of the screen
        status_bar.pack(side=ttk.BOTTOM, fill='x')
