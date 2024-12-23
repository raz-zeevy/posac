import tkinter as tk
from lib.gui.components.form import Label, BoldLabel, DataButton
from lib.gui.components.variables_table import VariablesTable
from lib.help.posac_help import Help
from lib.utils import *

class EVariablesTab(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.notebook = parent
        self._create_widgets()

    def _create_widgets(self):
        label = BoldLabel(self, text='Specify where in the data file the '
                                   'EXTERNAL variables are located.\n'
                                   'If no external variables are used, '
                                   'press next.')
        label.pack(side='top', fill='both', padx=0, pady=(2, 0))
        
        # Variables Table Frame
        self.vars_table_frame = tk.Frame(self)
        self.vars_table = VariablesTable(
            self.notebook,
            self.vars_table_frame,
            new_default_label="extvar",
            check_box_callback=None,  # External variables don't need checkbox callback,
            help=Help.EXTERNAL_VARS
        )
        self.vars_table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 0))
        
        # Create buttons frame
        self._create_data_buttons()

    def _create_data_buttons(self):
        padx = (30, 30)
        frame = tk.Frame(self)
        self.add_button = DataButton(frame, text='Add Variable', width=14)
        self.add_button.pack(side='left', padx=padx, fill='x')
        self.remove_button = DataButton(frame, text='Remove Variable', width=15)
        self.remove_button.pack(side='left', padx=padx, fill='x')
        self.clear_button = DataButton(frame, text='Clear Variables', width=15)
        self.clear_button.pack(side='left', padx=padx, fill='x')
        frame.pack(side='left', fill='x', padx=rreal_size(75), pady=real_size(10))

    # Delegate methods to vars_table
    def get_all_variables(self): return self.vars_table.get_all_variables()
    def get_all_variables_values(self): return self.vars_table.get_all_variables_values()
    def get_vars_num(self): return len(self.vars_table)
    def get_selected_variables(self): return self.vars_table.get_selected_variables()
    
    def add_variable(self, values_=None, check=True):
        self.vars_table.add_variable(values_, check)
    
    def remove_variable(self):
        self.vars_table.remove_variable()
    
    def clear_variables(self):
        self.vars_table.clear_variables()
    
    def show_low_high(self):
        self.vars_table.show_low_high()
    
    def hide_low_high(self):
        self.vars_table.hide_low_high()
    
    def set_default(self):
        self.vars_table.clear_variables()
        self.hide_low_high()

    def set_variable(self, i: int, values: list):
        self.vars_table.set_variable(i, values)

    def set_variables(self, vars):
        self.vars_table.set_variables(vars)
