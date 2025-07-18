import os
import tkinter as tk
from tkinter import ttk

from lib.gui.components.form import BoldLabel, BrowseButton, Entry
from lib.help.posac_help import Help
from lib.utils import real_size

py_ENTRIES = 25
pl_ENTRIES = 75
pl_ENTRIES_INNER = 60

EXT = dict(
    POSAC=("Posac files", "*.pos"),
    LSA1=("LSA1 files", "*.ls1"),
    LSA2=("LSA2 files", "*.ls2"),
)


class OFilesTab(tk.Frame):
    DEFAULT_OUT_POS = "C:/Program Files/POSAC/job.pos"
    DEFAULT_OUT_LS1 = "C:/Program Files/POSAC/job.ls1"
    DEFAULT_OUT_LS2 = "C:/Program Files/POSAC/job.ls2"

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self.gui = self._parent.gui
        self._create_widgets()

    def _create_widgets(self):
        label = BoldLabel(
            self, text="POSAC/LSA results will be written in the following files:"
        )
        label.pack(pady=real_size(10))
        self.posac_entry, self.posac_browse = self._create_output_entry(
            "POSAC", self.DEFAULT_OUT_POS
        )
        self.lsa1_entry, self.lsa1_browse = self._create_output_entry(
            "LSA1", self.DEFAULT_OUT_LS1
        )
        self.lsa2_entry, self.lsa2_browse = self._create_output_entry(
            "LSA2", self.DEFAULT_OUT_LS2
        )
        self.exit_button = ttk.Button(
            self, text="Exit POSAC", bootstyle="secondary", width=15
        )
        self.exit_button.pack(pady=real_size((60, 0)))

    def _create_output_entry(self, title, default):
        # Use a frame that can expand horizontally
        entry_frame = tk.Frame(self)
        entry_frame.pack(fill="x", pady=real_size(py_ENTRIES), padx=real_size(10))

        # Add a label on the left
        label = BoldLabel(entry_frame, text=title, size=9)
        label.pack(side=tk.LEFT, padx=(5, 0))

        # Add the browse button on the right with fixed position
        button = BrowseButton(
            entry_frame,
            command=lambda: self.browse_and_modify_entry(
                f"Save {title.lower().capitalize()} Output To..", None, EXT[title]
            ),
        )
        button.pack(side=tk.RIGHT, padx=(0, 5))

        # Add the entry that will expand/shrink in the middle
        entry = Entry(entry_frame, help=Help.OUTPUT_FILES)
        entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(10, 10))
        entry.insert(0, default)

        # Bind the entry to sync with others when it's modified in real-time
        entry.bind("<KeyRelease>", self._sync_entries)
        # Store the entry type to know which one it is
        entry.type = title

        # Save the entry reference in the button's command
        button.config(
            command=lambda: self.browse_and_modify_entry(
                f"Save {title.lower().capitalize()} Output To..", entry, EXT[title]
            )
        )

        return entry, button

    def _sync_entries(self, event=None):
        """Synchronize all entries in real-time when one is edited"""
        # Determine which entry triggered the event
        trigger_entry = event.widget if event else None

        if trigger_entry:
            # Get the path from the triggered entry
            path = trigger_entry.get()
            if not path:
                return

            # Get the directory and base filename without extension
            try:
                directory = os.path.dirname(path)
                base_filename = os.path.splitext(os.path.basename(path))[0]

                # Create new paths with appropriate extensions
                new_posac_path = os.path.join(directory, f"{base_filename}.pos")
                new_lsa1_path = os.path.join(directory, f"{base_filename}.ls1")
                new_lsa2_path = os.path.join(directory, f"{base_filename}.ls2")

                # Update all entries except the one that triggered the event
                # Save the current cursor position in the active entry
                cursor_pos = trigger_entry.index(tk.INSERT)

                if trigger_entry != self.posac_entry:
                    self.posac_entry.delete(0, tk.END)
                    self.posac_entry.insert(0, new_posac_path.replace("/", "\\"))

                if trigger_entry != self.lsa1_entry:
                    self.lsa1_entry.delete(0, tk.END)
                    self.lsa1_entry.insert(0, new_lsa1_path.replace("/", "\\"))

                if trigger_entry != self.lsa2_entry:
                    self.lsa2_entry.delete(0, tk.END)
                    self.lsa2_entry.insert(0, new_lsa2_path.replace("/", "\\"))

                # Restore cursor position in the active entry
                trigger_entry.icursor(cursor_pos)
            except Exception:
                # If there's an error parsing the path, just return without syncing
                return

    def get_default_base_name(self):
        """Get the default base name for files, using job name or data file name"""
        # Try to get job name first
        job_name = self._parent.general_tab.get_job_name()
        if job_name and job_name.strip():
            return job_name.strip()

        # If no job name, try to get data file name without extension
        data_file = self._parent.general_tab.get_data_file()
        if data_file and data_file.strip():
            return os.path.splitext(os.path.basename(data_file))[0]

        # Default fallback
        return "job"

    def browse_and_modify_entry(self, title, entry, file_types: tuple):
        # Get default base name for files
        default_base_name = self.get_default_base_name()

        # Set the default filename to save as
        default_extension = file_types[1][-4:]  # e.g. '.pos'
        default_filename = f"{default_base_name}{default_extension}"

        output_file = self.gui.save_file_diaglogue(
            title=title,
            file_types=[file_types],
            default_extension=file_types[1][-4:],
            initial_file_name=default_filename,
            allow_overwrite=True,
        )

        if output_file:
            # Update the current entry
            entry.delete(0, tk.END)
            entry.insert(0, output_file)

            # Get the directory and base filename
            new_directory = os.path.dirname(output_file)
            base_filename = os.path.splitext(os.path.basename(output_file))[0]

            # Create new paths with consistent separators
            new_posac_path = os.path.join(new_directory, f"{base_filename}.pos")
            new_lsa1_path = os.path.join(new_directory, f"{base_filename}.ls1")
            new_lsa2_path = os.path.join(new_directory, f"{base_filename}.ls2")

            # Update all entries with Windows-style path separators
            self.posac_entry.delete(0, tk.END)
            self.posac_entry.insert(0, new_posac_path.replace("/", "\\"))

            self.lsa1_entry.delete(0, tk.END)
            self.lsa1_entry.insert(0, new_lsa1_path.replace("/", "\\"))

            self.lsa2_entry.delete(0, tk.END)
            self.lsa2_entry.insert(0, new_lsa2_path.replace("/", "\\"))

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

    def set_all_from_dir(self, dir, name):
        self.set_posac_out(os.path.join(dir, f"{name}.pos"))
        self.set_lsa1_out(os.path.join(dir, f"{name}.ls1"))
        self.set_lsa2_out(os.path.join(dir, f"{name}.ls2"))

    def reset_default(self):
        self.set_all(self.DEFAULT_OUT_POS, self.DEFAULT_OUT_LS1,
                     self.DEFAULT_OUT_LS2)