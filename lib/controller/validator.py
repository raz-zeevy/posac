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
    def validate_range_string(value, col_index, row_values):
        if not value: return True
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
        except ValueError:
            return False
        return True