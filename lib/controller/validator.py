from fnmatch import fnmatch
from pathlib import Path
from lib.utils import *
import os
from lib.controller.controller_const import SUPPORTED_DATA_FILE_TYPES
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

    @staticmethod
    @mode_dependent
    def validate_for_run(controller):
        """Validates all required fields before running POSAC analysis"""
        errors = []
        
        # Data file validation
        data_file = controller.notebook.general_tab.get_data_file()
        if not data_file:
            errors.append("Data file is required")
        elif not os.path.exists(data_file):
            errors.append(f"Data file not found: {data_file}")
        
        # Check if the data file is a out of the supported data file types
        if Path(data_file).suffix.lower() not in SUPPORTED_DATA_FILE_TYPES:
            errors.append(f"Unsupported data file type: {data_file}\n please use one of the following types: {', '.join(SUPPORTED_DATA_FILE_TYPES)}")
        # Job name validation
        job_name = controller.notebook.general_tab.get_job_name()
        if not job_name or job_name.isspace():
            errors.append("Job name is required")
            
        # Internal variables validation
        int_vars = controller.notebook.internal_variables_tab.get_vars_num()
        if int_vars <= 0:
            errors.append("At least one internal variable must be configured")
            
        # Lines per case validation
        lines_per_case = controller.notebook.general_tab.get_lines_per_case()
        try:
            if int(lines_per_case) <= 0:
                errors.append("Lines per case must be a positive number")
        except (ValueError, TypeError):
            errors.append("Lines per case must be a valid number")

        # Output files validation
        pos_out = controller.notebook.output_files_tab.get_posac_out()
        ls1_out = controller.notebook.output_files_tab.get_lsa1_out()
        ls2_out = controller.notebook.output_files_tab.get_lsa2_out()
        
        if not all([pos_out, ls1_out, ls2_out]):
            errors.append("All output file paths must be specified")
            
        return errors    