import numpy as np
from typing import List, Optional, Dict


class DataLoadingException(Exception):
    """Custom exception for data loading errors."""
    pass


class VariableFormat:
    """Represents the format specification for a variable in the data file.
    
    Attributes:
        line (int): Line number where the variable is located (1-based)
        col (int): Column position where the variable starts (1-based)
        width (int): Width of the variable field
        label (str, optional): Label/name for the variable
    """
    
    def __init__(self, index: int, line: int, col: int, width: int, label: str = ""):
        self.index = int(index)
        self.line = int(line)
        self.col = int(col)
        self.width = int(width)
        self.label = str(label)
    
    def __repr__(self):
        return f"VariableFormat(index={self.index}, line={self.line}, col={self.col}, width={self.width}, label='{self.label}')"
    
    def to_dict(self) -> dict:
        """Convert to dictionary format for backward compatibility"""
        return {
            "index": self.index,
            "line": self.line,
            "col": self.col,
            "width": self.width,
            "label": self.label
        }


def validate_input(line_index: int, var: VariableFormat, lines: List[str]) -> None:
    """
    Validate input format for a specific variable in a file.

    Args:
        line_index: Index of the current line
        var: VariableFormat object containing line, col, and width information
        lines: List of lines from the file
    Raises:
        ValueError: If the input validation fails
    """
    if line_index + var.line - 1 >= len(lines):
        raise ValueError(f"Invalid line number {var.line + 1}. Exceeds the file's line count.")

    line_content = lines[line_index + var.line - 1]
    if var.col - 1 >= len(line_content):
        raise ValueError(f"Invalid column number {var.col} in line {line_index + var.line}.")

    if var.col - 1 + var.width > len(line_content):
        raise ValueError(
            f"Invalid width in line {line_index + var.line}, column {var.col}: "
            "Width exceeds the line length."
        )


def validate_format_spec(var_format: VariableFormat) -> None:
    """Validate a variable format specification before loading data.
    
    Args:
        var_format: The format specification to validate
        
    Raises:
        ValueError: If any format values are invalid
    """
    if var_format.line < 1:
        raise ValueError(f"Line number must be positive, got {var_format.line}")
    if var_format.col < 1:
        raise ValueError(f"Column number must be positive, got {var_format.col}")
    if var_format.width < 1:
        raise ValueError(f"Width must be positive, got {var_format.width}")


def load_supported_formats(path: str, extension: str, has_header: bool = False) -> np.ndarray:
    """
    Load supported formats like CSV, TSV, or Excel using NumPy.

    :param path: Path to the file
    :param extension: File extension (e.g., .csv, .tsv)
    :param has_header: Whether the file has a header
    :return: NumPy array with data
    """
    delimiter = ',' if extension == ".csv" else '\t'
    data = []

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        start_index = 1 if has_header else 0

        for line in lines[start_index:]:
            line_data = line.strip().split(delimiter)
            data.append(line_data)

    data_array = np.array(data, dtype=str)
    return data_array


def load_other_formats(
    path: str,
    lines_per_var: int,
    delimiter: Optional[str] = None,
    manual_format: Optional[List[VariableFormat]] = None,
    safe_mode: bool = False,
) -> np.ndarray:
    """Load custom-formatted files with fixed-width fields or custom delimiters."""
    data = []
    failed_rows = []

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

        if len(lines) % lines_per_var != 0:
            raise DataLoadingException(
                "Number of lines in the file is not a multiple of lines_per_var."
            )

        if manual_format and safe_mode:
            for var_format in manual_format:
                validate_format_spec(var_format)

        for i in range(0, len(lines), lines_per_var):
            if not lines[i].strip():
                continue

            try:
                row = []
                if manual_format:
                    for var in manual_format:
                        var = VariableFormat(**var) if isinstance(var, dict) else var
                        if safe_mode:
                            validate_input(i, var, lines)
                        # Get the line for this variable
                        line = lines[i + var.line - 1]
                        # Extract value and strip any whitespace
                        value = line[var.col - 1:var.col - 1 + var.width].strip()
                        row.append(int(value))
                else:
                    combined_row = "".join(lines[i:i + lines_per_var]).strip().replace("\n", "")
                    row = [int(val) for val in combined_row.split(delimiter)] if delimiter else [int(val) for val in combined_row]
            except ValueError as e:
                failed_rows.append(i + 1)
            except Exception as e:
                failed_rows.append(i + 1)
            else:
                data.append(row)

    if not any(data):
        raise DataLoadingException("Failed to load any rows from the file.")

    if failed_rows:
        
        (f"Warning: Failed to load rows at indices: {failed_rows}")

    return np.array(data, dtype=int)


def create_posac_data_file(data_matrix: np.ndarray, output_path: str) -> None:
    """Create the POSAC data file (POSACDATA.DAT) for the POSAC program.
    
    Args:
        data_matrix: 2D numpy array containing the data to write. Each element should be
            an integer that will be formatted as a 2-character wide field.
        output_path: Path where the output file will be written.
    
    Raises:
        ValueError: If data_matrix contains values that cannot be formatted properly
        IOError: If there are issues writing to the output file
    """
    def parse_item(item: int) -> str:
        if not isinstance(item, (int, np.integer)):
            raise ValueError(f"Value {item} is not an integer")
        if item < 0 or item > 99:
            raise ValueError(f"Value {item} cannot be formatted as 2 characters")
        return f"{item:2d}"

    try:
        with open(output_path, 'w', encoding="ascii") as file:
            for row in data_matrix:
                line = "".join(parse_item(item) for item in row)
                file.write(line + "\n")
    except IOError as e:
        raise IOError(f"Failed to write to {output_path}: {str(e)}")

if __name__ == '__main__':
    # Example usage
    file_path = "example_data.csv"  # Replace with your file path
    extension = ".csv"
    has_header = True

    try:
        data = load_supported_formats(file_path, extension, has_header)
        print("Data loaded successfully:\n", data)

        # Example of creating a Posac data file
        output_path = "POSACDATA.DAT"
        sample_data_matrix = np.random.randint(0, 10, (5, 5)).tolist()
        create_posac_data_file(sample_data_matrix, output_path)
        print(f"Posac data file created at {output_path}")

    except DataLoadingException as e:
        print(f"Error loading data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
