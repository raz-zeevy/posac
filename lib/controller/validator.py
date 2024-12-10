from lib.utils import *

class Validator():
    def __init__(self, gui):
        self.gui = gui

    def mode_dependent(func):
        def wrapper(*args, **kwargs):
            if IS_NO_VALIDATE():
                return
            else:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    @mode_dependent
    def validate_input_page(data_path, lines_num, is_manual_input,
                            additional_options):
        pass

    @staticmethod
    @mode_dependent
    def validate_integer(value, col_index, row_values):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    @mode_dependent
    def validate_line_number(value, col_index, row_values, max_lines):
        try:
            num = int(value)
            return 0 < num <= max_lines  # Line numbers should be positive and <= max_lines
        except ValueError:
            return False

    @staticmethod
    @mode_dependent
    def validate_field_width(value, col_index, row_values):
        try:
            num = int(value)
            return num in [1, 2]  # Field width must be either 1 or 2
        except ValueError:
            return False

    @staticmethod
    @mode_dependent
    def validate_start_col(value, col_index, row_values):
        try:
            num = int(value)
            return num >= 0  # Start column should be non-negative
        except ValueError:
            return False

    @staticmethod
    @mode_dependent
    def validate_valid_range(value, col_index, row_values):
        try:
            num = int(value)
            # Check if this is the high value
            if col_index == 6:  # Valid High column
                low_val = int(row_values[5]) if row_values[5] else float('-inf')
                return num >= low_val
            return True
        except ValueError:
            return False

    @staticmethod
    @mode_dependent
    def validate_range_string(value, col_index, row_values):
        if not value: 
            return True
            
        values = [item for item in row_values[1:] if item]
        if not row_values[col_index] and len(values) >= int(row_values[0]):
            return False
            
        # validate that the value is in the format of %d-%d
        if '-' not in value:
            return False
            
        try:
            from_, to_ = value.split('-')
            if not from_.isdigit() or not to_.isdigit():
                return False
                
            # Add validation for range order
            from_num = int(from_)
            to_num = int(to_)
            if from_num > to_num:
                return False
                
        except ValueError:
            return False
            
        return True