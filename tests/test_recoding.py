import numpy as np
import pytest

from lib.gui.tabs.internal_recoding_tab import RecodingOperation
from lib.posac.recoding import RecodingError, apply_recoding


@pytest.fixture
def sample_data():
    """Sample data for testing recoding operations"""
    return np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 1]])


def test_no_operations(sample_data):
    """Test that data is unchanged when no operations are provided"""
    result = apply_recoding(sample_data, [])
    assert np.array_equal(result, sample_data)
    assert result is not sample_data  # Should be a copy


def test_single_value_recode():
    """Test recoding a single value in one variable"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    operation.selected_variables = "1"  # First column
    operation.recoding_pairs = [("2", "9")]  # Recode 2 to 9

    result = apply_recoding(data, [operation])
    expected = np.array([[1, 2], [9, 2], [3, 2]])
    assert np.array_equal(result, expected)


def test_multiple_value_recode():
    """Test recoding multiple values in one variable"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    operation.selected_variables = "1"
    operation.recoding_pairs = [("1", "7"), ("2", "8"), ("3", "9")]

    result = apply_recoding(data, [operation])
    expected = np.array([[7, 2], [8, 2], [9, 2]])
    assert np.array_equal(result, expected)


def test_multiple_variables_recode():
    """Test recoding values in multiple variables"""
    data = np.array([[1, 1], [2, 2], [3, 3]])
    operation = RecodingOperation()
    operation.selected_variables = "1,2"
    operation.recoding_pairs = [("1", "9")]

    result = apply_recoding(data, [operation])
    expected = np.array([[9, 9], [2, 2], [3, 3]])
    assert np.array_equal(result, expected)


def test_inversion():
    """Test value inversion"""
    data = np.array([[1, 1], [2, 2], [3, 3]])
    operation = RecodingOperation()
    operation.selected_variables = "1"
    operation.invert = True

    result = apply_recoding(data, [operation])
    expected = np.array([[3, 1], [2, 2], [1, 3]])
    assert np.array_equal(result, expected)


def test_multiple_operations():
    """Test applying multiple operations in sequence"""
    data = np.array([[1, 1], [2, 2], [3, 3]])

    op1 = RecodingOperation()
    op1.selected_variables = "1"
    op1.recoding_pairs = [("1", "9")]

    op2 = RecodingOperation()
    op2.selected_variables = "2"
    op2.recoding_pairs = [("2", "8")]

    result = apply_recoding(data, [op1, op2])
    expected = np.array([[9, 1], [2, 8], [3, 3]])
    assert np.array_equal(result, expected)


def test_sequential_value_recode():
    """Test that recoding pairs are applied simultaneously, not sequentially"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    operation.selected_variables = "1"
    operation.recoding_pairs = [
        ("1", "2"),
        ("2", "3"),
    ]  # If applied sequentially, 1 would become 3

    result = apply_recoding(data, [operation])
    expected = np.array(
        [[2, 2], [3, 2], [3, 2]]
    )  # 1->2, 2->3, but original 1 stays as 2
    assert np.array_equal(result, expected)


def test_circular_recode():
    """Test circular recoding (e.g., 1->2, 2->3, 3->1)"""
    data = np.array([[1, 1], [2, 2], [3, 3]])
    operation = RecodingOperation()
    operation.selected_variables = "1"
    operation.recoding_pairs = [("1", "2"), ("2", "3"), ("3", "1")]

    result = apply_recoding(data, [operation])
    expected = np.array([[2, 1], [3, 2], [1, 3]])
    assert np.array_equal(result, expected)


def test_invalid_variable_index():
    """Test handling of invalid variable indices"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    operation.selected_variables = "3"  # Index out of bounds
    operation.recoding_pairs = [("1", "2")]

    with pytest.raises(RecodingError, match="Invalid variable index"):
        apply_recoding(data, [operation])


def test_invalid_recoding_values():
    """Test handling of non-integer recoding values"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    operation.selected_variables = "1"
    operation.recoding_pairs = [("1", "a")]  # Non-integer value

    with pytest.raises(RecodingError, match="Invalid recoding pair"):
        apply_recoding(data, [operation])


def test_empty_operation():
    """Test handling of empty recoding operation"""
    data = np.array([[1, 2], [2, 2], [3, 2]])
    operation = RecodingOperation()
    # No variables selected

    with pytest.raises(RecodingError, match="No variables selected"):
        apply_recoding(data, [operation])