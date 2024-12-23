import tkinter as tk
import ttkbootstrap as ttk
from lib.gui.components.form import NavigationButton
from lib.help.posac_help import Help
from lib.utils import *

PADDING_BUTTONS_X = real_size(20)


class Navigation(tk.Frame):
    def __init__(self, root, gui):
        super().__init__(root)
        self.cur = 0
        self.gui = gui
        
        center_frame = ttk.Frame(self)
        center_frame.pack(pady=(15, 25), expand=True)
        
        self.button_previous = NavigationButton(center_frame, text="Previous",
                                                help=Help.BACK_COMMAND)
        self.button_previous.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        
        self.button_next = NavigationButton(center_frame, text="Next",
                                            help=Help.NEXT_COMMAND)
        self.button_next.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        
        self.button_run = NavigationButton(center_frame, text="Run", bootstyle="dark-outline",
                                           help=Help.RUN_COMMAND)
        self.button_run.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
