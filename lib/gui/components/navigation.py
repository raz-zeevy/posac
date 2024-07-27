import os
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from lib.utils import *

PADDING_BUTTONS_X = real_size(50)


class Navigation(tk.Frame):
    def __init__(self, root, gui):
        super().__init__(root)
        self.cur = 0
        #
        # pack the navigation at the bottom of the screen but above the help
        # bar
        self.gui = gui
        self.image_references = {}
        #
        center_frame = ttk.Frame(self)
        center_frame.pack(pady=(15, 25), expand=True)
        self.button_previous = self.create_button(center_frame,
                                                  image="left.png")
        self.button_previous.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        self.button_next = self.create_button(center_frame,
                                              image="right.png", )
        self.button_next.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)
        self.button_run = self.create_button(center_frame,
                                             image="go.png",
                                             iwidth=rreal_size(30),
                                             iheight=rreal_size(30))
        self.button_run.pack(side=ttk.LEFT, padx=PADDING_BUTTONS_X)

    def create_button(self, frame, **kwargs):
        image_file = kwargs.pop('image')
        iwidth = kwargs.pop('iwidth', rreal_size(50))
        iheight = kwargs.pop('iheight', rreal_size(35))
        icons_dir = get_path("lib/assets/navigation")
        image_path = os.path.join(icons_dir, image_file)
        image = Image.open(image_path, "r").resize((iwidth, iheight))
        self.image_references[image_file] = ImageTk.PhotoImage(image)
        return tk.Button(frame, image=self.image_references[image_file],
                         autostyle=False, background='white',
                         relief='raise', borderwidth=2, padx=5, pady=5,
                         width=rreal_size(66), height=rreal_size(39),
                         **kwargs)
