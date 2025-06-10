import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np

from lib.utils import IS_PROD

logger = logging.getLogger(__name__)


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

    def __init__(
        self,
        index: int,
        line: int,
        col: int,
        width: int,
        label: str = "",
        valid_low: int = 0,
        valid_high: int = 9,
    ):
        self.index = int(index)
        self.line = int(line)
        self.col = int(col)
        self.width = int(width)
        self.label = str(label)
        self.valid_low = int(valid_low)
        self.valid_high = int(valid_high)

    def __repr__(self):
        return f"VariableFormat(index={self.index}, line={self.line}, col={self.col}, width={self.width}, label='{self.label}', valid_low={self.valid_low}, valid_high={self.valid_high})"

    def to_dict(self) -> dict:
        """Convert to dictionary format for backward compatibility"""
        return {
            "index": self.index,
            "line": self.line,
            "col": self.col,
            "width": self.width,
            "label": self.label,
            "valid_low": self.valid_low,
            "valid_high": self.valid_high,
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
        raise ValueError(
            f"Invalid line number {var.line + 1}. Exceeds the file's line count."
        )

    line_content = lines[line_index + var.line - 1]
    if var.col - 1 >= len(line_content):
        raise ValueError(
            f"Invalid column number {var.col} in line {line_index + var.line}."
        )

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


def filter_non_ascii(text):
    """
    Filter out non-ASCII characters from text, keeping only ASCII and spaces.
    And filters /t as well

    Args:
        text: The input text to filter

    Returns:
        A string containing only ASCII characters and spaces
    """
    text = text.replace("\t", "")
    # Keep only ASCII characters (codes 0-127) and spaces
    return re.sub(r"[^\x00-\x7F]", "", text)


def load_supported_formats(
    path: str, extension: str, has_header: bool = False
) -> np.ndarray:
    """
    Load supported formats like CSV, TSV, or Excel using NumPy.

    :param path: Path to the file
    :param extension: File extension (e.g., .csv, .tsv)
    :param has_header: Whether the file has a header
    :return: NumPy array with data
    """
    delimiter = "," if extension == ".csv" else "\t"
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
    appendix_fields: Tuple[int, int] = None,
) -> Tuple[np.ndarray, Union[np.ndarray, None]]:
    """
    Load custom-formatted files with fixed-width fields or custom delimiters.

    Args:
        path: Path to the data file
        lines_per_var: Number of lines per variable
        delimiter: Delimiter to use for the data
        manual_format: Manual format of the data
        safe_mode: Whether to validate the input format
        appendix_fields: Tuple of the appendix fields (start col, end col) or
            (variable_ix, -1) if it's a csv file

    Returns:
        np.ndarray: Data matrix
    """
    data = []
    failed_rows = []
    errors = set()
    warnings = set()
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [filter_non_ascii(line) for line in lines]
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
                        value = line[var.col - 1 : var.col - 1 + var.width].strip()
                        row.append(int(value))
                else:
                    combined_row = (
                        "".join(lines[i : i + lines_per_var]).strip().replace("\n", "")
                    )
                    row = (
                        [int(val) for val in combined_row.split(delimiter)]
                        if delimiter
                        else [int(val) for val in combined_row]
                    )
            except ValueError as e:
                failed_rows.append(i + 1)
                warnings.add(e)
            except Exception as e:
                failed_rows.append(i + 1)
                errors.add(e)
            else:
                data.append(row)

    if not any(data):
        if IS_PROD():
            raise DataLoadingException("Failed to load any rows from the file.")
        else:
            raise DataLoadingException(
                f"Failed to load any rows from the file. Errors: {errors}"
            )

    if failed_rows:
        logger.warning(f"Warning: Failed to load rows at indices: {failed_rows}")

    has_appendix_fields = appendix_fields != (0, 0)
    if has_appendix_fields:
        # get for each line the values from col appendix_fields[0] to appendix_fields[1] [single value per line]
        appendix_data = []
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            lines = [filter_non_ascii(line) for line in lines]
            for line in lines:
                appendix_data.append(
                    int(line[appendix_fields[0] - 1 : appendix_fields[1]].strip())
                )

    return np.array(data, dtype=int), (
        np.array(appendix_data, dtype=int) if has_appendix_fields else None
    )


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
        # return 2 characters, left padded with zeros
        return f"{item:2d}"

    try:
        with open(output_path, 'w', encoding="ascii") as file:
            for row in data_matrix:
                line = "".join(parse_item(item) for item in row)
                file.write(line + "\n")
    except IOError as e:
        raise IOError(f"Failed to write to {output_path}: {str(e)}")

def add_apendix_data(
    data_path: str,
    appendix_data: np.ndarray,
) -> None:
    """Add the appendix data to the data_matrix.

    Args:
        data_path: Path to the data file
        appendix_columns: Tuple of the appendix columns (start col, end col)
        appendix_variable: Index of the appendix variable
    """
    if not Path(data_path).exists():
        raise FileNotFoundError(f"File {data_path} does not exist")

    appendix_data = appendix_data.reshape(-1, 1)
    data = np.genfromtxt(data_path, delimiter=2, dtype=int)
    data = np.concatenate((data, appendix_data), axis=1)

    # save the data to the data_path
    np.savetxt(data_path, data, fmt="%2d", delimiter="")


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
