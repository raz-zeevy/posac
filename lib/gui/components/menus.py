from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from lib.utils import *
from PIL import Image, ImageTk
from tktooltip import ToolTip
import logging

logger = logging.getLogger(__name__)

m_POSACSEP_TABLE = "Posacsep Table"
m_POSAC_AXES_FILE = "Posac-axes File"
m_POSAC_OUTPUT = "Posac Output"
m_POSAC_LSA_DIAG = "POSAC/LSA Diagrams"
m_POSACSEP_DIAG = "Posacsep Diagrams"

class Menu(tk.Menu):
    def __init__(self, root):
        # Menu
        super().__init__(root)
        # File Menu
        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As..")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")
        self.add_cascade(label="File", menu=self.file_menu)
        # View Menu
        self.view_menu = tk.Menu(self)
        self.data_file_menu = self.add_submenus(self.view_menu, label="Input Data "
                                                                   "File",
                                  excel=True)
        self.posac_output_menu = self.add_submenus(self.view_menu,
                                                   label=m_POSAC_OUTPUT)
        self.lsa1_output_menu = self.add_submenus(self.view_menu, label="LSA1 Output")
        self.lsa2_output_menu = self.add_submenus(self.view_menu, label="LSA2 Output")
        self.view_menu.add_cascade(label=m_POSAC_LSA_DIAG)
        self.posacsep_tabe_menu = self.add_submenus(self.view_menu,
                                                    label=m_POSACSEP_TABLE)
        self.posacsep = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label=m_POSACSEP_DIAG,
                                   menu=self.posacsep)
        self.posac_axes_menu = self.add_submenus(self.view_menu,
                                                 label=m_POSAC_AXES_FILE)
        self.add_cascade(label="View", menu=self.view_menu)
        # Options Menu
        self.add_command(label="Options")
        # Help Menu
        self.help_menu = tk.Menu(self)
        self.help_menu.add_command(label="Report Error")
        self.help_menu.add_command(label="About Posac")
        self.add_cascade(label="Help", menu=self.help_menu)

    def add_posacsep_items(self, items_num):
        # remove current items
        self.posacsep.delete(0, "end")
        # add new items
        for i in range(1, items_num+1):
            self.posacsep.add_command(label=f"Item {i}",
                                      command=None)
        # self.view_menu.add_cascade(label=m_POSACSEP_DIAG, menu=self.posacsep)

    def add_submenus(self, parent_menu, label, excel=False):
        submenu = tk.Menu(parent_menu, tearoff=0)
        submenu.add_command(label="Notepad", command=None)
        submenu.add_command(label="Word", command=None)
        if excel:
            submenu.add_command(label="Excel", command=None)
        parent_menu.add_cascade(label=label, menu=submenu)
        return submenu

    def enable_view_results(self, posac_axes=False):
        self.view_menu.entryconfig(m_POSAC_OUTPUT,
                                        state="normal")
        self.view_menu.entryconfig("LSA1 Output",
                                        state="normal")
        self.view_menu.entryconfig("LSA2 Output",
                                        state="normal")
        self.view_menu.entryconfig(m_POSAC_LSA_DIAG,
                                        state='normal')
        self.view_menu.entryconfig(m_POSACSEP_TABLE,
                                        state='normal')
        self.view_menu.entryconfig(m_POSACSEP_DIAG,
                                        state='normal')
        if posac_axes:
            self.view_menu.entryconfig(m_POSAC_AXES_FILE,
                                        state='normal')

    def disable_view_results(self):
        self.view_menu.entryconfig(m_POSAC_OUTPUT,
                                        state="disable")
        self.view_menu.entryconfig("LSA1 Output",
                                        state="disable")
        self.view_menu.entryconfig("LSA2 Output",
                                        state="disable")
        self.view_menu.entryconfig(m_POSAC_LSA_DIAG,
                                        state='disable')
        self.view_menu.entryconfig(m_POSACSEP_TABLE,
                                        state='disable')
        self.view_menu.entryconfig(m_POSACSEP_DIAG,
                                        state='disable')
        self.view_menu.entryconfig(m_POSAC_AXES_FILE,
                                        state='disable')
        
    def update_history_menu(self, paths, max_length=30):
        """
        In the file menu, remove all existing path items after the "Exit" item,
        add a separating line below the "Exit" item, and then add each path item from the list.
        :param paths: A list of file paths to add to the menu.
        :return: None
        """

        def truncate_path(path, max_length):
            if len(path) > max_length:
                return "..." + path[-(max_length - 3):]
            return path

        # Find the index of the "Exit" item
        exit_index = None
        for index in range(self.file_menu.index('end') + 1):
            if self.file_menu.type(
                    index) == 'command' and self.file_menu.entrycget(index,
                                                                     'label') == 'Exit':
                exit_index = index
                break

        if exit_index is not None:
            # Remove all items after the "Exit" item
            self.file_menu.delete(exit_index + 1, 'end')

            if paths:
                # Add a separator before the new paths
                self.file_menu.add_separator()
                for path in paths:
                    truncated_path = truncate_path(path, max_length)
                    self.file_menu.add_command(label=truncated_path)
                    
class IconMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root, autostyle=False, pady=3, padx=5)
        # Icon Menu
        self.image_references = {}
        from PIL import Image, ImageTk
        self.load_icon_images()
        self.m_button_new = self.add_button("new.png", tooltip="New")
        self.m_button_open = self.add_button("open.png", tooltip="Open")
        self.m_button_save = self.add_button("save.png", tooltip="Save")
        ###
        self.m_button_run = self.add_button("go.png", tooltip="Run Posac")
        #
        self.m_button_undo = self.add_button("undo.png", tooltip="Undo",
                                             state='disable')
        self.m_button_redo = self.add_button("redo.png", tooltip="Redo",
                                             state='disable')
        ###
        self.m_button_help = self.add_button("help.png", tooltip="Help")
        icon_menu_border = tk.Frame(root,
                                    autostyle=False,
                                    borderwidth=1, relief='flat',
                                    background='grey', pady=0)
        icon_menu_border.pack(side=ttk.TOP, fill='x')

    def load_icon_images(self):
        """Load toolbar icons"""
        try:
            icons_dir = get_path("lib/assets/toolbar")
            # load all png files from ./assets/toolbar to image_references
            for file in os.listdir(get_path(icons_dir)):
                if file.endswith(".png") or file.endswith(".ico"):
                    image_path = os.path.join(icons_dir, file)
                    try:
                        image = Image.open(image_path, "r").resize(real_size((19, 19), _round=True))
                        self.image_references[file] = ImageTk.PhotoImage(image)
                    except Exception as e:
                        logger.warning(f"Failed to load icon {file}: {e}")
        except Exception as e:
            logger.error(f"Failed to load icons: {e}")
            # Fallback to no icons
            self.image_references = {}

    def add_button(self, image: str, command=None, tooltip=None, **kwargs):
        if not "width" in kwargs:
            kwargs["width"] = real_size(25, _round=True)
        if not "height" in kwargs:
            kwargs["height"] = real_size(25, _round=True)
        
        try:
            img = self.image_references.get(image)
            button = tk.Button(self,
                              autostyle=False,
                              image=img if img else None,
                              bg='white', relief='raised',
                              borderwidth=2, **kwargs)
            button.pack(side=ttk.LEFT)
            ToolTip(button, msg=tooltip)
            if tooltip:
                ToolTip(button, msg=tooltip, delay=0.5)
            return button
        except Exception as e:
            logger.error(f"Failed to create button {image}: {e}")
            return None
