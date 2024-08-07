import tkinter as tk
from tkinter import ttk
from lib.gui.components.form import Label, BoldLabel, BrowseButton
from lib.utils import real_size, rreal_size

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
        self.posac_entry, self.posac_browse = self._create_output_entry(
            'POSAC',
            self.DEFAULT_OUT_POS)
        self.lsa1_entry, self.lsa1_browse = self._create_output_entry('LS1',
                                                                      self.DEFAULT_OUT_LS1)
        self.lsa2_entry, self.lsa2_browse = self._create_output_entry('LS2',
                                                                      self.DEFAULT_OUT_LS2)
        self.exit_button = ttk.Button(self, text='Exit POSAC',
                                      bootstyle='secondary', width=15)
        self.exit_button.pack(pady=real_size((60, 0)))

    def _create_output_entry(self, title, default):
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=real_size(py_ENTRIES))
        label = BoldLabel(entry_frame, text=title, size=9)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(entry_frame, width=rreal_size(70))
        xpad = pl_ENTRIES_INNER - (len(title) * 8)
        entry.pack(side=tk.LEFT, padx=real_size((xpad, 0)))
        entry.insert(0, default)
        button = BrowseButton(entry_frame)
        xpad = pl_ENTRIES_INNER - 30
        button.pack(side=tk.LEFT, padx=real_size((xpad, 0)))
        return entry, button

    def get_posac_out(self):
        return self.posac_entry.get()

    def get_lsa1_out(self):
        return self.lsa1_entry.get()

    def get_lsa2_out(self):
        return self.lsa2_entry.get()

    def get_all(self):
        return {
            'posac': self.get_posac_out(),
            'lsa1': self.get_lsa1_out(),
            'lsa2': self.get_lsa2_out()
        }

    def set_posac_out(self, path):
        self.posac_entry.delete(0, tk.END)
        self.posac_entry.insert(0, path)

    def set_lsa1_out(self, path):
        self.lsa1_entry.delete(0, tk.END)
        self.lsa1_entry.insert(0, path)

    def set_lsa2_out(self, path):
        self.lsa2_entry.delete(0, tk.END)
        self.lsa2_entry.insert(0, path)

    def set_all(self, posac, lsa1, lsa2):
        self.set_posac_out(posac)
        self.set_lsa1_out(lsa1)
        self.set_lsa2_out(lsa2)

