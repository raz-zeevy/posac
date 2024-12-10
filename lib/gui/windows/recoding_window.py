import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tktooltip import ToolTip
from lib.components.window import Window
from lib.utils import rreal_size, get_resource, real_size
from lib.components.form import NavigationButton
from tkinter import messagebox
import re
from lib.pages.data_page import DataPage  # Add this import at the top
import logging
from typing import Tuple, List, Set


class RecodeWindow(Window):
    SAVED_VALUES = dict(
        RECODED_VARS=set()  # Track variables with applied recoding
    )
    _instance = None  # Add class variable to track instance

    def __new__(cls, parent, **kwargs):
        # If an instance exists and is valid, return it
        if cls._instance is not None and cls._instance.winfo_exists():
            cls._instance.focus_force()
            cls._instance.lift()
            return cls._instance
        
        # Create new instance if none exists
        return super().__new__(cls)

    def __init__(self, parent, **kwargs):
        # Only initialize if this is a new instance
        if not hasattr(self, '_initialized'):
            super().__init__(**kwargs, geometry=f"{rreal_size(600)}x{rreal_size(570)}")
            RecodeWindow._instance = self
            self.parent = parent
            self.title("Recode Variables")
            self.iconbitmap(get_resource("icon.ico"))
            self.center_window()
            self.create_widgets()
            self.old_values_tracker = []
            self._initialized = True
            self.resizable(True, True)


    def on_closing(self):
        RecodeWindow._instance = None
        super().on_closing()

    @classmethod
    def is_open(cls):
        return cls._instance is not None and cls._instance.winfo_exists()

    @classmethod
    def reset(cls):
        cls._instance = None
        cls.reset_default()

    def create_widgets(self):
        # Instruction Label
        instruction_label = ttk.Label(
            self,
            text=(
                "To recode variables, enter the indices of selected variables "
                "(e.g., 1, 3, 5-7) in the 'Variable Indices' box, then you can use the manual "
                "recoding option for recoding by manual values, or if for a "
                "subset of "
                "variables, you want simple inversion of existing values, "
                "select the inverse option below."
            ),
            wraplength=rreal_size(580),
            justify="left"
        )
        instruction_label.pack(pady=(10, 5), padx=10)

        # Frame for Variable Index Entry
        var_index_frame = ttk.Frame(self)
        var_index_frame.pack(fill='x', padx=10, pady=real_size(3))

        # Variable Index Input
        ttk.Label(var_index_frame, text="Variable Indices:").pack(
            side='left', padx=(10, 5))
        self.var_index_entry = ttk.Entry(var_index_frame, width=20)
        self.var_index_entry.pack(side='left', padx=10, pady=5)
        ToolTip(self.var_index_entry,
                msg="Enter variable indices for this recoding operation (e.g., 1, 3, 5-7)")

        manual_recoding_frame = ttk.LabelFrame(self, text="Manual Recoding")
        manual_recoding_frame.pack(fill='both', expand=True, padx=10,
                                   pady=(0, 10))
        manual_recoding_label_frame = ttk.Frame(manual_recoding_frame)
        manual_recoding_label_frame.pack(fill='x', padx=10, pady=(5, 5))
        manual_recoding_label = ttk.Label(
            manual_recoding_label_frame,
            text=("Specify "
                  "old values (e.g., 2-8, 11) and the new value you want to "
                  "assign. Old "
                  "values must be mutually exclusive. Click 'Add' to add the "
                  "mapping in the list below, or Select one or more "
                  "pairs and click 'Remove' to delete them from the list."
                  ),
            wraplength=rreal_size(550),
            justify="left"
        )
        manual_recoding_label.pack(side="left", pady=(5, 5),
                                   padx=real_size(10))

        # Frame for Old and New Value Inputs
        input_frame = ttk.Frame(manual_recoding_frame)
        input_frame.pack(fill='x', padx=10, pady=real_size((0, 10)))

        # Old Values Entry
        old_values_frame = ttk.LabelFrame(input_frame, text="Old Values")
        old_values_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.old_values_entry = ttk.Entry(old_values_frame)
        self.old_values_entry.pack(fill='x', padx=5, pady=5)
        ToolTip(self.old_values_entry, msg="Enter old values (e.g., 2-8, 11)")

        # New Value Entry
        new_value_frame = ttk.LabelFrame(input_frame, text="New Value")
        new_value_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.new_value_entry = ttk.Entry(new_value_frame)
        self.new_value_entry.pack(fill='x', padx=5, pady=5)
        ToolTip(self.new_value_entry, msg="Enter the new value for recoding")

        # Treeview for Pairs
        self.create_treeview(manual_recoding_frame)

        # Inversion Option
        self.create_inversion_option()

        # Action Buttons
        self.create_action_buttons()

    def create_treeview(self, frame):
        # Frame for Treeview and scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='x', expand=False, padx=10, pady=(0, 10))

        # Frame to hold buttons on the left side
        button_frame = ttk.Frame(tree_frame)
        button_frame.pack(side='left', fill='y', padx=(0, 5))

        # Add and Remove Buttons
        self.add_button = ttk.Button(button_frame, text="Add",
                                     command=self._add_pair)
        self.add_button.pack(fill='x', pady=(0, 5))
        ToolTip(self.add_button, msg="Add the old-new value pair")

        self.remove_button = ttk.Button(button_frame, text="Remove",
                                        command=self._remove_pair)
        self.remove_button.pack(fill='x')
        ToolTip(self.remove_button, msg="Remove selected pair")

        # Treeview for pairs
        columns = ('Old Values', 'New Value')
        self.pair_tree = ttk.Treeview(tree_frame, columns=columns,
                                      show='headings', height=7)
        self.pair_tree.heading('Old Values', text='Old Values')
        self.pair_tree.heading('New Value', text='New Value')
        self.pair_tree.column('Old Values', anchor='center')
        self.pair_tree.column('New Value', anchor='center')
        self.pair_tree.pack(side='left', fill='both', expand=True)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical',
                                  command=self.pair_tree.yview)
        self.pair_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def create_inversion_option(self):
        inversion_frame = ttk.LabelFrame(self, text="Inversion")
        inversion_frame.pack(fill='x', padx=10, pady=(0, 10))

        invert_label = ttk.Label(
            inversion_frame,
            text=(
                "Select to reverse the values after recoding. If no recoding pairs are defined, "
                "the inversion will apply to the original values."
            ),
            wraplength=rreal_size(450),
            justify="left"
        )
        invert_label.pack(side='left', padx=real_size(10), pady=real_size(3))

        self.invert_var = tk.BooleanVar()
        invert_check = ttk.Checkbutton(inversion_frame,
                                       variable=self.invert_var,
                                       bootstyle="round-toggle")
        invert_check.pack(side='right', padx=real_size((0, 40)))
        ToolTip(invert_check, msg="Select to invert values after recoding")

    def create_action_buttons(self):
        action_frame = ttk.Frame(self)
        action_frame.pack(pady=(10, 10))

        apply_button = NavigationButton(action_frame, text="Apply",
                                        command=self.apply_recoding)
        apply_button.pack(side='left', padx=(0, 10))
        ToolTip(apply_button, msg="Apply recoding")

        cancel_button = NavigationButton(action_frame, text="Cancel",
                                         command=self.cancel_recoding,
                                         style="secondary")
        cancel_button.pack(side='left', padx=(10, 0))
        ToolTip(cancel_button, msg="Cancel without applying")

    def _add_pair(self, old_values=None, new_value=None):
        old_values = old_values or self.old_values_entry.get().strip()
        new_value = new_value or self.new_value_entry.get().strip()

        if not old_values and not new_value:
            return

        if not self.validate_old_values(old_values):
            messagebox.showwarning("Invalid Input", "Old values must be a comma-separated list of numbers or ranges.")
            return

        # Validate old values and exclusivity
        if not self.check_exclusivity(old_values):
            messagebox.showwarning("Invalid Input", "Old values may appear only once.")
            return

        # Validate new value
        if not self.validate_new_value(new_value):
            messagebox.showwarning("Invalid Input", "New value must be a number between 0 and 99.")
            return

        # Add new pair to treeview
        self.pair_tree.insert('', 'end', values=(old_values, new_value))
        self.old_values_entry.delete(0, 'end')
        self.new_value_entry.delete(0, 'end')

    def validate_old_values(self, old_values):
        return bool(
            re.match(r'^\s*(\d+(-\d+)?)(\s*,\s*\d+(-\d+)?)*\s*$', old_values))

    def validate_variable_index(self, var_index):
        return bool(
            re.match(r'^\s*(\d+(-\d+)?)(\s*,\s*\d+(-\d+)?)*\s*$', var_index))

    def check_exclusivity(self, old_values):
        # Get current values from treeview instead of tracker
        existing_values = set()
        for item in self.pair_tree.get_children():
            old_vals = str(self.pair_tree.item(item)['values'][0])
            existing_values.update(self.parse_ranges(old_vals))
        
        # Check if new values overlap with existing ones
        current_ranges = set(self.parse_ranges(old_values))
        return not (current_ranges & existing_values)

    def validate_new_value(self, new_value):
        try:
            value = int(new_value)
            return 0 <= value <= 99
        except ValueError:
            return False

    def parse_ranges(self, value_range):
        ranges = []
        for part in value_range.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ranges.extend(range(start, end + 1))
            else:
                ranges.append(int(part))
        return ranges

    def validate_recoding_request(self) -> Tuple[bool, str, List[int]]:
        """
        Validates the recoding request and returns validation status, error message, and parsed indices
        Returns:
            Tuple[bool, str, List[int]]: (is_valid, error_message, parsed_indices)
        """
        var_indices = self.var_index_entry.get().strip()
        
        # Validate input format
        if not var_indices or not self.validate_variable_index(var_indices):
            return False, "Please enter valid variable indices.", []

        try:
            # Get DataPage and validate data availability
            data_page = next(page for page in self.parent.pages.values() 
                           if isinstance(page, DataPage))
            
            if not hasattr(data_page, 'data') or data_page.data is None:
                return False, "No data available for recoding.", []
            
            max_var_index = len(data_page.data.columns)
            logging.debug(f"Found {max_var_index} variables in data")

        except (StopIteration, AttributeError) as e:
            logging.error(f"Error accessing data page: {str(e)}")
            return False, "Cannot access data. Please ensure data is loaded.", []

        # Parse and validate indices
        try:
            indices = self.parse_ranges(var_indices)
            out_of_range = [idx for idx in indices if idx > max_var_index or idx < 1]
            
            if out_of_range:
                error_msg = (f"Variable indices {', '.join(map(str, out_of_range))} "
                           f"are out of range.\nAvailable variables are 1-{max_var_index}.")
                return False, error_msg, []

            # Check for already recoded variables
            already_recoded = [idx for idx in indices if idx in self.SAVED_VALUES['RECODED_VARS']]
            if already_recoded:
                error_msg = (f"Variable(s) {', '.join(map(str, already_recoded))} already recoded. "
                           "To recode again, please press 'Cancel' and 'Previous'")
                return False, error_msg, []

            logging.debug(f"Validated indices for recoding: {indices}")
            return True, "", list(indices)

        except ValueError as e:
            logging.error(f"Error parsing indices: {str(e)}")
            return False, "Please enter valid variable indices.", []

    def parse_ranges(self, value_range: str) -> Set[int]:
        """
        Parse a string of ranges into a set of integers
        Args:
            value_range: String containing ranges (e.g., "1-3,5,7-9")
        Returns:
            Set of integers
        """
        try:
            ranges = []
            for part in value_range.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start > end:
                        raise ValueError(f"Invalid range: {start}-{end}")
                    ranges.extend(range(start, end + 1))
                else:
                    ranges.append(int(part))
            return set(ranges)
        except ValueError as e:
            logging.error(f"Error parsing range '{value_range}': {str(e)}")
            raise

    def apply_recoding(self):
        """Apply recoding with validation and error handling"""
        logging.debug("Starting recoding application")
        
        is_valid, error_msg, indices = self.validate_recoding_request()
        
        if not is_valid:
            messagebox.showerror("Recoding Error", error_msg)
            return

        try:
            # Add validated indices to saved values
            self.SAVED_VALUES['RECODED_VARS'].update(indices)
            
            # Apply the recoding
            self._apply_recoding_func()
            self.destroy()
            self.parent.show_recode_msg()
            
            logging.info(f"Successfully applied recoding for indices: {indices}")
            
        except Exception as e:
            logging.error(f"Error during recoding application: {str(e)}")
            messagebox.showerror(
                "Recoding Error",
                f"An error occurred while applying recoding: {str(e)}"
            )

    def _apply_recoding_func(self):
        """
        This function should be overridden by the data page
        """
        raise Exception("Shouldn't be called")

    def cancel_recoding(self):
        self.destroy()

    def _remove_pair(self):
        selected_items = self.pair_tree.selection()
        for item in selected_items:
            self.pair_tree.delete(item)

    def _sync_tracker(self):
        """Synchronize the old_values_tracker with current treeview items"""
        self.old_values_tracker = []
        for item in self.pair_tree.get_children():
            old_values = str(self.pair_tree.item(item)['values'][0])
            self.old_values_tracker.append(old_values)

    #######
    # API #
    #######

    def add_pair(self, old_value: str, new_value: str):
        self._add_pair(str(old_value), str(new_value))

    def set_variables_indices(self, indices_str : str):
        self.var_index_entry.delete(0, 'end')
        self.var_index_entry.insert(0, indices_str)

    def get_recoding_pairs(self):
        """
        :return: a list of tuples containing the recoding pairs
        """
        return [(str(self.pair_tree.item(item)['values'][0]),
                 str(self.pair_tree.item(item)['values'][1]))
                for item in self.pair_tree.get_children()]

    def set_inverse(self, inverse: bool):
        self.invert_var.set(inverse)

    def get_recoding_details(self):
        """
        :return: a dictionary containing the recoding details
        """
        return dict(
            var_indices_str = self.var_index_entry.get(),
            manual = self.get_recoding_pairs(),
            invert = self.invert_var.get()
        )

    @classmethod
    def reset_default(cls):
        cls.SAVED_VALUES = dict(
            RECODED_VARS=set()
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RecodeWindow(root)
    app.mainloop()
