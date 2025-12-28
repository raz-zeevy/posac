import copy
import os
import tkinter as tk

import ttkbootstrap as ttk

from lib.gui.components.form import (
    BoldLabel,
    BrowseButton,
    Entry,
    Label,
    SelectionBox,
    SpinBox,
)
from lib.gui.components.help_bar import HelpBar
from lib.gui.components.helpables import Helpable
from lib.gui.windows.window import Window
from lib.help.posac_help import Help
from lib.utils import real_size, rreal_size

t_POSAC_AXES = "Do you want to save Posac-Axes scores obtained for subjects?"
POSAC_AXES_OPTIONS = ["Yes", "No"]
POSAC_AXES_DEFAULT = False

t_ASCII_OUTPUT = "Do you want the 3 ASCII output files to be written?"
ASCII_OUTPUT_OPTIONS = ["Yes", "No"]
ASCII_OUTPUT_DEFAULT = "No"

t_SPECIAL_GRAPHIC_CHAR = (
    "Enter special graphic character to be used in ASCII output files"
)
t_FORM_FEED = "Enter special FORM FEED character if needed by printer"
t_POWER_WEIGHTS = "Power of balancing weights (incomparable and comparable)"
POWER_WEIGHTS_LOW = 4
POWER_WEIGHTS_HIGH = 4
t_MAX_ITERATION = "Enter maximum number of iterations"
MAX_ITERATIONS = 15

ENTRIES_PAD_LEFT = 10
ENTRIES_PAD_RIGHT = 30
ENTRIES_PAD_Y = 15


class PosacAxesFrame(ttk.Frame):
    SET_A_TEXT = """For X,Y recode 0 thru 25=1, 26 thru 50=2,51 thru 75=3,76 thru 100=4;
For J,L recode 0 thru 50=1, 51 thru 100=2,101 thru 150=3,151 thru 200=4."""

    SET_B_TEXT = """For X,Y recode 0 thru 10=1, 11 thru 20=2,21 thru 30=3, 31 thru 40=4,41 thru 50=5,
51 thru 60=6,61 thru 70=7, 71 thru 80=8,81 thru 90=9, 91 thru 100=10.
For J,L recode 0 thru 20=1, 21 thru 40=2,41 thru 60=3,61 thru 80=4, 81 thru 100=5, 101 thru 120=6,121 thru 140=7, 141 thru 160=8,161 thru 180=9, 181 thru 200=10."""

    def __init__(self, parent, gui=None):
        super().__init__(parent)
        self.gui = gui
        self._create_widgets()
        self._create_recoding_frame()

    def _create_widgets(self):
        # Create checkbox frame
        self.checkbox_frame = ttk.Frame(self)
        self.checkbox_frame.pack(fill="x", padx=real_size(10), pady=real_size(0))

        self.save_axes_var = tk.StringVar(value="No")
        label = BoldLabel(self.checkbox_frame, text=t_POSAC_AXES)
        label.pack(anchor="w", padx=real_size(10), pady=real_size(5))

        self.save_axes_menu = SelectionBox(
            self.checkbox_frame,
            values=POSAC_AXES_OPTIONS,
            textvariable=self.save_axes_var,
            help = Help.POSAC_AXES
        )
        self.save_axes_menu.state(["readonly"])
        self.save_axes_menu.pack(padx=real_size(10), pady=real_size(0))

        # Bind the selection change
        self.save_axes_var.trace_add("write", self._on_checkbox_change)

    def _create_recoding_frame(self):
        self.recoding_frame = ttk.Frame(self)

        # label
        label = BoldLabel(
            self.recoding_frame,
            text="Choose one of the folowing two sets of recoding systems for the oriringal coordinates X Y J L before they are added to the raw",
            wraplength=rreal_size(425),
            anchor="w",
            justify="left",
        )
        label.pack(padx=real_size(0), pady=real_size(0))

        # Create SET A text display with styling
        set_a_frame = ttk.LabelFrame(self.recoding_frame, text="SET A")
        set_a_frame.pack(fill="x", padx=real_size(10), pady=real_size(2))
        set_a_label = ttk.Label(
            set_a_frame,
            text=self.SET_A_TEXT,
            wraplength=rreal_size(425),
        )
        set_a_label.pack(padx=real_size(10), pady=real_size(3))

        # Create SET B text display
        set_b_frame = ttk.LabelFrame(self.recoding_frame, text="SET B")
        set_b_frame.pack(fill="x", padx=real_size(10), pady=real_size(2))
        set_b_label = ttk.Label(
            set_b_frame,
            text=self.SET_B_TEXT,
            wraplength=rreal_size(425),
        )
        set_b_label.pack(padx=real_size(10), pady=real_size(3))

        # Create controls frame
        controls_frame = ttk.Frame(self.recoding_frame)
        controls_frame.pack(fill="x", padx=real_size(10), pady=real_size(3))

        # A/B Selection
        selection_frame = ttk.Frame(controls_frame)
        selection_frame.pack(fill="x", pady=real_size(3))
        selection_label = Label(selection_frame, text="Choose (A/B)")
        selection_label.pack(side="left", padx=(ENTRIES_PAD_LEFT, 0))

        self.set_selection_var = tk.StringVar(value="A")
        self.set_selection = SelectionBox(
            selection_frame,
            values=["A", "B"],
            textvariable=self.set_selection_var,
            width=rreal_size(5),
        )
        self.set_selection.state(["readonly"])
        self.set_selection.pack(side="right", padx=(0, ENTRIES_PAD_RIGHT))

        # Record Length
        length_frame = ttk.Frame(controls_frame)
        # length_frame.pack(fill="x", pady=real_size(3))
        length_label = Label(length_frame, text="Datafile record length")
        length_label.pack(side="left", padx=(ENTRIES_PAD_LEFT, 0))

        self.record_length = SpinBox(
            length_frame, from_=1, to=999, width=rreal_size(10)
        )
        self.record_length.set(80)  # Default value
        self.record_length.pack(side="right", padx=(0, ENTRIES_PAD_RIGHT))

        # File Selection
        file_frame = ttk.Frame(controls_frame)
        file_frame.pack(fill="x", pady=real_size(3))
        file_label = Label(file_frame, text="New File")
        file_label.pack(side="left", padx=(ENTRIES_PAD_LEFT, 0))

        right_frame = ttk.Frame(file_frame)
        right_frame.pack(side="right", padx=(0, ENTRIES_PAD_RIGHT))

        self.file_entry = Entry(right_frame, width=rreal_size(40),)
        self.file_entry.pack(side="left", padx=(0, real_size(10)))

        self.browse_button = BrowseButton(right_frame, command=self._browse_file)
        self.browse_button.pack(side="right")

    def _on_checkbox_change(self, *args):
        if self.save_axes_var.get() == "Yes":
            self.recoding_frame.pack(fill="x", padx=real_size(10), pady=real_size(5))
        else:
            self.recoding_frame.pack_forget()

    def _browse_file(self):
        file_path = self.gui.save_file_diaglogue(
            title="Save As", file_types=(("PAX files", "*.pax"), ("All files", "*.*"))
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)


class OptionsWindow(Window):
    DEFAULT_VALUES = dict(
        ascii_output=ASCII_OUTPUT_DEFAULT,
        special_graphic_char="",
        form_feed="",
        power_weights_low=POWER_WEIGHTS_LOW,
        power_weights_high=POWER_WEIGHTS_HIGH,
        max_iterations=MAX_ITERATIONS,
        # Add new posac axes settings
        posac_axes=POSAC_AXES_DEFAULT,
        set_selection="A",
        record_length=80,
        posac_axes_out="C:/Program Files/POSAC/job.pax",
    )
    RESET_VALUES = copy.deepcopy(DEFAULT_VALUES)

    def __init__(self, gui, **kwargs):
        width, height = rreal_size(625), rreal_size(470)
        self.gui = gui
        super().__init__(**kwargs, geometry=f"{width}x{height}")

    def setup_window(self, **kwargs):
        """Initialize the options window."""
        self.title("Technical Options")
        self.create_widgets()
        self.update_idletasks()  # Ensure all elements are rendered before centering
        self.center_window()
        self.set_settings(**self.DEFAULT_VALUES)

    def create_widgets(self):
        self.create_notebook()
        self.help_bar = HelpBar(self)
        self.help_bar.pack(side=tk.BOTTOM, fill="x")

        # Apply and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        self.apply_button = ttk.Button(
            button_frame, text="Apply", command=self.apply_settings
        )
        self.apply_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(
            button_frame, text="Cancel", command=self.cancel_settings
        )
        self.cancel_button.pack(side=tk.LEFT, padx=10)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.create_posac_axes_tab()
        self.create_ascii_output_tab()
        self.create_technical_tab()

    def create_posac_axes_tab(self):
        self.posac_axes_frame = PosacAxesFrame(self.notebook, gui=self.gui)
        self.notebook.add(self.posac_axes_frame, text="Posac-Axes")

    def create_ascii_output_tab(self):
        self.theme_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theme_tab, text="ASCII Output Files")
        label = BoldLabel(self.theme_tab, text=t_ASCII_OUTPUT)
        label.pack(anchor="w", padx=10, pady=10)
        self.ascii_output_var = tk.StringVar(value=ASCII_OUTPUT_DEFAULT)
        ascii_output_menu = SelectionBox(
            self.theme_tab,
            values=ASCII_OUTPUT_OPTIONS,
            textvariable=self.ascii_output_var,
            help = Help.ASCII_OUTPUT_FILES
        )
        ascii_output_menu.state(["readonly"])
        ascii_output_menu.pack(padx=10, pady=10)

    def create_technical_tab(self):
        self.technical_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.technical_tab, text="Technical Options")

        self.special_graphic_char_entry = self._create_label_entry(
            self.technical_tab, t_SPECIAL_GRAPHIC_CHAR, default="",
            help = Help.GRAPHIC_CHARS
        )
        self.form_feed_entry = self._create_label_entry(
            self.technical_tab, t_FORM_FEED, default="",
            help = Help.FORMFEED
        )
        self.create_power_weights_entries()
        self.max_iterations = self._create_label_entry(
            self.technical_tab,
            t_MAX_ITERATION,
            default=str(MAX_ITERATIONS),
            width=rreal_size(5),
            help = Help.ITERATIONS_NUMBER
        )

    def create_power_weights_entries(self):
        w_entry = rreal_size(3)
        power_frame = ttk.Frame(self.technical_tab)
        power_frame.pack(
            fill="x",
            padx=real_size((ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT)),
            pady=ENTRIES_PAD_Y,
        )

        label_power_weights = Label(power_frame, text=t_POWER_WEIGHTS)
        label_power_weights.pack(side="left")

        self.power_weights_low_entry = Entry(power_frame, width=w_entry, help = Help.BALANCING_WEIGHTS)
        self.power_weights_low_entry.insert(0, str(POWER_WEIGHTS_LOW))
        self.power_weights_low_entry.pack(side="right", padx=real_size((10, 0)))

        self.power_weights_high_entry = Entry(power_frame, width=w_entry, help = Help.BALANCING_WEIGHTS)
        self.power_weights_high_entry.insert(0, str(POWER_WEIGHTS_HIGH))
        self.power_weights_high_entry.pack(side="right", padx=real_size((10, 0)))

    def _create_label_entry(self, parent, text, **kwargs):
        frame = tk.Frame(parent)
        default = kwargs.pop("default", "")
        frame.pack(
            fill="x",
            padx=real_size((ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT)),
            pady=real_size(ENTRIES_PAD_Y),
        )
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        entry = Entry(frame, **kwargs)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default)
        return entry

    def set_defaults(self):
        # Update PosacAxesFrame settings
        self.posac_axes_frame.save_axes_var.set(self.DEFAULT_VALUES["posac_axes"])
        self.posac_axes_frame.set_selection_var.set(
            self.DEFAULT_VALUES["set_selection"]
        )
        self.posac_axes_frame.record_length.set(self.DEFAULT_VALUES["record_length"])
        self.posac_axes_frame.file_entry.delete(0, tk.END)
        self.posac_axes_frame.file_entry.insert(
            0, self.DEFAULT_VALUES["posac_axes_out"]
        )

        # Update ASCII output settings
        self.ascii_output_var.set(self.DEFAULT_VALUES["ascii_output"])

        # Update technical tab settings
        self.special_graphic_char_entry.delete(0, tk.END)
        self.special_graphic_char_entry.insert(
            0, self.DEFAULT_VALUES["special_graphic_char"]
        )

        self.form_feed_entry.delete(0, tk.END)
        self.form_feed_entry.insert(0, self.DEFAULT_VALUES["form_feed"])

        self.power_weights_low_entry.delete(0, tk.END)
        self.power_weights_low_entry.insert(0, self.DEFAULT_VALUES["power_weights_low"])

        self.power_weights_high_entry.delete(0, tk.END)
        self.power_weights_high_entry.insert(
            0, self.DEFAULT_VALUES["power_weights_high"]
        )

        self.max_iterations.delete(0, tk.END)
        self.max_iterations.insert(0, self.DEFAULT_VALUES["max_iterations"])

    def get_settings(self):
        settings = {
            "posac_axes": self.posac_axes_frame.save_axes_var.get() == "Yes",
            "ascii_output": self.ascii_output_var.get(),
            "special_graphic_char": self.special_graphic_char_entry.get(),
            "form_feed": self.form_feed_entry.get(),
            "power_weights_low": self.power_weights_low_entry.get(),
            "power_weights_high": self.power_weights_high_entry.get(),
            "max_iterations": int(self.max_iterations.get()),
            # Always include posac axes settings regardless of Yes/No selection
            "set_selection": self.posac_axes_frame.set_selection_var.get(),
            "record_length": self.posac_axes_frame.record_length.get(),
            "posac_axes_out": self.posac_axes_frame.file_entry.get(),
        }
        return settings

    @staticmethod
    def get_settings_static():
        posac_axes_val = OptionsWindow.DEFAULT_VALUES["posac_axes"]
        posac_axes_bool = posac_axes_val is True or posac_axes_val == "Yes"
        return {
            "posac_axes": posac_axes_bool,
            "ascii_output": OptionsWindow.DEFAULT_VALUES["ascii_output"],
            "special_graphic_char": OptionsWindow.DEFAULT_VALUES["special_graphic_char"],
            "form_feed": OptionsWindow.DEFAULT_VALUES["form_feed"],
            "power_weights_low": OptionsWindow.DEFAULT_VALUES["power_weights_low"],
            "power_weights_high": OptionsWindow.DEFAULT_VALUES["power_weights_high"],
            "max_iterations": OptionsWindow.DEFAULT_VALUES["max_iterations"],
            "set_selection": OptionsWindow.DEFAULT_VALUES["set_selection"],
            "record_length": OptionsWindow.DEFAULT_VALUES["record_length"],
            "posac_axes_out": OptionsWindow.DEFAULT_VALUES["posac_axes_out"],
        }

    def set_settings(self, **settings):
        known_settings = set(self.DEFAULT_VALUES.keys())

        for key in settings:
            if key not in known_settings:
                raise ValueError(f"Unknown setting: {key}")

        if "posac_axes" in settings:
            self.posac_axes_frame.save_axes_var.set(
                "Yes"
                if (settings["posac_axes"] and settings["posac_axes"] != "No")
                else "No"
            )

        if "set_selection" in settings:
            self.posac_axes_frame.set_selection_var.set(settings["set_selection"])
        if "record_length" in settings:
            self.posac_axes_frame.record_length.set(settings["record_length"])
        if "posac_axes_out" in settings:
            self.posac_axes_frame.file_entry.delete(0, tk.END)
            self.posac_axes_frame.file_entry.insert(0, settings["posac_axes_out"])

        # Show/hide the recoding frame based on posac_axes setting
        if "posac_axes" in settings:
            self.posac_axes_frame._on_checkbox_change()

        if "ascii_output" in settings:
            self.ascii_output_var.set(settings["ascii_output"])
        if "special_graphic_char" in settings:
            self.special_graphic_char_entry.delete(0, tk.END)
            self.special_graphic_char_entry.insert(0, settings["special_graphic_char"])
        if "form_feed" in settings:
            self.form_feed_entry.delete(0, tk.END)
            self.form_feed_entry.insert(0, settings["form_feed"])
        if "power_weights_low" in settings:
            self.power_weights_low_entry.delete(0, tk.END)
            self.power_weights_low_entry.insert(0, settings["power_weights_low"])
        if "power_weights_high" in settings:
            self.power_weights_high_entry.delete(0, tk.END)
            self.power_weights_high_entry.insert(0, settings["power_weights_high"])
        if "max_iterations" in settings:
            self.max_iterations.delete(0, tk.END)
            self.max_iterations.insert(0, settings["max_iterations"])

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

    @staticmethod
    def reset_default():
        OptionsWindow.set(**OptionsWindow.RESET_VALUES)

    @staticmethod
    def set_posac_axes_out_dir(path):
        OptionsWindow.set(posac_axes_out=os.path.join(path, "job.pax"))

# Example of how to use the window and set default values:
if __name__ == "__main__":
    root = tk.Tk()
    Helpable.init(root)
    root.withdraw()  # Hide the root window
    window = OptionsWindow(None)
    window.mainloop()

    # Test settings
    test_settings = {
        "posac_axes": "Yes",
        "set_selection": "B",
        "record_length": 100,
        "posac_axes_out": "test.pax",
        "ascii_output": "Yes",
        "special_graphic_char": "*",
        "form_feed": "#",
        "power_weights_low": 5,
        "power_weights_high": 6,
        "max_iterations": 20,
    }

    # Create window and apply test settings
    window = OptionsWindow(None)
    window.set_settings(**test_settings)

    # Verify settings were applied correctly
    current_settings = window.get_settings()
    print("Settings applied correctly:", current_settings == test_settings)
    print("Current settings:", current_settings)

    window.mainloop()
