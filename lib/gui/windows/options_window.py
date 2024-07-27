from lib.gui.components.form import BoldLabel, SelectionBox
from lib.gui.components.form import Label
from lib.gui.components.help_bar import HelpBar
from lib.gui.windows.window import Window
import tkinter as tk
import ttkbootstrap as ttk

from lib.utils import real_size, rreal_size

t_POSAC_AXES = 'Do you want to save Posac-Axes scores obtained for subjects?'
POSAC_AXES_OPTIONS = ['Yes', 'No']
POSAC_AXES_DEFAULT = 'No'

t_ASCII_OUTPUT = 'Do you want the 3 ASCII output files to be written?'
ASCII_OUTPUT_OPTIONS = ['Yes', 'No']
ASCII_OUTPUT_DEFAULT = 'No'

t_SPECIAL_GRAPHIC_CHAR = 'Enter special graphic character to be used in ASCII output files'
t_FORM_FEED = 'Enter special FORM FEED character if needed by printer'
t_POWER_WEIGHTS = 'Power of balancing weights (incomparable and comparable)'
POWER_WEIGHTS_LOW = 4
POWER_WEIGHTS_HIGH = 4
t_MAX_ITERATION = 'Enter maximum number of iterations'
MAX_ITERATION_LOW = 15

ENTRIES_PAD_LEFT = 10
ENTRIES_PAD_RIGHT = 30
ENTRIES_PAD_Y = 15


class OptionsWindow(Window):
    DEFAULT_VALUES = dict(posac_axes=POSAC_AXES_DEFAULT,
                          ascii_output=ASCII_OUTPUT_DEFAULT,
                          special_graphic_char='',
                          form_feed='',
                          power_weights_low=POWER_WEIGHTS_LOW,
                          power_weights_high=POWER_WEIGHTS_HIGH,
                          max_iterations=MAX_ITERATION_LOW)

    def __init__(self, **kwargs):
        width, height = rreal_size(600), rreal_size(450)
        super().__init__(**kwargs, geometry=f"{width}x{height}")
        self.title("Options")
        self.resizable(False, False)
        self.create_widgets()
        self.set_defaults()
        self.bind("<Escape>", lambda x: self.on_closing())

    def create_widgets(self):
        self.create_notebook()
        self.help_bar = HelpBar(self)
        self.help_bar.pack(side=tk.BOTTOM, fill="x")

        # Apply and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        self.apply_button = ttk.Button(button_frame, text="Apply",
                                       command=self.apply_settings)
        self.apply_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(button_frame, text="Cancel",
                                        command=self.cancel_settings)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.create_posac_axes_tab()
        self.create_ascii_output_tab()
        self.create_technical_tab()

    def create_posac_axes_tab(self):
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="Posac-Axes")

        label = BoldLabel(self.general_tab, text=t_POSAC_AXES)
        label.pack(anchor="w", padx=10, pady=10)

        self.posac_axes_var = tk.StringVar(value=POSAC_AXES_DEFAULT)
        posac_axes_menu = SelectionBox(self.general_tab,
                                       values=POSAC_AXES_OPTIONS,
                                       textvariable=self.posac_axes_var)
        posac_axes_menu.state(["readonly"])
        posac_axes_menu.pack(padx=10, pady=10)

    def create_ascii_output_tab(self):
        self.theme_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theme_tab, text="ASCII Output Files")
        label = BoldLabel(self.theme_tab, text=t_ASCII_OUTPUT)
        label.pack(anchor="w", padx=10, pady=10)
        self.ascii_output_var = tk.StringVar(value=ASCII_OUTPUT_DEFAULT)
        ascii_output_menu = ttk.Combobox(self.theme_tab,
                                         values=ASCII_OUTPUT_OPTIONS,
                                         textvariable=self.ascii_output_var)
        ascii_output_menu.state(["readonly"])
        ascii_output_menu.pack(padx=10, pady=10)

    def create_technical_tab(self):
        self.technical_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.technical_tab, text="Technical Options")

        self.special_graphic_char_entry = self._create_label_entry(
            self.technical_tab, t_SPECIAL_GRAPHIC_CHAR, default="")
        self.form_feed_entry = self._create_label_entry(self.technical_tab,
                                                        t_FORM_FEED,
                                                        default="")
        self.create_power_weights_entries()
        self.max_iteration_low_entry = self._create_label_entry(
            self.technical_tab, t_MAX_ITERATION,
            default=str(MAX_ITERATION_LOW), width=rreal_size(5))

    def create_power_weights_entries(self):
        w_entry = rreal_size(3)
        power_frame = ttk.Frame(self.technical_tab)
        power_frame.pack(fill='x',
                         padx=real_size((ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT)),
                         pady=ENTRIES_PAD_Y)

        label_power_weights = Label(power_frame, text=t_POWER_WEIGHTS)
        label_power_weights.pack(side='left')

        self.power_weights_low_entry = ttk.Entry(power_frame, width=w_entry)
        self.power_weights_low_entry.insert(0, str(POWER_WEIGHTS_LOW))
        self.power_weights_low_entry.pack(side='right',
                                          padx=real_size((10, 0)))

        self.power_weights_high_entry = ttk.Entry(power_frame, width=w_entry)
        self.power_weights_high_entry.insert(0, str(POWER_WEIGHTS_HIGH))
        self.power_weights_high_entry.pack(side='right',
                                           padx=real_size((10, 0)))

    def _create_label_entry(self, parent, text, **kwargs):
        frame = tk.Frame(parent)
        default = kwargs.pop('default', "")
        frame.pack(fill='x',
                   padx=real_size((ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT)),
                   pady=real_size(ENTRIES_PAD_Y))
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame, **kwargs)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default)
        return entry

    def set_defaults(self):
        self.posac_axes_var.set(self.DEFAULT_VALUES['posac_axes'])
        self.ascii_output_var.set(self.DEFAULT_VALUES['ascii_output'])
        self.special_graphic_char_entry.delete(0, tk.END)
        self.special_graphic_char_entry.insert(0, self.DEFAULT_VALUES[
            'special_graphic_char'])
        self.form_feed_entry.delete(0, tk.END)
        self.form_feed_entry.insert(0, self.DEFAULT_VALUES['form_feed'])
        self.power_weights_low_entry.delete(0, tk.END)
        self.power_weights_low_entry.insert(0, self.DEFAULT_VALUES[
            'power_weights_low'])
        self.power_weights_high_entry.delete(0, tk.END)
        self.power_weights_high_entry.insert(0, self.DEFAULT_VALUES[
            'power_weights_high'])
        self.max_iteration_low_entry.delete(0, tk.END)
        self.max_iteration_low_entry.insert(0, self.DEFAULT_VALUES[
            'max_iteration_low'])

    def get_settings(self):
        return {
            'posac_axes': self.posac_axes_var.get(),
            'ascii_output': self.ascii_output_var.get(),
            'special_graphic_char': self.special_graphic_char_entry.get(),
            'form_feed': self.form_feed_entry.get(),
            'power_weights_low': self.power_weights_low_entry.get(),
            'power_weights_high': self.power_weights_high_entry.get(),
            'max_iteration_low': self.max_iteration_low_entry.get()
        }

    def set_settings(self, **settings):
        known_settings = set(self.DEFAULT_VALUES.keys())

        for key in settings:
            if key not in known_settings:
                raise ValueError(f"Unknown setting: {key}")

        if 'posac_axes' in settings:
            self.posac_axes_var.set(settings['posac_axes'])
        if 'ascii_output' in settings:
            self.ascii_output_var.set(settings['ascii_output'])
        if 'special_graphic_char' in settings:
            self.special_graphic_char_entry.delete(0, tk.END)
            self.special_graphic_char_entry.insert(0, settings[
                'special_graphic_char'])
        if 'form_feed' in settings:
            self.form_feed_entry.delete(0, tk.END)
            self.form_feed_entry.insert(0, settings['form_feed'])
        if 'power_weights_low' in settings:
            self.power_weights_low_entry.delete(0, tk.END)
            self.power_weights_low_entry.insert(0,
                                                settings['power_weights_low'])
        if 'power_weights_high' in settings:
            self.power_weights_high_entry.delete(0, tk.END)
            self.power_weights_high_entry.insert(0, settings[
                'power_weights_high'])
        if 'max_iteration_low' in settings:
            self.max_iteration_low_entry.delete(0, tk.END)
            self.max_iteration_low_entry.insert(0,
                                                settings['max_iteration_low'])
    @staticmethod
    def set(**settings):
        known_settings = set(OptionsWindow.DEFAULT_VALUES.keys())

        for key in settings:
            if key not in known_settings:
                raise ValueError(f"Unknown setting: {key}")

        OptionsWindow.DEFAULT_VALUES.update(settings)
    def apply_settings(self):
        settings = self.get_settings()
        self.__class__.DEFAULT_VALUES.update(settings)
        self.destroy()

    def cancel_settings(self):
        self.destroy()


# Example of how to use the window and set default values:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    window = OptionsWindow()
    window.mainloop()
