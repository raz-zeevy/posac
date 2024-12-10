import tkinter as tk
import ttkbootstrap as ttk
from lib.gui.components.form import NavigationButton
from lib.utils import *

PADDING_BUTTONS_X = real_size(20)


class Navigation(tk.Frame):
    def __init__(self, root, gui):
        super().__init__(root)
        self.cur = 0
        self.gui = gui
        
        center_frame = ttk.Frame(self)
        center_frame.pack(pady=(15, 25), expand=True)
        
        self.button_previous = NavigationButton(center_frame, text="Previous")
        self.button_previous.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        
        self.button_next = NavigationButton(center_frame, text="Next")
        self.button_next.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        
        self.button_run = NavigationButton(center_frame, text="Run", bootstyle="dark-outline")
        self.button_run.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
