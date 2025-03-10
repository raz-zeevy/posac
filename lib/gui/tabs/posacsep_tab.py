import tkinter as tk
from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.form import BoldLabel, SelectionBox, Label, TableView
from lib.help.posac_help import Help
from lib.utils import real_size, rreal_size
from lib.controller.validator import Validator
TOP_LABEL = 'POSACSEP-A PROGRAM FOR OPTIMALLY PARTITIONING POSAC SPACE BY ' \
            'EACH ' \
            'ITEM (VARIABLE).\nNow INPUT the THRESHOLD by each ITEM or ' \
            'choose ' \
            '"No" to abort POSACSEP.\nHere "THRESHOLD" is the lowest ' \
            'category in ' \
            'the highest group.'

NO_POSACESEP_LABEL = 'You must abort PosacSep option from the Dos Window by ' \
                     'pressing ' \
                     'CTRL+C'

COMBO_LABEL = 'Posacsep choose'
COMBO_VALUES = ['Yes', 'No']
COLS = [
    'Var No.',
    'Var THRESHOLD',
]
class PosacsepTab(tk.Frame):
    DEFAULT_VALUE = 2

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_widgets()

    def _create_widgets(self):
        labels_frame = tk.Frame(self)
        for row in TOP_LABEL.split("\n"):
            label = BoldLabel(labels_frame, text=row, anchor='w', size=10)
            label.pack(side='top', fill='x',
                       padx=(0, 0), pady=(0, 0))
        labels_frame.pack(side='top', fill='x',
                          expand=False, padx=real_size((5, 0)),
                          pady=(0, 0))
        #
        self._create_combo_box()
        #
        self.vars_table_frame = tk.Frame(self)
        self.vars_table = TableView(self.vars_table_frame,
                                           index=False,
                                           auto_index = False,
                                           disable_sub_menu=True,
                                           disable_cols_edit = [0],
                                           columns=COLS,
                                           add_check_box=False,
                                           cell_right_padding=0,
                                           validation_callback=Validator.
                                           validate_integer,
                                           help=Help.POSACSEP_THRESHOLDS)
        self.vars_table.heading(COLS[0], text=COLS[0], anchor="c")
        self.vars_table.column(COLS[0], width=rreal_size(50), anchor='c')
        self.vars_table.heading(COLS[1], text=COLS[1], anchor="w")
        self.vars_table.column(COLS[1], width=rreal_size(120), anchor='w')
        self.vars_table_frame.pack(fill='y', expand=True,
                                   padx=real_size(10), pady=real_size((0, 0)))
        #
        self.no_posacsep_frame = tk.Frame(self)
        no_posacsep_label = BoldLabel(self.no_posacsep_frame,
                                      text=NO_POSACESEP_LABEL,
                                      size=11)
        no_posacsep_label.pack(side='top', fill='x',
                               padx=(0, 0), pady=(0, 0))
    def _create_combo_box(self):
        self.combo_frame = tk.Frame(self)
        self.combo_frame.pack(fill='both',
                              pady=real_size((20, 20)),
                              padx=(self.winfo_pixels(220), 0),
                              expand=False)
        label = Label(self.combo_frame, text=COMBO_LABEL)
        label.pack(side='left', padx=real_size(10))
        self.combo_box = SelectionBox(self.combo_frame,
                                      values=COMBO_VALUES,
                                      default=COMBO_VALUES[0],
                                      help=Help.POSACSEP_OPTION)
        self.combo_box.pack(side='left', padx=real_size((10, 0)))
        self.combo_box.bind('<<ComboboxSelected>>', lambda e:
        self.on_posacsep_change())

    def on_posacsep_change(self):
        if self.get_combo():
            self.no_posacsep_frame.pack_forget()
            self.vars_table_frame.pack(fill='y', expand=True,
                                       padx=real_size(10),
                                       pady=real_size((0, 15)))
        else:
            self.vars_table_frame.pack_forget()
            self.no_posacsep_frame.pack(fill='both', expand=True,
                                        padx=real_size(10),
                                        pady=real_size((0, 15)))

    def set_combo(self, value: bool):
        if value:
            self.combo_box.set('Yes')
        else:
            self.combo_box.set('No')
        self.on_posacsep_change()

    def get_values(self):
        return [int(i[1]) for i in self.vars_table.get_all_values()]

    def get_combo(self):
        return self.combo_box.get() == 'Yes'

    def set_values(self, values):
        for i, row in enumerate(values):
            self.vars_table.set_row(i, [self.vars_table.get_row(i)[COLS[
                0]],row])

    def get_all(self):
        return dict(
            posacsep=self.get_combo(),
            values=self.get_values()
        )

    def set_all(self, **kwargs):
        self.set_combo(kwargs['posacsep'])
        self.set_values(kwargs['values'])

    def set_to_default(self):
        self.set_combo(True)
        for i in range(len(self.vars_table)):
            self.vars_table.set_row(i, [
                self.vars_table.get_row(i)[COLS[0]],
                self.DEFAULT_VALUE])

    # API

    def add_internal_variable(self, var_num):
        self.vars_table.add_row(
            values=[var_num, self.DEFAULT_VALUE]
        )

    def remove_internal_variable(self):
        self.vars_table.remove_row(-1)

    def clear_internal_variables(self):
        self.vars_table.clear_rows()
