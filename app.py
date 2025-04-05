import argparse
import os

from lib.__version__ import VERSION

os.environ['VERSION'] = VERSION

# Import error handler early
import sys

from lib.controller.controller import Controller
from lib.utils import IS_PROD, SET_MODE_DEV, SET_MODE_PROD

SET_MODE_PROD()

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--debug", action="store_true")
    args = args.parse_args()
    if args.debug:
        SET_MODE_DEV()
    try:
        a = Controller()
        a.run_process()
    except Exception as e:
        # This will be caught by our global exception handler
        # but we add this as a fallback
        if IS_PROD():
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            sys.exit(1)
        else:
            raise