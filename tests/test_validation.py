import os
from unittest.mock import MagicMock

import pytest

from lib.controller.validator import Validator
from lib.utils import SET_MODE_DEV


class TestRunValidation:
    """Test class for POSAC validation scenarios"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment with mocked GUI"""
        SET_MODE_DEV()

        # Create mock GUI and notebook
        self.gui = MagicMock()
        self.notebook = MagicMock()
        self.controller = MagicMock()

        # Setup notebook tabs
        self.general_tab = MagicMock()
        self.internal_variables_tab = MagicMock()
        self.output_files_tab = MagicMock()

        # Link mocks together
        self.controller.gui = self.gui
        self.controller.notebook = self.notebook
        self.notebook.general_tab = self.general_tab
        self.notebook.internal_variables_tab = self.internal_variables_tab
        self.notebook.output_files_tab = self.output_files_tab

        # Set default return values for all methods
        self.general_tab.get_data_file.return_value = "tests/data_files/data.csv"
        self.general_tab.get_job_name.return_value = "test"
        self.general_tab.get_lines_per_case.return_value = 1
        self.internal_variables_tab.get_vars_num.return_value = 1
        self.output_files_tab.get_posac_out.return_value = "output/test.pos"
        self.output_files_tab.get_lsa1_out.return_value = "output/test.ls1"
        self.output_files_tab.get_lsa2_out.return_value = "output/test.ls2"

        # Create validator with mock GUI
        self.validator = Validator(self.gui)
        yield

    def test_missing_data_file(self):
        """Test validation when data file is missing"""
        self.general_tab.get_data_file.return_value = ""

        errors = self.validator.validate_for_run(self.controller)
        assert "Data file is required" in errors

    def test_nonexistent_data_file(self):
        """Test validation when data file doesn't exist"""
        self.general_tab.get_data_file.return_value = "nonexistent.dat"
        self.general_tab.get_job_name.return_value = "test"
        self.general_tab.get_lines_per_case.return_value = 1

        errors = self.validator.validate_for_run(self.controller)
        assert any("Data file not found" in error for error in errors)

    def test_missing_job_name(self):
        """Test validation when job name is missing"""
        self.general_tab.get_data_file.return_value = "tests/data_files/data.csv"
        self.general_tab.get_job_name.return_value = ""
        self.general_tab.get_lines_per_case.return_value = 1

        errors = self.validator.validate_for_run(self.controller)
        assert "Job name is required" in errors

    def test_missing_internal_variables(self):
        """Test validation when no internal variables are configured"""
        self.general_tab.get_data_file.return_value = "tests/data_files/data.csv"
        self.general_tab.get_job_name.return_value = "test"
        self.general_tab.get_lines_per_case.return_value = 1
        self.internal_variables_tab.get_vars_num.return_value = 0

        errors = self.validator.validate_for_run(self.controller)
        assert "At least one internal variable must be configured" in errors

    def test_missing_output_files(self):
        """Test validation when output files are not specified"""
        self.general_tab.get_data_file.return_value = "tests/data_files/data.csv"
        self.general_tab.get_job_name.return_value = "test"
        self.general_tab.get_lines_per_case.return_value = 1
        self.internal_variables_tab.get_vars_num.return_value = 1
        self.output_files_tab.get_posac_out.return_value = ""
        self.output_files_tab.get_lsa1_out.return_value = ""
        self.output_files_tab.get_lsa2_out.return_value = ""

        errors = self.validator.validate_for_run(self.controller)
        assert "All output file paths must be specified" in errors

    def test_valid_configuration(self):
        """Test validation with valid configuration"""
        self.general_tab.get_data_file.return_value = os.path.abspath(
            r"tests\simple_test\KEDDIR2.DAT"
        )
        self.general_tab.get_job_name.return_value = "test"
        self.general_tab.get_lines_per_case.return_value = 1
        self.internal_variables_tab.get_vars_num.return_value = 1
        self.output_files_tab.get_posac_out.return_value = "output/test.pos"
        self.output_files_tab.get_lsa1_out.return_value = "output/test.ls1"
        self.output_files_tab.get_lsa2_out.return_value = "output/test.ls2"

        errors = self.validator.validate_for_run(self.controller)
        assert len(errors) == 0, f"Should have no validation errors {errors}"

    def test_multiple_errors(self):
        """Test that multiple validation errors are reported together"""
        self.general_tab.get_data_file.return_value = ""
        self.general_tab.get_job_name.return_value = ""
        self.internal_variables_tab.get_vars_num.return_value = 0

        errors = self.validator.validate_for_run(self.controller)

        expected_errors = {
            "Data file is required",
            "Job name is required",
            "At least one internal variable must be configured",
        }

        assert all(error in errors for error in expected_errors)
        assert len(errors) >= len(expected_errors)