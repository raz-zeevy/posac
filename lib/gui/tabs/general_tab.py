import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Tuple

from lib.gui.components.form import BrowseButton, Entry, Label, SelectionBox, SpinBox
from lib.help.posac_help import Help
from lib.utils import real_size

ENTRIES_PAD_Y = 7
ENTRIES_PAD_RIGHT = 100
ENTRIES_PAD_LEFT = 40


class GeneralTab(tk.Frame):
    DEFAULT_VALUES = dict(job_name="",
                          data_file="",
                          lines_per_case=1,
                          plot_item_diagram=True,
                          plot_external_diagram=True,
                          only_freq=0,
                          posac_type="D",
                          subject_type="S",
                          id_location=(0, 0))

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._notebook = parent
        self._create_widgets()
        self.gui = self._notebook.gui

    ###########
    #   GUI   #
    ###########

    def _create_widgets(self):
        self.job_name_frame = tk.Frame(self)
        self.job_name_frame.pack(fill='x', padx=10, pady=real_size(2))
        self.job_name_entry = self._create_label_entry(
            "What name do you want for this "
            "Posac job?", width=40, help=Help.NAME_OF_JOB)
        self._create_data_input()
        self.lines_per_case_entry = self._create_label_spinbox(
            "How many lines per case in the data file?",
            from_=1,
            to=999,
            default=1,
            width=6,
            help=Help.LINES_PER_CASE,
        )
        self.plot_item_diagram_entry = self._create_label_combo(
            "Do you want item diagrams plotted?", ["Yes", "No"],
            default="Yes",
            width=5, help=Help.ITEM_DIAGRAMS)
        self.plot_external_diagram_entry = self._create_label_combo(
            "Do you want external diagrams plotted?", ["Yes", "No"],
            default="Yes",
            width=5, help=Help.EXTERNAL_DIAGRAMS)
        self.only_freq_entry = self._create_label_spinbox(
            "To process only profiles with frequency>f, enter value of f",
            from_=0, to=99, default=0, width=6, help=Help.FREQUENCY)
        self.posac_type_combo = self._create_label_combo(
            "Run Distributional Posac, Structural Posac or just Profiles? (D/S/P)",
            ["D", "S", "P"],
            default="D",
            width=5, help=Help.STRUCTURAL_POSAC)
        self.subject_type_combo = self._create_label_combo(
            "Are Data Subjects, Identified Subjects or Profiles and frequencies? (S/I/P)",
            ["S", "I", "P"],
            default="S",
            width=5, help=Help.DATA_SUBJECTS)
        #
        self._create_id_location()

    def _create_data_input(self):
        data_input_frame = tk.Frame(self)
        data_input_frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT + 40, 0),
                              pady=real_size(ENTRIES_PAD_Y))
        self.data_input_label = Label(data_input_frame, text=
        "Data File:")
        self.data_input_label.pack(side=tk.LEFT)
        right_frame = tk.Frame(data_input_frame)
        right_frame.pack(side=tk.RIGHT, padx=(0, 30))
        self.data_input_entry = Entry(right_frame, width=50, help=Help.INPUT_DATA_FILE)
        self.data_input_entry.pack(side=tk.LEFT)
        # add a browse button
        self.browse_button = BrowseButton(right_frame,
                                          command=self.browse_data_file)
        self.browse_button.pack(side=tk.LEFT, padx=(40, 0))

    def _create_id_location(self):
        id_location_frame = tk.Frame(self)
        id_location_frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT, 0),
                             pady=real_size(ENTRIES_PAD_Y))
        self.id_location = Label(id_location_frame, text=
        "If data are identified subjects or "
        "Profiles and Frquencies, where in "
        "record 1 are the id label/frequencies "
        "located? (columns from-to)",
                               wraplength=400)
        self.id_location.pack(side=tk.LEFT, padx=(0, 30))

        id_location_right = tk.Frame(id_location_frame)
        id_location_right.pack(side=tk.RIGHT, padx=(0, 30))

        from_label = Label(id_location_right, text="From")
        from_label.pack(side=tk.LEFT, padx=(0, 5))

        # Replace SpinBox with Entry
        self.id_location_from_entry = Entry(id_location_right, width=5)
        self.id_location_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.id_location_from_entry.insert(0, "0")  # Default value

        # Register numeric validation
        validate_cmd = self.id_location_from_entry.register(
            self._validate_numeric_input
        )
        self.id_location_from_entry.configure(
            validate="key", validatecommand=(validate_cmd, "%P")
        )

        to_label = Label(id_location_right, text="To")
        to_label.pack(side=tk.LEFT, padx=(0, 5))

        # Replace SpinBox with Entry
        self.id_location_to_entry = Entry(id_location_right, width=5)
        self.id_location_to_entry.pack(side=tk.LEFT)
        self.id_location_to_entry.insert(0, "0")  # Default value

        # Register numeric validation
        self.id_location_to_entry.configure(
            validate="key", validatecommand=(validate_cmd, "%P")
        )

        # Add validation for range
        self.id_location_from_entry.bind("<FocusOut>", self._validate_id_location_range)
        self.id_location_to_entry.bind("<FocusOut>", self._validate_id_location_range)

    def _validate_numeric_input(self, value):
        """Validate that input is numeric"""
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _validate_id_location_range(self, event=None):
        """Validate that 'from' is not greater than 'to'"""
        try:
            from_val = int(self.id_location_from_entry.get())
            to_val = int(self.id_location_to_entry.get())
        except ValueError:
            # Only show error if both fields have values and they're invalid
            if self.id_location_from_entry.get() and self.id_location_to_entry.get():
                messagebox.showerror(
                    "Invalid Input", "Please enter valid numeric values"
                )
                # Reset both values to 0
                self.id_location_from_entry.delete(0, tk.END)
                self.id_location_from_entry.insert(0, "0")
                self.id_location_to_entry.delete(0, tk.END)
                self.id_location_to_entry.insert(0, "0")

    def _create_label_entry(self, text, **kwargs):
        frame = tk.Frame(self)
        default = kwargs.pop("default", "")
        frame.pack(
            fill="x",
            padx=(ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT),
            pady=real_size(ENTRIES_PAD_Y),
        )
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        entry = Entry(frame, **kwargs)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default)
        return entry

    def _create_label_combo(self, text, values, default, **kwargs):
        frame = tk.Frame(self)
        frame.pack(
            fill="x",
            padx=(ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT),
            pady=real_size(ENTRIES_PAD_Y),
        )
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        combo = SelectionBox(frame, values=values, **kwargs)
        combo.set(default)
        combo.pack(side=tk.RIGHT)
        return combo

    def _create_label_spinbox(self, text, **kwargs):
        frame = tk.Frame(self)
        frame.pack(
            fill="x",
            padx=(ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT),
            pady=real_size(ENTRIES_PAD_Y),
        )
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        spinbox = SpinBox(frame, **kwargs)
        spinbox.pack(side=tk.RIGHT)
        return spinbox

    ##########
    # Browse #
    ##########

    def browse_data_file(self):
        data_file = self.gui.browse_file_dialogue(
            title="Select Data File",
            file_types=(("Data files", "*.dat;*.prn;*.txt"),
                        ("All files", "*.*"),)
        )
        if data_file:
            self.data_input_entry.delete(0, tk.END)
            self.data_input_entry.insert(0, data_file)
        data_file_path = Path(data_file)
        self._notebook.output_files_tab.set_all_from_dir(
            data_file_path.parent, data_file_path.stem
        )
        self._notebook.gui.set_posac_axes_out_dir(data_file_path.parent)

    #############
    #  Getters  #
    #############

    def get_job_name(self):
        return self.job_name_entry.get()

    def get_data_file(self):
        return self.data_input_entry.get()

    def get_lines_per_case(self):
        try:
            return int(self.lines_per_case_entry.get())
        except ValueError:
            return 0  # Return invalid value for validation to catch

    def get_plot_item_diagram(self) -> bool:
        return self.plot_item_diagram_entry.get() == \
            self.plot_item_diagram_entry.cget("values")[0]

    def get_plot_external_diagram(self) -> bool:
        return self.plot_external_diagram_entry.get() == \
            self.plot_external_diagram_entry.cget("values")[0]

    # todo: Figure out the frequence data type and return it (int or float)
    def get_only_freq(self):
        return int(self.only_freq_entry.get())

    def get_posac_type(self):
        return self.posac_type_combo.get()

    def get_subject_type(self):
        return self.subject_type_combo.get()

    def get_id_location(self) -> Tuple[int, int]:
        try:
            from_val = int(self.id_location_from_entry.get() or "0")
            to_val = int(self.id_location_to_entry.get() or "0")

            if from_val <= to_val:
                return (from_val, to_val)
            return (0, 0)
        except ValueError:
            return (0, 0)

    def get_all(self):
        return dict(
            job_name=self.get_job_name(),
            data_file=self.get_data_file(),
            lines_per_case=self.get_lines_per_case(),
            plot_item_diagram=self.get_plot_item_diagram(),
            plot_external_diagram=self.get_plot_external_diagram(),
            only_freq=self.get_only_freq(),
            posac_type=self.get_posac_type(),
            subject_type=self.get_subject_type(),
            id_location=self.get_id_location()
        )

    #############
    #  Setters  #
    #############

    def set_job_name(self, value):
        self.job_name_entry.delete(0, tk.END)
        self.job_name_entry.insert(0, value)

    def set_data_file(self, value):
        self.data_input_entry.delete(0, tk.END)
        self.data_input_entry.insert(0, value)

    def set_lines_per_case(self, value):
        try:
            value = int(value)
            if value < 1:
                value = 1
            self.lines_per_case_entry.delete(0, tk.END)
            self.lines_per_case_entry.insert(0, str(value))
        except ValueError:
            self.lines_per_case_entry.delete(0, tk.END)
            self.lines_per_case_entry.insert(0, "1")

    def set_plot_item_diagram(self, value):
        if value:
            self.plot_item_diagram_entry.current(0)
        else:
            self.plot_item_diagram_entry.current(1)

    def set_plot_external_diagram(self, value):
        if value:
            self.plot_external_diagram_entry.current(0)
        else:
            self.plot_external_diagram_entry.current(1)

    def set_only_freq(self, value):
        self.only_freq_entry.delete(0, tk.END)
        self.only_freq_entry.insert(0, value)

    def set_posac_type(self, value):
        self.posac_type_combo.set(value)

    def set_subject_type(self, value):
        self.subject_type_combo.set(value)

    def set_id_location(self, val_from, val_to):
        try:
            val_from = int(val_from)
            val_to = int(val_to)
            if val_from < 0:
                val_from = 0
            if val_to < 0:
                val_to = 0
            self.id_location_from_entry.delete(0, tk.END)
            self.id_location_from_entry.insert(0, str(val_from))
            self.id_location_to_entry.delete(0, tk.END)
            self.id_location_to_entry.insert(0, str(val_to))
        except ValueError:
            self.id_location_from_entry.delete(0, tk.END)
            self.id_location_from_entry.insert(0, "0")
            self.id_location_to_entry.delete(0, tk.END)
            self.id_location_to_entry.insert(0, "0")

    def set(self, **kwargs):
        if 'job_name' in kwargs: self.set_job_name(kwargs['job_name'])
        if 'data_file' in kwargs: self.set_data_file(kwargs['data_file'])
        if 'lines_per_case' in kwargs:
            self.set_lines_per_case(kwargs['lines_per_case'])
        if 'plot_item_diagram' in kwargs:
            self.set_plot_item_diagram(kwargs['plot_item_diagram'])
        if 'plot_external_diagram' in kwargs:
            self.set_plot_external_diagram(kwargs['plot_external_diagram'])
        if 'only_freq' in kwargs: self.set_only_freq(kwargs['only_freq'])
        if 'posac_type' in kwargs: self.set_posac_type(kwargs['posac_type'])
        if 'subject_type' in kwargs:
            self.set_subject_type(kwargs['subject_type'])
        if 'id_location' in kwargs:
            self.set_id_location(kwargs['id_location'][0],
                                 kwargs['id_location'][1])

    def set_default(self):
        self.set(**GeneralTab.DEFAULT_VALUES)
