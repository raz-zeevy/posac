import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Optional

from lib.gui.components.form import BoldLabel, Entry, Label, SelectionBox
from lib.gui.components.ranges_table import RangesTable
from lib.help.posac_help import Help
from lib.utils import real_size
from lib.controller.validator import Validator

px_TOP_INPUTS = 50
py_TOP_INPUTS = 10
px_TOP_INPUTS_INNER = 10


def parse_range(range_str: str) -> Optional[Tuple[int, int]]:
    """Parse a range string like '1-9' into a tuple of (from, to)."""
    if not range_str or not range_str.strip():
        return None
    try:
        parts = range_str.split('-')
        if len(parts) != 2:
            return None
        from_val = int(parts[0])
        to_val = int(parts[1])
        return (from_val, to_val)
    except (ValueError, AttributeError):
        return None


def clip_range_to_valid(trait_range_str: str, valid_ranges_list: List[str]) -> List[str]:
    """
    Clip a trait range to fit within valid external variable ranges.

    Args:
        trait_range_str: A range string like "3-7"
        valid_ranges_list: List of valid range strings like ["1-2", "4-6"]

    Returns:
        List of clipped range strings that fit within valid ranges.
        Example: trait "3-7" with valid ["1-2", "4-6"] returns ["4-6"]
    """
    trait_range = parse_range(trait_range_str)
    if not trait_range:
        return []

    trait_from, trait_to = trait_range
    result = []

    for valid_range_str in valid_ranges_list:
        valid_range = parse_range(valid_range_str)
        if not valid_range:
            continue

        valid_from, valid_to = valid_range
        # Find intersection
        intersect_from = max(trait_from, valid_from)
        intersect_to = min(trait_to, valid_to)

        if intersect_from <= intersect_to:
            result.append(f"{intersect_from}-{intersect_to}")

    return result


class TraitsTab(tk.Frame):
    class TraitData:
        def __init__(self, label: str, data: List[List]):
            self.label : str = label
            self.data : List[List] = data

        def __str__(self):
            return f'{self.label}: {self.data}'

        def __repr__(self):
            return str(self)

        def __eq__(self, other):
            return self.label == other.label and self.data == other.data

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.notebook = parent
        self._traits = []
        self.main_frame = None
        self._current_trait = 1
        self._create_widgets()
        self._showing_traits = False
        self._update_frames(False)

    def _create_widgets(self):
        self._create_table()
        self._create_no_traits_label()

    def _update_frames(self, show_traits: bool):
        """
        this function updates the frames according to the context,
        it updates the frame content according to the number of traits
        and doesn't update the table itself (it's done by set_trait)
        :param show_traits: boolean
        :return:
        """
        if not show_traits:
            self.main_frame.pack_forget()
            self.not_traits_frame.pack(fill='both', expand=True, padx=0,
                                       pady=0)
        else:
            self.not_traits_frame.pack_forget()
            self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)
            self.traits_num_box.config(
                dict(values=[str(i + 1) for i in
                             range(len(self._traits))])
            )
            self.select_trait(self._current_trait)
        self._showing_traits = show_traits

    def _create_no_traits_label(self):
        self.not_traits_frame = tk.Frame(self)
        label = BoldLabel(self.not_traits_frame,
                          text='You must define the number of traits in the previous '
                               'screen', size=11)
        label.pack(pady=real_size(py_TOP_INPUTS))

    def _create_table(self):
        self.main_frame = tk.Frame(self)
        # Upper Frame
        upper_frame = tk.Frame(self.main_frame)
        upper_frame.pack(fill='x', padx=0, pady=real_size(py_TOP_INPUTS))
        # Traits Selection
        traits_num_frame = tk.Frame(upper_frame)
        trait_num_label = Label(traits_num_frame, text="Trait Number")
        trait_num_label.pack(side='left')
        self.traits_num_box = SelectionBox(traits_num_frame,
                                           values=[str(i + 1) for i in
                                                   range(len(
                                                       self._traits))])
        self.traits_num_box.bind('<<ComboboxSelected>>',
                                 self._on_trait_num_change)
        self.traits_num_box.pack(side='right', padx=real_size(
            px_TOP_INPUTS_INNER))
        traits_num_frame.pack(side='left', padx=(real_size(px_TOP_INPUTS), 0),
                              pady=real_size(2))
        # Trait Label
        trait_label_frame = tk.Frame(upper_frame)
        trait_label = Label(trait_label_frame, text='Trait Label')
        trait_label.pack(side='left')
        self.trait_entry = Entry(trait_label_frame)
        self.trait_entry.pack(side='right', padx=real_size(
            px_TOP_INPUTS_INNER))
        trait_label_frame.pack(side='right',
                               padx=(0, real_size(px_TOP_INPUTS)),
                               pady=real_size(2))
        # Traits Table
        self.ranges_table_frame = tk.Frame(self.main_frame)
        self.traits_table = RangesTable(self.ranges_table_frame,
                                        help=Help.EXTERNAL_TRAITS)
        # Set custom validation after creation
        self.traits_table.custom_validation = self._validate_trait_range
        self.ranges_table_frame.pack(fill='both', expand=True, padx=10,
                                     pady=(0, 0))
        # Bottom Label
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(fill='x', padx=0, pady=real_size(py_TOP_INPUTS))
        self.bottom_label = BoldLabel(bottom_frame, text='',
                                      size=11)
        self.bottom_label.pack(padx=real_size(px_TOP_INPUTS))

    def _on_trait_num_change(self, event):
        self._update_traits_from_table()
        self.select_trait(int(event.widget.get()))

    def _validate_trait_range(self, value: dict, col_index: int, row_values: dict):
        """
        Custom validation for trait ranges to ensure they're within external variable ranges.
        """
        # First, do the standard range validation
        if not self.traits_table.perform_standard_validation(value, col_index, row_values):
            return False

        if not value:
            return True

        actual_value = list(value.values())[0]

        # For range columns (col_index > 1), validate against external vars
        if col_index > 1 and actual_value.strip():
            # Validate against external variable ranges
            # Get the row index (which external variable this is)
            if hasattr(self.notebook, 'external_variables_ranges_tab'):
                all_ext_ranges = self.notebook.external_variables_ranges_tab.get_all_ranges_values()

                # Get the row index from the currently editing item
                # Note: Relying on _current_editing_item is fragile but maintaining existing behavior for now
                if hasattr(self.traits_table, '_current_editing_item') and self.traits_table._current_editing_item:
                    try:
                        children = self.traits_table.get_children()
                        # Find the index of the item being edited
                        ext_var_index = children.index(self.traits_table._current_editing_item)
                        ext_var_num = ext_var_index + 1  # Convert to 1-based for display

                        if 0 <= ext_var_index < len(all_ext_ranges):
                            ext_var_ranges = all_ext_ranges[ext_var_index]

                            # Validate the trait range against external ranges
                            if not Validator.validate_trait_range_against_external(actual_value, ext_var_ranges):
                                messagebox.showwarning(
                                    "Invalid Trait Range",
                                    f"Trait range '{actual_value}' is not within the admissible ranges for external variable {ext_var_num}.\n\n"
                                    f"Admissible ranges: {', '.join(ext_var_ranges)}\n\n"
                                    f"Trait ranges must be fully contained within one of the admissible ranges."
                                )
                                return False
                    except (ValueError, IndexError):
                        pass

        return True

    def _update_traits_from_table(self):
        if self._showing_traits:
            self._traits[
                self._current_trait - 1].label = self.trait_entry.get()
            self._traits[self._current_trait - 1].data = self.traits_table. \
                get_all_values()

    #######
    # Get #
    #######

    def get_current_trait(self):
        return self._current_trait

    def get_traits(self):
        return self._traits

    def get_traits_values(self) -> List[dict]:
        """
        This function returns the traits values in the format that is
        expected by the POSAC input writer
        the data is the ranges for traits without the first two columns
        (external variable index and number of ranges)
        """
        self._update_traits_from_table()
        traits = []
        for trait in self._traits:
            trait_value = {}
            trait_value["data"] = [[rng for rng in rngs[1:] if rng] for rngs in trait.data if rngs]
            trait_value['label'] = trait.label
            traits.append(trait_value)
        return traits

    def get_traits_num(self):
        return len(self._traits)

    #######
    # Set #
    #######

    def select_trait(self, i):
        """
        Set the current trait to the (i)-th trait
        :param i: 1..len(traits)
        :return:
        """
        self.trait_entry.delete(0, tk.END)
        self.trait_entry.insert(0, self._traits[i - 1].label)
        self.traits_num_box.set(i)
        self.traits_table.clear_rows()
        self.bottom_label.config(text=f'This is trait No. {i} of '
                                      f'{len(self._traits)} traits')
        for ranges_row in self._traits[i - 1].data:
            self.traits_table.add_row(ranges_row)
        self._current_trait = i

    def set_trait(self, i, label=None, data: List[List] = None):
        if i > len(self._traits):
            raise ValueError(f'Trait index {i} is out of bounds for the number of traits {len(self._traits)}')
        if label is not None:
            self._traits[i - 1].label = label
        if data is not None:
            self._traits[i - 1].data = data
        if self._current_trait == i:
            self.select_trait(i)

    def set_traits(self, traits):
        self._traits = [self.TraitData(None, None) for _ in traits]
        for i, trait in enumerate(traits):
            self.set_trait(i+1, label=trait.label,
                           data=trait.data)
            self.select_trait(i + 1)

    #######
    # API #
    #######

    def update_traits_num(self, traits_num, var_num, ext_var_ranges=None):
        """
        Update the number of traits.

        :param traits_num: Number of traits
        :param var_num: Number of external variables
        :param ext_var_ranges: List of ranges for each external variable.
                               Each item is a list like ['1', '1-9'] or ['2', '1-2', '4-6']
        """
        self._update_traits_from_table()
        while len(self._traits) < traits_num:
            # Initialize trait ranges based on external variable ranges
            if ext_var_ranges:
                ranges = [list(range_data) for range_data in ext_var_ranges]
            else:
                ranges = [RangesTable.DEFAULT_VALUE.copy() for _ in range(var_num)]
            label = f"trait{len(self._traits) + 1}"
            self._traits.append(self.TraitData(label, ranges))
        while len(self._traits) > traits_num:
            self._traits.pop()
        self._current_trait = max(1, min(self._current_trait, len(self._traits)))
        if traits_num == 0:
            self._update_frames(False)
        else:
            self._update_frames(True)

    def add_external_variable(self, ext_var_range=None):
        """
        Add a new external variable to all traits.

        :param ext_var_range: The range data for the new external variable.
                             e.g., ['1', '1-9'] or ['2', '1-2', '4-6']
        """
        for trait in self._traits:
            if ext_var_range:
                trait.data.append(list(ext_var_range))
            else:
                trait.data.append(RangesTable.get_new_row())
        if self._traits:
            self.select_trait(self._current_trait)

    def remove_external_variable(self):
        for trait in self._traits:
            if trait:
                trait.data.pop()
        if self._traits:
            self.select_trait(self._current_trait)

    def reset_default(self):
        for trait in self._traits:
            trait.label = f"trait{self._traits.index(trait) + 1}"
            trait.data = [RangesTable.DEFAULT_VALUE] * len(trait.data)
        if self._traits:
            self.select_trait(self._current_trait)

    def clear_external_variables(self):
        self._traits = []
        self.update_traits_num(0, 0)

    def add_trait(self, label : str, data : List[List]):
        """
        Add a trait to the traits list
        :param label: the label of the trait
        :param data: the data of the tra
        :return:
        """
        self._traits.append(self.TraitData(label, data))
        self.select_trait(len(self._traits))
        self.update_traits_num(len(self._traits), len(data))

    def update_external_variable_ranges(self, ext_var_index: int, new_ranges: List[str]):
        """
        Update trait ranges when external variable ranges change.
        Automatically clips trait ranges to fit within the new valid ranges.

        :param ext_var_index: Index of the external variable (0-based)
        :param new_ranges: List of new valid ranges like ["1-2", "4-6"]
        """
        if not self._traits:
            return

        # Validate inputs
        if not isinstance(new_ranges, list):
            return

        # Update each trait's data for this external variable
        for trait in self._traits:
            if ext_var_index < len(trait.data):
                # Get current trait ranges for this external variable
                trait_var_data = trait.data[ext_var_index]

                # Extract number of ranges and range strings
                if not trait_var_data or len(trait_var_data) < 2:
                    continue

                current_ranges = [r for r in trait_var_data[1:] if r and r.strip()]

                # Clip each trait range to the new valid ranges
                clipped_ranges = []
                for trait_range in current_ranges:
                    if trait_range and trait_range.strip():
                        clipped = clip_range_to_valid(trait_range, new_ranges)
                        clipped_ranges.extend(clipped)

                # Limit to maximum NUM_RANGES to prevent data corruption
                clipped_ranges = clipped_ranges[:RangesTable.NUM_RANGES]

                # Update the trait data with clipped ranges
                new_trait_data = [str(len(clipped_ranges))]
                new_trait_data.extend(clipped_ranges)
                # Pad with empty strings to maintain table structure (total of NUM_RANGES + 1)
                while len(new_trait_data) < (RangesTable.NUM_RANGES + 1):
                    new_trait_data.append('')

                # Ensure we don't exceed the expected length
                new_trait_data = new_trait_data[:RangesTable.NUM_RANGES + 1]

                trait.data[ext_var_index] = new_trait_data

        # Refresh UI if we're viewing the current trait
        if self._traits and self._showing_traits:
            self.select_trait(self._current_trait)
