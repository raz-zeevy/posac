import datetime
import logging
import os
import subprocess
import sys
import tempfile
import traceback
import webbrowser
from pathlib import Path
from urllib.parse import quote

import pyautogui

from lib.controller.session import Session
from lib.utils import IS_PROD

# Configure logging
logger = logging.getLogger(__name__)

# Global variable to store the singleton instance
_error_reporter_instance = None


class ErrorReporter:
    """Handles error reporting functionality for unhandled exceptions"""

    @classmethod
    def get_instance(cls, gui=None, controller=None):
        """Get or create the singleton instance of ErrorReporter"""
        global _error_reporter_instance
        if _error_reporter_instance is None:
            _error_reporter_instance = cls(gui, controller)
        elif gui is not None and controller is not None:
            # Update the existing instance with new references if provided
            _error_reporter_instance.gui = gui
            _error_reporter_instance.controller = controller
        return _error_reporter_instance

    def __init__(self, gui=None, controller=None):
        self.gui = gui
        self.controller = controller

        # Create a platform-appropriate path for bug reports
        if sys.platform == "win32":
            # On Windows, use AppData/Local instead of Roaming
            self.bug_reports_dir = (
                Path(os.environ.get("LOCALAPPDATA")) / "Posac" / "bug_reports"
            )
        else:
            # For non-Windows platforms
            self.bug_reports_dir = (
                Path(os.path.expanduser("~"))
                / ".local"
                / "share"
                / "Posac"
                / "bug_reports"
            )

        # Ensure the directory exists
        try:
            self.bug_reports_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Bug reports directory: {self.bug_reports_dir}")
        except Exception as e:
            logger.error(f"Failed to create bug reports directory: {e}")
            # Fallback to temp directory if we can't create the intended directory
            self.bug_reports_dir = Path(tempfile.gettempdir()) / "Posac" / "bug_reports"
            self.bug_reports_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Using fallback bug reports directory: {self.bug_reports_dir}")

    def capture_screenshot(self, filename):
        """Capture a screenshot of the current screen"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            logger.info(f"Screenshot saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return False

    def save_session(self, filename):
        """Save the current session state"""
        try:
            session = Session(self.controller)
            session.save(filename)
            logger.info(f"Session saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False

    def save_log(self, filename, exception_info):
        """Save exception information and log to a file"""
        try:
            with open(filename, "w") as f:
                f.write(f"Exception occurred at: {datetime.datetime.now()}\n\n")
                f.write(f"Exception type: {exception_info['type']}\n")
                f.write(f"Exception message: {exception_info['message']}\n\n")
                f.write("Traceback:\n")
                f.write(exception_info["traceback"])
            logger.info(f"Error log saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save log: {e}")
            return False

    def open_folder(self, folder_path):
        """Open the folder in file explorer"""
        try:
            folder_path = str(folder_path)  # Convert Path to string if needed
            logger.info(f"Attempting to open folder: {folder_path}")

            if not os.path.exists(folder_path):
                logger.error(f"Folder does not exist: {folder_path}")
                return False

            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", folder_path], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", folder_path], check=True)

            logger.info(f"Successfully opened folder: {folder_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to open folder {folder_path}: {e}")
            return False

    def compose_email(self, files):
        """Open the default email client with a pre-composed message"""
        try:
            recipient = "raz3zeevy@gmail.com"
            subject = "Posac Error Report"
            body = f"""
Hello,

An error occurred in the Posac application at {datetime.datetime.now()}.

This email was automatically generated by the Posac error reporting system.

Please find attached files with details about the error.

System Information:
- OS: {sys.platform}
- Python: {sys.version}
- Posac Version: {os.environ.get("VERSION", "Unknown")}

Thank you.
            """

            # Create mailto URL
            mailto_url = (
                f"mailto:{recipient}?subject={quote(subject)}&body={quote(body)}"
            )

            # Open default email client
            webbrowser.open(mailto_url)
            logger.info(f"Email client opened with {len(files)} files to attach")

            return True
        except Exception as e:
            logger.error(f"Failed to compose email: {e}")
            return False

    def report_error(self, exception_info):
        """Generate error report files and offer to send them"""
        # Create a timestamp-based folder for this error report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.bug_reports_dir / timestamp

        try:
            report_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created report directory: {report_dir}")
        except Exception as e:
            logger.error(f"Failed to create report directory: {e}")
            # Fallback to parent directory
            report_dir = self.bug_reports_dir

        # Create filenames
        screenshot_file = report_dir / "screenshot.png"
        log_file = report_dir / "error.log"
        session_file = report_dir / "session.mmp"

        # Capture data
        screenshot_success = self.capture_screenshot(screenshot_file)
        log_success = self.save_log(log_file, exception_info)
        session_success = self.save_session(session_file)

        # List of successfully created files
        files = []
        if screenshot_success:
            files.append(str(screenshot_file))
        if log_success:
            files.append(str(log_file))
        if session_success:
            files.append(str(session_file))

        # Compose and send email
        if files:
            # Open the folder for the user
            folder_opened = self.open_folder(report_dir)
            if not folder_opened:
                logger.warning(
                    f"Could not open folder, will show path instead: {report_dir}"
                )

            # Inform user where files are saved
            message = f"Error report files have been saved to:\n{report_dir}\n\n"

            if folder_opened:
                message += "The folder has been opened for you. "

            message += "Please attach these files to the email that has been opened."

            self.compose_email(files)

            if self.gui:
                # Use warning icon instead of info
                self.gui.show_warning("Error Report Files", message)
            else:
                print(message)

        return files


def global_exception_handler(exctype, value, tb):
    """Global exception handler for unhandled exceptions"""
    # Format the traceback
    traceback_text = "".join(traceback.format_exception(exctype, value, tb))

    # Log the exception
    logger.critical(f"Unhandled exception:\n{traceback_text}")

    # In production mode, show dialog and offer to report
    if IS_PROD():
        import tkinter as tk
        from tkinter import messagebox

        # Create a basic root window if none exists
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
        except:
            root = None

        # Show error message with ERROR icon instead of QUESTION
        error_message = f"An unexpected error has occurred:\n\n{str(value)}\n\nWould you like to report this error?"
        report = messagebox.askquestion(
            "ERROR: Application Failure", error_message, icon="error"
        )

        if report == "yes":  # askquestion returns 'yes' or 'no' instead of True/False
            # Collect exception info
            exception_info = {
                "type": exctype.__name__,
                "message": str(value),
                "traceback": traceback_text,
            }

            # Use the singleton instance of ErrorReporter
            reporter = ErrorReporter.get_instance()
            reporter.report_error(exception_info)

            # Use error icon for the thank you message as well
            messagebox.showinfo(
                "Error Report Submitted",
                "Thank you for reporting this error. The application will now close.",
                icon="warning",
            )

        # Exit the application
        exit()
    else:
        # In development mode, use the default exception handler
        sys.__excepthook__(exctype, value, tb)


# Set the global exception handler
sys.excepthook = global_exception_handler


def install_tk_exception_handler(root):
    """Install error handler for Tkinter callback exceptions"""
    old_report_callback_exception = root.report_callback_exception

    def report_callback_exception(exc_type, exc_value, exc_traceback):
        # Call our global exception handler
        global_exception_handler(exc_type, exc_value, exc_traceback)
        # Optionally call the original handler
        old_report_callback_exception(exc_type, exc_value, exc_traceback)

    root.report_callback_exception = report_callback_exception