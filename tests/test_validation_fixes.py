"""
Tests for validation function fixes.

These tests focus on the specific validation issues we encountered and fixed:
1. Validator.validate_range_string expecting dict but receiving string
2. Parameter type mismatches between validation functions
3. Column data handling edge cases

These tests don't require GUI components and focus on the core logic.
"""

import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.controller.validator import Validator


@pytest.mark.unit
class TestValidatorRangeString:
    """Test the Validator.validate_range_string function that was causing crashes"""

    def test_validate_range_string_with_dict(self):
        """Test that validate_range_string handles dict input correctly"""
        # Test valid range string
        result = Validator.validate_range_string(
            {"2 from-to": "1-5"},
            1,
            {"ranges": "2", "1 from-to": "1-3", "2 from-to": "4-6"}
        )
        assert result is True

        # Test invalid range string
        result = Validator.validate_range_string(
            {"2 from-to": "invalid"},
            1,
            {"ranges": "2", "1 from-to": "1-3", "2 from-to": "4-6"}
        )
        assert result is False

        # Test empty dict
        result = Validator.validate_range_string(
            {},
            1,
            {"ranges": "2", "1 from-to": "1-3"}
        )
        assert result is True

    def test_validate_range_string_parameter_types(self):
        """Test that validate_range_string handles parameter types correctly"""
        # The function expects a dict and row_values as dict
        test_cases = [
            ({"col": "1-5"}, True, "Valid range"),
            ({"col": "5-1"}, False, "Invalid range (from > to)"),
            ({"col": "abc"}, False, "Invalid range (non-numeric)"),
            ({"col": "1-"}, False, "Invalid range (incomplete)"),
            ({"col": "1"}, False, "Invalid range (no dash)"),
            ({}, True, "Empty dict should be valid"),
        ]

        for value_dict, expected, description in test_cases:
            result = Validator.validate_range_string(
                value_dict,
                1,
                {"ranges": "2", "1 from-to": "1-3"}
            )
            assert result == expected, f"Failed: {description}"

    def test_range_order_validation(self):
        """Test that ranges with from > to are rejected"""
        # Valid range
        result = Validator.validate_range_string(
            {"test": "1-5"},
            1,
            {"ranges": "2", "1 from-to": "1-3", "2 from-to": ""}
        )
        assert result is True

        # Invalid range (from > to)
        result = Validator.validate_range_string(
            {"test": "5-1"},
            1,
            {"ranges": "2", "1 from-to": "1-3", "2 from-to": ""}
        )
        assert result is False

    def test_numeric_validation(self):
        """Test that non-numeric values are rejected"""
        test_cases = [
            ("1-5", True),
            ("10-20", True),
            ("a-5", False),
            ("1-b", False),
            ("a-b", False),
            ("1.5-2.5", False),  # Decimals should fail
        ]

        for value, expected in test_cases:
            result = Validator.validate_range_string(
                {"test": value},
                1,
                {"ranges": "2", "1 from-to": "1-3", "2 from-to": ""}
            )
            assert result == expected, f"Failed for value: {value}"

    def test_format_validation(self):
        """Test various format validations"""
        test_cases = [
            ("1-5", True, "Standard format"),
            ("1", False, "Missing dash"),
            ("-5", False, "Missing from value"),
            ("1-", False, "Missing to value"),
            # Note: Empty strings are handled by RangesTable, not passed to validator
            # ("", True, "Empty string should be valid"),  # This is handled at RangesTable level
            # ("  ", True, "Whitespace should be valid"),  # This is handled at RangesTable level
            ("1--5", False, "Double dash"),
            ("1-5-9", False, "Multiple dashes"),
        ]

        for value, expected, description in test_cases:
            result = Validator.validate_range_string(
                {"test": value},
                1,
                {"ranges": "2", "1 from-to": "1-3", "2 from-to": ""}
            )
            assert result == expected, f"Failed: {description} (value: '{value}')"


@pytest.mark.unit
class TestRangesTableValidationLogic:
    """Test the validation logic that was used in RangesTable"""

    def simulate_ranges_table_validate(self, value_dict, col_index, row_values_list):
        """Simulate the RangesTable.validate method logic"""
        if not value_dict:
            return True

        # Extract actual value from dict (this is what RangesTable does)
        actual_value = list(value_dict.values())[0]

        # Validate Ranges column (col_index 1)
        if col_index == 1:
            try:
                num = int(actual_value)
                return num <= 10  # MAX_RANGES = 10
            except ValueError:
                return False

        # For range columns (col_index > 1)
        if actual_value.strip():
            # Check if we're allowed to have a range in this position
            try:
                num_ranges = int(row_values_list[0]) if row_values_list[0].strip() else 0
                if col_index - 1 > num_ranges:
                    return False
            except (ValueError, IndexError):
                return False

            # Validate the range format using the Validator
            # Convert row_values_list to dict format expected by Validator
            row_values_dict = {}
            column_names = ["Ranges"] + [f"{i} from-to" for i in range(1, 11)]
            for i, val in enumerate(row_values_list):
                if i < len(column_names):
                    row_values_dict[column_names[i]] = val

            result = Validator.validate_range_string(value_dict, col_index - 1, row_values_dict)
            return result

        return True

    def test_ranges_column_validation(self):
        """Test validation of the Ranges column"""
        # Valid ranges
        assert self.simulate_ranges_table_validate({"Ranges": "3"}, 1, ["3", "1-5", "6-9"]) is True
        assert self.simulate_ranges_table_validate({"Ranges": "1"}, 1, ["1", "1-5"]) is True
        assert self.simulate_ranges_table_validate({"Ranges": "10"}, 1, ["10"]) is True

        # Invalid ranges
        assert self.simulate_ranges_table_validate({"Ranges": "abc"}, 1, ["abc"]) is False
        assert self.simulate_ranges_table_validate({"Ranges": "15"}, 1, ["15"]) is False
        assert self.simulate_ranges_table_validate({"Ranges": "0"}, 1, ["0"]) is True

    def test_range_string_validation(self):
        """Test validation of range string columns"""
        # Valid range strings
        assert self.simulate_ranges_table_validate(
            {"2 from-to": "1-5"},
            3,
            ["3", "1-3", "4-6", "", "", "", "", "", "", "", ""]
        ) is True

        # Invalid range strings
        assert self.simulate_ranges_table_validate(
            {"2 from-to": "invalid"},
            3,
            ["3", "1-3", "4-6", "", "", "", "", "", "", "", ""]
        ) is False

        assert self.simulate_ranges_table_validate(
            {"2 from-to": "5-1"},
            3,
            ["3", "1-3", "4-6", "", "", "", "", "", "", "", ""]
        ) is False

    def test_range_position_validation(self):
        """Test validation of range position vs number of ranges"""
        # Try to set range #3 when only 2 ranges are specified
        assert self.simulate_ranges_table_validate(
            {"3 from-to": "1-5"},
            4,  # Column index for "3 from-to"
            ["2", "1-3", "4-6", "", "", "", "", "", "", "", ""]  # Only 2 ranges specified
        ) is False

        # Valid case: set range #2 when 3 ranges are specified
        assert self.simulate_ranges_table_validate(
            {"2 from-to": "1-5"},
            3,  # Column index for "2 from-to"
            ["3", "1-3", "4-6", "", "", "", "", "", "", "", ""]  # 3 ranges specified
        ) is True

    def test_empty_values(self):
        """Test handling of empty values"""
        # Empty dict should return True
        assert self.simulate_ranges_table_validate({}, 1, ["2", "1-5"]) is True

        # Dict with empty string value should return True (handled by RangesTable logic)
        assert self.simulate_ranges_table_validate({"2 from-to": ""}, 3, ["2", "1-5"]) is True

        # Dict with whitespace should return True (handled by RangesTable logic)
        assert self.simulate_ranges_table_validate({"2 from-to": "   "}, 3, ["2", "1-5"]) is True


@pytest.mark.unit
class TestEmptyStringHandling:
    """Test that empty strings are handled correctly at the RangesTable level"""

    def test_empty_string_logic(self):
        """Test the empty string logic from RangesTable"""
        # This simulates the logic from RangesTable.validate

        def check_empty_value(value_dict):
            if not value_dict:
                return True
            actual_value = list(value_dict.values())[0]
            # RangesTable only calls validator if actual_value.strip() is not empty
            if actual_value.strip():
                # Would call validator here in real code
                return "call_validator"
            else:
                # Empty or whitespace values are considered valid without validation
                return True

        # Test cases
        assert check_empty_value({}) is True
        assert check_empty_value({"test": ""}) is True
        assert check_empty_value({"test": "   "}) is True
        assert check_empty_value({"test": "\t\n"}) is True
        assert check_empty_value({"test": "1-5"}) == "call_validator"


@pytest.mark.unit
class TestParameterTypeConsistency:
    """Test that all validation functions handle parameter types consistently"""

    def test_dict_parameter_extraction(self):
        """Test that dict parameters are extracted correctly"""
        # Test the pattern used in our fixes
        test_dict = {"column_name": "test_value"}

        # This is the pattern that was causing issues
        extracted_value = list(test_dict.values())[0]
        assert extracted_value == "test_value"

        # Test with empty dict
        empty_dict = {}
        if empty_dict:  # This check prevents the error
            extracted = list(empty_dict.values())[0]
        else:
            extracted = None
        assert extracted is None

    def test_row_values_dict_format(self):
        """Test that row values are handled in dict format correctly"""
        # Test the format expected by Validator functions
        row_values = {
            "Ranges": "2",
            "1 from-to": "1-3",
            "2 from-to": "4-6"
        }

        # Test accessing values by key
        assert row_values["Ranges"] == "2"
        assert row_values["1 from-to"] == "1-3"

        # Test handling missing keys
        missing_value = row_values.get("3 from-to", "")
        assert missing_value == ""


@pytest.mark.unit
class TestRegressionPrevention:
    """Tests specifically designed to catch regressions of the bugs we fixed"""

    def test_no_attributeerror_on_dict_access(self):
        """Ensure we don't get AttributeError when accessing dict values"""
        # Test the exact scenario that caused AttributeError: 'str' object has no attribute 'values'

        # This should work without error
        result = Validator.validate_range_string(
            {"test": "1-5"},
            1,
            {"ranges": "2", "1 from-to": "1-3"}
        )
        assert isinstance(result, bool)

        # Test with empty dict
        result = Validator.validate_range_string(
            {},
            1,
            {"ranges": "2"}
        )
        assert result is True

    def test_parameter_type_consistency(self):
        """Test that all validation calls use consistent parameter types"""
        # Test data that matches the structure we expect
        test_value = {"2 from-to": "1-5"}
        col_index = 1
        row_values = {"ranges": "2", "1 from-to": "1-3", "2 from-to": ""}

        # This call should not raise any TypeError or AttributeError
        try:
            result = Validator.validate_range_string(test_value, col_index, row_values)
            assert isinstance(result, bool)
        except Exception as e:
            pytest.fail(f"Validation should handle consistent parameter types: {e}")

    def test_edge_case_values(self):
        """Test edge cases that could cause validation to crash"""
        edge_cases = [
            # Note: Empty strings are handled by RangesTable, not passed to validator
            # ({"test": ""}, True, "Empty string"),
            # ({"test": "   "}, True, "Whitespace"),
            ({"test": "1-1"}, True, "Same from and to"),
            ({"test": "0-0"}, True, "Zero range"),
            ({"test": "999-999"}, True, "Large numbers"),
        ]

        for value_dict, expected, description in edge_cases:
            try:
                result = Validator.validate_range_string(
                    value_dict,
                    1,
                    {"ranges": "1", "1 from-to": "1-3", "2 from-to": ""}
                )
                assert result == expected, f"Failed: {description}"
            except Exception as e:
                pytest.fail(f"Validation crashed on {description}: {e}")


@pytest.mark.unit
class TestIntegrationWithOriginalBugs:
    """Test scenarios that recreate the original bugs we fixed"""

    def test_keyerror_scenario_simulation(self):
        """Simulate the KeyError scenario without GUI components"""
        # This simulates what happened in the EditableTreeView

        # Simulate column names (what was in _col_names)
        col_names = ["Ranges"] + [f"{i} from-to" for i in range(1, 11)]

        # Simulate partial data (what was returned by self.set())
        partial_data = {"Ranges": "2", "1 from-to": "1-5"}

        # This was causing KeyError when trying to access missing columns
        # Our fix: handle missing columns gracefully
        columns_values = {}
        for col in col_names:
            if col in partial_data:
                columns_values[col] = partial_data[col]
            else:
                columns_values[col] = ""  # Default for missing columns

        # Verify all columns are present now
        assert len(columns_values) == len(col_names)
        assert columns_values["Ranges"] == "2"
        assert columns_values["1 from-to"] == "1-5"
        assert columns_values["2 from-to"] == ""  # Missing column gets default
        assert columns_values["10 from-to"] == ""  # Missing column gets default

    def test_string_vs_dict_scenario_simulation(self):
        """Simulate the string vs dict parameter scenario"""
        # This simulates what happened in RangesTable.validate

        # Original (buggy) approach that was passing string to Validator
        def buggy_approach(value_dict):
            if not value_dict:
                return True
            value = list(value_dict.values())[0]  # Extract string
            # This was the bug: passing string instead of dict to Validator
            # return Validator.validate_range_string(value, 1, ["2", "1-3"])  # BUG!

        # Fixed approach that passes dict to Validator
        def fixed_approach(value_dict):
            if not value_dict:
                return True
            # Pass the original dict to Validator (our fix)
            return Validator.validate_range_string(value_dict, 1, {"ranges": "2", "1 from-to": "1-3"})

        test_input = {"2 from-to": "1-5"}

        # The fixed approach should work
        result = fixed_approach(test_input)
        assert isinstance(result, bool)

        # Verify that the validator function gets the expected dict format
        result2 = Validator.validate_range_string(
            test_input,
            1,
            {"ranges": "2", "1 from-to": "1-3"}
        )
        assert isinstance(result2, bool)