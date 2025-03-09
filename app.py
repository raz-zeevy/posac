import os
from lib.__version__ import VERSION
os.environ['VERSION'] = VERSION

# Import error handler early
from lib.error_handler import global_exception_handler
from lib.controller.controller import Controller
from lib.utils import *

SET_MODE_PRODUCTION()

if __name__ == '__main__':
    try:
        a = Controller() 
        a.run_process()
    except Exception as e:
        # This will be caught by our global exception handler
        # but we add this as a fallback
        if IS_PRODUCTION():
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            sys.exit(1)
        else:
            raise