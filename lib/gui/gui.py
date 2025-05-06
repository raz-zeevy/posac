import os
import tkinter as tk
from tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.help_bar import HelpBar
from lib.gui.components.helpables import Helpable
from lib.gui.components.menus import IconMenu, Menu
from lib.gui.components.navigation import Navigation
from lib.gui.const import p_ICON
from lib.gui.navigator import Navigator
from lib.gui.notebook import PosacNotebook
from lib.gui.pages.start_page import StartPage
from lib.gui.windows.about_window import AboutWindow
from lib.gui.windows.diagram_window import DiagramWindow
from lib.gui.windows.message_window import MessageWindow
from lib.gui.windows.options_window import OptionsWindow
from lib.utils import *

ROOT_TITLE = f"Posac Program-v{os.environ.get('VERSION')}"
THEME_NAME = 'sandstone'

def gui_only(func, *args, **kwargs):
    def wrapper(self, *args, **kwargs):
        if IS_PROD():
            return func(self, *args, **kwargs)

    return wrapper

class GUI():
    def __init__(self, controller):
        # Main window
        self.root = ttk.Window(
            themename=THEME_NAME,
        )
        self.root_title = ROOT_TITLE + ("-dev" if IS_DEV() else "")
        self.root.title(self.root_title)
        # set the icon
        self.root.iconbitmap(get_resource(p_ICON))
        # self.root.config(cursor="question_arrow")
        # Initialize an attribute to store images
        self.image_references = {}

        # set the dpi_ratio enviroment variable
        os.environ['DPI_RATIO'] = str(self.root.winfo_fpixels('1i')/96)
        # Set the window to be square
        self.root.geometry(f'{real_size(WINDOW_WIDTH,_round=True)}x'
                           f'{real_size(WINDOW_HEIGHT, _round=True)}')
        self.root.resizable(True, True)
        EditableTreeView.configure_style(
            row_height=real_size(30))
        # init common gui
        self.center_window()
        #
        Helpable.init(self.root)
        self.init_window()
        self.navigator = Navigator(self, controller)
        self.view_results = None

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
        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
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
        self.navigation = Navigation(self.root, self)
        self.navigation.pack(side=tk.BOTTOM, fill="x")
        #
        self.create_main_frame()

        # Add binding for Report Error menu item
        self.menu.help_menu.entryconfig("Report Error", command=self.report_error)

    def create_main_frame(self):
        # Create the Notebook widget
        main_frame = ttk.Frame(self.root)
        main_frame.pack(
            expand=True,
            fill="both",
            padx=0,
            pady=0,
        )
        self.notebook_frame = ttk.Frame(main_frame)
        # self.notebook_frame.pack(expand=True, fill='both', padx=30, pady=0,)
        self.notebook = PosacNotebook(self.notebook_frame, self)
        self.notebook.pack(expand=True, fill="both")
        self.start_page = StartPage(main_frame)
        self.start_page.pack(expand=True, fill="both")

    def create_start_frame(self):
        pass

    def set_save_title(self, save_path):
        if save_path:
            self.root.title(f"{self.root_title} - {save_path}")
        else:
            self.root.title(self.root_title)

    #########################
    # Dialogues and Windows #
    #########################

    def show_diagram_window(self, graph_data_lst):
        self.diagram_window = DiagramWindow(self.root, graph_data_lst=graph_data_lst)
        pass

    def show_about_window(self, section=None):
        self.help_window = AboutWindow()

    def show_options_window(self):
        self.technical_options = OptionsWindow(self)

    def set_options(self, **options):
        OptionsWindow.set(**options)

    def get_technical_options(self, *args):
        if not args:
            return OptionsWindow.DEFAULT_VALUES
        else:
            return OptionsWindow.DEFAULT_VALUES[args[0]]

    def show_error(self, title, msg):
        # Handle the error if your data contains non-ASCII characters
        Messagebox.show_error(msg, title=title)
        # You might want to inform the user with a message box
        # messagebox.showerror("Save Error", "The file contains non-ASCII characters.")

    def show_warning(self, title, msg):
        # Handle the error if your data contains non-ASCII characters
        Messagebox.show_warning(msg, title=title)
        # You might want to inform the user with a message box
        # messagebox.showerror("Save Error", "The file contains non-ASCII characters.")

    @gui_only
    def show_msg(self, msg, title=None, yes_command=None,
                 no_command=None,
                 buttons=['Yes:primary', 'No:secondary']):
        if yes_command:
            result = MessageWindow.show_question(
                self.root,
                msg,
                title,
                yes_command=yes_command,
                no_command=no_command,
                buttons=buttons,
            )
            return result
        else:
            return MessageWindow.show_message(self.root, msg, title)

    def save_file_diaglogue(
        self,
        file_types=None,
        default_extension=None,
        initial_file_name=None,
        title=None,
        allow_overwrite=True,
    ):
        while True:
            file_name = filedialog.asksaveasfilename(
                filetypes=file_types,
                defaultextension=default_extension,
                title=title,
                initialfile=initial_file_name,
            )

            # User cancelled the dialog
            if not file_name:
                return None

            # Check if file already exists
            if os.path.exists(file_name):
                if allow_overwrite:
                    return file_name
                else:
                    # Show error message that file exists and cannot be overwritten
                    self.show_error(
                        "File Exists",
                        f"The file '{os.path.basename(file_name)}' already exists and cannot be overwritten.\n\nPlease choose a different filename.",
                    )
                    # Keep initial_file_name for next dialog
                    initial_file_name = os.path.basename(file_name)
            else:
                # File doesn't exist, return the filename
                return file_name

    def get_input_file_name(self) -> str:
        """
        Placeholder for the controller-planted method that returns the input
        file name
        :return:
        """
        pass

    def save_session_dialogue(self, data_file_name=""):
        file_name = filedialog.asksaveasfilename(filetypes=[('Memory files',
                                                             f'*.{SESSION_FILE_EXTENSION}')],
                                                 defaultextension=f'.{SESSION_FILE_EXTENSION}',
                                                 title="Save Posac Session",
                                                 confirmoverwrite=True,
                                                 initialfile=data_file_name)
        return file_name

    def open_session_dialogue(self):
        file_name = filedialog.askopenfilename(filetypes=[(f'{SESSION_FILE_EXTENSION}',
                                                          f'*.{SESSION_FILE_EXTENSION}')],
                                               title="Open Posac Session")
        return file_name

    def browse_file_dialogue(self, title="Open",
                             file_types=[]):
        filename = filedialog.askopenfilename(
            filetypes=file_types,
            title=title)
        return filename

    #########
    # Menus #
    #########

    def enable_view_results(self, posac_axes=False):
        self.menu.enable_view_results(posac_axes)
        self.view_results = True

    def disable_view_results(self):
        self.menu.disable_view_results()
        self.view_results = False

    #######
    # API #
    #######

    def reset(self):
        self.notebook.reset_to_default()
        self.disable_view_results()
        self.navigator.set_page(0)
        OptionsWindow.reset_default()

    def get_state(self):
        return {
            'notebook' : self.notebook.get_state(),
            'navigator' : self.navigator.cur_page,
            'view_results' : self.view_results,
            'options' : OptionsWindow.DEFAULT_VALUES
        }

    def load_state(self, state : dict):
        self.reset()
        self.notebook.set_state(state['notebook'])
        self.navigator.set_page(state['navigator'])
        if state['view_results']:
            self.enable_view_results()
        else:
            self.disable_view_results()
        OptionsWindow.set(**state['options'])

    def report_error(self):
        """Placeholder for the controller-planted method"""
        pass

if __name__ == '__main__':
    gui = GUI(None)
    gui.run_process()