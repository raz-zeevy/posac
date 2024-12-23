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

    def __init__(self, master, **kw):
        self.master = master
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
        if not values_:
            values = RangesTable.DEFAULT_VALUE.copy()
            [values.append('') for _ in range(RangesTable.NUM_RANGES)]
        else:
            values = values_.copy()
            if len(values) <= (RangesTable.NUM_RANGES + 1):
                values = [len(values)] + values +  [''] * ((RangesTable.NUM_RANGES) - len(values))
            else:
                raise ValueError(f"Too many ranges for variables")
        return values

    def set_default(self):
        for i in range(len(self)):
            self.set_range(i, self.DEFAULT_VALUE)

    def set_range(self, i: int, values_: list):
        values = self.get_new_row(values_)
        self.set_row(i, values)

    def validate(self, value, col_index, row_values):
        """
        Validates table cell input with specific error messages for each case
        :param value: The value being entered
        :param col_index: 1 -> n
        :param row_values: Current row values
        :return: bool
        """
        if not value: 
            return True

        # Validate Ranges column (col_index 1)
        if col_index == 1:
            try:
                num = int(value)
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
        if value.strip():
            # First check if we're allowed to have a range in this position
            num_ranges = int(row_values[0]) if row_values[0].strip() else 0
            if col_index - 1 > num_ranges:
                messagebox.showwarning(
                    "Invalid Range Position",
                    f"Cannot add range #{col_index-1} when only {num_ranges} ranges are specified.\n"
                    f"Please increase the number of ranges first."
                )
                return False

            # Then validate the range format
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
