from lib.controller.validator import Validator
from lib.gui.components.form import TableView
from tkinter import messagebox
from lib.utils import rreal_size

class VariablesTable(TableView):
    INDEX_COL_NAME = 'Var. No.'
    COLS = {
        'sel_var': 'Sel. Var.',
        'line_number': 'Line No.',
        'field_width': 'Field Width',
        'start_col': 'Start Col',
        'label': 'Label',
        'valid_low': 'Valid Low',
        'valid_high': 'Valid High',
    }
    DEFAULT_VALUES = ['1', '1', '0', 'v1', '0', '9']  # Common default values

    def __init__(self, notebook, master, check_box_callback=None,
                 new_default_label="var", **kwargs):
        """
        Args:
            master: Parent widget
            check_box_callback: Optional callback for checkbox changes (used by internal variables)
            **kwargs: Additional arguments for TableView
        """
        self.notebook = notebook
        self.new_default_label = new_default_label
        super().__init__(
            master=master,
            columns=self.COLS.values(),
            index_col_name=self.INDEX_COL_NAME,
            add_check_box=True,
            disable_sub_menu=True,
            check_box_callback=check_box_callback,
            validation_callback=self.validate,
            **kwargs
        )
        self._setup_columns() 

    def _setup_columns(self):
        """Configure column properties"""
        self.column('Label', stretch=True)
        for col in ['Sel. Var.', 'Line No.', 'Field Width', 'Start Col',
                   'Valid Low', 'Valid High', 'Label']:
            self.heading(col, text=col, anchor="w")
            self.column(col, width=rreal_size(60), anchor='w')
        self.column('Field Width', width=rreal_size(80), anchor='w')

    def validate(self, value, col_index, row_values):
        """Validates table cell input"""
        if not value:
            return True

        max_lines = self.notebook.get_lines_per_case()
        error_messages = {
            2: f"Line number must be between 1 and {max_lines}",
            3: "Field width must be either 1 or 2",
            4: "Start column must be a non-negative integer",
            6: "Valid low must be an integer",
            7: "Valid high must be an integer and greater than valid low"
        }

        validators = {
            2: lambda v, c, r: Validator.validate_line_number(v, c, r, max_lines),
            3: Validator.validate_field_width,
            4: Validator.validate_start_col,
            6: Validator.validate_valid_range,
            7: Validator.validate_valid_range
        }

        if col_index in validators:
            if not validators[col_index](value, col_index, row_values):
                messagebox.showwarning("Invalid Input", error_messages[col_index])
                return False
        
        return True

    def add_variable(self, values_: list = [], check=True):
        """Add a new variable to the table"""
        var_prefix = self.new_default_label
        def add_from_default():
            def_start_col, def_line_num, def_field_width = 1, 1, 1
            def_value = [def_line_num, def_field_width, def_start_col,
                         f'{var_prefix}{len(self) + 1}', '0', '9']
            values = def_value.copy()
            if len(values) < len(def_value):
                values.extend(def_value[len(values):])
            self.add_row(values, check=check)

        def add_row_from_previous():
            """add row considering the line, start col and width of preivous row"""
            prev_row = self.get_variable(-1)
            line_num = prev_row[1]  # Line number
            width = int(prev_row[2])  # Field width
            start_col = int(prev_row[3])  # Start column
            next_start = start_col + width
            values = [line_num, str(width), str(next_start), 
                     f'{var_prefix}{len(self) + 1}', '0', '9']
            self.add_row(values, check=check)

        values = values_.copy()
        if not values_:
            if len(self) == 0:
                add_from_default()
            else:
                add_row_from_previous()
        elif len(values) < 7:
            # extend using default values
            values.extend(self.DEFAULT_VALUES[len(values):])
            self.add_row(values, check=check)

    def get_variable(self, i: int):
        """Get values of a specific variable row"""
        return list(self.get_row(i).values())
    
    def remove_variable(self):
        """Remove the last variable from the table"""
        self.remove_row(-1)

    def clear_variables(self):
        """Clear all variables from the table"""
        self.clear_rows()

    def hide_low_high(self):
        """Hide Valid Low/High columns"""
        self.hide_column('Valid Low')
        self.hide_column('Valid High')
        for col in ['Label']:
            self.column(col, width=rreal_size(400))
            self.column(col, stretch=True)

    def show_low_high(self):
        """Show Valid Low/High columns"""
        self.show_column('Valid Low')
        self.show_column('Valid High')
        for col in ['Label']:
            self.column(col, stretch=False)
            self.column(col, width=rreal_size(200))

    def get_all_variables(self):
        """Get all variables without indices"""
        return [list(row)[1:] for row in self.get_all_values()]

    def get_all_variables_values(self):
        """Get all variables with indices"""
        return self.get_all_values()

    def get_selected_variables(self):
        """Get selected variables without indices"""
        return [list(row)[1:] for row in self.get_check_rows_values()]

    def get_selected_variables_nums(self):
        """Get indices of selected variables"""
        return self.get_check_rows_indices() 

    def set_variable(self, i: int, values: list):
        """Set values for a specific variable row"""
        self.set_row(i, values)

    def set_variables(self, vars):
        """Set all variables at once"""
        self.clear_rows()
        for var in vars:
            self.add_variable(var, check=True)