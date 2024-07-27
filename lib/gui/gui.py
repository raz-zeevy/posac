import tkinter as tk
from tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.notebook import PosacNotebook
from lib.gui.windows.about_window import AboutWindow
from lib.gui.windows.options_window import OptionsWindow
from lib.utils import *
from lib.gui.components.menus import Menu, IconMenu
from lib.gui.components.help_bar import HelpBar
from lib.gui.components.navigation import Navigation
from lib.gui.navigator import Navigator

ROOT_TITLE = "Posac Program-v3.00"
THEME_NAME = 'sandstone'
p_ICON = 'icon.ico'

def gui_only(func, *args, **kwargs):
    def wrapper(self, *args, **kwargs):
        if IS_PRODUCTION():
            return func(self, *args, **kwargs)

    return wrapper

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
            row_height=real_size(30))

        # init common gui
        self.center_window()
        #
        self.init_window()
        self.navigator = Navigator(self)

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
        self.navigation = Navigation(self.root, self)
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

    def create_start_frame(self):
        pass

        #########################
        # Dialogues and Windows #
        #########################

    def show_diagram_window(self, graph_data_lst):
        # self.diagram_window = DiagramWindow(self, graph_data_lst)
        # self.diagram_window.bind("<F1>", lambda x: self.show_help_windw())
        pass

    def show_about_window(self, section=None):
        self.help_window = AboutWindow()

    def show_options_window(self):
        self.technical_options = OptionsWindow()

    def set_options(self, **options):
        OptionsWindow.set(**options)
    def get_technical_option(self, *args):
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
            clicked_yes = Messagebox.show_question(msg, title, buttons=[
                buttons[0], buttons[1]])
            if clicked_yes == buttons[0].split(":")[0]:
                yes_command()
            elif no_command:
                no_command()
            return clicked_yes
        else:
            Messagebox.show_info(msg, title)

    def save_file_diaglogue(self, file_types=None, default_extension=None,
                            initial_file_name=None, title=None):
        file_name = filedialog.asksaveasfilename(filetypes=file_types,
                                                 defaultextension=default_extension,
                                                 title=title,
                                                 confirmoverwrite=True,
                                                 initialfile=initial_file_name)
        return file_name

    def get_input_file_name(self) -> str:
        """
        Placeholder for the controller-planted method that returns the input
        file name
        :return:
        """
        pass

    def run_button_dialogue(self):
        default_output_file_name = self.get_input_file_name().split(".")[
                                       0] + ".fss"
        output_file_path = self.save_file_diaglogue(
            file_types=[('fss', '*.fss')],
            default_extension='.fss',
            initial_file_name=default_output_file_name,
            title="Save Output File To...")
        return output_file_path

    def save_session_dialogue(self):
        file_name = filedialog.asksaveasfilename(filetypes=[('mem', '*.mem')],
                                                 defaultextension='.mem',
                                                 title="Save FSSA Session",
                                                 confirmoverwrite=True)
        return file_name

    def open_session_dialogue(self):
        file_name = filedialog.askopenfilename(filetypes=[('mem', '*.mem')],
                                               title="Open FSSA Session")
        return file_name

if __name__ == '__main__':
    gui = GUI()
    gui.run_process()