import pytest
from lib.posac.data_loader import VariableFormat, load_other_formats, load_supported_formats, validate_format_spec, create_posac_data_file
import numpy as np
import os

# Test data paths - Update paths to match actual file locations
JNEEDS_PATH = os.path.join("tests", "data_files", "jneedsTR.datt")  # Fixed path
KEDDIR_PATH = os.path.join("tests", "data_files", "simple_test", "KEDDIR2.DAT")

class TestVariableFormat:
    def test_variable_format_creation(self):
        """Test VariableFormat object initialization and attribute assignment
        
        Verifies:
        - All attributes are correctly assigned during initialization
        - Both required and optional parameters work
        """
        var_format = VariableFormat(index=1, line=1, col=1, width=2, label="test_var")
        assert var_format.index == 1, "Index should be 1"
        assert var_format.line == 1, "Line number should be 1"
        assert var_format.col == 1, "Column number should be 1"
        assert var_format.width == 2, "Width should be 2"
        assert var_format.label == "test_var", "Label should match input"

    def test_to_dict_conversion(self):
        """Test conversion of VariableFormat object to dictionary
        
        Verifies:
        - All required attributes are included in dictionary
        - Dictionary format matches expected structure for backward compatibility
        """
        var_format = VariableFormat(index=1, line=2, col=3, width=1)
        expected_dict = {
            "index": 1,
            "line": 2,
            "col": 3,
            "width": 1,
            "label": ""
        }
        assert var_format.to_dict() == expected_dict, "Dictionary conversion should match expected format"

class TestDataLoader:
    @pytest.fixture
    def simple_format(self):
        """Fixture providing a simple variable format for single-line data
        
        Returns:
        - List of VariableFormat objects for testing single-character columns
        """
        return [
            VariableFormat(index=1, line=1, col=1, width=1),
            VariableFormat(index=2, line=1, col=2, width=1),
            VariableFormat(index=3, line=1, col=3, width=1)
        ]

    def test_load_single_line_data(self, simple_format):
        """Test loading data where each case is on a single line"""
        test_data = "123\n456\n789\n"
        with open("test_temp.dat", "w") as f:
            f.write(test_data)
        
        try:
            result = load_other_formats(
                "test_temp.dat",
                lines_per_var=1,
                manual_format=simple_format
            )
            expected = np.array([[1, 2, 3], 
                               [4, 5, 6],
                               [7, 8, 9]], dtype=int)
            assert np.array_equal(result, expected), "Loaded data should match input format"
        finally:
            os.remove("test_temp.dat")

    def test_load_multi_line_data(self):
        """Test loading data where each case spans multiple lines"""
        test_data = "123\n45 \n678\n90 \n"  # Two cases, each using 2 lines
        format_spec = [
            VariableFormat(index=1, line=1, col=1, width=2),  # First two chars of first line
            VariableFormat(index=2, line=2, col=1, width=2),  # First two chars of second line
            VariableFormat(index=3, line=1, col=3, width=1)   # Third char of first line
        ]
        
        with open("test_temp.dat", "w") as f:
            f.write(test_data)
        
        try:
            result = load_other_formats(
                "test_temp.dat",
                lines_per_var=2,
                manual_format=format_spec
            )
            expected = np.array([[12, 45, 3], 
                               [67, 90, 8]], dtype=int)
            assert np.array_equal(result, expected), "Multi-line data should be correctly assembled"
        finally:
            os.remove("test_temp.dat")

    def test_real_data_jneeds(self):
        """Test loading real JNEEDS data file"""
        format_spec = [
            VariableFormat(index=1, line=1, col=1, width=1),
            VariableFormat(index=2, line=1, col=2, width=1)
        ]
        
        result = load_other_formats(
            JNEEDS_PATH,
            lines_per_var=1,
            manual_format=format_spec
        )
        
        # Verify data properties
        assert isinstance(result, np.ndarray), "Result should be numpy array"
        assert result.shape[1] == 2, "Should have 2 variables"
        assert all(val in [1, 2] for val in result.flatten()), "Values should be 1 or 2"

    def test_format_validation(self):
        """Test validation of format specifications
        
        Verifies:
            - Invalid line numbers are caught
            - Invalid column numbers are caught
            - Invalid widths are caught
        """
        test_cases = [
            (0, 1, 1, "Line number must be positive"),
            (1, 0, 1, "Column number must be positive"),
            (1, 1, 0, "Width must be positive")
        ]
        
        for line, col, width, expected_msg in test_cases:
            var_format = VariableFormat(index=1, line=line, col=col, width=width)
            with pytest.raises(ValueError, match=expected_msg):
                validate_format_spec(var_format)

    def test_load_csv_data(self):
        """Test loading CSV formatted data file
        
        Verifies:
        - Correct loading of CSV with header
        - Proper handling of numeric values
        - Correct array shape and content
        - Proper column separation
        """
        result = load_supported_formats(
            os.path.join("tests", "data_files", "data.csv"),
            extension=".csv",
            has_header=True
        )
        
        # Test data structure
        assert isinstance(result, np.ndarray), "Result should be numpy array"
        assert result.shape[1] == 22, "Should have 22 variables (columns)"
        assert result.shape[0] == 54, "Should have 50 cases (rows)"
        
        # Test specific known values from first row
        first_row = result[0]
        expected_first_row = ['5','4','3','1','2','4','5','3','2','1','3','3','5','5','5','4','1','1','3','4','1','1']
        assert np.array_equal(first_row, expected_first_row), "First row values should match expected"
        
        # Test value ranges (all values should be 1-5)
        all_values = result.flatten()
        assert all(val in ['1','2','3','4','5'] for val in all_values), "All values should be between 1 and 5"

    def test_csv_header_handling(self):
        """Test proper handling of CSV headers
        
        Verifies:
        - Data is loaded correctly with header skipped
        - First row of data is not header content
        """
        # Load with and without header
        with_header = load_supported_formats(
            os.path.join("tests", "data_files", "data.csv"),
            extension=".csv",
            has_header=True
        )
        
        without_header = load_supported_formats(
            os.path.join("tests", "data_files", "data.csv"),
            extension=".csv",
            has_header=False
        )
        
        # With header should have one less row
        assert len(with_header) == len(without_header) - 1, "Header option should affect number of rows"
        
        # First row with header=True should be actual data, not header text
        first_row = with_header[0]
        assert all(val.isdigit() for val in first_row), "First row should contain only numeric values"

    def test_csv_error_handling(self):
        """Test error handling for CSV loading
        
        Verifies:
        - Proper handling of missing files
        - Proper handling of invalid paths
        """
        with pytest.raises(FileNotFoundError):
            load_supported_formats(
                "nonexistent.csv",
                extension=".csv",
                has_header=True
            )

    def test_create_posac_data_file(self):
        """Test creating POSAC data file with valid input
        
        Verifies:
        - Correct formatting of integers as 2-character fields
        - Proper file creation and content
        - Correct handling of numpy arrays
        """
        test_data = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        output_path = "test_posac.dat"
        
        try:
            create_posac_data_file(test_data, output_path)
            
            # Read and verify file contents
            with open(output_path, 'r') as f:
                lines = f.readlines()
            
            # Verify correct formatting
            assert len(lines) == 3, "Should have 3 rows"
            assert lines[0].strip() == "1 2 3", "First row should be properly formatted"
            assert lines[1].strip() == "4 5 6", "Second row should be properly formatted"
            assert lines[2].strip() == "7 8 9", "Third row should be properly formatted"
            
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_create_posac_data_file_invalid_values(self):
        """Test error handling for invalid input values
        
        Verifies:
        - Proper handling of non-integer values
        - Proper handling of out-of-range values
        - Appropriate error messages
        """
        test_cases = [
            (np.array([[1.5, 2, 3]]), "Value 1.5 is not an integer"),
            (np.array([[100, 2, 3]]), "Value 100 cannot be formatted as 2 characters"),
            (np.array([[-1, 2, 3]]), "Value -1 cannot be formatted as 2 characters")
        ]
        
        output_path = "test_posac.dat"
        
        for data, expected_error in test_cases:
            with pytest.raises(ValueError, match=expected_error):
                create_posac_data_file(data, output_path)

    def test_create_posac_data_file_io_error(self):
        """Test handling of IO errors
        
        Verifies:
        - Proper handling of invalid file paths
        - Appropriate error messages for IO issues
        """
        test_data = np.array([[1, 2, 3]])
        invalid_path = "/invalid/directory/test.dat"
        
        with pytest.raises(IOError):
            create_posac_data_file(test_data, invalid_path)