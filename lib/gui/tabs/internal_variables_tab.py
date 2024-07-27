import tkinter as tk
from lib.gui.components.editable_tree_view import EditableTreeView
from lib.utils import *
from lib.gui.components.form import *


class IVariablesTab(tk.Frame):
    INDEX_COL_NAME = 'Var. No.'
    COLS = {
        'sel_var': 'Sel. Var.',
        'line_number': 'Line No.',
        'field_width': 'Field Width',
        'start_col': 'Start Col',
        'label': 'Label'
    }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()
        self.set_default()

    def _create_widgets(self):
        label = BoldLabel(self, text='Specify where in the data file the '
                                     'INTERNAL variables are located')
        label.pack(side='top', fill='both', padx=0, pady=(2, 0))
        self.vars_table_frame = tk.Frame(self)
        self.vars_table = EditableTreeView(self.vars_table_frame,
                                           columns=self.COLS.values(),
                                           index_col_name=self.INDEX_COL_NAME,
                                           add_check_box=True)
        self.vars_table.column('Label', stretch=True)
        for col in ['Sel. Var.', 'Line No.', 'Field Width', 'Start Col',
                    'Label']:
            self.vars_table.heading(col, text=col, anchor="w")
            self.vars_table.column(col, width=rreal_size(60), anchor='w')
            # self.column(col, stretch=False)
        self.vars_table.column('Field Width', width=rreal_size(80),
                               anchor='w')
        self.vars_table_frame.pack(fill='both', expand=True, padx=10,
                                   pady=(0, 0))
        self._create_data_buttons()

    #######
    # Gui #
    #######
    def _create_data_buttons(self):
        padx = (30, 30)
        frame = tk.Frame(self)
        self.add_button = DataButton(frame, text='Add Variable',
                                     width=14)
        self.add_button.pack(side='left', padx=padx, fill='x')
        self.remove_button = DataButton(frame, text='Remove Variable',
                                        width=15,
                                        command=None)
        self.remove_button.pack(side='left', padx=padx, fill='x')
        self.clear_button = DataButton(frame, text='Clear Variables',
                                       width=15,
                                       command=None)
        self.clear_button.pack(side='left', padx=(30, 0), fill='x')
        frame.pack(side='left', fill='x', padx=rreal_size(75),
                   pady=real_size(10))

    #############
    # Get & Set #
    #############

    def get_all_variables(self):
        return [list(row)[1:] for row in self.vars_table.get_all_values()]

    def get_all_variables_values(self):
        return self.vars_table.get_all_values()

    def get_selected_variables(self):
        return [list(row)[1:] for row in
                self.vars_table.get_check_rows_values()]

    def set_variable(self, i : int, values : list):
        self.vars_table.set_row(i, values)

    def set_default(self):
        self.vars_table.clear_rows()

    def get_vars_num(self):
        return len(self.get_all_variables())

    #########
    #  API  #
    #########

    def add_variable(self, values_: list = [], check=True):
        """
        Add a new variable to the table
        :param values: list of length 4 containing values for the columns
        :return:
        """
        cur_index = len(self.vars_table)
        values = values_.copy()
        if not values: values = ['1', '1', '0', f'v{cur_index + 1}']
        self.vars_table.add_row(values, check=check)

    def remove_variable(self):
        self.vars_table.remove_row(-1)

    def clear_variables(self):
        self.vars_table.clear_rows()
