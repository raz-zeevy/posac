from lib.controller.validator import Validator
from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.form import TableView
from lib.utils import rreal_size
from tkinter import messagebox

class RangesTable(TableView):
    INDEX_COL_NAME = 'Ext. Var. No.'
    COLS = {
        'ranges': 'Ranges',
    }
    FROM_TO = 'from-to'
    DEFAULT_VALUE = ['1', '1-9']
    NUM_RANGES = 10

    def __init__(self, master, on_value_changed=None, **kw):
        self.master = master
        self.on_value_changed = on_value_changed
        self.custom_validation = None  # Can be set externally for additional validation
        self._current_editing_item = None  # Track which item is being edited
        columns = list(self.COLS.values()) + [f"{i} {self.FROM_TO}" for i in
                                              range(1, self.NUM_RANGES + 1)]
        super().__init__(master, columns=columns, disable_sub_menu=True,
                         index_col_name=self.INDEX_COL_NAME,
                         add_check_box=False,
                         validation_callback=self.validate,
                         **kw)
        for col in columns:
            self.heading(col, text=col, anchor="w")
            self.column(col, width=rreal_size(60), anchor='w')
            self.column(col, stretch=False)
        self.heading('Ranges', anchor='center')

    @staticmethod
    def get_new_row(values_=None):
        # Total columns: 1 for "Ranges" (num_ranges) + NUM_RANGES for actual ranges
        # So we need NUM_RANGES + 1 total values
        if not values_:
            # Default: ['1', '1-9', '', '', '', '', '', '', '', '', '']
            # That's 1 + 10 = 11 values total
            values = RangesTable.DEFAULT_VALUE.copy()
            # DEFAULT_VALUE has 2 elements, need to add 9 more to reach 11 total
            while len(values) < (RangesTable.NUM_RANGES + 1):
                values.append('')
        else:
            values = [str(len(values_))] + values_.copy()
            # values_ already contains [num_ranges, range1, range2, ...]
            # Just pad with empty strings to fill remaining slots
            if len(values) <= (RangesTable.NUM_RANGES + 1):
                while len(values) < (RangesTable.NUM_RANGES + 1):
                    values.append('')
            else:
                raise ValueError(f"Too many ranges for variables")
        return values

    def set_default(self):
        for i in range(len(self)):
            self.set_range(i, self.DEFAULT_VALUE)

    def set_range(self, i: int, values_: list):
        values = self.get_new_row(values_)
        self.set_row(i, values)

    def get_ranges_for_variable(self, var_index: int) -> list:
        """
        Get the range values for a specific external variable.

        :param var_index: Index of the variable (0-based)
        :return: List of range strings (e.g., ['1-2', '4-6'])
        """
        if var_index >= len(self):
            return []

        # Get the item ID for this row index
        children = self.get_children()
        if var_index >= len(children):
            return []

        item_id = children[var_index]
        # Use parent's set() to avoid triggering our override
        # This returns a dict of column_name: value
        row_values = super(RangesTable, self).set(item_id)
        # Skip first column (number of ranges) and collect range strings
        ranges = [r for r in list(row_values.values())[1:] if r and r.strip()]
        return ranges

    def set_ranges_for_variable(self, var_index: int, ranges: list):
        """
        Set the range values for a specific external variable.

        :param var_index: Index of the variable (0-based)
        :param ranges: List of range strings (e.g., ['1-2', '4-6'])
        """
        if var_index >= len(self):
            return

        # Build the full row data
        num_ranges = str(len(ranges))
        row_data = [num_ranges] + ranges
        # Pad with empty strings
        while len(row_data) < self.NUM_RANGES + 1:
            row_data.append('')

        self.set_range(var_index, row_data)

    def _enter_edit_mode(self, item_id, column_id):
        """Override to track which item is being edited."""
        self._current_editing_item = item_id
        super()._enter_edit_mode(item_id, column_id)

    def set(self, item, column=None, value=None):
        """
        Override set method to trigger callback when values change.

        Note: Treeview's set() has two modes:
        - set(item) with no column/value: Returns dict of all column values (read mode)
        - set(item, column, value): Sets a specific cell value (write mode)
        """
        # Call parent's set method first
        result = super().set(item, column, value)

        # Track if we should trigger callback (only once per edit session)
        should_trigger_callback = False

        # If the "Ranges" column was changed, truncate excessive ranges
        if column is not None and value is not None and value != '':
            col_name = self._display_columns[int(column[1:]) - 1] if column.startswith('#') else column
            if col_name == self.COLS['ranges']:
                try:
                    num_ranges = int(value)
                    # Clear any ranges beyond the specified number (without triggering callbacks)
                    for i in range(num_ranges + 1, self.NUM_RANGES + 1):
                        range_col = f"{i} {self.FROM_TO}"
                        super().set(item, range_col, '')
                    # Now trigger callback once after all clearing is done
                    should_trigger_callback = True
                except (ValueError, AttributeError):
                    pass

        # Only trigger callback when WRITING a non-empty value
        # Don't trigger for clearing operations (value == '') to avoid cascading updates
        if self.on_value_changed and column is not None and value is not None and value != '' and not should_trigger_callback:
            should_trigger_callback = True

        # Trigger callback once with the final state
        if should_trigger_callback and self.on_value_changed:
            try:
                children = self.get_children()
                row_index = children.index(item)
                # Get the updated ranges for this variable
                new_ranges = self.get_ranges_for_variable(row_index)
                # Call the callback with row index and new ranges
                self.on_value_changed(row_index, new_ranges)
            except (ValueError, IndexError, AttributeError):
                pass  # Ignore if we can't determine the row

        return result

    def validate(self, value: dict, col_index: int, row_values: list):
        """
        Validates table cell input with specific error messages for each case
        :param value dict: The value being entered
        :param col_index: 1 -> n
        :param row_values: Current row values
        :return: bool
        """
        # If custom validation is set, use it instead
        if self.custom_validation:
            return self.custom_validation(value, col_index, row_values)

        # Otherwise, use default validation
        if not value:
            return True

        # Extract the actual value from the dict
        actual_value = list(value.values())[0]

        # Validate Ranges column (col_index 1)
        if col_index == 1:
            try:
                num = int(actual_value)
            except ValueError:
                messagebox.showwarning(
                    "Invalid Input",
                    "Please enter a valid number for ranges"
                )
                return False

            if num > self.NUM_RANGES:
                messagebox.showwarning(
                    "Invalid Range Count",
                    f"Number of ranges cannot exceed {self.NUM_RANGES}"
                )
                return False

            return True

        # For range columns (col_index > 1)
        if actual_value.strip():
            # First check if we're allowed to have a range in this position
            num_ranges = int(row_values[self.COLS['ranges']]) if row_values[self.COLS['ranges']].strip() else 0
            if col_index - 1 > num_ranges:
                messagebox.showwarning(
                    "Invalid Range Position",
                    f"Cannot add range #{col_index-1} when only {num_ranges} ranges are specified.\n"
                    f"Please increase the number of ranges first."
                )
                return False

            # Then validate the range format - pass the original dict to maintain consistency
            res = Validator.validate_range_string(value, col_index - 1, row_values)
            if not res:
                range_num = col_index - 1
                messagebox.showwarning(
                    "Invalid Range Format",
                    f"Invalid format for range #{range_num}\n"
                    "Range must be in format: number-number\n"
                    "Examples: 1-5, 2-9, etc.\n"
                    "First number must be less than or equal to second number."
                )
                return False

        return True
