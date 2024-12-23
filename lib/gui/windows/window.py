import ttkbootstrap as ttk
import tkinter as tk
from lib.utils import rreal_size, get_resource
from abc import ABC, abstractmethod

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
        if not hasattr(self, '_widgets_created'):
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
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
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