import tkinter as tk
import ttkbootstrap as ttk
from lib.gui.components.form import Label

ENTRIES_PAD_Y = 5
ENTRIES_PAD_RIGHT = 100
ENTRIES_PAD_LEFT = 40

class GeneralTab(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()

    ###########
    #   GUI   #
    ###########

    def _create_widgets(self):
        self.job_name_frame = tk.Frame(self)
        self.job_name_frame.pack(fill='x', padx=10, pady=2)
        self.job_name_entry = self._create_label_entry(
            "What name do you want for this "
            "Posac job?")
        self._create_data_input()
        self.lines_per_case_entry = self._create_label_entry(
            "How many lines per case in the data file?",
            default=1, width=6)
        self.plot_item_diagram_entry = self._create_label_combo(
            "Do you want item diagrams plotted?", ["Yes", "No"],
            default="Yes",
            width=5)
        self.plot_external_diagram_entry = self._create_label_combo(
            "Do you want external diagrams plotted?", ["Yes", "No"],
            default="Yes",
            width=5)
        self.only_freq_entry = self._create_label_entry(
            "To process only profiles with frequency>f, enter value of f",
            default=0, width=6)
        self.posac_type_combo = self._create_label_combo(
            "Run Distributional Posac, Structural Posac or just Profiles? (D/S/P)",
            ["D", "S", "P"],
            default="D",
            width=5)
        self.subject_type_combo = self._create_label_combo(
            "Data Subjects, Identified Subjects or Profiles and frequencies? (S/I/P)",
            ["S", "I", "P"],
            default="S",
            width=5)
        #
        self._create_id_location()

    def _create_data_input(self):
        data_input_frame = tk.Frame(self)
        data_input_frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT+40, 0),
                              pady=ENTRIES_PAD_Y)
        self.data_input_label = Label(data_input_frame, text=
        "Data File:")
        self.data_input_label.pack(side=tk.LEFT)
        right_frame = tk.Frame(data_input_frame)
        right_frame.pack(side=tk.RIGHT, padx=(0, 30))
        self.data_input_entry = ttk.Entry(right_frame, width=50)
        self.data_input_entry.pack(side=tk.LEFT)
        # add a browse button
        self.browse_button = ttk.Button(right_frame, text="Browse")
        self.browse_button.pack(side=tk.LEFT, padx=(40, 0))

    def _create_id_location(self):
        id_location_frame = tk.Frame(self)
        id_location_frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT, 0),
                               pady=ENTRIES_PAD_Y)
        self.id_location = Label(id_location_frame, text=
        "If data are identidies subjects or "
        "Profiles and Frquencies, where in "
        "record 1 are the id label/frequencies "
        "located? (columns from-to)",
                                 wraplength=400)
        self.id_location.pack(side=tk.LEFT, padx=(0, 30))
        id_location_right = tk.Frame(id_location_frame)
        id_location_right.pack(side=tk.RIGHT, padx=(0, 30))
        from_label = Label(id_location_right, text="From")
        from_label.pack(side=tk.LEFT, padx=(0, 5))
        self.id_location_from_entry = ttk.Entry(id_location_right, width=5)
        self.id_location_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.id_location_from_entry.insert(0, "0")
        to_label = Label(id_location_right, text="To")
        to_label.pack(side=tk.LEFT, padx=(0, 5))
        self.id_location_to_entry = ttk.Entry(id_location_right, width=5)
        self.id_location_to_entry.pack(side=tk.LEFT)
        self.id_location_to_entry.insert(0, "0")

    def _create_label_entry(self, text, **kwargs):
        frame = tk.Frame(self)
        default = kwargs.pop('default', "")
        frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT),
                   pady=ENTRIES_PAD_Y)
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame, **kwargs)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default)
        return entry

    def _create_label_combo(self, text, values, default,
                            **kwargs):
        frame = tk.Frame(self)
        frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT, ENTRIES_PAD_RIGHT),
                   pady=ENTRIES_PAD_Y)
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        combo = ttk.Combobox(frame, values=values, **kwargs)
        combo.set(default)
        combo.pack(side=tk.RIGHT)
        return combo

    #############
    # Get & Set #
    #############
