from typing import List

import numpy as np

from lib.gui.tabs.internal_recoding_tab import RecodingOperation


class RecodingError(Exception):
    """Custom exception for recoding errors"""

    pass


def validate_recoding_operation(data: np.ndarray, operation: RecodingOperation) -> None:
    """Validate a recoding operation before applying it.

    Args:
        data: Input data array
        operation: Recoding operation to validate

    Raises:
        RecodingError: If operation is invalid
        ValueError: If input parameters are invalid
    """
    if not operation.selected_variables:
        raise RecodingError("No variables selected for recoding")

    try:
        # Validate variable indices
        for idx in operation.selected_variables_parsed:
            var_idx = int(idx) - 1
            if var_idx < 0 or var_idx >= data.shape[1]:
                raise RecodingError(f"Invalid variable index: {idx}")

        # Validate recoding pairs
        try:
            for old, new in operation.recoding_pairs_parsed:
                if new > 99 or new < 0:
                    raise RecodingError(
                        f"Invalid recoding pair: {old}->{new}. New value must be between 0 and 99."
                    )
        except ValueError:
            raise RecodingError(
                f"Invalid recoding pair: {old}->{new}. Values must be integers."
            )

    except ValueError as e:
        raise RecodingError(f"Invalid recoding specification: {str(e)}")


def apply_recoding_operation(
    data: np.ndarray, operation: RecodingOperation
) -> np.ndarray:
    """Apply a single recoding operation to data.

    Args:
        data: 2D numpy array where each row is a case and each column is a variable
        operation: Single recoding operation to apply

    Returns:
        Data with recoding operation applied

    Raises:
        RecodingError: If recoding operation is invalid
    """
    validate_recoding_operation(data, operation)

    try:
        recoded_data = data.copy()

        # Convert variable indices to 0-based indexing
        var_indices = [int(idx) - 1 for idx in operation.selected_variables_parsed]

        # Create mapping dictionary from recoding pairs
        value_map = {}
        for old_value_set, new_val in operation.recoding_pairs_parsed:
            for old_val in old_value_set:
                value_map[old_val] = new_val

        # Apply recoding to selected variables
        for var_idx in var_indices:
            # Create a copy of the column for simultaneous recoding
            new_column = recoded_data[:, var_idx].copy()

            # Apply value mapping simultaneously
            for old_val, new_val in value_map.items():
                mask = recoded_data[:, var_idx] == old_val
                new_column[mask] = new_val

            # Update column with all recodings applied
            recoded_data[:, var_idx] = new_column

            # Apply inversion if needed
            if operation.invert:
                max_val = np.max(recoded_data[:, var_idx])
                recoded_data[:, var_idx] = max_val - recoded_data[:, var_idx] + 1

        return recoded_data

    except Exception as e:
        raise RecodingError(f"Failed to apply recoding: {str(e)}")


def apply_recoding(data: np.ndarray, operations: List[RecodingOperation]) -> np.ndarray:
    """Apply multiple recoding operations to data.

    Args:
        data: Original data as numpy array
        operations: List of recoding operations to apply

    Returns:
        Recoded data array
    """
    if not operations:
        return data.copy()

    recoded_data = data.copy()
    for operation in operations:
        recoded_data = apply_recoding_operation(recoded_data, operation)

    return recoded_data
