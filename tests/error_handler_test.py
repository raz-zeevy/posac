import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lib.error_handler import ErrorReporter
from lib.utils import SET_MODE_DEV


class TestErrorReporter:
    @pytest.fixture
    def error_reporter(self):
        """Create an ErrorReporter instance for testing"""
        SET_MODE_DEV()  # Ensure we're in test mode
        gui_mock = MagicMock()
        controller_mock = MagicMock()
        reporter = ErrorReporter(gui=gui_mock, controller=controller_mock)

        # Override bug reports directory to use a temporary directory
        reporter.bug_reports_dir = Path(tempfile.mkdtemp())
        return reporter

    def test_capture_screenshot(self, error_reporter):
        """Test screenshot capture functionality"""
        with patch("pyautogui.screenshot") as mock_screenshot:
            mock_screenshot.return_value = MagicMock()

            # Create a temporary file for the screenshot
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                filename = temp_file.name

            try:
                # Test successful screenshot capture
                result = error_reporter.capture_screenshot(filename)
                assert result is True
                mock_screenshot.assert_called_once()
                mock_screenshot.return_value.save.assert_called_once_with(filename)

                # Test exception handling
                mock_screenshot.side_effect = Exception("Screenshot error")
                result = error_reporter.capture_screenshot(filename)
                assert result is False
            finally:
                # Clean up
                if os.path.exists(filename):
                    os.remove(filename)

    def test_save_log(self, error_reporter):
        """Test log saving functionality"""
        # Create a temporary file for the log
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as temp_file:
            filename = temp_file.name

        try:
            # Test successful log saving
            exception_info = {
                "type": "ValueError",
                "message": "Test error message",
                "traceback": "Test traceback",
            }

            result = error_reporter.save_log(filename, exception_info)
            assert result is True

            # Verify file contents
            with open(filename, "r") as f:
                content = f.read()
                assert "Exception type: ValueError" in content
                assert "Exception message: Test error message" in content
                assert "Test traceback" in content

            # Test exception handling
            with patch("builtins.open", side_effect=Exception("File error")):
                result = error_reporter.save_log(filename, exception_info)
                assert result is False
        finally:
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)

    def test_report_error(self, error_reporter):
        """Test error reporting functionality"""
        # Mock all the component methods
        with patch.object(
            error_reporter, "capture_screenshot", return_value=True
        ) as mock_screenshot:
            with patch.object(
                error_reporter, "save_log", return_value=True
            ) as mock_log:
                with patch.object(
                    error_reporter, "save_session", return_value=True
                ) as mock_session:
                    with patch.object(
                        error_reporter, "compose_email", return_value=True
                    ) as mock_email:
                        with patch.object(
                            error_reporter, "open_folder", return_value=True
                        ) as mock_open_folder:
                            exception_info = {
                                "type": "ValueError",
                                "message": "Test error message",
                                "traceback": "Test traceback",
                            }

                            # Test successful error reporting
                            files = error_reporter.report_error(exception_info)

                            # Verify all methods were called
                            mock_screenshot.assert_called_once()
                            mock_log.assert_called_once()
                            mock_session.assert_called_once()
                            mock_email.assert_called_once()
                            mock_open_folder.assert_called_once()

                            # Verify files list contains 3 files
                            assert len(files) == 3

                            # Test with some failures
                            mock_screenshot.return_value = False
                            mock_log.return_value = True
                            mock_session.return_value = False

                            files = error_reporter.report_error(exception_info)

                            # Verify only one file in the list
                            assert len(files) == 1

    def test_open_folder(self, error_reporter):
        """Test folder opening functionality"""
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        try:
            # Test successful folder opening
            mock_open = None
            if sys.platform == "win32":
                mock_patch = patch("os.startfile")
            else:
                mock_patch = patch("subprocess.run")

            with mock_patch as mock_open:
                # For Windows
                if sys.platform == "win32":
                    result = error_reporter.open_folder(temp_dir)
                    assert result is True
                    mock_open.assert_called_once_with(temp_dir)
                # For macOS/Linux
                else:
                    result = error_reporter.open_folder(temp_dir)
                    assert result is True
                    if sys.platform == "darwin":
                        mock_open.assert_called_once_with(
                            ["open", temp_dir], check=True
                        )
                    else:
                        mock_open.assert_called_once_with(
                            ["xdg-open", temp_dir], check=True
                        )

                # Test exception handling
                mock_open.side_effect = Exception("Open folder error")
                result = error_reporter.open_folder(temp_dir)
                assert result is False
        finally:
            # Clean up
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
