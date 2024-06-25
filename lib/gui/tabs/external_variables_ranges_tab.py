import tkinter as tk
from lib.gui.components.form import BoldLabel, SpinBox
from lib.gui.components.ranges_table import RangesTable
from lib.utils import rreal_size, real_size


class EVRangesTab(tk.Frame):
    DEFAULT_VALUE = ['1', '1-9']

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._create_ranges_table()
        self._create_no_ranges_label()
        self._switch_frames('no_ranges')
        self.num_external_ranges = 0

    def _switch_frames(self, context: str):
        if context == 'no_ranges':
            self.main_frame.pack_forget()
            self.not_ranges_frame.pack(fill='both', expand=True, padx=0,
                                       pady=0)
        elif context == 'ranges':
            self.not_ranges_frame.pack_forget()
            self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)
    def _create_no_ranges_label(self):
        self.not_ranges_frame = tk.Frame(self)
        label = BoldLabel(self.not_ranges_frame,
                          text='Define Number of external variables '
                               '(previous screen)', size=11)
        label.pack(pady=real_size(10))

    def _create_ranges_table(self):
        # align the next to the left
        self.main_frame = tk.Frame(self)
        label = BoldLabel(self.main_frame,
                          text='Admissible ranges for the external '
                               'variables. If no ranges are specified, '
                               'press next.', )
        label.pack(side='top', fill='both', padx=0, pady=(2, 0))
        # Ranges Table
        self.ranges_table_frame = tk.Frame(self.main_frame)
        self.ranges_table = RangesTable(self.ranges_table_frame)
        self.ranges_table_frame.pack(fill='both', expand=True, padx=10,
                                     pady=(0, 0))
        # Traits number
        traits_num_frame = tk.Frame(self.main_frame)
        traits_num_label = BoldLabel(traits_num_frame,
                                     text='How many EXTERNAL TRAITS '
                                          'do you want to define? ('
                                          '0-12)')
        traits_num_label.pack(side='left', padx=(75, 0))
        self.traits_num_spinbox = SpinBox(traits_num_frame,
                                          width=5,
                                          from_=0, to=12,
                                          default=0,
                                          command=None)
        self.traits_num_spinbox.pack(side='right',
                                     padx=real_size((0, 120)))
        traits_num_frame.pack(side='bottom', fill='both', padx=0, pady=(20,
                                                                        20),
                              expand=False)

    ##############
    # Validation #
    ##############

    #############
    # Get & Set #
    #############

    def get_all_ranges(self):
        res = []
        for row in self.ranges_table.get_all_values():
            res.append([item for item in row if item])
        return res

    def add_range(self, values_: list = [], check=True):
        """
        Add a new variable to the table
        :param values: list of length 4 containing values for the columns
        :return:
        """
        self.num_external_ranges += 1
        if self.num_external_ranges == 1:
            self._switch_frames('ranges')
        #
        values = values_.copy()
        if not values:
            values = self.DEFAULT_VALUE.copy()
            [values.append('') for _ in range(9)]
        self.ranges_table.add_row(values, check=check)

    def set_range(self, i: int, values_: list):
        values = self.ranges_table.get_new_row(values_)
        self.ranges_table.set_row(i, values)

    def set_default(self):
        for i in range(len(self.ranges_table)):
            self.set_range(i, self.DEFAULT_VALUE)

    def get_external_traits_num(self) -> int:
        return int(self.traits_num_spinbox.get())

    def set_traits_num(self, value):
        if not 0 <= value <= 12:
            raise UserWarning("The number of external traits should be "
                              "between 0 and 12")
        self.traits_num_spinbox.set(value)
        self.on_change_traits_num()

    def get_all(self):
        return {
            'ranges': self.get_all_ranges(),
            'traits_num': self.get_external_traits_num()
        }

    def set_all(self, ranges, traits_num):
        self.set_traits_num(traits_num)
        for i, range_ in enumerate(ranges):
            self.set_range(i, range_)

    #########
    #  API  #
    #########

    def on_change_traits_num(self):
        """This is a callback function that is called when the user changes the
        number of external traits and is implemented in Notebook
        """
        raise Exception("This method should be implemented in Notebook.")

    def remove_range(self):
        self.ranges_table.remove_row(-1)
        self.num_external_ranges -= 1
        if self.num_external_ranges == 0:
            self._switch_frames('no_ranges')

    def clear_ranges(self):
        self.ranges_table.clear_rows()
        self.num_external_ranges = 0
        self.set_traits_num(0)
        self._switch_frames('no_ranges')
