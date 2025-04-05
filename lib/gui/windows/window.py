import tkinter as tk
from abc import ABC, abstractmethod

from lib.utils import get_resource


class Window(tk.Toplevel, ABC):
    _instances = {}  # Dictionary to store instances of each window class

    def __new__(cls, *args, **kwargs):
        # If an instance exists and is valid, return it
        if cls in cls._instances and cls._instances[cls] is not None:
            try:
                if cls._instances[cls].winfo_exists():
                    cls._instances[cls].focus_force()
                    cls._instances[cls].lift()
                    return cls._instances[cls]
            except (tk.TclError, AttributeError):
                cls._instances[cls] = None

        instance = super().__new__(cls)
        cls._instances[cls] = instance
        return instance

    def __init__(self, parent=None, geometry=None, **kwargs):
        if not hasattr(self, "_widgets_created"):
            super().__init__(parent)
            self.parent = parent

            # Common window setup
            if geometry:
                self.geometry(geometry)
            self.iconbitmap(get_resource("icon.ico"))
            self.resizable(False, False)
            self.center_window()

            # For modal dialog behavior
            self.result = None

            # Create widgets and mark as initialized
            self.setup_window(**kwargs)
            self._widgets_created = True

    @abstractmethod
    def setup_window(self):
        """Override this method in subclasses to setup window-specific widgets"""
        pass

    @classmethod
    def clear_instances(cls):
        """Clear all stored instances - useful for testing"""
        cls._instances = {}

    def center_window(self):
        """Center the window on the screen"""
        # First make sure the window has been drawn so we get proper dimensions
        self.update_idletasks()

        # Get window dimensions after all widgets are in place
        width = self.winfo_width()
        height = self.winfo_height()

        # If window hasn't been drawn yet, try to get dimensions from geometry
        if width == 1 and height == 1:
            try:
                geometry = self.geometry()
                if "x" in geometry and "+" in geometry:
                    dimensions = geometry.split("+")[0]
                    width, height = map(int, dimensions.split("x"))
            except:
                # If we can't determine size, use reasonable defaults
                width = 400
                height = 300

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position for perfect center
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Ensure we're not positioning off-screen
        x = max(0, x)
        y = max(0, y)

        # Set the geometry
        self.geometry(f'+{x}+{y}')

    def show_modal(self):
        """Show window as modal dialog and return result"""
        self.transient(self.parent)
        self.grab_set()
        self.wait_window()
        return self.result

    def cancel(self):
        """Common cancel behavior"""
        self.result = None
        self.destroy()

    @classmethod
    def show_dialog(cls, parent, **kwargs):
        """Class method to create and show a modal dialog"""
        dialog = cls(parent, **kwargs)
        return dialog.show_modal()