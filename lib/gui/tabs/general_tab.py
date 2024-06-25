import tkinter as tk
import ttkbootstrap as ttk
from lib.gui.components.form import Label
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
        self._parent = parent
        self._create_widgets()

    ###########
    #   GUI   #
    ###########

    def _create_widgets(self):
        self.job_name_frame = tk.Frame(self)
        self.job_name_frame.pack(fill='x', padx=10, pady=real_size(2))
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
        data_input_frame.pack(fill='x', padx=(ENTRIES_PAD_LEFT + 40, 0),
                              pady=real_size(ENTRIES_PAD_Y))
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
                               pady=real_size(ENTRIES_PAD_Y))
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
                   pady=real_size(ENTRIES_PAD_Y))
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
                   pady=real_size(ENTRIES_PAD_Y))
        label = Label(frame, text=text)
        label.pack(side=tk.LEFT)
        combo = ttk.Combobox(frame, values=values, **kwargs)
        combo.set(default)
        combo.pack(side=tk.RIGHT)
        return combo

    #############
    #  Getters  #
    #############

    def get_job_name(self): return self.job_name_entry.get()

    def get_data_file(self): return self.data_input_entry.get()

    def get_lines_per_case(self): return int(self.lines_per_case_entry.get())

    def get_plot_item_diagram(self) -> bool:
        return self.plot_item_diagram_entry.get() == self.plot_item_diagram_entry.cget("values")[0]

    def get_plot_external_diagram(self) -> bool:
        return self.plot_external_diagram_entry.get() == self.plot_external_diagram_entry.cget("values")[0]

    #todo: Figure out the frequence data type and return it (int or float)
    def get_only_freq(self): return int(self.only_freq_entry.get())

    def get_posac_type(self): return self.posac_type_combo.get()

    def get_subject_type(self): return self.subject_type_combo.get()

    def get_id_location(self): return \
        int(self.id_location_from_entry.get()), \
        int(self.id_location_to_entry.get())

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
        self.lines_per_case_entry.delete(0, tk.END)
        self.lines_per_case_entry.insert(0, value)

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

    def set_posac_type(self, value): self.posac_type_combo.set(value)

    def set_subject_type(self, value): self.subject_type_combo.set(value)

    def set_id_location(self, val_from, val_to):
        self.id_location_from_entry.delete(0, tk.END)
        self.id_location_from_entry.insert(0, val_from)
        self.id_location_to_entry.delete(0, tk.END)
        self.id_location_to_entry.insert(0, val_to)

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