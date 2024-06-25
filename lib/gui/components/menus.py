import tkinter as tk
import ttkbootstrap as ttk
from lib.utils import *
from PIL import Image, ImageTk
class Menu(tk.Menu):
    def __init__(self, root):
        # Menu
        super().__init__(root)
        # File Menu
        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")
        self.add_cascade(label="File", menu=self.file_menu)
        # View Menu
        self.view_menu = tk.Menu(self)
        self.data_file_menu = tk.Menu(self.view_menu)
        self.view_menu.add_command(label="Data File")
        self.view_menu.add_cascade(label="Posac Output")
        self.view_menu.add_cascade(label="LSA1 Output")
        self.view_menu.add_cascade(label="LSA2 Output")
        self.view_menu.add_cascade(label="POSAC/LSA Diagrams")
        self.view_menu.add_cascade(label="Posacsep Table")
        self.view_menu.add_cascade(label="Posacsep Diagrams")
        self.view_menu.add_cascade(label="Posac-axes File")
        self.add_cascade(label="View", menu=self.view_menu)
        # Options Menu
        self.add_command(label="Options")
        # Help Menu
        self.help_menu = tk.Menu(self)
        self.help_menu.add_command(label="Contents")
        self.help_menu.add_command(label="About Posac")
        self.add_cascade(label="Help", menu=self.help_menu)


class IconMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root, autostyle=False, pady=3, padx=5)
        # Icon Menu
        self.image_references = {}
        from PIL import Image, ImageTk
        self.load_icon_images()
        self.m_button_new = self.add_button("new.png")
        self.m_button_open = self.add_button("open.png")
        self.m_button_save = self.add_button("save.png")
        ###
        self.m_button_run = self.add_button("go.png")
        #
        self.m_button_undo = self.add_button("undo.png")
        self.m_button_redo = self.add_button("redo.png")
        ###
        self.m_button_help = self.add_button("help.png")
        icon_menu_border = tk.Frame(root,
                                    autostyle=False,
                                    borderwidth=1, relief='flat',
                                    background='grey', pady=0)
        icon_menu_border.pack(side=ttk.TOP, fill='x')

    def load_icon_images(self):
        icons_dir = get_path("lib/assets/toolbar")
        # load all png files from ./assets/toolbar to image_references
        for file in os.listdir(get_path(icons_dir)):
            if file.endswith(".png") or file.endswith(".ico"):
                image_path = os.path.join(icons_dir, file)
                image = Image.open(image_path, "r").resize(real_size((19,
                                                                      19),
                                                                     _round=True))
                self.image_references[file] = ImageTk.PhotoImage(image)

    def add_button(self, image: str, command=None, **kwargs):
        if not "width" in kwargs:
            kwargs["width"] = real_size(25, _round=True)
        if not "height" in kwargs:
            kwargs["height"] = real_size(25, _round=True)
        button = tk.Button(self,
                           autostyle=False,
                           image=self.image_references[image],
                           bg='white', relief='raised',
                           borderwidth=2, **kwargs)
        button.pack(side=ttk.LEFT)
        return button
