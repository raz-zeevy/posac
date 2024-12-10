import tkinter as tk
from lib.gui.components.form import Label, BoldLabel, DataButton
from lib.gui.components.variables_table import VariablesTable
from lib.utils import *

class IVariablesTab(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.notebook = parent
        self._create_widgets()
        self.set_default()

    def _create_widgets(self):
        label = BoldLabel(self, text='Specify where in the data file the '
                                   'INTERNAL variables are located')
        label.pack(side='top', fill='both', padx=0, pady=(2, 0))
        
        # Variables Table Frame
        self.vars_table_frame = tk.Frame(self)
        self.vars_table = VariablesTable(
            self.notebook,
            self.vars_table_frame,
            check_box_callback=lambda row_id, is_on: self._on_toggle_row()
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
        self.clear_button.pack(side='left', padx=(30, 0), fill='x')
        frame.pack(side='bottom', fill='x', padx=rreal_size(75), pady=real_size(10))

    # Delegate methods to vars_table
    def get_all_variables(self): return self.vars_table.get_all_variables()
    def get_all_variables_values(self): return self.vars_table.get_all_variables_values()
    def get_selected_variables(self): return self.vars_table.get_selected_variables()
    def get_selected_variables_nums(self): return self.vars_table.get_selected_variables_nums()
    def get_vars_num(self): return len(self.vars_table)
    
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

    def _on_toggle_row(self, row_id, is_on):
        print("toggled row", row_id, is_on)

    def on_change_recoding_num(self):
        """This is a callback function that is called when the user changes the
        number of recoding operations and is implemented in Notebook
        """
        raise Exception("This method should be implemented in Notebook.")

    def set_variable(self, i: int, values: list):
        self.vars_table.set_variable(i, values)

    def set_variables(self, vars):
        self.vars_table.set_variables(vars)