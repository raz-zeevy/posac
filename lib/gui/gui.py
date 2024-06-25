import tkinter as tk
import tkinter.ttk
import ttkbootstrap as ttk

from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.posac_notebook import PosacNotebook
from lib.utils import *
from lib.gui.components.menus import Menu, IconMenu
from lib.gui.components.help_bar import HelpBar
from lib.gui.components.navigation import Navigation

ROOT_TITLE = "Posac Program-v3.00"
THEME_NAME = 'sandstone'
p_ICON = 'icon.ico'

class GUI():
    def __init__(self):
        # Main window
        self.root = ttk.Window(
            themename=THEME_NAME
        )
        self.root.title(ROOT_TITLE)
        # set the icon
        # self.root.iconbitmap(get_resource(p_ICON))

        # Initialize an attribute to store images
        self.image_references = {}

        # set the dpi_ratio enviroment variable
        os.environ['DPI_RATIO'] = str(self.root.winfo_fpixels('1i')/96)
        # Set the window to be square
        self.root.geometry(f'{real_size(WINDOW_WIDTH,_round=True)}x'
                           f'{real_size(WINDOW_HEIGHT, _round=True)}')
        self.root.resizable(False, False)
        EditableTreeView.configure_style(
            row_height=30)

        # init tabs
        self.current_page = None
        self.pages = {}
        for Page in []:
            page_name = Page.__name__
            self.pages[page_name] = Page(self)

        # init common gui
        self.center_window()
        #
        self.init_window()

    def run_process(self):
        self.root.mainloop()

    ##################
    # Initialization #
    ##################

    def center_window(self):
        self.root.update_idletasks()  # Update "requested size" from geometry
        # manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split(
            'x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = (screen_height / 2) - (size[1] / 2) - (screen_height / 10)
        self.root.geometry("+%d+%d" % (x, y))

    def init_window(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        #
        self.icon_menu = IconMenu(self.root)
        self.icon_menu.pack(side=tk.TOP, fill="x")
        #
        self.help_bar = HelpBar(self.root)
        self.help_bar.pack(side=tk.BOTTOM, fill="x")
        #
        self.navigation = Navigation(self.root)
        self.navigation.pack(side=tk.BOTTOM, fill="x")
        #
        self.create_main_frame()

    def create_main_frame(self):
        # Create the Notebook widget
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=30, pady=0)
        self.notebook = PosacNotebook(main_frame)
        self.notebook.pack(expand=True,
                      fill='both',)


if __name__ == '__main__':
    gui = GUI()
    gui.run_process()