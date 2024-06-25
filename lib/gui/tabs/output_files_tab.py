import tkinter as tk
from tkinter import ttk
from lib.gui.components.form import Label, BoldLabel
from lib.utils import real_size

py_ENTRIES = 25
pl_ENTRIES = 75
pl_ENTRIES_INNER = 60


class OFilesTab(tk.Frame):
    DEFAULT_OUT_POS = 'C:/Program Files/POSAC/job.pos'
    DEFAULT_OUT_LS1 = 'C:/Program Files/POSAC/job.ls1'
    DEFAULT_OUT_LS2 = 'C:/Program Files/POSAC/job.ls2'

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()

    def _create_widgets(self):
        label = BoldLabel(self, text='POSAC/LSA results will be written in '
                                     'the '
                                     'following files:')
        label.pack(pady=real_size(10))
        self._create_output_entry('POSAC', self.DEFAULT_OUT_POS)
        self._create_output_entry('LS1', self.DEFAULT_OUT_LS1)
        self._create_output_entry('LS2', self.DEFAULT_OUT_LS2)
        self.exit_button = ttk.Button(self, text='Exit POSAC',
                                      bootstyle='secondary', width=15)
        self.exit_button.pack(pady=real_size((60,0)))

    def _create_output_entry(self, title, default):
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=real_size(py_ENTRIES))
        label = BoldLabel(entry_frame, text=title, size=9)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(entry_frame, width=45)
        xpad = pl_ENTRIES_INNER - (len(title) * 8)
        entry.pack(side=tk.LEFT, padx=real_size((xpad, 0)))
        entry.insert(0, default)
        button = ttk.Button(entry_frame, text='Browse', width=10)
        xpad = pl_ENTRIES_INNER - 30
        button.pack(side=tk.LEFT, padx=real_size((xpad, 0)))
        return entry, button
